"""
迁移 phonebook.db：添加 address 字段
"""

import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".openclaw" / "skills" / "clawphone" / "phonebook.db"

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 检查是否已有 address 列
    cur.execute("PRAGMA table_info(phones)")
    columns = [row[1] for row in cur.fetchall()]

    if "address" not in columns:
        print("迁移：添加 address 列到 phones 表...")
        cur.execute("ALTER TABLE phones ADD COLUMN address TEXT")
        conn.commit()
        print("[OK] 迁移完成")
    else:
        print("[OK] address 列已存在，无需迁移")

    conn.close()

if __name__ == "__main__":
    migrate()
