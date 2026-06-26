import sqlite3
import pandas as pd
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "receipts.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    time TEXT,
                    store TEXT,
                    amount REAL,
                    category TEXT
                 )''')
    try:
        c.execute("ALTER TABLE receipts ADD COLUMN time TEXT")
    except sqlite3.OperationalError:
        pass
    c.execute('''CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT
                 )''')
    # Default budget if not set
    c.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('budget', '0.0')")
    conn.commit()
    conn.close()

def add_receipt(date, time, store, amount, category):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO receipts (date, time, store, amount, category) VALUES (?, ?, ?, ?, ?)",
              (date, time, store, amount, category))
    conn.commit()
    conn.close()

def get_receipts():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT id, date, COALESCE(time, '') as time, store, amount, category FROM receipts ORDER BY id DESC", conn)
    conn.close()
    return df

def get_budget():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM config WHERE key='budget'")
    row = c.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0

def set_budget(amount):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('budget', ?)", (str(amount),))
    conn.commit()
    conn.close()

def get_total_spent():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM receipts")
    row = c.fetchone()
    conn.close()
    return float(row[0] or 0.0)

def export_to_csv(filename):
    df = get_receipts()
    df.to_csv(filename, index=False)

def export_to_excel(filename):
    df = get_receipts()
    df.to_excel(filename, index=False)
