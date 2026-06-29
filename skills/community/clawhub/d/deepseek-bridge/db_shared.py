#!/usr/bin/env python3
"""
Shared SQLite database for OpenClaw ↔ DeepSeek bridge.
Both bridge.py (8080) and deepseek_ui.py (8081) import this module.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat_shared.db")


def get_conn():
    return sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_question(question):
    """Save a new question, return record id."""
    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO conversations (question, status) VALUES (?, ?)",
        (question, "pending")
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def update_answer(record_id, answer, status="completed"):
    """Update answer for a record."""
    conn = get_conn()
    conn.execute(
        "UPDATE conversations SET answer = ?, status = ?, updated_at = ? WHERE id = ?",
        (answer, status, datetime.now(), record_id)
    )
    conn.commit()
    conn.close()


def get_all_conversations(limit=100):
    """Get all conversations, most recent last."""
    conn = get_conn()
    cursor = conn.execute(
        "SELECT id, question, answer, status, created_at FROM conversations ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    results = [
        {
            "id": row[0],
            "question": row[1],
            "answer": row[2] or "",
            "status": row[3],
            "created_at": row[4],
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return list(reversed(results))  # oldest first for display


def get_pending():
    """Get all pending questions (status='pending')."""
    conn = get_conn()
    cursor = conn.execute(
        "SELECT id, question FROM conversations WHERE status = ? ORDER BY id",
        ("pending",)
    )
    results = [{"id": row[0], "question": row[1]} for row in cursor.fetchall()]
    conn.close()
    return results


# Initialize DB on module load
init_db()