import sqlite3
from datetime import date
import bisect

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
        self._price_cache = {}
        self.interpolate = True
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
            self.clear_price_cache()
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
        # origin: 'avanza' (from CSV import) or 'virtual' (synthetic, created by
        # virtual portfolio operations). Lets the import pipeline and reset logic
        # distinguish real from synthetic transactions.
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
                processed INT DEFAULT 0,
                origin TEXT DEFAULT 'avanza'
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
        # is_virtual: 1 for virtual portfolios, 0 for physical Avanza accounts.
        # parent_account: links a virtual account to its physical source.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
                account_id TEXT PRIMARY KEY,
                nickname TEXT,
                is_virtual INTEGER DEFAULT 0,
                parent_account TEXT
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

        # asset_prices contains historical asset prices (in SEK) from both
        # transaction events and external API fetches. Prices are stored in SEK:
        # transaction-sourced rows derive SEK from the CSV total (already SEK),
        # external rows are converted at fetch time using the live FX rate.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asset_prices(
                asset_id INTEGER NOT NULL,
                price_date DATE NOT NULL,
                price REAL NOT NULL,
                source TEXT CHECK(source IN ('transaction', 'external')),
                PRIMARY KEY(asset_id, price_date),
                FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
                );""")

        # exchange_rates stores live FX rates fetched during price updates.
        # One row per (currency, rate_date). SEK is the quote currency:
        # rate = how many SEK per 1 unit of `currency`. Stored for the
        # historical record and future use; NOT read by get_price (all
        # asset_prices rows are already SEK-converted at write time).
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates(
                currency TEXT NOT NULL,
                rate_date DATE NOT NULL,
                rate REAL NOT NULL,
                source TEXT,
                PRIMARY KEY(currency, rate_date)
                );""")

        # Migrate: normalize asset names (trim leading/trailing whitespace).
        # Avanza CSV exports occasionally contain instrument names with stray
        # whitespace (issue #79), which breaks exact-name lookups (e.g. account
        # allocate). Trim both transactions.asset_name and assets.asset so the
        # asset_prices backfill below (which JOINs on the name) matches cleanly.
        # Idempotent: the WHERE clause makes re-runs on already-clean data a no-op.
        cursor.execute("UPDATE transactions SET asset_name = trim(asset_name) WHERE asset_name != trim(asset_name)")
        cursor.execute("UPDATE assets SET asset = trim(asset) WHERE asset != trim(asset)")

        # Retroactive Migration: populate asset_prices with historical transaction prices from processed transactions.
        # Prices are stored in SEK. For buy/sell with a non-zero total, the SEK
        # price is derived from the CSV total (already SEK), correcting for
        # courtage sign: sell (total>0) adds courtage back, buy (total<0)
        # subtracts it. For Tillgångsinsättning (total=0), the native CSV price
        # is used as-is (the live FX fetch in update_prices will correct it).
        cursor.execute("""
            INSERT OR IGNORE INTO asset_prices (asset_id, price_date, price, source)
            SELECT a.asset_id, t.date,
                   CASE WHEN abs(t.total) > 0.0001 AND abs(t.amount) > 0.0001
                        THEN (abs(t.total) + CASE WHEN t.total > 0 THEN t.courtage ELSE -t.courtage END) / abs(t.amount)
                        ELSE t.price END,
                   'transaction'
            FROM transactions t
            JOIN assets a ON t.asset_name = a.asset
            WHERE t.processed = 1 AND t.transaction_type IN ('Köp', 'Sälj', 'Tillgångsinsättning')
            """)

        # One-time Migration (issue #81): rebuild existing transaction-sourced
        # asset_prices rows that still hold native-currency prices to SEK.
        # Guarded by a metadata flag so it only runs once. Only rows where the
        # transaction has a non-zero total are eligible (those have a derivable
        # SEK price from the CSV total); total=0 rows are left for update_prices.
        cursor.execute("SELECT value FROM metadata WHERE key = 'sek_prices_migrated'")
        if not cursor.fetchone():
            cursor.execute("""
                UPDATE asset_prices
                SET price = (
                    SELECT (abs(t.total) + CASE WHEN t.total > 0 THEN t.courtage ELSE -t.courtage END) / abs(t.amount)
                    FROM transactions t
                    JOIN assets a ON t.asset_name = a.asset
                    WHERE a.asset_id = asset_prices.asset_id
                      AND t.date = asset_prices.price_date
                      AND t.transaction_type IN ('Köp', 'Sälj')
                      AND abs(t.total) > 0.0001
                      AND abs(t.amount) > 0.0001
                    LIMIT 1
                )
                WHERE source = 'transaction'
                  AND EXISTS (
                    SELECT 1 FROM transactions t
                    JOIN assets a ON t.asset_name = a.asset
                    WHERE a.asset_id = asset_prices.asset_id
                      AND t.date = asset_prices.price_date
                      AND t.transaction_type IN ('Köp', 'Sälj')
                      AND abs(t.total) > 0.0001
                      AND abs(t.amount) > 0.0001
                  )
            """)
            cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('sek_prices_migrated', '1')")

        # Migrate: add transfer_net column if missing (existing databases)
        try:
            cursor.execute("ALTER TABLE cohort_data ADD COLUMN transfer_net REAL DEFAULT 0")
        except Exception:
            pass  # Column already exists

        # Migrate: add origin column to transactions if missing (existing databases)
        try:
            cursor.execute("ALTER TABLE transactions ADD COLUMN origin TEXT DEFAULT 'avanza'")
        except Exception:
            pass  # Column already exists

        # Migrate: add is_virtual and parent_account to accounts if missing
        try:
            cursor.execute("ALTER TABLE accounts ADD COLUMN is_virtual INTEGER DEFAULT 0")
        except Exception:
            pass  # Column already exists
        try:
            cursor.execute("ALTER TABLE accounts ADD COLUMN parent_account TEXT")
        except Exception:
            pass  # Column already exists

        # Create helper SQL views (virtual-portfolio-aware, issue #74).
        # Views are dropped and recreated on every connect, so enriching them
        # needs no migration. Accounts without a row in `accounts` (e.g. raw
        # physical accounts that only appear in transactions) default to
        # is_virtual = 0 / parent_account = NULL via the LEFT JOIN + COALESCE.
        cursor.execute("DROP VIEW IF EXISTS v_account_asset_holdings;")
        cursor.execute("""
            CREATE VIEW v_account_asset_holdings AS
                SELECT
                    t.account,
                    COALESCE(ac.is_virtual, 0) AS is_virtual,
                    ac.parent_account,
                    t.asset_name,
                    SUM(t.amount) AS held_amount
                FROM transactions t
                LEFT JOIN accounts ac ON ac.account_id = t.account
                WHERE t.transaction_type IN ('Köp', 'Sälj', 'Tillgångsinsättning', 'Värdepappersuttag', 'Byte')
                GROUP BY t.account, COALESCE(ac.is_virtual, 0), ac.parent_account, t.asset_name
                HAVING ABS(SUM(t.amount)) > 0.0001;
        """)

        cursor.execute("DROP VIEW IF EXISTS v_account_current_valuations;")
        cursor.execute("""
            CREATE VIEW v_account_current_valuations AS
                SELECT
                    acc.account,
                    COALESCE(ac.is_virtual, 0) AS is_virtual,
                    ac.parent_account,
                    COALESCE(ac.nickname, acc.account) AS display_name,
                    COALESCE((
                        SELECT SUM(total) FROM transactions WHERE account = acc.account
                    ), 0.0) AS cash,
                    COALESCE((
                        SELECT SUM(t.amount * a.latest_price)
                        FROM transactions t
                        JOIN assets a ON t.asset_name = a.asset
                        WHERE t.account = acc.account
                          AND t.transaction_type IN ('Köp', 'Sälj', 'Tillgångsinsättning', 'Värdepappersuttag', 'Byte')
                    ), 0.0) AS assets,
                    COALESCE((
                        SELECT SUM(total) FROM transactions WHERE account = acc.account
                    ), 0.0) +
                    COALESCE((
                        SELECT SUM(t.amount * a.latest_price)
                        FROM transactions t
                        JOIN assets a ON t.asset_name = a.asset
                        WHERE t.account = acc.account
                          AND t.transaction_type IN ('Köp', 'Sälj', 'Tillgångsinsättning', 'Värdepappersuttag', 'Byte')
                    ), 0.0) AS total
                FROM (SELECT DISTINCT account FROM transactions) acc
                LEFT JOIN accounts ac ON ac.account_id = acc.account;
        """)

        # Per-physical-account rollup combining the account's own valuation with
        # its virtual children, so dashboards/reports can show the hierarchy
        # (e.g. "main account incl. virtuals") directly in SQL without double
        # counting — children are summed once into the parent's combined_*.
        cursor.execute("DROP VIEW IF EXISTS v_virtual_portfolio_rollup;")
        cursor.execute("""
            CREATE VIEW v_virtual_portfolio_rollup AS
                SELECT
                    p.account AS parent_account,
                    p.display_name AS parent_display_name,
                    p.cash AS own_cash,
                    p.assets AS own_assets,
                    p.total AS own_total,
                    COALESCE(SUM(c.cash), 0.0)  AS virtual_cash,
                    COALESCE(SUM(c.assets), 0.0) AS virtual_assets,
                    COALESCE(SUM(c.total), 0.0)  AS virtual_total,
                    p.cash    + COALESCE(SUM(c.cash), 0.0)  AS combined_cash,
                    p.assets  + COALESCE(SUM(c.assets), 0.0) AS combined_assets,
                    p.total   + COALESCE(SUM(c.total), 0.0)  AS combined_total,
                    COUNT(c.account) AS virtual_count
                FROM v_account_current_valuations p
                LEFT JOIN accounts ca ON ca.parent_account = p.account AND COALESCE(ca.is_virtual, 0) = 1
                LEFT JOIN v_account_current_valuations c ON c.account = ca.account_id
                WHERE p.is_virtual = 0
                GROUP BY p.account, p.display_name, p.cash, p.assets, p.total;
        """)

        cursor.execute("DROP VIEW IF EXISTS v_external_capital_flows;")
        cursor.execute("""
            CREATE VIEW v_external_capital_flows AS
                SELECT
                    date,
                    account,
                    transaction_type,
                    origin,
                    total AS flow_amount
                FROM transactions
                WHERE transaction_type IN ('Insättning', 'Autogiroinsättning', 'Uttag', 'Intern överföring')
                UNION ALL
                SELECT
                    date,
                    account,
                    transaction_type,
                    origin,
                    amount * price AS flow_amount
                FROM transactions
                WHERE transaction_type = 'Tillgångsinsättning';
        """)

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
        # Use ON CONFLICT DO UPDATE (not INSERT OR REPLACE) so that existing
        # is_virtual / parent_account values on the row are preserved instead of
        # being wiped by a delete-and-reinsert.
        cursor.execute(
            "INSERT INTO accounts (account_id, nickname) VALUES (?, ?) "
            "ON CONFLICT(account_id) DO UPDATE SET nickname = excluded.nickname",
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
        # Only null out the nickname; keep the row so virtual-account config
        # (is_virtual / parent_account) is preserved. Empty non-virtual rows are
        # pruned afterwards to match the old "delete the row" behaviour.
        cursor.execute(
            "UPDATE accounts SET nickname = NULL WHERE account_id = ? AND nickname IS NOT NULL",
            (account_id,)
        )
        removed = cursor.rowcount > 0
        cursor.execute(
            "DELETE FROM accounts WHERE account_id = ? AND nickname IS NULL "
            "AND COALESCE(is_virtual, 0) = 0 AND parent_account IS NULL",
            (account_id,)
        )
        self.conn.commit()
        return removed

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

    # ---- Virtual account helpers (issue #74) ----

    def get_virtual_map(self) -> dict:
        """
        Return a mapping of virtual account_id -> parent_account for all
        virtual accounts (is_virtual = 1). Used by the import dedup logic and
        the hierarchical account display.
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        cursor = self.conn.cursor()
        cursor.execute("SELECT account_id, parent_account FROM accounts WHERE COALESCE(is_virtual, 0) = 1")
        return {row[0]: row[1] for row in cursor.fetchall()}

    def is_virtual_account(self, account_id: str) -> bool:
        """Return True if the given account is a virtual portfolio."""
        if not self.conn:
            raise Exception("Database connection not established.")
        cursor = self.conn.cursor()
        cursor.execute("SELECT is_virtual FROM accounts WHERE account_id = ?", (account_id,))
        row = cursor.fetchone()
        return bool(row and row[0])

    def get_account_parent(self, account_id: str):
        """Return the parent_account for an account, or None."""
        if not self.conn:
            raise Exception("Database connection not established.")
        cursor = self.conn.cursor()
        cursor.execute("SELECT parent_account FROM accounts WHERE account_id = ?", (account_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_date_range(self) -> tuple:
        """
        Get the minimum and maximum transaction dates.
        
        Returns:
        tuple: (min_date, max_date) as strings in YYYY-MM-DD format, or (None, None) if no transactions
        """
        if not self.conn:
            raise Exception("Database connection not established.")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT MIN(date), MAX(date) FROM transactions")
        result = cursor.fetchone()
        return (result[0], result[1]) if result else (None, None)

    def clear_price_cache(self) -> None:
        """Clear the in-memory price cache."""
        self._price_cache = {}

    def get_price(self, asset_id: int, target_date=None, interpolate: bool = None) -> tuple:
        """
        Get the price of an asset as of a target date.
        Uses exact match if available, otherwise linear interpolation between nearest dates.
        
        Parameters:
        asset_id (int): Asset ID.
        target_date (date or str, optional): Target date. If None, retrieves latest price.
        interpolate (bool, optional): Whether to interpolate missing prices. Defaults to self.interpolate.
        
        Returns:
        tuple: (price (float), is_interpolated (bool), interpolation_gap (int or None), price_date (date or None))
        """
        if interpolate is None:
            interpolate = self.interpolate

        if isinstance(target_date, str):
            target_date = date.fromisoformat(target_date)

        if asset_id not in self._price_cache:
            cursor = self.get_cursor()
            cursor.execute(
                "SELECT price_date, price FROM asset_prices WHERE asset_id = ? ORDER BY price_date ASC",
                (asset_id,)
            )
            rows = cursor.fetchall()
            self._price_cache[asset_id] = [(row[0], row[1]) for row in rows]

        prices = self._price_cache[asset_id]

        if not prices:
            # Fallback 1: No price points at all. Fetch from assets table.
            cursor = self.get_cursor()
            cursor.execute(
                "SELECT latest_price, average_price, average_purchase_price, latest_price_date FROM assets WHERE asset_id = ?",
                (asset_id,)
            )
            row = cursor.fetchone()
            if row:
                latest, avg, avg_pur, latest_date = row
                price = latest if latest is not None and latest > 0 else (
                    avg if avg is not None and avg > 0 else (
                        avg_pur if avg_pur is not None and avg_pur > 0 else 0.0
                    )
                )
                if isinstance(latest_date, str):
                    latest_date = date.fromisoformat(latest_date)
                return price, False, None, latest_date
            return 0.0, False, None, None

        if target_date is None:
            # Fallback 2: target_date is None. Return latest price.
            cursor = self.get_cursor()
            cursor.execute("SELECT latest_price, latest_price_date FROM assets WHERE asset_id = ?", (asset_id,))
            row = cursor.fetchone()
            if row and row[0] is not None and row[0] > 0:
                latest_price, latest_date = row[0], row[1]
                if isinstance(latest_date, str):
                    latest_date = date.fromisoformat(latest_date)
                return latest_price, False, None, latest_date
            return prices[-1][1], False, None, prices[-1][0]

        # Use bisect to find target date in the sorted list of prices
        dates = [p[0] for p in prices]
        idx = bisect.bisect_left(dates, target_date)

        # Case 1: Exact match
        if idx < len(dates) and dates[idx] == target_date:
            return prices[idx][1], False, 0, target_date

        # Case 2: Before first known price point
        if idx == 0:
            # Flat-carry the first known price forward. Do NOT use
            # assets.latest_price here — it is a current value that would
            # leak a future price into historical valuations.
            return prices[0][1], False, None, prices[0][0]

        # Case 3: After last known price point
        if idx == len(dates):
            # Try latest_price from assets first, but only if its date is >= last price date in asset_prices
            cursor = self.get_cursor()
            cursor.execute("SELECT latest_price, latest_price_date FROM assets WHERE asset_id = ?", (asset_id,))
            row = cursor.fetchone()
            if row and row[0] is not None and row[0] > 0:
                latest_price, latest_date = row[0], row[1]
                if isinstance(latest_date, str):
                    latest_date = date.fromisoformat(latest_date)
                if latest_date and latest_date >= prices[-1][0]:
                    return latest_price, False, None, latest_date
            return prices[-1][1], False, None, prices[-1][0]

        # Case 4: Between two known price points
        t_before, p_before = prices[idx - 1]
        t_after, p_after = prices[idx]

        if interpolate:
            days_total = (t_after - t_before).days
            days_target = (target_date - t_before).days
            if days_total == 0:
                return p_before, False, 0, t_before
            interpolated_price = p_before + (p_after - p_before) * (days_target / days_total)
            # Return target_date as price_date to prevent false staleness warnings
            return interpolated_price, True, days_total, target_date
        else:
            # Revert to nearest price before target date and return its actual date (so it can be flagged as stale)
            return p_before, False, None, t_before


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