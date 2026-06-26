"""Debug QMD FTS search"""
import sqlite3

conn = sqlite3.connect("C:/Users/Administrator/.cache/qmd/index.sqlite")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check FTS table structure
cursor.execute("PRAGMA table_info(documents_fts)")
print("FTS columns:", cursor.fetchall())

# Try a simple FTS query
print("\nTrying FTS query:")
try:
    cursor.execute("SELECT * FROM documents_fts LIMIT 2")
    rows = cursor.fetchall()
    print(f"FTS rows: {len(rows)}")
    for r in rows:
        print(f"  {dict(r)}")
except Exception as e:
    print(f"FTS error: {e}")

# Try LIKE query
print("\nTrying LIKE query:")
cursor.execute("""
    SELECT d.path, d.title, c.doc
    FROM documents d
    LEFT JOIN content c ON d.hash = c.hash
    WHERE d.title LIKE '%python%' OR c.doc LIKE '%python%'
    LIMIT 3
""")
rows = cursor.fetchall()
print(f"LIKE rows: {len(rows)}")
for r in rows:
    print(f"  path: {r['path']}, title: {r['title']}")

conn.close()
