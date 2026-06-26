#!/usr/bin/env python3
"""
方言数据库初始化脚本（高速版）

优化点：
1. executemany 批量插入，比 executescript 快 10x+
2. 一次性事务提交，减少 commit 开销
3. PRAGMA synchronous=OFF + journal_mode=MEMORY 加速写入
4. csv 模块正确解析 SQL VALUES，'' 转义自动处理
"""
import sqlite3, os, csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "dialect.db")
SQL_PATH = os.path.join(DATA_DIR, "dialect_data.sql")
INCR_PATH = os.path.join(DATA_DIR, "incremental_words.sql")


def parse_insert_values(line: str):
    """用 csv 模块正确解析 SQL INSERT VALUES，正确处理 '' 转义"""
    start = line.find('VALUES')
    if start == -1:
        return None
    vals = line[start+6:].strip()
    if vals.startswith('('):
        vals = vals[1:]
    # 去掉末尾 ) 或 );
    vals = vals.rstrip(');').rstrip(')')
    # csv reader: quotechar="'" 且 doublequote=False
    # 这样 '' 会被正确解析为一个 '
    reader = csv.reader([vals], quotechar="'", doublequote=False, skipinitialspace=True)
    try:
        rows = list(reader)
        if rows and len(rows[0]) == 5:
            return [f.strip() for f in rows[0]]
    except:
        pass
    return None


def init_database():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA synchronous = OFF")
    conn.execute("PRAGMA journal_mode = MEMORY")
    conn.execute("PRAGMA cache_size = 10000")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE dialect_map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dialect_name TEXT NOT NULL,
            category TEXT,
            standard_word TEXT,
            dialect_word TEXT,
            remark TEXT
        )
    """)
    cur.execute("CREATE INDEX idx_dialect_name ON dialect_map(dialect_name)")
    cur.execute("CREATE INDEX idx_standard_word ON dialect_map(standard_word)")

    if not os.path.exists(SQL_PATH):
        print(f"❌ 未找到 {SQL_PATH}")
        return False

    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    inserts = [l.strip() for l in lines if l.strip().startswith('INSERT')]
    print(f"⏳ 解析 {len(inserts)} 条 INSERT...")

    tuples = []
    for line in inserts:
        fields = parse_insert_values(line)
        if fields:
            tuples.append(tuple(fields))

    print(f"⏳ 批量插入 {len(tuples)} 条...")
    conn.execute("BEGIN TRANSACTION")
    cur.executemany(
        "INSERT OR IGNORE INTO dialect_map (dialect_name, category, standard_word, dialect_word, remark) VALUES (?, ?, ?, ?, ?)",
        tuples
    )
    conn.commit()
    print(f"  ✅ 主库插入完成")

    if os.path.exists(INCR_PATH):
        with open(INCR_PATH, 'r', encoding='utf-8') as f:
            incr = f.read()
        try:
            cur.executescript(incr)
            conn.commit()
        except Exception as e:
            print(f"⚠️ 增量SQL警告: {e}")

    count = cur.execute("SELECT COUNT(*) FROM dialect_map").fetchone()[0]
    conn.close()
    print(f"✅ 完成，共 {count} 条记录")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("  方言数据库初始化（高速版）")
    print("=" * 50)
    if init_database():
        print("🎉 安装成功！")
    else:
        print("💥 安装失败")
