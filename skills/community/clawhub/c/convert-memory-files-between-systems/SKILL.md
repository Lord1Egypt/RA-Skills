---
name: "convert-memory-files-between-systems"
description: "如何将 memory-lancedb-pro 的记忆文件转换为原版 markdown 格式，并导入到 memos-local-openclaw-plugin 系统中。TRIGGER 当用户提到记忆文件转换、markdown 文件导入、配置文件修改、数据库导入、记忆插件更换、或任何涉及将记忆数据从一个系统迁移到另一个系统的需求时。"
---

# 将 memory-lancedb-pro 记忆文件转换并导入到 memos-local-openclaw-plugin

本技能帮助你将 memory-lancedb-pro 的记忆文件转换为原版 markdown 格式，并导入到 memos-local-openclaw-plugin 系统中，确保数据迁移的顺利进行。

## 当使用此技能
- 当你需要将 memory-lancedb-pro 的记忆文件转换为原版 markdown 格式
- 当你需要从 memory-lancedb-pro 切换到 memos-local-openclaw-plugin 记忆系统
- 当你需要解决配置文件被自动还原的问题
- 当你需要确保记忆数据在新系统中的正确性和完整性

## 步骤
1. **确认 memory-lancedb-pro 的数据存储位置和格式**
   - 数据存储在 SQLite 数据库和 lancedb-pro 目录
   - 原版记忆文件是 markdown 格式，存储在 `memory-md` 目录
   - memory-lancedb-pro 已有 mdMirror 功能，可以创建 markdown 文件
   - **为什么这很重要**：了解数据存储位置和格式是进行数据迁移的前提。

2. **检查 JSONL 备份文件的结构**
   - JSONL 文件结构如下：
     ```json
     {
       "text": "记忆内容",
       "timestamp": "时间戳",
       "category": "类别（decision, fact 等）",
       "metadata": {
         "l0_abstract": "摘要",
         "l1_overview": "概述",
         "l2_content": "详细内容"
       }
     }
     ```
   - **为什么这很重要**：了解 JSONL 文件的结构有助于正确转换数据。

3. **将记忆从 JSONL 备份文件转换为 markdown 文件**
   - 使用 Python 脚本将 657 条记忆转换为 21 个 markdown 文件
   - **为什么这很重要**：确保记忆数据以正确的格式保存，便于后续导入。

4. **删除配置文件中关于 memory-lancedb-pro 的所有内容**
   - 使用 Python 脚本精确删除相关配置
   - **为什么这很重要**：避免手动编辑配置文件时出现的格式问题，确保配置文件的有效性和持久化。

5. **确认当前记忆系统**
   - 确认 `slots.memory: memos-local-openclaw-plugin`
   - 21 个 markdown 记忆文件在 `~/.openclaw/memory/` 目录
   - **为什么这很重要**：确保新系统已经正确配置并准备就绪。

6. **将转换好的 markdown 记忆文件导入到 memos-local-openclaw-plugin 系统中**
   - 检查 memos-local-openclaw-plugin 的数据库位置：`/home/hahaha1234/.openclaw/memos-local/memos.db`
   - 检查数据库结构，确认 `chunks` 表的字段
   - 编写 Python 脚本将 markdown 记忆文件导入到 `chunks` 表中
   - **为什么这很重要**：确保记忆数据正确导入到新系统中，避免数据丢失或格式错误。

7. **验证导入结果**
   - 数据库总记录从 212 条增加到 869 条
   - **为什么这很重要**：验证数据迁移的完整性，确保所有记忆都已成功导入。

## 坑和解决方案
❌ 使用 sed 和 grep 删除配置文件中的相关行 → 由于 sed 的转义问题和 grep 的逐行删除导致 JSON 无效 → ✅ 使用 Python 脚本精确删除相关配置，避免格式问题

## 关键代码和配置
### Python 脚本：删除配置文件中的 memory-lancedb-pro 相关内容
```python
import json

# 读取配置文件
with open('/path/to/config.json', 'r') as file:
    config = json.load(file)

# 删除 memory-lancedb-pro 相关配置
if 'memory-lancedb-pro' in config['plugins']['entries']:
    del config['plugins']['entries']['memory-lancedb-pro']

if 'memory-lancedb-pro' in config['plugins']['load']['paths']:
    config['plugins']['load']['paths'].remove('memory-lancedb-pro')

if 'memory-lancedb-pro' in config['plugins']['allow']:
    config['plugins']['allow'].remove('memory-lancedb-pro')

# 保存配置文件
with open('/path/to/config.json', 'w') as file:
    json.dump(config, file, indent=2)
```

### Python 脚本：将 markdown 记忆文件导入到 memos 数据库
```python
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
```

## 环境和前提条件
- **memory-lancedb-pro 版本号**：5.1.1
- **JSONL 备份文件中的记忆条目包含字段**：`text`、`timestamp`、`category` 和 `metadata`
- **memos-local-openclaw-plugin 的数据库文件路径**：`/home/hahaha1234/.openclaw/memos-local/memos.db`
- **`chunks` 表的字段**：`session_key`、`turn_id`、`content` 等
- **Python 脚本将 markdown 文件中的记忆条目逐条导入到 `chunks` 表中**，确保数据格式正确

## 伴随文件
- `scripts/delete_memory_lancedb_pro_config.py` — 删除配置文件中 memory-lancedb-pro 相关内容的 Python 脚本
- `scripts/import_markdown_to_memos.py` — 将 markdown 记忆文件导入到 memos 数据库的 Python 脚本

<!-- metadata: {{"openclaw": {{"emoji": "🦊"}}}} -->

## Companion files

- `scripts/remove_memory_lancedb_pro.py` — automation script
- `scripts/import_markdown_to_memos.py` — automation script