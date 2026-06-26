"""Local SQLite database for EchoMark ratings."""
import sqlite3
from config import LOCAL_DB_FILE, CONFIG_DIR
import os


def _get_connection():
    """Get a connection to the local database, initializing if needed."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    conn = sqlite3.connect(LOCAL_DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the local database and create tables if they don't exist."""
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            accuracy INTEGER NOT NULL,
            efficiency INTEGER NOT NULL,
            usability INTEGER NOT NULL,
            stability INTEGER NOT NULL,
            overall REAL NOT NULL,
            comment TEXT DEFAULT '',
            timestamp TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_ratings_tool ON ratings(tool_name)
    """)
    conn.commit()
    conn.close()


def save_rating(tool_name, accuracy, efficiency, usability, stability, overall, comment=""):
    """Save a rating to the local database."""
    init_db()
    conn = _get_connection()
    conn.execute(
        """INSERT INTO ratings (tool_name, accuracy, efficiency, usability, stability, overall, comment)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (tool_name, accuracy, efficiency, usability, stability, overall, comment),
    )
    conn.commit()
    conn.close()


def query_ratings(tool_name):
    """Return aggregated stats for a tool from local data.

    Returns dict with keys: tool_name, total_ratings, avg_accuracy, avg_efficiency,
    avg_usability, avg_stability, avg_overall, last_updated.
    Returns None if no ratings found.
    """
    init_db()
    conn = _get_connection()
    row = conn.execute(
        """SELECT
               tool_name,
               COUNT(*) as total_ratings,
               ROUND(AVG(accuracy), 1) as avg_accuracy,
               ROUND(AVG(efficiency), 1) as avg_efficiency,
               ROUND(AVG(usability), 1) as avg_usability,
               ROUND(AVG(stability), 1) as avg_stability,
               ROUND(AVG(overall), 1) as avg_overall,
               MAX(timestamp) as last_updated
           FROM ratings
           WHERE tool_name = ?""",
        (tool_name,),
    ).fetchone()
    conn.close()

    if row is None or row["total_ratings"] == 0:
        return None

    return dict(row)


def list_tools():
    """List all tools that have been rated locally.

    Returns list of dicts with keys: tool_name, total_ratings, avg_overall, last_rated.
    """
    init_db()
    conn = _get_connection()
    rows = conn.execute(
        """SELECT
               tool_name,
               COUNT(*) as total_ratings,
               ROUND(AVG(overall), 1) as avg_overall,
               MAX(timestamp) as last_rated
           FROM ratings
           GROUP BY tool_name
           ORDER BY last_rated DESC"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_rating_history(tool_name):
    """Return individual rating records for a tool from local data.

    Returns list of dicts with all rating fields.
    """
    init_db()
    conn = _get_connection()
    rows = conn.execute(
        """SELECT * FROM ratings
           WHERE tool_name = ?
           ORDER BY id DESC""",
        (tool_name,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
