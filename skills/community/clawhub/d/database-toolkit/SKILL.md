# Database Ops - 数据库操作

> SQLite/MySQL数据库直接操作，支持查询/更新/备份
> 最后更新：2026-04-13

---

## 功能概述

- 📊 **查询数据**：SQL查询执行
- 🔧 **数据维护**：增删改数据
- 💾 **备份恢复**：数据库备份
- 📈 **统计分析**：数据统计分析

---

## 支持的数据库

### SQLite（本地）
```
路径：
- data/stock_profiles.db
- data/commodity_options.db
- data/financial_data.db
- lottery_v3.db
```

### MySQL（远程）
```
待配置：
- Host: localhost
- Port: 3306
```

---

## 核心命令

### 1. 查询
```
命令：db查询 [SQL]

示例：
- db查询 SELECT * FROM stocks LIMIT 10
- db查询 SELECT code, name FROM stocks WHERE price > 100
```

### 2. 统计
```
命令：db统计 [表名]

示例：
- db统计 stock_profiles
- db统计 odds_history
```

### 3. 备份
```
命令：db备份 [数据库]

示例：
- db备份 stock_profiles
- db备份 all
```

### 4. 表结构
```
命令：db结构 [表名]

示例：
- db结构 stocks
- db结构 odds_history
```

---

## 常用查询模板

### 股票数据
```sql
-- 最近采集的股票
SELECT code, name, price, change_pct 
FROM stocks 
ORDER BY update_time DESC LIMIT 10

-- 涨跌幅排行
SELECT code, name, change_pct 
FROM stocks 
ORDER BY change_pct DESC LIMIT 10
```

### 竞彩数据
```sql
-- 最近的推荐
SELECT league, home_team, away_team, prediction, odds 
FROM odds_history 
ORDER BY created_at DESC LIMIT 10

-- 命中率统计
SELECT league, COUNT(*) as total, 
       SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins
FROM odds_history GROUP BY league
```

---

## 注意事项

- 写操作需谨慎，建议先备份
- 敏感数据查询需脱敏
- 定期备份重要数据
- 大数据量查询注意性能


## Code Implementation

Python实现: database_ops.py

`python
from database_ops import DatabaseOps, sqlite_query

# 创建连接
db = DatabaseOps('data.db')

# 查询
results = db.execute('SELECT * FROM stocks LIMIT 10')

# 插入
db.insert('stocks', {'code': '000001', 'name': 'Test', 'price': 10.0})

# 批量插入
db.insert_many('stocks', [{'code': '1', 'price': 10}, {'code': '2', 'price': 20}])

# 统计
count = db.count('stocks')
stats = db.stats('stocks')

# 备份
backup_path = db.backup('backup.db')

db.close()

# 快速查询
results = sqlite_query('data.db', 'SELECT * FROM stocks')
`
