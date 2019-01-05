class User(object):
    def __init__(self, name, email):
        if ('@' in email) and (email.endswith('.org') or email.endswith('.edu') or email.endswith('.com')):
            self.name = name
            self.email = email
            self.books = {}
        else:
            print('Unable to create new user. Incorrect email provided')

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("The email address of {user} has been updated to {address}".format(user=self.name, address = self.email))

    def __repr__(self):
        return "User {user}, email: {address}, books read: {books}".format(user=self.name, address=self.email, books =str(len(self.books)))

    def __eq__(self, other_user):
        '''
        two users are equal if they have the same name and email
        '''
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        return False

    def read_book(self, book, rating = None):
        self.books[book] = rating
    
    def get_average_rating(self):
        sum_ratings = 0
        for book_rating in self.books.values():
            if book_rating != None:
                sum_ratings += book_rating
        average_rating = sum_ratings / len(self.books)
        return average_rating 

class Book(object):
    def __init__(self, title, isbn, price):
        '''
        title - string
        isbn - number
        '''
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []
    
    def __repr__(self):
        return "Book named {title} costs {price}".format(title=self.title, price = self.price)

    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("ISBN for {book} updated to {isbn}".format(book = self.title, isbn = self.isbn))

    def add_rating(self, rating):
        '''
        valid rating = 0 .. 4

        '''
        if (rating!= None):
            if (rating >=0) and (rating <=4):
                self.ratings.append(rating)
            else:
                print("Invalid Rating")
        else:
            print('Rating not provided')

    def __eq__(self, other_book):
        '''
        books are equal if they have the same title and isbn
        '''
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        return False

    def get_average_rating(self):
        sum_ratings = 0
        for book_rating in self.ratings:
            sum_ratings += book_rating
        average_rating = sum_ratings / len(self.ratings)
        return average_rating

    def __hash__(self):
        '''
        hash method to allow Book objects to be dictionary keys
        '''
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author
    
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "{title} by {author} costs {price}".format(title = self.title, author = self.author, price = self.price)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level
    
    def __repr__(self):
        return "{title}, a {level} manual on {subject} costs {price}".format(title = self.title, level = self.level, subject=self.subject, price = self.price)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "The object contains {users_num} users and {books_num} books read by them. For more details: use print_users() and print_catalog()".format(users_num = str(len(self.users)), books_num = str(len(self.books)))

    def __eq__(self, other_tome_rater):
        return (self.users == other_tome_rater.users) and (self.books == other_tome_rater.books)

    def is_isbn_unique(self, isbn):
        isbn_unique = True
        for book in self.books:
            if book.isbn == isbn:
                isbn_unique = False
                break
        return isbn_unique

    def create_book(self, title, isbn, price):
        if self.is_isbn_unique(isbn):
            new_book = Book(title, isbn, price)
            return new_book
        else:
            print('Book with such ISBN already exists')
    
    def create_novel(self, title, author, isbn, price):
        if self.is_isbn_unique(isbn):
            new_fiction = Fiction(title, author, isbn, price)
            return new_fiction
        else:
            print('Book with such ISBN already exists')

    def create_non_fiction(self, title, subject, level, isbn, price):
        if self.is_isbn_unique(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn, price)
            return new_non_fiction
        else:
             print('Book with such ISBN already exists')
    
    def add_book_to_user(self, book, email, rating = None):
        if email not in self.users:
            print("No user with email {email}".format(email=email))
        else:
            user = self.users[email]
            user.read_book(book, rating)
            book.add_rating(rating)
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1
    
    def add_user(self, name, email, user_books = None):
        '''
        create new user, add them  and add books to their list (if provided)
        '''
        if email not in self.users:
            new_user = User(name, email)
            self.users[email] = new_user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)
        else:
            print('User with email {email} already exists'.format(email = email))

    def print_catalog(self):
        '''
        print all books: used as keys in the self.books
        '''
        for book in self.books:
            print(book)
    
    def print_users(self):
        '''
        print all users: values in self.users
        '''
        for user in self.users.values():
            print(user)
        
    def most_read_book(self):
        '''
        return the most read book in self.books: having the highest value in the self.books dict {book: how many times read}
        '''
        max_reads = float("-inf")
        max_read_book = ''
        for book, read_count in self.books.items():
            if read_count > max_reads:
                max_reads = read_count
                max_read_book = book
        return max_read_book

    def get_n_most_read_books(self, n):
        n_most_read_books = []
        sorted_list_of_dict = sorted(self.books.items(), key = lambda kv: kv[1], reverse = True)
        for i in range(min(n, len(sorted_list_of_dict))):
            n_most_read_books.append(sorted_list_of_dict[i][0])
        return n_most_read_books

    def get_n_most_prolific_readers(self, n):
        n_most_prolific_readers = []
        book_prices = {}
        for user in self.users:
            book_prices[user] = len(self.users[user].books)
        users_rating_sorted = sorted(book_prices.items(), key = lambda kv: kv[1], reverse=True)
        for i in range(min(n, len(self.users))):
            n_most_prolific_readers.append(self.users[users_rating_sorted[i][0]])
        return n_most_prolific_readers

    def highest_rated_book(self):
        '''
        return the book with highest average rating in self.books. Books are keys in self.books
        '''
        highest_rating = float("-inf")
        highest_rated_book = ''
        for book in self.books:
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                highest_rated_book = book
        return highest_rated_book
    
    def most_positive_user(self):
        '''
        return the user in self.users with the highest average rating
        '''
        max_average_rating = 0
        most_positive_user = ''
        for user in self.users.values():
            if user.get_average_rating() > max_average_rating:
                max_average_rating = user.get_average_rating()
                most_positive_user = user
        return most_positive_user

    def get_worth_of_user(self, user_email):
        total_cost = 0
        for user in self.users.values():
            for book in user.books:
                total_cost += book.price
        return total_cost
    
    def get_n_most_expensive_books(self,n):
        n_most_expensive_books = []
        books_prices = {}
        for book in self.books:
            books_prices[book] = book.price
        books_prices_sorted = sorted(books_prices.items(), key = lambda kv: kv[1], reverse=True)
        for i in range(min(n, len(self.books))):
            n_most_expensive_books.append(books_prices_sorted[i][0])

        return n_most_expensive_books    


