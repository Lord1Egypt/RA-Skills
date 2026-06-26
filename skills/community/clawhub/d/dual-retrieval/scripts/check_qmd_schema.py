"""Check QMD database schema"""
import sqlite3

conn = sqlite3.connect('C:/Users/Administrator/.cache/qmd/index.sqlite')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', tables)

for t in tables:
    name = t[0]
    cursor.execute(f'PRAGMA table_info({name})')
    cols = cursor.fetchall()
    print(f'\n{name}:')
    for c in cols:
        print(f'  {c}')
    
    # Sample data
    cursor.execute(f'SELECT * FROM {name} LIMIT 2')
    rows = cursor.fetchall()
    print(f'  Sample rows: {len(rows)}')
    for r in rows[:2]:
        print(f'    {str(r)[:200]}')

conn.close()
