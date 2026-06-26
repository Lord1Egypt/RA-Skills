# Database Toolkit
## 数据库操作工具箱 | 简化的数据库处理解决方案

<p align="center">
  <img src="https://img.shields.io/pypi/v/database-toolkit" alt="PyPI">
  <img src="https://img.shields.io/github/stars/XiLi/database-toolkit" alt="Stars">
  <img src="https://img.shields.io/github/license/XiLi/database-toolkit" alt="License">
</p>

---

## 项目简介

Database Toolkit (数据库工具箱) 是一套强大的SQLite和MySQL数据库操作工具，让数据库操作变得简单高效。无论你是开发者还是数据分析师，这个工具都能帮助你轻松完成数据库任务。

> **让数据库操作变得更简单!**

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 🗄️ 多数据库支持 | SQLite (本地) / MySQL (远程) |
| 📝 完整SQL支持 | 查询/插入/更新/删除 |
| 🔄 事务支持 | 开始/提交/回滚 |
| 💾 备份恢复 | 数据库备份 |
| 📤 数据导入导出 | JSON格式 |
| ⚡ 批量操作 | 批量插入 |
| 🔍 智能查询 | 参数化查询防注入 |

---

## 快速开始

### 安装

```bash
pip install pandas
# MySQL支持: pip install pymysql
```

### SQLite使用

```python
from database_ops import DatabaseOps

db = DatabaseOps('myapp.db')

# 创建表
db.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

# 插入数据
db.insert('users', {'name': '张三', 'email': 'test@example.com'})

# 查询
users = db.execute('SELECT * FROM users LIMIT 10')

db.close()
```

### MySQL使用

```python
from database_ops import MySQLConnection

db = MySQLConnection(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='myapp'
)

# 使用方法相同
db.insert('users', {'name': '测试'})
users = db.execute('SELECT * FROM users')

db.close()
```

---

## 详细功能

### 查询

```python
# 普通查询
results = db.execute('SELECT * FROM users')

# 参数化查询 (防SQL注入)
results = db.execute(
    'SELECT * FROM users WHERE age > ? AND city = ?',
    (25, '北京')
)

# 获取单条
user = db.fetch_one('SELECT * FROM users WHERE id = ?', (1,))

# 获取单个值
count = db.fetch_value('SELECT COUNT(*) FROM users')
```

### 插入/更新/删除

```python
# 插入单条
db.insert('users', {'name': '张三', 'age': 28})

# 批量插入
users = [
    {'name': '李四', 'age': 25},
    {'name': '王五', 'age': 30}
]
db.insert_many('users', users)

# 更新
db.update('users', {'age': 29}, 'name = ?', ('张三',))

# 删除
db.delete('users', 'id = ?', (1,))
```

### 事务处理

```python
try:
    db.begin()
    db.insert('orders', {'user_id': 1, 'amount': 100})
    db.insert('orders', {'user_id': 1, 'amount': 200})
    db.commit()
except:
    db.rollback()
```

### 统计

```python
# 统计行数
count = db.count('users')

# 表统计
stats = db.stats('users')
# {'table': 'users', 'columns': 5, 'rows': 1000}
```

### 备份

```python
# 备份数据库
backup_path = db.backup('backup_20260101.db')

# 导出到JSON
from database_ops import export_to_json
export_to_json('myapp.db', 'users', 'users.json')

# 从JSON导入
from database_ops import import_from_json
import_from_json('myapp.db', 'users', 'new_users.json')
```

---

## API参考

| 方法 | 功能 |
|------|------|
| execute() | 执行SQL |
| insert() | 插入单条 |
| insert_many() | 批量插入 |
| update() | 更新数据 |
| delete() | 删除数据 |
| fetch_one() | 获取单条 |
| fetch_value() | 获取单个值 |
| count() | 统计行数 |
| stats() | 表统计 |
| backup() | 备份数据库 |

---

## 依赖

- pandas
- pymysql (可选,用于MySQL)

---

## 许可证

MIT License

---

## 🔧 OpenClaw / Claude Code 使用

本技能已集成到 OpenClaw 技能系统,可直接使用:

`python
# 在 OpenClaw 或 Claude Code 中使用
from ai_workflow import run_workflow
from chart_generator import ChartGenerator
from data_parser import DataParser
from database_ops import DatabaseOps
from excel_parser import ExcelParser
from feishu_sheets import FeishuSheets
`

或通过 skills 目录调用:

`python
import sys
sys.path.insert(0, 'path/to/skills')
`

