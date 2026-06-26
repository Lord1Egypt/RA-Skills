import sqlite3
from datetime import date

def adapt_date(val):
    """Convert datetime.date to ISO format string."""
    return val.isoformat()

def convert_date(val):
    """Convert ISO format string to datetime.date."""
    return date.fromisoformat(val.decode() if isinstance(val, bytes) else val)

# Register the adapter and converter
sqlite3.register_adapter(date, adapt_date)
sqlite3.register_converter("date", convert_date)

class DatabaseHandler:
    """
    A class that handles connection to a sqllite3 database.
    """

    def __init__(self, db_file: str):
        """
        Parameters:
        db_file (str): Path to the database file.
        """
        self.db_file = db_file
        self.conn = None
        self.connect()
        self.tables = self.create_tables()
        self.disconnect()

    def connect(self) -> None:
        """
        Connects to the database with PARSE_DECLTYPES and PARSE_COLNAMES enabled.
        """
        # PARSE_DECLTYPES is used to convert sqlite3 date objects to python datetime objects
        # https://docs.python.org/3/library/sqlite3.html#sqlite3.PARSE_DECLTYPES
        # PARSE_COLNAMES is used to access columns by name
        # https://docs.python.org/3/library/sqlite3.html#sqlite3.PARSE_COLNAMES
        self.conn = sqlite3.connect(self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def disconnect(self) -> None:
        """
        Disconnects from the database. Sets self.conn to None.
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def commit(self) -> None:
        """
        Commits changes to the database. Raises exception if no connection is established.
        """
        if self.conn:
            self.conn.commit()
        else:
            raise Exception("Cannot commit changes, database connection not established.")
        
    def get_cursor(self) -> sqlite3.Cursor:
        """
        Returns a cursor to the database.

        Returns:
        sqlite3.Cursor: Cursor to the database.
        """
        if self.conn == None:
            self.connect()
        return self.conn.cursor()

    def create_tables(self) -> list:
        """
        Creates transaction tables in the database if they do not exist. Raises exception if no connection is established.

        Returns:
        list: List of tables in the database (wether existing or created).
        """
        if not self.conn:
            raise Exception("Database connection not established.")

        cursor = self.conn.cursor()

        # Enable foreign key support, used by cohort_assets table to reference assets and cohort_data
        cursor.execute("PRAGMA foreign_keys = ON;")

        # transactions contains all raw transactions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                date DATE NOT NULL, 
                account TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                asset_name TEXT NOT NULL,
                amount REAL NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                courtage REAL NOT NULL,
                currency TEXT NOT NULL,
                isin TEXT NOT NULL,
                processed INT DEFAULT 0
                )""")

        # cohort_data contains the capital, deposits and withdrawals per account per month
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cohort_data(
                month DATE NOT NULL,
                account TEXT NOT NULL,
                deposit REAL DEFAULT 0,
                withdrawal REAL DEFAULT 0,
                capital REAL DEFAULT 0,
                active_base REAL DEFAULT 0,
                closed_return REAL DEFAULT NULL,
                transfer_net REAL DEFAULT 0,
                PRIMARY KEY(month, account)
                );""")
                
        # cohort_cash_flows tracks aggregated cash flows for a cohort in a specific transaction month.
        # NOTE: Accumulating cash flows on a monthly basis is mathematically suboptimal for the Modified Dietz 
        # calculation and could be improved with further accuracy by logging exact transaction dates.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cohort_cash_flows(
                cohort_month DATE NOT NULL,
                account TEXT NOT NULL,
                transaction_month DATE NOT NULL,
                amount REAL DEFAULT 0,
                FOREIGN KEY (cohort_month, account) REFERENCES cohort_data (month, account),
                PRIMARY KEY (cohort_month, account, transaction_month)
            );""")

        # assets contains the total amount of each asset and the latest price
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets(
                asset_id INTEGER,
                asset TEXT UNIQUE NOT NULL,
                amount REAL DEFAULT 0,
                average_price REAL DEFAULT 0,
                average_purchase_price REAL DEFAULT 0,
                average_sale_price REAL DEFAULT 0,
                purchased_amount REAL DEFAULT 0,
                sold_amount REAL DEFAULT 0,
                latest_price REAL,
                latest_price_date DATE,
                PRIMARY KEY(asset_id)
                );""")

        # cohort_assets contains the amount of each asset held, purchased and sold each month per account
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cohort_assets(
                month DATE NOT NULL,
                asset_id INTEGER NOT NULL,
                account TEXT NOT NULL,
                amount REAL DEFAULT 0,
                average_price REAL DEFAULT 0,
                average_purchase_price REAL DEFAULT 0,
                average_sale_price REAL DEFAULT 0,
                purchased_amount REAL DEFAULT 0,
                sold_amount REAL DEFAULT 0,
                FOREIGN KEY (asset_id) REFERENCES assets (asset_id),
                FOREIGN KEY (month, account) REFERENCES cohort_data (month, account),
                PRIMARY KEY(month, asset_id, account)
                );""")
        
        # accounts contains account-level configuration like nicknames
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
                account_id TEXT PRIMARY KEY,
                nickname TEXT
                );""")

        # metadata contains system state information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata(
                key TEXT PRIMARY KEY,
                value TEXT
                );""")
        
        # cohort_stats contains statistics about capital transfers and gain/loss for each month
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cohort_stats(
                month DATE NOT NULL,
                deposit REAL DEFAULT 0,
                withdrawal REAL DEFAULT 0,
                capital REAL DEFAULT 0,
                value REAL DEFAULT 0,
                total_gainloss REAL DEFAULT 0,
                realized_gainloss REAL DEFAULT 0,
                unrealized_gainloss REAL DEFAULT 0,
                total_gainloss_per REAL DEFAULT 0,
                realized_gainloss_per REAL DEFAULT 0,
                unrealized_gainloss_per REAL DEFAULT 0,
                annual_per_yield REAL DEFAULT NULL,
                acc_deposit REAL DEFAULT 0,
                acc_value REAL DEFAULT 0,
                acc_withdrawal REAL DEFAULT 0,
                acc_net_deposit REAL DEFAULT 0,
                acc_total_gainloss REAL DEFAULT 0,
                acc_realized_gainloss REAL DEFAULT 0,
                acc_unrealized_gainloss REAL DEFAULT 0,
                PRIMARY KEY(month)
                );""")
        
        # year_stats contains statistics about capital transfers and gain/loss for each year
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS year_stats(
                year DATE NOT NULL,
                deposit REAL DEFAULT 0,
                withdrawal REAL DEFAULT 0,
                capital REAL DEFAULT 0,
                value REAL DEFAULT 0,
                total_gainloss REAL DEFAULT 0,
                realized_gainloss REAL DEFAULT 0,
                unrealized_gainloss REAL DEFAULT 0,
                total_gainloss_per REAL DEFAULT 0,
                realized_gainloss_per REAL DEFAULT 0,
                unrealized_gainloss_per REAL DEFAULT 0,
                annual_per_yield REAL DEFAULT NULL,
                acc_deposit REAL DEFAULT 0,
                acc_value REAL DEFAULT 0,
                acc_withdrawal REAL DEFAULT 0,
                acc_net_deposit REAL DEFAULT 0,
                acc_total_gainloss REAL DEFAULT 0,
                acc_realized_gainloss REAL DEFAULT 0,
                acc_unrealized_gainloss REAL DEFAULT 0,
                PRIMARY KEY(year)
                );""")

        # Migrate: add transfer_net column if missing (existing databases)
        try:
            cursor.execute("ALTER TABLE cohort_data ADD COLUMN transfer_net REAL DEFAULT 0")
        except Exception:
            pass  # Column already exists

        self.conn.commit()

        # Return a list of tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in cursor.fetchall()]

    def reset_table(self, table: str) -> int:
        """
        Deletes all rows from the specified table. Raises exception if the table does not exist.

        Parameters:
        table (str): Name of the table to be reset.

        Returns:
        int: Number of rows deleted from the table.
        """
        if not table in self.tables:
            raise Exception("Table {} does not exist.".format(table))
        
        cursor = self.get_cursor()

        cursor.execute("DELETE FROM {}".format(table))

        self.commit()

        return cursor.rowcount
    
    def reset_tables(self) -> int:
        """
        Deletes all rows from all tables.

        Returns:
        int: Number of rows deleted from all tables.
        """

        cursor = self.get_cursor()

        # Delete all rows from all tables
        for table in self.tables:
            cursor.execute("DELETE FROM {}".format(table))

        self.commit()

        return cursor.rowcount

    def get_db_stats(self, stats: list) -> dict:
        """
        Returns a dictionary with the requested stats from the database. Available stats are:
        * "Transactions" - Number of transactions
        * "Unprocessed" - Number of unprocessed transactions
        * "Processed" - Number of processed transactions
        * "Assets" - Number of unique assets
        * "Capital" - Total capital
        * "Tables" - Number of tables in the database

        Parameters:
        stats (list): List of stats to be retreived from the database.

        Returns:
        dict: Dictionary with the requested stats from the database.
        """
        if not self.conn:
            raise Exception("Database connection not established.")

        cursor = self.conn.cursor()

        # Create a dictionary to store the stats
        stat_value = {}

        # Get number of transactions
        if "Transactions" in stats:
            cursor.execute("SELECT COUNT(*) FROM transactions")
            stat_value["Transactions"] = cursor.fetchone()[0]

        # Get number of processed transactions
        if "Processed" in stats:
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE processed = 1")
            stat_value["Processed"] = cursor.fetchone()[0]

        # Get number of unprocessed transactions
        if "Unprocessed" in stats:
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE processed = 0")
            stat_value["Unprocessed"] = cursor.fetchone()[0]

        # Get number of unique assets
        if "Assets" in stats:
            cursor.execute("SELECT COUNT(*) FROM assets")
            stat_value["Assets"] = cursor.fetchone()[0]

        # Get total capital
        if "Capital" in stats:
            # Take SUM of capital if there are any rows in cohort_data, otherwise set capital to 0
            cursor.execute("SELECT CASE WHEN COUNT(*) > 0 THEN SUM(capital) ELSE 0 END FROM cohort_data")
            stat_value["Capital"] = cursor.fetchone()[0]

        # Get number of tables
        if "Tables" in stats:
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            stat_value["Tables"] = cursor.fetchone()[0]

        return stat_value

    def get_db_stat(self, stat: str) -> float:
        """
        Function that takes a single string corresponding to a stat in get_db_stats

        Parameters:
        stat (str): String corresponding to a stat in get_db_stats

        Returns:
        int or float: Value of the requested stat
        """
        return self.get_db_stats([stat])[stat]

    def set_metadata(self, key: str, value: str) -> None:
        """
        Set a metadata key-value pair.
        
        Parameters:
        key (str): Metadata key
        value (str): Metadata value
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()

    def get_metadata(self, key: str, default: str = None) -> str:
        """
        Get a metadata value by key.
        
        Parameters:
        key (str): Metadata key
        default (str): Default value if key doesn't exist
        
        Returns:
        str: Metadata value or default
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM metadata WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else default

    def get_all_metadata(self) -> dict:
        """
        Get all metadata as a dictionary.
        
        Returns:
        dict: All metadata key-value pairs
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value FROM metadata")
        return dict(cursor.fetchall())

    def set_account_nickname(self, account_id: str, nickname: str) -> None:
        """
        Set a nickname for an account.
        
        Parameters:
        account_id (str): Account ID
        nickname (str): Nickname for the account
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO accounts (account_id, nickname) VALUES (?, ?)",
            (account_id, nickname)
        )
        self.conn.commit()

    def get_account_nickname(self, account_id: str) -> str:
        """
        Get the nickname for an account.
        
        Parameters:
        account_id (str): Account ID
        
        Returns:
        str: Nickname or None if not set
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT nickname FROM accounts WHERE account_id = ?", (account_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def remove_account_nickname(self, account_id: str) -> bool:
        """
        Remove the nickname for an account.
        
        Parameters:
        account_id (str): Account ID
        
        Returns:
        bool: True if a nickname was removed, False if none existed
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE account_id = ?", (account_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_all_account_nicknames(self) -> dict:
        """
        Get all account nicknames as a dictionary.
        
        Returns:
        dict: Account ID -> nickname mappings
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT account_id, nickname FROM accounts WHERE nickname IS NOT NULL")
        return dict(cursor.fetchall())


# Example Usage
if __name__ == "__main__":
    # Connect to asset_data.db sqllite3 database
    db_handler = DatabaseHandler('./data/asset_data.db')
    db_handler.connect()

    # Create table for storing transactions if it does not exist
    db_handler.create_tables()

    # Get stats from database
    stats = ["Transactions", "Processed", "Unprocessed", "Assets", "Capital", "Tables"]
    stats = db_handler.get_db_stats(stats)

    # Print each stat and its value
    for stat in stats:
        print(stat, stats[stat])

    db_handler.disconnect()