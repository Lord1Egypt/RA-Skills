# 表结构查询指南

## 查看表结构的方法

### 1. 使用 skill 命令

```bash
# 查看表结构
python3 archery_query.py --desc your_table_name

# 列出数据库中的所有表
python3 archery_query.py --list-tables your_database_name
```

### 2. 使用 SQL 命令

```bash
# MySQL/TiDB
python3 archery_query.py "SHOW COLUMNS FROM your_table_name"

# 查看表创建语句
python3 archery_query.py "SHOW CREATE TABLE your_table_name"

# StarRocks
python3 archery_query.py "DESC your_table_name"
```

## 常见字段类型

| 类型 | 说明 | 示例 |
|------|------|------|
| INT/BIGINT | 整数类型 | id, count |
| VARCHAR/TEXT | 字符串类型 | name, description |
| DECIMAL | 小数类型 | amount, price |
| DATETIME/TIMESTAMP | 时间类型 | create_time, update_time |
| JSON | JSON 类型 | metadata, config |
| BOOLEAN | 布尔类型 | is_active, status |

## 查询优化建议

### 索引字段查询更快

```bash
# 查看索引
python3 archery_query.py "SHOW INDEX FROM your_table_name"

# 使用索引字段查询（更快）
python3 archery_query.py "SELECT * FROM your_table_name WHERE indexed_field = 'value' LIMIT 10"
```

### 限制返回行数

```bash
# 使用 LIMIT 限制结果
python3 archery_query.py "SELECT * FROM your_table_name LIMIT 100"

# 使用 --limit 参数
python3 archery_query.py --limit 50 "SELECT * FROM your_table_name"
```

### 只查询需要的字段

```bash
# 避免 SELECT *（查询所有字段）
python3 archery_query.py "SELECT field1, field2 FROM your_table_name LIMIT 10"
```

## 复杂查询示例

```bash
# 聚合查询
python3 archery_query.py "SELECT COUNT(*) FROM your_table_name WHERE status = 'active'"

# 排序查询
python3 archery_query.py "SELECT * FROM your_table_name ORDER BY create_time DESC LIMIT 20"

# 分组查询
python3 archery_query.py "SELECT status, COUNT(*) FROM your_table_name GROUP BY status"

# 连接查询
python3 archery_query.py "SELECT t1.field1, t2.field2 FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id LIMIT 10"
```

## 导出查询结果

```bash
# JSON 格式输出
python3 archery_query.py --format json "SELECT * FROM your_table_name LIMIT 10"
```

## 注意事项

1. 大表查询务必使用 LIMIT
2. 有索引的字段查询更快
3. 避免在生产环境执行复杂查询

## 使用 table_finder 工具

### 快速搜索表

```bash
# 模糊搜索表名
python3 scripts/table_finder.py --search "record"

# 输出示例:
# 找到 15 个匹配的表:
#   1. payment_record           [100%]
#   2. order_record             [100%]
#   3. shipment_record          [100%]
#   4. record_history           [85%]
```

### 查看表结构

```bash
# 查看表结构
python3 scripts/table_finder.py --desc payment_record

# 输出示例:
# 字段总数: 20
# 字段名                              类型                允许空    键
# --------------------------------------------------------------------------------
# id                                  bigint(20)         NO       PRI
# order_id                            varchar(50)        NO       MUL
# status                              varchar(10)        YES
```

### 搜索字段名

```bash
# 在所有表中搜索字段名
python3 scripts/table_finder.py --field "status"

# 输出示例:
# 找到 50 个匹配的字段:
# 表名                                    字段名              类型
# --------------------------------------------------------------------------------
# payment_record                        status              varchar(10)
# order_record                          status              varchar(20)
# shipment_record                       status              int(11)
```

### 列出所有表

```bash
# 列出数据库中的所有表（按前缀分组）
python3 scripts/table_finder.py --list

# 输出示例:
# 【payment】(10 个)
#   - payment_record
#   - payment_history
#   ...
# 【order】(15 个)
#   - order_record
#   - order_item
#   ...
```

### 缓存管理

```bash
# 刷新缓存（重新查询数据库）
python3 scripts/table_finder.py --refresh

# 缓存位置: ~/.archery/cache/table_cache.json
```

