"""SQLite cache layer with TTL support. No external network access."""
import json
import sqlite3
from datetime import datetime, timedelta


class Cache:
    """SQLite-based cache with TTL. Thread-safe via WAL mode."""

    def __init__(self, db_path="cache.db"):
        self.db_path = db_path
        self._mem_conn = None  # Shared connection for :memory: databases
        self._init_db()

    def _init_db(self):
        """Initialize tables. For :memory:, keep connection open."""
        if self.db_path == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:", check_same_thread=False)
            conn = self._mem_conn
        else:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")

        conn.executescript("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                data TEXT,
                expires_at REAL
            );
            CREATE TABLE IF NOT EXISTS fundamentals (
                ticker TEXT PRIMARY KEY,
                data TEXT
            );
            CREATE TABLE IF NOT EXISTS price_history (
                ticker TEXT,
                date TEXT,
                open REAL, high REAL, low REAL, close REAL, volume INTEGER,
                PRIMARY KEY (ticker, date)
            );
            CREATE INDEX IF NOT EXISTS idx_price ON price_history(ticker);
        """)
        conn.commit()

        if self.db_path != ":memory:":
            conn.close()

    def _connect(self):
        """Get connection — shared for :memory:, fresh for file-based."""
        if self.db_path == ":memory:":
            return self._mem_conn
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _maybe_close(self, conn):
        """Close connection only for file-based DBs."""
        if self.db_path != ":memory:":
            conn.close()

    def get(self, key):
        """Return dict or None (checks TTL)."""
        try:
            conn = self._connect()
            try:
                cur = conn.execute(
                    "SELECT data, expires_at FROM cache WHERE key = ?", (key,)
                )
                row = cur.fetchone()
                if not row:
                    return None
                data_json, expires = row
                if expires and datetime.now().timestamp() > expires:
                    conn.execute("DELETE FROM cache WHERE key = ?", (key,))
                    conn.commit()
                    return None
                return json.loads(data_json)
            finally:
                self._maybe_close(conn)
        except Exception:
            return None

    def set(self, key, data, ttl_seconds=3600):
        """Store with TTL."""
        try:
            conn = self._connect()
            try:
                expires = (datetime.now() + timedelta(seconds=ttl_seconds)).timestamp()
                conn.execute(
                    "INSERT OR REPLACE INTO cache (key, data, expires_at) VALUES (?, ?, ?)",
                    (key, json.dumps(data, default=str), expires),
                )
                conn.commit()
            finally:
                self._maybe_close(conn)
        except Exception:
            pass

    def get_fundamentals(self, ticker):
        try:
            conn = self._connect()
            try:
                cur = conn.execute("SELECT data FROM fundamentals WHERE ticker = ?", (ticker,))
                row = cur.fetchone()
                return json.loads(row[0]) if row else None
            finally:
                self._maybe_close(conn)
        except Exception:
            return None

    def set_fundamentals(self, ticker, data):
        try:
            conn = self._connect()
            try:
                conn.execute(
                    "INSERT OR REPLACE INTO fundamentals (ticker, data) VALUES (?, ?)",
                    (ticker, json.dumps(data, default=str)),
                )
                conn.commit()
            finally:
                self._maybe_close(conn)
        except Exception:
            pass

    def get_price_history(self, ticker):
        try:
            conn = self._connect()
            try:
                conn.row_factory = sqlite3.Row
                cur = conn.execute(
                    "SELECT date, open, high, low, close, volume FROM price_history WHERE ticker = ? ORDER BY date DESC LIMIT 100",
                    (ticker,),
                )
                rows = cur.fetchall()
                return [dict(r) for r in rows] if rows else None
            finally:
                self._maybe_close(conn)
        except Exception:
            return None

    def set_price_history(self, ticker, rows_list):
        try:
            conn = self._connect()
            try:
                for r in rows_list:
                    conn.execute(
                        """INSERT OR REPLACE INTO price_history
                           (ticker, date, open, high, low, close, volume)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (ticker, r["date"], r["open"], r["high"], r["low"], r["close"], r["volume"]),
                    )
                conn.commit()
            finally:
                self._maybe_close(conn)
        except Exception:
            pass

    def clear_expired(self):
        try:
            conn = self._connect()
            try:
                conn.execute("DELETE FROM cache WHERE expires_at < ?", (datetime.now().timestamp(),))
                conn.commit()
            finally:
                self._maybe_close(conn)
        except Exception:
            pass
