"""SQLite database layer for email bridge."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import Account, AccountStatus, EmailProvider, Message, EmailCategory


DEFAULT_DB_PATH = Path.home() / ".email-bridge" / "email_bridge.db"


class Database:
    """SQLite-backed storage for accounts and messages."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._init_schema()
        return self._conn

    def _init_schema(self):
        """Initialize database schema."""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                provider TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                display_name TEXT,
                config TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                message_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                sender TEXT NOT NULL,
                sender_name TEXT,
                recipients TEXT DEFAULT '[]',
                received_at TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                is_starred INTEGER DEFAULT 0,
                category TEXT DEFAULT 'normal',
                preview TEXT,
                body_text TEXT,
                body_html TEXT,
                synced_at TEXT NOT NULL,
                provider_data TEXT DEFAULT '{}',
                UNIQUE(account_id, message_id)
            );

            CREATE INDEX IF NOT EXISTS idx_messages_account ON messages(account_id);
            CREATE INDEX IF NOT EXISTS idx_messages_received ON messages(received_at DESC);
            CREATE INDEX IF NOT EXISTS idx_messages_read ON messages(is_read);
            CREATE INDEX IF NOT EXISTS idx_messages_category ON messages(category);
        """)

    # Account operations
    def list_accounts(self, include_disabled: bool = False) -> list[Account]:
        """List all accounts."""
        query = "SELECT * FROM accounts"
        if not include_disabled:
            query += " WHERE status = ?"
            rows = self.conn.execute(query, (AccountStatus.ACTIVE.value,)).fetchall()
        else:
            rows = self.conn.execute(query).fetchall()
        return [self._row_to_account(row) for row in rows]

    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID."""
        row = self.conn.execute(
            "SELECT * FROM accounts WHERE id = ?", (account_id,)
        ).fetchone()
        return self._row_to_account(row) if row else None

    def add_account(self, account: Account) -> Account:
        """Add a new account."""
        self.conn.execute(
            """INSERT INTO accounts
               (id, email, provider, status, display_name, config, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                account.id, account.email, account.provider.value,
                account.status.value, account.display_name,
                json.dumps(account.config),
                account.created_at.isoformat(), account.updated_at.isoformat()
            )
        )
        self.conn.commit()
        return account

    def update_account(self, account: Account) -> Account:
        """Update an existing account."""
        account.updated_at = datetime.utcnow()
        self.conn.execute(
            """UPDATE accounts SET
               email = ?, provider = ?, status = ?, display_name = ?,
               config = ?, updated_at = ?
               WHERE id = ?""",
            (
                account.email, account.provider.value, account.status.value,
                account.display_name, json.dumps(account.config),
                account.updated_at.isoformat(), account.id
            )
        )
        self.conn.commit()
        return account

    def delete_account(self, account_id: str) -> bool:
        """Delete an account and its messages."""
        self.conn.execute("DELETE FROM messages WHERE account_id = ?", (account_id,))
        self.conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        self.conn.commit()
        return True

    # Message operations
    def list_messages(
        self,
        account_id: Optional[str] = None,
        unread_only: bool = False,
        category: Optional[EmailCategory] = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[Message]:
        """List messages with optional filters."""
        query = "SELECT * FROM messages WHERE 1=1"
        params = []

        if account_id:
            query += " AND account_id = ?"
            params.append(account_id)
        if unread_only:
            query += " AND is_read = 0"
        if category:
            query += " AND category = ?"
            params.append(category.value)

        query += " ORDER BY received_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.conn.execute(query, params).fetchall()
        return [self._row_to_message(row) for row in rows]

    def search_messages(
        self,
        keyword: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        account_id: Optional[str] = None,
        limit: int = 50
    ) -> list[Message]:
        """Search messages by keyword and/or time range."""
        query = "SELECT * FROM messages WHERE 1=1"
        params = []

        if keyword:
            query += " AND (subject LIKE ? OR sender LIKE ? OR preview LIKE ?)"
            kw = f"%{keyword}%"
            params.extend([kw, kw, kw])
        if start_time:
            query += " AND received_at >= ?"
            params.append(start_time.isoformat())
        if end_time:
            query += " AND received_at <= ?"
            params.append(end_time.isoformat())
        if account_id:
            query += " AND account_id = ?"
            params.append(account_id)

        query += " ORDER BY received_at DESC LIMIT ?"
        params.append(limit)

        rows = self.conn.execute(query, params).fetchall()
        return [self._row_to_message(row) for row in rows]

    def get_message(self, message_id: str) -> Optional[Message]:
        """Get a single message by ID."""
        row = self.conn.execute(
            "SELECT * FROM messages WHERE id = ?", (message_id,)
        ).fetchone()
        return self._row_to_message(row) if row else None

    def find_message(self, message_id: str) -> Optional[Message]:
        """Find a message by flexible ID lookup.

        Tries exact match first, then message_id suffix, then partial match.
        """
        # Try exact match first
        msg = self.get_message(message_id)
        if msg:
            return msg

        # Try matching by message_id suffix (e.g., "mock-001" matches "abc:mock-001")
        row = self.conn.execute(
            "SELECT * FROM messages WHERE message_id = ?", (message_id,)
        ).fetchone()
        if row:
            return self._row_to_message(row)

        # Try partial match on id (ends with)
        row = self.conn.execute(
            "SELECT * FROM messages WHERE id LIKE ?", (f"%:{message_id}%",)
        ).fetchone()
        if row:
            return self._row_to_message(row)

        return None

    def add_message(self, message: Message) -> Message:
        """Add or update a message."""
        self.conn.execute(
            """INSERT OR REPLACE INTO messages
               (id, account_id, message_id, subject, sender, sender_name,
                recipients, received_at, is_read, is_starred, category,
                preview, body_text, body_html, synced_at, provider_data)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                message.id, message.account_id, message.message_id,
                message.subject, message.sender, message.sender_name,
                json.dumps(message.recipients), message.received_at.isoformat(),
                int(message.is_read), int(message.is_starred),
                message.category.value, message.preview,
                message.body_text, message.body_html,
                message.synced_at.isoformat(), json.dumps(message.provider_data)
            )
        )
        self.conn.commit()
        return message

    def mark_read(self, message_id: str, is_read: bool = True) -> bool:
        """Mark a message as read/unread."""
        self.conn.execute(
            "UPDATE messages SET is_read = ? WHERE id = ?",
            (int(is_read), message_id)
        )
        self.conn.commit()
        return True

    def count_unread(self, account_id: Optional[str] = None) -> int:
        """Count unread messages."""
        if account_id:
            row = self.conn.execute(
                "SELECT COUNT(*) FROM messages WHERE account_id = ? AND is_read = 0",
                (account_id,)
            ).fetchone()
        else:
            row = self.conn.execute(
                "SELECT COUNT(*) FROM messages WHERE is_read = 0"
            ).fetchone()
        return row[0] if row else 0

    def _row_to_account(self, row: sqlite3.Row) -> Account:
        return Account(
            id=row["id"],
            email=row["email"],
            provider=EmailProvider(row["provider"]),
            status=AccountStatus(row["status"]),
            display_name=row["display_name"],
            config=json.loads(row["config"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def _row_to_message(self, row: sqlite3.Row) -> Message:
        return Message(
            id=row["id"],
            account_id=row["account_id"],
            message_id=row["message_id"],
            subject=row["subject"],
            sender=row["sender"],
            sender_name=row["sender_name"],
            recipients=json.loads(row["recipients"]),
            received_at=datetime.fromisoformat(row["received_at"]),
            is_read=bool(row["is_read"]),
            is_starred=bool(row["is_starred"]),
            category=EmailCategory(row["category"]),
            preview=row["preview"],
            body_text=row["body_text"],
            body_html=row["body_html"],
            synced_at=datetime.fromisoformat(row["synced_at"]),
            provider_data=json.loads(row["provider_data"]),
        )

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
