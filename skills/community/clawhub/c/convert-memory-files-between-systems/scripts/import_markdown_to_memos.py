import sqlite3
import os
import re

# 连接数据库
conn = sqlite3.connect('/home/hahaha1234/.openclaw/memos-local/memos.db')
cursor = conn.cursor()

# 创建 chunks 表（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY,
    session_key TEXT,
    turn_id INTEGER,
    content TEXT,
    timestamp TEXT,
    category TEXT,
    importance REAL,
    scope TEXT
)
''')

# 读取 markdown 文件
memory_dir = '/home/hahaha1234/.openclaw/memory/'
for filename in os.listdir(memory_dir):
    if filename.endswith('.md'):
        with open(os.path.join(memory_dir, filename), 'r') as file:
            content = file.read()

        # 解析 markdown 文件
        date = re.search(r'# (\d{4}-\d{2}-\d{2}) 记忆', content).group(1)
        memories = re.findall(r'## \[(\d{2}:\d{2}:\d{2})\] (DECISION|FACT) - 重要性:(\d+\.\d+)\n\n**范围**: (.+?)\n\n(.+?)\n\n---', content, re.DOTALL)

        # 插入数据到数据库
        for memory in memories:
            timestamp, category, importance, scope, content = memory
            cursor.execute('''
            INSERT INTO chunks (session_key, turn_id, content, timestamp, category, importance, scope)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (date, 0, content, timestamp, category, float(importance), scope))

# 提交并关闭连接
conn.commit()
conn.close()