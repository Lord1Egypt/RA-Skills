# Database Ops - 数据库操作工具箱

<p align="center">
  <img src="https://img.shields.io/pypi/v/database-ops-toolkit?style=flat-square" alt="PyPI">
  <img src="https://img.shields.io/pypi/l/database-ops-toolkit?style=flat-square" alt="License">
</p>

## 📖 简介

**Database Ops** 是强大的 SQLite/MySQL 数据库操作工具,让数据库操作变得简单高效。

### 🎯 适用场景

- 📊 数据存储和查询
- 🔧 快速原型开发
- 💾 数据备份和迁移
- 📈 统计分析
- 🔄 数据同步

## 🚀 功能特性

| 功能 | 说明 |
|------|------|
| 🗄️ **多数据库支持** | SQLite / MySQL |
| 📝 **完整SQL支持** | 查询/插入/更新/删除 |
| 🔄 **事务支持** | 提交/回滚 |
| 💾 **备份恢复** | 数据库备份 |
| 📤 **数据导入导出** | JSON/CSV |
| ⚡ **批量操作** | 批量插入 |
| 🔍 **智能查询** | 参数化查询防注入 |

## 📦 安装

```bash
# 基础 (SQLite)
pip install pandas

# 完整 (SQLite + MySQL)
pip install pandas pymysql
```

## 🎬 快速开始

### SQLite 使用

```python
from database_ops import DatabaseOps

# 连接数据库 (自动创建)
db = DatabaseOps('myapp.db')

# 创建表
db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        created_at TEXT
    )
''')

# 插入数据
db.insert('users', {
    'name': '张三',
    'email': 'zhangsan@example.com',
    'created_at': '2026-01-01'
})

# 查询
users = db.execute('SELECT * FROM users LIMIT 10')
for user in users:
    print(user)

db.close()
```

### MySQL 使用

```python
from database_ops import MySQLConnection

# 连接MySQL
db = MySQLConnection(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='myapp'
)

# 使用同上...
db.close()
```

## 📚 详细示例

### 条件查询

```python
# 参数化查询 (防SQL注入)
results = db.execute(
    'SELECT * FROM users WHERE age > ? AND city = ?',
    (25, '北京')
)

# 获取单条
user = db.fetch_one(
    'SELECT * FROM users WHERE id = ?',
    (1,)
)

# 获取单个值
count = db.fetch_value('SELECT COUNT(*) FROM users')
```

### 批量插入

```python
# 批量插入大量数据
users = [
    {'name': '用户1', 'email': 'u1@test.com'},
    {'name': '用户2', 'email': 'u2@test.com'},
    {'name': '用户3', 'email': 'u3@test.com'},
    # ... 更多数据
]

db.insert_many('users', users)
print(f"插入 {len(users)} 条记录")
```

### 事务处理

```python
try:
    db.begin()  # 开始事务
    
    db.insert('orders', {'user_id': 1, 'amount': 100})
    db.insert('orders', {'user_id': 1, 'amount': 200})
    # 如果这里出错
    
    db.commit()  # 提交
    print("订单创建成功!")
except:
    db.rollback()  # 回滚
    print("订单创建失败,已回滚")
```

### 数据统计

```python
# 统计表行数
count = db.count('users')
print(f"用户总数: {count}")

# 表统计信息
stats = db.stats('orders')
print(stats)
# {'table': 'orders', 'columns': 5, 'rows': 1000, 'structure': [...]}
```

### 备份和恢复

```python
# 备份数据库
backup_path = db.backup('backup_20260101.db')
print(f"备份完成: {backup_path}")

# 备份到JSON
from database_ops import export_to_json

export_to_json('myapp.db', 'users', 'users.json')
```

### 从JSON导入

```python
from database_ops import import_from_json

# 导入JSON数据到表
count = import_from_json('myapp.db', 'users', 'new_users.json')
print(f"导入了 {count} 条记录")
```

## 📋 API 参考

### 连接

```python
db = DatabaseOps('file.db')  # SQLite
db = MySQLConnection(host, port, user, password, database)  # MySQL
db.connect()   # 连接
db.close()     # 关闭
```

### 查询

```python
results = db.execute(sql, params)    # 执行SQL
results = db.query(sql, params)      # 查询别名
row = db.fetch_one(sql, params)      # 单条
value = db.fetch_value(sql, params)  # 单个值
```

### 写入

```python
id = db.insert(table, data)          # 插入单条
count = db.insert_many(table, rows)  # 批量插入
count = db.update(table, data, where, params)  # 更新
count = db.delete(table, where, params)        # 删除
```

### 表结构

```python
tables = db.get_tables()           # 所有表
columns = db.get_columns('users')  # 列名
info = db.get_table_info('users')  # 表结构
```

### 事务

```python
db.begin()      # 开始
db.commit()     # 提交
db.rollback()   # 回滚
```

## 🔧 快速函数

```python
# 无需创建对象
from database_ops import sqlite_query, sqlite_execute, sqlite_backup

# 查询
results = sqlite_query('app.db', 'SELECT * FROM users LIMIT 10')

# 执行
sqlite_execute('app.db', 'DELETE FROM users WHERE old = 1')

# 备份
backup_path = sqlite_backup('app.db', 'backup.db')
```

## ⚠️ 注意事项

1. **写操作前备份** - 重要数据先备份
2. **使用参数化查询** - 防止SQL注入
3. **大数据事务** - 批量操作使用事务保证一致性
4. **连接管理** - 操作完后及时关闭

## 📄 许可证

MIT License