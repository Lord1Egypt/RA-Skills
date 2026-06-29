"""SQLite database handler for financial-categorizer.

Manages tables for transactions, categories, match rules, manual overrides,
and metadata. Follows a connect/disconnect pattern with date type adapters.
"""

import sqlite3
from datetime import date, datetime


def adapt_date(val):
    """Convert datetime.date to ISO format string for SQLite storage."""
    return val.isoformat()


def convert_date(val):
    """Convert ISO format string from SQLite to datetime.date."""
    return date.fromisoformat(val.decode() if isinstance(val, bytes) else val)


def adapt_datetime(val):
    """Convert datetime.datetime to ISO format string for SQLite storage."""
    return val.isoformat()


def convert_datetime(val):
    """Convert ISO format string from SQLite to datetime.datetime."""
    s = val.decode() if isinstance(val, bytes) else val
    return datetime.fromisoformat(s)


sqlite3.register_adapter(date, adapt_date)
sqlite3.register_converter("date", convert_date)
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)


class DatabaseHandler:
    """Handles connection to a SQLite database for financial categorization.

    Creates the schema on init. Supports connect/disconnect/commit pattern
    with PARSE_DECLTYPES and PARSE_COLNAMES for automatic type conversion.

    For :memory: databases, the connection is kept open after init since
    closing it would destroy all data. For file-based databases, the
    connection is closed after schema creation.
    """

    def __init__(self, db_file: str):
        """
        Args:
            db_file: Path to the SQLite database file. Use ':memory:' for
                     an in-memory database (useful for testing).
        """
        self.db_file = db_file
        self.conn = None
        self.connect()
        self.create_tables()
        # Keep connection open for :memory: databases (data is lost on disconnect)
        if db_file != ":memory:":
            self.disconnect()

    def connect(self) -> None:
        """Open a connection with type parsing enabled."""
        if self.db_file != ":memory:":
            import os
            db_dir = os.path.dirname(self.db_file)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
        self.conn = sqlite3.connect(
            self.db_file,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def disconnect(self) -> None:
        """Close the current connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    # Alias — follows Python convention
    close = disconnect

    def commit(self) -> None:
        """Commit pending changes. Raises if not connected."""
        if self.conn:
            self.conn.commit()
        else:
            raise RuntimeError("Cannot commit: no database connection.")

    def get_cursor(self) -> sqlite3.Cursor:
        """Return a cursor, connecting automatically if needed."""
        if self.conn is None:
            self.connect()
        return self.conn.cursor()

    # ------------------------------------------------------------------ #
    #  Schema
    # ------------------------------------------------------------------ #

    def create_tables(self) -> list[str]:
        """Create all tables if they don't exist. Returns table names."""
        if not self.conn:
            raise RuntimeError("Database connection not established.")

        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT UNIQUE NOT NULL,
                parent_id   INTEGER REFERENCES categories(id) ON DELETE SET NULL,
                category_type TEXT NOT NULL DEFAULT 'expense'
                              CHECK(category_type IN ('income','expense','transfer')),
                description TEXT,
                associated_account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT UNIQUE NOT NULL,
                type            TEXT NOT NULL DEFAULT 'tracked'
                                CHECK(type IN ('tracked','external')),
                ownership_ratio REAL NOT NULL DEFAULT 1.0
                                CHECK(ownership_ratio > 0 AND ownership_ratio <= 1.0),
                currency        TEXT NOT NULL DEFAULT 'SEK',
                description     TEXT,
                cash_neutral    INTEGER NOT NULL DEFAULT 0 CHECK(cash_neutral IN (0, 1))
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        DATE NOT NULL,
                description TEXT NOT NULL,
                amount      REAL NOT NULL,
                account_id  INTEGER NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
                source_file TEXT,
                imported_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
                comment     TEXT,
                status      TEXT NOT NULL DEFAULT 'settled'
                            CHECK(status IN ('pending','settled')),
                matched_rule_id INTEGER REFERENCES match_rules(id) ON DELETE SET NULL,
                adjusted_amount REAL,
                UNIQUE(date, description, amount, account_id, status)
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS match_rules(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                pattern     TEXT NOT NULL,
                match_type  TEXT NOT NULL DEFAULT 'regex'
                            CHECK(match_type IN ('regex','exact','contains')),
                priority    INTEGER DEFAULT 0,
                amount_min  REAL,
                amount_max  REAL,
                enabled     INTEGER DEFAULT 1,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS id_matches(
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
                category_id    INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(transaction_id)
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS transaction_links(
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                from_transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
                to_transaction_id   INTEGER REFERENCES transactions(id) ON DELETE CASCADE,
                link_type           TEXT NOT NULL CHECK(link_type IN ('internal_transfer','external_transfer','reimbursement')),
                ratio               REAL NOT NULL DEFAULT 1.0
                                    CHECK(ratio > 0 AND ratio <= 1.0),
                created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                comment             TEXT,
                to_account_id       INTEGER REFERENCES accounts(id) ON DELETE SET NULL
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS transfer_rules(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern     TEXT NOT NULL,
                match_type  TEXT NOT NULL DEFAULT 'contains'
                            CHECK(match_type IN ('regex','exact','contains')),
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS metadata(
                key   TEXT PRIMARY KEY,
                value TEXT
            )""")

        self.conn.commit()

        # Check and migrate schemas dynamically if tables already existed without the new columns
        cur.execute("PRAGMA table_info(transaction_links)")
        cols_links = [row[1] for row in cur.fetchall()]
        if "to_account_id" not in cols_links:
            cur.execute("ALTER TABLE transaction_links ADD COLUMN to_account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL")

        cur.execute("PRAGMA table_info(categories)")
        cols_cats = [row[1] for row in cur.fetchall()]
        if "associated_account_id" not in cols_cats:
            cur.execute("ALTER TABLE categories ADD COLUMN associated_account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL")

        cur.execute("PRAGMA table_info(accounts)")
        cols_accounts = [row[1] for row in cur.fetchall()]
        if "cash_neutral" not in cols_accounts:
            cur.execute("PRAGMA foreign_keys = OFF;")
            try:
                cur.execute("ALTER TABLE accounts RENAME TO accounts_old;")
                cur.execute("""
                    CREATE TABLE accounts(
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        name            TEXT UNIQUE NOT NULL,
                        type            TEXT NOT NULL DEFAULT 'tracked'
                                        CHECK(type IN ('tracked','external')),
                        ownership_ratio REAL NOT NULL DEFAULT 1.0
                                        CHECK(ownership_ratio > 0 AND ownership_ratio <= 1.0),
                        currency        TEXT NOT NULL DEFAULT 'SEK',
                        description     TEXT,
                        cash_neutral    INTEGER NOT NULL DEFAULT 0 CHECK(cash_neutral IN (0, 1))
                    )""")
                cur.execute("""
                    INSERT INTO accounts (id, name, type, ownership_ratio, currency, description, cash_neutral)
                    SELECT 
                        id, 
                        name, 
                        CASE 
                            WHEN type IN ('personal', 'shared') THEN 'tracked'
                            ELSE 'external'
                        END,
                        ownership_ratio, 
                        currency, 
                        description,
                        0
                    FROM accounts_old
                """)
                cur.execute("DROP TABLE accounts_old;")
                self.conn.commit()
            finally:
                cur.execute("PRAGMA foreign_keys = ON;")

        self.conn.commit()

        # Check if any tables still have references to "accounts_old" (which occurs if upgraded to bugged v1.1.0)
        cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND sql LIKE '%accounts_old%'")
        corrupted_tables = cur.fetchall()
        if corrupted_tables:
            self.conn.commit()
            old_isolation = self.conn.isolation_level
            self.conn.isolation_level = None
            try:
                # Drop all views first to prevent broken view references from blocking table renames/DDL
                cur.execute("SELECT name FROM sqlite_master WHERE type='view'")
                views = [r[0] for r in cur.fetchall()]
                for view_name in views:
                    cur.execute(f"DROP VIEW IF EXISTS {view_name};")
                
                cur.execute("PRAGMA foreign_keys = OFF;")
                cur.execute("BEGIN TRANSACTION;")
                for table_name, old_sql in corrupted_tables:
                    # Replace references to accounts_old with accounts
                    new_sql = old_sql.replace('"accounts_old"', 'accounts').replace('accounts_old', 'accounts')
                    
                    cur.execute(f"ALTER TABLE {table_name} RENAME TO {table_name}_old;")
                    cur.execute(new_sql)
                    
                    # Copy columns dynamically
                    cur.execute(f"PRAGMA table_info({table_name}_old)")
                    cols = [r[1] for r in cur.fetchall()]
                    cols_str = ", ".join(f'"{c}"' for c in cols)
                    cur.execute(f"INSERT INTO {table_name} ({cols_str}) SELECT {cols_str} FROM {table_name}_old")
                    cur.execute(f"DROP TABLE {table_name}_old;")
                cur.execute("COMMIT;")
            except Exception as e:
                try:
                    cur.execute("ROLLBACK;")
                except sqlite3.OperationalError:
                    pass
                raise e
            finally:
                cur.execute("PRAGMA foreign_keys = ON;")
                self.conn.isolation_level = old_isolation
            self.conn.commit()
            
            # Recreate all views dynamically
            from financial_categorizer.stats import Stats
            stats = Stats(self)
            stats._ensure_views()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cur.fetchall()]

    # ------------------------------------------------------------------ #
    #  Metadata helpers
    # ------------------------------------------------------------------ #

    def set_metadata(self, key: str, value: str) -> None:
        cur = self.get_cursor()
        cur.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
            (key, value),
        )
        self.commit()

    def get_metadata(self, key: str, default: str = None) -> str | None:
        cur = self.get_cursor()
        cur.execute("SELECT value FROM metadata WHERE key = ?", (key,))
        row = cur.fetchone()
        return row[0] if row else default

    def get_all_metadata(self) -> dict:
        cur = self.get_cursor()
        cur.execute("SELECT key, value FROM metadata")
        return dict(cur.fetchall())

    # ------------------------------------------------------------------ #
    #  Account helpers
    # ------------------------------------------------------------------ #

    def add_account(
        self,
        name: str,
        type: str = "tracked",
        ownership_ratio: float = 1.0,
        currency: str = "SEK",
        description: str = None,
        cash_neutral: int = 0,
    ) -> int:
        """Add a new account. Returns the account id."""
        cur = self.get_cursor()
        cur.execute(
            "INSERT INTO accounts (name, type, ownership_ratio, currency, description, cash_neutral) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, type, ownership_ratio, currency, description, cash_neutral),
        )
        self.commit()
        return cur.lastrowid

    def get_account(self, account_id: int) -> dict | None:
        """Look up an account by ID."""
        cur = self.get_cursor()
        cur.execute(
            "SELECT id, name, type, ownership_ratio, currency, description, cash_neutral "
            "FROM accounts WHERE id = ?",
            (account_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "ownership_ratio": row[3],
            "currency": row[4],
            "description": row[5],
            "cash_neutral": row[6],
        }

    def get_account_by_name(self, name: str) -> dict | None:
        """Look up an account by name."""
        cur = self.get_cursor()
        cur.execute(
            "SELECT id, name, type, ownership_ratio, currency, description, cash_neutral "
            "FROM accounts WHERE name = ?",
            (name,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "ownership_ratio": row[3],
            "currency": row[4],
            "description": row[5],
            "cash_neutral": row[6],
        }

    def list_accounts(self) -> list[dict]:
        """Return all accounts."""
        cur = self.get_cursor()
        cur.execute(
            "SELECT id, name, type, ownership_ratio, currency, description, cash_neutral "
            "FROM accounts ORDER BY name"
        )
        return [
            {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "ownership_ratio": row[3],
                "currency": row[4],
                "description": row[5],
                "cash_neutral": row[6],
            }
            for row in cur.fetchall()
        ]

    def update_account(
        self,
        account_id: int,
        name: str | None = None,
        type: str | None = None,
        ownership_ratio: float | None = None,
        currency: str | None = None,
        description: str | None = ...,
        cash_neutral: int | None = None,
    ) -> bool:
        """Update an account's fields. Returns True if any change was made."""
        updates = []
        params = []
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if type is not None:
            updates.append("type = ?")
            params.append(type)
        if ownership_ratio is not None:
            old = self.get_account(account_id)
            updates.append("ownership_ratio = ?")
            params.append(ownership_ratio)
        else:
            old = None
        if currency is not None:
            updates.append("currency = ?")
            params.append(currency)
        if description is not ...:
            updates.append("description = ?")
            params.append(description)
        if cash_neutral is not None:
            updates.append("cash_neutral = ?")
            params.append(cash_neutral)

        if not updates:
            return False

        params.append(account_id)
        cur = self.get_cursor()
        cur.execute(
            f"UPDATE accounts SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        self.commit()
        changed = cur.rowcount > 0

        # If ownership_ratio changed, recalc adjusted_amount for this account's transactions
        if changed and old and old["ownership_ratio"] != ownership_ratio:
            self.recalculate_adjusted_amounts()

        return changed

    def recalculate_adjusted_amounts(self) -> int:
        """Recalculate adjusted_amount for all transactions.

        Step 1: base = amount * account.ownership_ratio
        Step 2: apply link adjustments:
          - external_transfer (no to_id): adjusted_amount = 0
          - internal_transfer: both sides neutralize toward 0, scaled by ratio
          - reimbursement: from side (reimb) neutralizes to 0,
            to side (expense) gets credited by from's amount * ratio
        """
        cur = self.get_cursor()

        # Step 1: base = amount * ownership_ratio
        cur.execute(
            "UPDATE transactions SET adjusted_amount = amount * "
            "(SELECT ownership_ratio FROM accounts WHERE accounts.id = transactions.account_id)"
        )
        total_updated = cur.rowcount

        # Step 2: apply link adjustments in Python (handles multiple links per txn)
        cur.execute(
            "SELECT from_transaction_id, to_transaction_id, link_type, ratio "
            "FROM transaction_links"
        )
        links = cur.fetchall()

        # Build per-transaction adjustments
        adjustments: dict[int, float] = {}  # txn_id -> delta to apply

        for from_id, to_id, link_type, ratio in links:
            if link_type == "external_transfer":
                adjustments[from_id] = "ZERO"  # marker to set to 0
            elif link_type == "reimbursement":
                # Get raw amount and ownership ratio for the reimbursement transaction
                cur.execute(
                    "SELECT t.amount, a.ownership_ratio FROM transactions t "
                    "JOIN accounts a ON t.account_id = a.id WHERE t.id = ?",
                    (from_id,)
                )
                from_amount, from_ratio = cur.fetchone()
                
                # Neutralize the reimbursement side completely (scaled by ratio)
                adjustments[from_id] = adjustments.get(from_id, 0) - (from_amount * from_ratio * ratio)
                
                # Credit the original expense transaction, scaled by the target account's ownership ratio
                if to_id is not None:
                    cur.execute(
                        "SELECT a.ownership_ratio FROM transactions t "
                        "JOIN accounts a ON t.account_id = a.id WHERE t.id = ?",
                        (to_id,)
                    )
                    to_ratio = cur.fetchone()[0]
                    adjustments[to_id] = adjustments.get(to_id, 0) + (from_amount * to_ratio * ratio)
            elif link_type == "internal_transfer":
                # Both sides neutralize to 0
                cur.execute("SELECT adjusted_amount FROM transactions WHERE id = ?", (from_id,))
                from_adj = cur.fetchone()[0]
                adjustments[from_id] = adjustments.get(from_id, 0) - from_adj * ratio
                if to_id is not None:
                    cur.execute("SELECT adjusted_amount FROM transactions WHERE id = ?", (to_id,))
                    to_adj = cur.fetchone()[0]
                    adjustments[to_id] = adjustments.get(to_id, 0) - to_adj * ratio

        # Apply adjustments
        for txn_id, delta in adjustments.items():
            if delta == "ZERO":
                cur.execute(
                    "UPDATE transactions SET adjusted_amount = 0 WHERE id = ?", (txn_id,)
                )
            else:
                cur.execute(
                    "UPDATE transactions SET adjusted_amount = adjusted_amount + ? WHERE id = ?",
                    (delta, txn_id),
                )

        self.commit()
        return total_updated

    def cleanup_orphaned_records(self, dry_run: bool = False) -> dict:
        """Find and optionally delete orphaned rows in id_matches and transaction_links.

        Returns a dict with count of orphaned records identified/removed:
        {
            "orphaned_id_matches": int,
            "orphaned_links": int
        }
        """
        cur = self.get_cursor()

        # Find orphaned id_matches
        cur.execute(
            "SELECT COUNT(*) FROM id_matches "
            "WHERE transaction_id NOT IN (SELECT id FROM transactions)"
        )
        orphaned_id_matches = cur.fetchone()[0]

        # Find orphaned transaction_links
        cur.execute(
            "SELECT COUNT(*) FROM transaction_links "
            "WHERE from_transaction_id NOT IN (SELECT id FROM transactions) "
            "OR (to_transaction_id IS NOT NULL AND to_transaction_id NOT IN (SELECT id FROM transactions))"
        )
        orphaned_links = cur.fetchone()[0]

        if not dry_run:
            # Delete orphaned id_matches
            cur.execute(
                "DELETE FROM id_matches "
                "WHERE transaction_id NOT IN (SELECT id FROM transactions)"
            )
            # Delete orphaned transaction_links
            cur.execute(
                "DELETE FROM transaction_links "
                "WHERE from_transaction_id NOT IN (SELECT id FROM transactions) "
                "OR (to_transaction_id IS NOT NULL AND to_transaction_id NOT IN (SELECT id FROM transactions))"
            )
            self.commit()

            # Recalculate adjusted amounts in case any links were removed
            if orphaned_links > 0:
                self.recalculate_adjusted_amounts()

        return {
            "orphaned_id_matches": orphaned_id_matches,
            "orphaned_links": orphaned_links
        }

    def delete_account(self, account_id: int) -> bool:
        """Delete an account. Fails if transactions reference it (ON DELETE RESTRICT).

        Returns True if the account was deleted.
        """
        cur = self.get_cursor()
        cur.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        self.commit()
        return cur.rowcount > 0

    def ensure_account(self, name: str, **kwargs) -> int:
        """Get account ID by name, creating it if it doesn't exist.

        Extra kwargs passed to add_account on creation.
        Returns the account ID.
        """
        existing = self.get_account_by_name(name)
        if existing:
            return existing["id"]
        return self.add_account(name, **kwargs)

    # ------------------------------------------------------------------ #
    #  Transfer rules
    # ------------------------------------------------------------------ #

    def get_transfer_rules(self) -> list[dict]:
        cur = self.get_cursor()
        cur.execute(
            "SELECT id, pattern, match_type, created_at FROM transfer_rules ORDER BY id"
        )
        return [
            {"id": r[0], "pattern": r[1], "match_type": r[2], "created_at": r[3]}
            for r in cur.fetchall()
        ]

    def add_transfer_rule(self, pattern: str, match_type: str = "contains") -> int:
        cur = self.get_cursor()
        cur.execute(
            "INSERT INTO transfer_rules (pattern, match_type) VALUES (?, ?)",
            (pattern, match_type),
        )
        self.commit()
        return cur.lastrowid

    def remove_transfer_rule(self, rule_id: int) -> bool:
        cur = self.get_cursor()
        cur.execute("DELETE FROM transfer_rules WHERE id = ?", (rule_id,))
        self.commit()
        return cur.rowcount > 0

    def get_transactions(
        self,
        category_id: int | None = None,
        uncategorized_only: bool = False,
        non_zero: bool = False,
        account_id: int | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """Query transactions from the database with optional filters.

        Args:
            category_id: Filter by category ID.
            uncategorized_only: If True, only return transactions with category_id IS NULL.
            non_zero: If True, exclude transactions with adjusted_amount = 0.
            account_id: Filter by account ID.
            limit: Maximum number of transactions to return.

        Returns:
            List of transaction dictionaries.
        """
        sql = """
            SELECT t.id, t.date, t.description, t.amount, t.adjusted_amount,
                   t.category_id, c.name AS category_name, a.name AS account_name
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE 1=1
        """
        params = []
        if category_id is not None:
            sql += " AND t.category_id = ?"
            params.append(category_id)
        if uncategorized_only:
            sql += " AND t.category_id IS NULL"
        if non_zero:
            sql += " AND (t.adjusted_amount IS NULL OR t.adjusted_amount != 0)"
        if account_id is not None:
            sql += " AND t.account_id = ?"
            params.append(account_id)

        sql += " ORDER BY t.date DESC, t.id DESC LIMIT ?"
        params.append(limit)

        cur = self.get_cursor()
        cur.execute(sql, tuple(params))
        return [
            {
                "id": row[0],
                "date": row[1],
                "description": row[2],
                "amount": row[3],
                "adjusted_amount": row[4],
                "category_id": row[5],
                "category_name": row[6],
                "account_name": row[7],
            }
            for row in cur.fetchall()
        ]

    def get_transaction_rule_match(self, transaction_id: int) -> dict | None:
        """Get the rule or manual match details that categorized a transaction.

        Returns:
            A dictionary with categorization explanation, or None if transaction not found.
        """
        cur = self.get_cursor()
        cur.execute(
            "SELECT t.id, t.date, t.description, t.amount, t.category_id, t.matched_rule_id, "
            "       c.name AS category_name "
            "FROM transactions t "
            "LEFT JOIN categories c ON c.id = t.category_id "
            "WHERE t.id = ?",
            (transaction_id,),
        )
        row = cur.fetchone()
        if not row:
            return None

        txn_id, txn_date, txn_desc, txn_amt, cat_id, rule_id, cat_name = row

        # Check if it was manually overridden
        cur.execute(
            "SELECT category_id FROM id_matches WHERE transaction_id = ?",
            (transaction_id,),
        )
        is_manual = cur.fetchone() is not None

        source = "uncategorized"
        rule_pattern = None
        rule_match_type = None

        if cat_id is not None:
            if is_manual:
                source = "manual"
            elif rule_id is not None:
                source = "rule"
                cur.execute(
                    "SELECT pattern, match_type FROM match_rules WHERE id = ?",
                    (rule_id,),
                )
                rule_row = cur.fetchone()
                if rule_row:
                    rule_pattern, rule_match_type = rule_row

        return {
            "id": txn_id,
            "date": txn_date,
            "description": txn_desc,
            "amount": txn_amt,
            "category_id": cat_id,
            "category_name": cat_name,
            "source": source,
            "rule_id": rule_id,
            "rule_pattern": rule_pattern,
            "rule_match_type": rule_match_type,
        }


# ------------------------------------------------------------------ #
#  Transfer Manager
# ------------------------------------------------------------------ #

VALID_LINK_TYPES = ("internal_transfer", "external_transfer", "reimbursement")


class TransferManager:
    """Manages transaction links (transfers, reimbursements).

    Links connect transactions to adjust their adjusted_amount:
    - internal_transfer: between own accounts (neutralize both sides)
    - external_transfer: outgoing to non-tracked account (set to 0)
    - reimbursement: partial/full refund of an expense
    """

    def __init__(self, db_handler: DatabaseHandler):
        self.db = db_handler

    def link_transactions(
        self,
        from_transaction_id: int,
        to_transaction_id: int | None,
        link_type: str,
        ratio: float = 1.0,
        comment: str | None = None,
        to_account_id: int | None = None,
    ) -> int:
        """Create a link between two transactions. Returns the link id."""
        if link_type not in VALID_LINK_TYPES:
            raise ValueError(f"Invalid link_type. Must be one of {VALID_LINK_TYPES}")
        if link_type == "internal_transfer" and to_transaction_id is None:
            raise ValueError("to_transaction_id is required for internal_transfer")
        if link_type == "external_transfer" and to_transaction_id is not None:
            raise ValueError("external_transfer does not take a to_transaction_id")

        cur = self.db.get_cursor()
        # Verify transactions exist
        cur.execute("SELECT id FROM transactions WHERE id = ?", (from_transaction_id,))
        if not cur.fetchone():
            raise ValueError(f"from_transaction_id {from_transaction_id} not found")
        if to_transaction_id is not None:
            cur.execute("SELECT id FROM transactions WHERE id = ?", (to_transaction_id,))
            if not cur.fetchone():
                raise ValueError(f"to_transaction_id {to_transaction_id} not found")
        if to_account_id is not None:
            cur.execute("SELECT id FROM accounts WHERE id = ?", (to_account_id,))
            if not cur.fetchone():
                raise ValueError(f"to_account_id {to_account_id} not found")

        cur.execute(
            "INSERT INTO transaction_links (from_transaction_id, to_transaction_id, link_type, ratio, comment, to_account_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (from_transaction_id, to_transaction_id, link_type, ratio, comment, to_account_id),
        )
        self.db.commit()
        link_id = cur.lastrowid

        self.db.recalculate_adjusted_amounts()
        return link_id

    def unlink(self, link_id: int) -> bool:
        """Remove a link. Returns True if it existed."""
        cur = self.db.get_cursor()
        cur.execute("DELETE FROM transaction_links WHERE id = ?", (link_id,))
        self.db.commit()
        removed = cur.rowcount > 0
        if removed:
            self.db.recalculate_adjusted_amounts()
        return removed

    def get_links(self, transaction_id: int) -> list[dict]:
        """Get all links involving a transaction."""
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT id, from_transaction_id, to_transaction_id, link_type, ratio, created_at, comment, to_account_id "
            "FROM transaction_links "
            "WHERE from_transaction_id = ? OR to_transaction_id = ?",
            (transaction_id, transaction_id),
        )
        return [
            {
                "id": row[0],
                "from_transaction_id": row[1],
                "to_transaction_id": row[2],
                "link_type": row[3],
                "ratio": row[4],
                "created_at": row[5],
                "comment": row[6],
                "to_account_id": row[7],
            }
            for row in cur.fetchall()
        ]

    def list_links(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
        link_type: str | None = None,
    ) -> list[dict]:
        """List links, optionally filtered by date range and type."""
        cur = self.db.get_cursor()
        conditions = []
        params = []

        if link_type is not None:
            conditions.append("tl.link_type = ?")
            params.append(link_type)
        if date_from is not None:
            conditions.append("t.date >= ?")
            params.append(date_from)
        if date_to is not None:
            conditions.append("t.date <= ?")
            params.append(date_to)

        where = ""
        if conditions:
            where = "WHERE " + " AND ".join(conditions)

        cur.execute(
            f"SELECT tl.id, tl.from_transaction_id, tl.to_transaction_id, "
            f"tl.link_type, tl.ratio, tl.created_at, tl.comment, tl.to_account_id "
            f"FROM transaction_links tl "
            f"JOIN transactions t ON t.id = tl.from_transaction_id "
            f"{where} ORDER BY tl.created_at",
            params,
        )
        return [
            {
                "id": row[0],
                "from_transaction_id": row[1],
                "to_transaction_id": row[2],
                "link_type": row[3],
                "ratio": row[4],
                "created_at": row[5],
                "comment": row[6],
                "to_account_id": row[7],
            }
            for row in cur.fetchall()
        ]

    def suggest_links(self, days_tolerance: int = 3, min_amount: float = 10.0) -> list[dict]:
        """Suggest potential internal transfers between own accounts.

        Finds pairs of transactions where:
        - They belong to different accounts
        - Their amounts are negatives of each other (one in, one out)
        - Dates are within days_tolerance of each other
        - Neither is already linked
        - Absolute amount >= min_amount (filters noise)

        Returns list of dicts with from/to transaction details.
        """
        cur = self.db.get_cursor()

        # Get transactions not already involved in any link
        cur.execute("""
            SELECT t.id, t.account_id, t.date, t.amount, t.adjusted_amount,
                   t.description, a.name as account_name
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            WHERE t.id NOT IN (
                SELECT from_transaction_id FROM transaction_links
                UNION
                SELECT to_transaction_id FROM transaction_links WHERE to_transaction_id IS NOT NULL
            )
            AND ABS(t.amount) >= ?
            ORDER BY t.date DESC, ABS(t.amount) DESC
        """, (min_amount,))

        rows = [
            {
                "id": r[0], "account_id": r[1], "date": r[2],
                "amount": r[3], "adjusted_amount": r[4],
                "description": r[5], "account_name": r[6],
            }
            for r in cur.fetchall()
        ]

        suggestions = []
        used = set()

        for i, a in enumerate(rows):
            if a["id"] in used:
                continue
            for j in range(i + 1, len(rows)):
                b = rows[j]
                if b["id"] in used:
                    continue
                # Must be different accounts
                if a["account_id"] == b["account_id"]:
                    continue
                # Amounts must be opposites (one positive, one negative, same magnitude)
                if abs(a["amount"] + b["amount"]) > 0.01:
                    continue
                # Dates must be close
                if abs((a["date"] - b["date"]).days) > days_tolerance:
                    continue

                # a is the outgoing (negative), b is the incoming (positive)
                if a["amount"] > 0:
                    a, b = b, a

                suggestions.append({
                    "from_transaction_id": a["id"],
                    "from_date": a["date"],
                    "from_amount": a["amount"],
                    "from_description": a["description"],
                    "from_account": a["account_name"],
                    "to_transaction_id": b["id"],
                    "to_date": b["date"],
                    "to_amount": b["amount"],
                    "to_description": b["description"],
                    "to_account": b["account_name"],
                    "days_apart": abs((a["date"] - b["date"]).days),
                })
                used.add(a["id"])
                used.add(b["id"])
                break  # each transaction matches at most once

        return suggestions

    # ------------------------------------------------------------------
    #  Transfer rules
    # ------------------------------------------------------------------

    def get_transfer_rules(self) -> list[dict]:
        cur = self.db.get_cursor()
        cur.execute(
            "SELECT id, pattern, match_type, created_at FROM transfer_rules ORDER BY id"
        )
        return [
            {"id": r[0], "pattern": r[1], "match_type": r[2], "created_at": r[3]}
            for r in cur.fetchall()
        ]

    def add_transfer_rule(self, pattern: str, match_type: str = "contains") -> int:
        cur = self.db.get_cursor()
        cur.execute(
            "INSERT INTO transfer_rules (pattern, match_type) VALUES (?, ?)",
            (pattern, match_type),
        )
        self.db.commit()
        return cur.lastrowid

    def remove_transfer_rule(self, rule_id: int) -> bool:
        cur = self.db.get_cursor()
        cur.execute("DELETE FROM transfer_rules WHERE id = ?", (rule_id,))
        self.db.commit()
        return cur.rowcount > 0

    def auto_link_transfers(
        self, days_tolerance: int = 3, dry_run: bool = False
    ) -> dict:
        """Auto-detect and link internal transfers using configurable transfer rules.

        External transfers are now handled by categorize (transfer-type categories).
        Returns dict with 'internal' list of created/would-be-created links.
        """
        import re

        cur = self.db.get_cursor()

        # Load configurable transfer rules
        transfer_rules = self.get_transfer_rules()

        account_number_re = re.compile(r"\d{4}\s\d{2}\s\d{5}")

        # Build account number map from descriptions of all transactions
        cur.execute("SELECT id, account_id, description FROM transactions")
        acct_num_map = {}
        for r in cur.fetchall():
            nums = account_number_re.findall(r[2] or "")
            if nums:
                acct_num_map.setdefault(r[1], set()).update(n.replace(" ", "") for n in nums)

        # Get IDs of already-linked transactions
        cur.execute("SELECT from_transaction_id FROM transaction_links")
        linked_from = {r[0] for r in cur.fetchall()}
        cur.execute("SELECT to_transaction_id FROM transaction_links WHERE to_transaction_id IS NOT NULL")
        linked_to = {r[0] for r in cur.fetchall()}
        already_linked = linked_from | linked_to

        # --- Internal transfer detection ---
        cur.execute("""
            SELECT t.id, t.account_id, t.date, t.amount, t.description, a.name
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            ORDER BY t.date DESC, ABS(t.amount) DESC
        """)
        all_txns = [
            {"id": r[0], "account_id": r[1], "date": r[2], "amount": r[3],
             "description": r[4] or "", "account_name": r[5]}
            for r in cur.fetchall()
        ]

        def matches_transfer_rule(desc: str) -> bool:
            dl = desc.lower()
            for rule in transfer_rules:
                if rule["match_type"] == "contains" and rule["pattern"].lower() in dl:
                    return True
                if rule["match_type"] == "exact" and rule["pattern"].lower() == dl:
                    return True
                if rule["match_type"] == "regex" and re.search(rule["pattern"], desc, re.IGNORECASE):
                    return True
            return False

        def has_account_number_match(a, b):
            b_nums = acct_num_map.get(b["account_id"], set())
            a_desc_nospace = a["description"].replace(" ", "")
            for n in b_nums:
                if n in a_desc_nospace:
                    return True
            a_nums = acct_num_map.get(a["account_id"], set())
            b_desc_nospace = b["description"].replace(" ", "")
            for n in a_nums:
                if n in b_desc_nospace:
                    return True
            return False

        internal_results = []
        used = set()

        candidates = [t for t in all_txns if t["id"] not in already_linked and abs(t["amount"]) >= 10]

        for i, a in enumerate(candidates):
            if a["id"] in used:
                continue
            best_match = None
            best_score = None
            for j in range(i + 1, len(candidates)):
                b = candidates[j]
                if b["id"] in used:
                    continue
                if a["account_id"] == b["account_id"]:
                    continue
                if abs(a["amount"] + b["amount"]) > 0.01:
                    continue
                days_apart = abs((a["date"] - b["date"]).days)
                if days_apart > days_tolerance:
                    continue

                # Require transfer evidence: rule match or account number match
                has_rule_match = (
                    matches_transfer_rule(a["description"]) or
                    matches_transfer_rule(b["description"])
                )
                has_acct_match = has_account_number_match(a, b)
                if not (has_rule_match or has_acct_match):
                    continue

                # Score: prefer (1) account number match, (2) fewer days apart
                score = (0 if has_acct_match else 1, days_apart)
                if best_score is None or score < best_score:
                    best_score = score
                    best_match = b

            if best_match is not None:
                b = best_match
                out_tx = a if a["amount"] < 0 else b
                in_tx = b if a["amount"] < 0 else a

                internal_results.append({
                    "from_transaction_id": out_tx["id"],
                    "to_transaction_id": in_tx["id"],
                    "from_account": out_tx["account_name"],
                    "to_account": in_tx["account_name"],
                    "amount": abs(out_tx["amount"]),
                    "from_date": out_tx["date"],
                    "to_date": in_tx["date"],
                    "from_desc": out_tx["description"],
                    "to_desc": in_tx["description"],
                })
                used.add(a["id"])
                used.add(b["id"])

        # Create links if not dry run
        if not dry_run:
            for item in internal_results:
                self.link_transactions(
                    item["from_transaction_id"], item["to_transaction_id"],
                    "internal_transfer", 1.0, "auto-linked"
                )

        return {"internal": internal_results}

    # Convenience methods

    def mark_transfer(
        self,
        from_transaction_id: int,
        to_transaction_id: int,
        ratio: float = 1.0,
        comment: str | None = None,
    ) -> int:
        """Link two transactions as an internal transfer."""
        return self.link_transactions(
            from_transaction_id, to_transaction_id, "internal_transfer", ratio, comment
        )

    def mark_external(
        self,
        transaction_id: int,
        ratio: float = 1.0,
        comment: str | None = None,
    ) -> int:
        """Mark a transaction as an external transfer."""
        return self.link_transactions(
            transaction_id, None, "external_transfer", ratio, comment
        )

    def mark_reimbursement(
        self,
        reimbursement_transaction_id: int,
        original_transaction_id: int,
        ratio: float = 1.0,
        comment: str | None = None,
    ) -> int:
        """Link a reimbursement to the original expense."""
        return self.link_transactions(
            reimbursement_transaction_id, original_transaction_id, "reimbursement", ratio, comment
        )
