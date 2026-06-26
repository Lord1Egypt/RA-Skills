---
name: clickhouse-database
description: "ClickHouse 数据库操作技能。通过 clickhouse-client CLI 连接数据库，执行 SELECT 查询、INSERT/UPDATE/DELETE 增删改、批量 SQL 执行、数据库/表管理、JSON 格式输出。适用场景：大数据查询、统计分析、数据导入导出、数据库巡检、表结构查看、远程连接、生产环境调试。触发关键词：ClickHouse、大数据查询、SQL 语句执行、连接ClickHouse、查表、数据增删改、clickhouse jdbc、查看表结构、表字段分析、查看索引、EXPLAIN 查询分析。"
license: "Copyright © 2026 少煊（年少有为，名声煊赫）<429668385@qq.com>. All rights reserved."
---

# ClickHouse Database Skill

Use the `clickhouse-client` CLI to connect to and interact with ClickHouse databases. Use the `-q` flag to execute SQL statements and combine with `--format` options to produce clean output suitable for processing. Pipe the result to `jq` for reliable JSON formatting.

## 快速使用场景

### 场景 1: 查询数据（最常用）

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SELECT * FROM users LIMIT 10;" --format=JSONEachRow | jq -s '.'
```

### 场景 2: 查看表结构

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "DESCRIBE TABLE users;" --format=TSV 2>/dev/null
```

### 场景 3: 插入/更新/删除数据

```bash
# 插入
clickhouse-client -h <host> -u <user> -d <db> -q "INSERT INTO users (name, email) VALUES ('Test', 'test@example.com');" 2>/dev/null

# 更新（需表引擎支持，如 MergeTree 家族）
clickhouse-client -h <host> -u <user> -d <db> -q "ALTER TABLE users UPDATE status=1 WHERE id=1;" 2>/dev/null

# 删除
clickhouse-client -h <host> -u <user> -d <db> -q "ALTER TABLE users DELETE WHERE id=1;" 2>/dev/null
```

### 场景 4: 统计数据报表

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SELECT COUNT(*) as total, SUM(amount) as revenue FROM orders WHERE toDate(create_time)=today();" --format=JSONEachRow | jq -s '.'
```

### 场景 5: 导出数据到文件

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SELECT * FROM users FORMAT CSV" > /tmp/users.csv 2>/dev/null
```

### 场景 6: 执行 SQL 脚本文件

```bash
clickhouse-client -h <host> -u <user> -d <db> --multiquery < script.sql 2>/dev/null
```

## 数据库连接

### 基础连接

```bash
clickhouse-client -h <hostname> --port <port> -u <username> -d <database-name>
```

**示例 (连接本地数据库):**
```bash
CLICKHOUSE_PASSWORD=yourpassword clickhouse-client -h 127.0.0.1 -u app_user -d app_db
```

### 从 JDBC URL 解析连接参数

用户可能提供 JDBC URL 格式：`jdbc:clickhouse://host:port/database`，需要解析为 clickhouse-client 参数：

```
jdbc:clickhouse://nexus.syrinxchina.com:8123/test3
  → -h nexus.syrinxchina.com --port 8123 -d test3
```

```bash
# 示例：从 JDBC URL 构建连接
JDBC_URL="jdbc:clickhouse://nexus.syrinxchina.com:8123/test3"
HOST=$(echo $JDBC_URL | sed -n 's/.*:\/\/\([^:]*\):\([0-9]*\)\/\(.*\)/\1/p')
PORT=$(echo $JDBC_URL | sed -n 's/.*:\/\/\([^:]*\):\([0-9]*\)\/\(.*\)/\2/p')
DB=$(echo $JDBC_URL | sed -n 's/.*:\/\/\([^:]*\):\([0-9]*\)\/\(.*\)/\3/p')
clickhouse-client -h "$HOST" --port "$PORT" -u root -d "$DB"
```

### 连接参数表

| Option | Description |
|--------|-------------|
| `-h` / `--host` | Hostname (default: localhost) |
| `--port` | TCP port (default: 9000, HTTP port: 8123) |
| `-u` / `--user` | Username (default: default) |
| `--password` | Password (default: empty) |
| `-d` / `--database` | Default database (default: default) |
| `-q` / `--query` | Execute query and exit |
| `--format` | Output format (TSV/CSV/JSON/JSONEachRow etc.) |
| `--multiquery` | Allow multiple queries in one command |
| `--secure` | Use SSL/TLS connection |
| `--connect-timeout` | Connection timeout (seconds) |
| `--send-timeout` | Send data timeout (seconds) |
| `--receive-timeout` | Receive data timeout (seconds) |

**连接示例 (完整参数):**
```bash
CLICKHOUSE_PASSWORD=password clickhouse-client -h 192.168.1.100 --port 9000 -u admin -d mydb --secure --connect-timeout=10 --format=JSONEachRow
```

### 使用配置文件

创建 `~/.clickhouse-client/config.xml` 简化频繁连接：

```xml
<config>
  <host>127.0.0.1</host>
  <port>9000</port>
  <user>app_user</user>
  <password>yourpassword</password>
  <database>app_db</database>
  <secure>0</secure>
</config>
```

```bash
clickhouse-client --config ~/.clickhouse-client/config.xml -q "SELECT 1;" --format=JSONEachRow
```

## 数据操作

### 查询 (SELECT)

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SELECT * FROM your_table LIMIT 5;" --format=JSONEachRow | jq -s '.'
```

**推荐格式化模式:**
- `--format=JSONEachRow`：每行一个 JSON 对象，适合多行结果
- `--format=JSON`：单个 JSON 对象包裹所有结果
- `--format=TSV`：制表符分隔，适合简单输出

### 插入 (INSERT)

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "INSERT INTO users (name, email) VALUES ('New User', 'new@example.com');" 2>/dev/null
```

### 更新 (ALTER UPDATE)

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "ALTER TABLE users UPDATE status = 'active' WHERE signup_date < '2026-01-01';" 2>/dev/null
```

### 删除 (ALTER DELETE)

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "ALTER TABLE sessions DELETE WHERE last_activity < subtractDays(now(), 30);" 2>/dev/null
```

## 高级查询与 JSON 输出

### 统计摘要查询

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT JSON_OBJECT(
  'total_users', (SELECT COUNT(*) FROM users),
  'active_users', (SELECT COUNT(*) FROM users WHERE status = 'active'),
  'avg_posts', (SELECT AVG(post_count) FROM user_stats)
) AS report;
" --format=JSON | jq .
```

### 通用 JSON 输出模式

**单行结果：**
```bash
clickhouse-client ... -q "SELECT JSON_OBJECT('key1', column1, 'key2', column2) FROM ..." --format=JSON | jq .
```

**多行结果：**
```bash
clickhouse-client ... -q "SELECT id, name FROM users LIMIT 5" --format=JSONEachRow | jq -s '.'
```

## 批量执行 SQL 文件

```bash
clickhouse-client -h <host> -u <user> -d <db> --multiquery < script.sql 2>/dev/null
```

**批量导入 CSV：**
```bash
clickhouse-client -h <host> -u <user> -d <db> -q "INSERT INTO my_table FORMAT CSV" < data.csv 2>/dev/null
```

## 错误处理

### 常见错误码

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 516 | Authentication failed | 检查用户名/密码是否正确 |
| 81 | Unknown database | 检查数据库名是否存在 |
| 210 | Can't connect to ClickHouse | 检查 ClickHouse 服务是否启动，端口是否开放 |
| 60 | Table doesn't exist | 检查表名拼写是否正确 |

### 超时配置

```bash
clickhouse-client -h <host> -u <user> -d <db> --connect-timeout=5 --send-timeout=30 --receive-timeout=30 -q "SELECT * FROM large_table;" --format=TSV
```

### 连接测试模式

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SELECT 1 AS connected;" --format=TSV 2>&1 | grep -q "connected" && echo "连接成功" || echo "连接失败"
```

## 数据库与表操作

### 创建数据库

```bash
clickhouse-client -h <host> -u <user> -q "CREATE DATABASE IF NOT EXISTS new_db ENGINE = Atomic;" --format=TSV
```

### 列出所有数据库

```bash
clickhouse-client -h <host> -u <user> -q "SHOW DATABASES;" --format=TSV
```

### 列出表

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SHOW TABLES;" --format=TSV
```

### 查看表结构

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "DESCRIBE TABLE users;" --format=TSV
```

### 查看索引

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SHOW INDEXES FROM users;" --format=TSV
```

### 查看建表语句

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "SHOW CREATE TABLE users;" --format=TSV
```

## DESCRIBE TABLE 详解

### 查看单表结构

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "DESCRIBE TABLE users;" --format=TSV
```

输出字段说明：

| 字段 | 说明 |
|------|------|
| name | 列名 |
| type | 数据类型（String、Int64、DateTime 等） |
| default_type | 默认值类型 |
| default_expression | 默认值表达式 |
| comment | 字段注释 |
| codec_expression | 压缩算法 |
| ttl_expression | TTL 表达式 |

### 格式化输出为 JSON

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT JSON_ARRAYAGG(JSON_OBJECT(
  'column', name,
  'type', type,
  'default_type', default_type,
  'default_value', default_expression,
  'comment', comment,
  'ttl', ttl_expression
)) AS columns
FROM system.columns
WHERE database = '<database>' AND table = '<table>'
ORDER BY position;" --format=JSON | jq .
```

### 快速查看主键和分区键

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT name, type, is_in_primary_key, is_in_partition_key
FROM system.columns
WHERE database = '<database>'
  AND table = '<table>'
  AND (is_in_primary_key = 1 OR is_in_partition_key = 1)
ORDER BY is_in_primary_key DESC, position;" --format=JSONEachRow | jq -s '.'
```

### EXPLAIN 查询分析（重要！）

**分析 SELECT 查询执行计划：**

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "EXPLAIN SELECT * FROM users WHERE phone = '13800138000';" --format=JSONEachRow | jq -s '.'
```

**输出关键字段说明：**

| 字段 | 说明 |
|------|------|
| Expression | 表达式计算 |
| Filter | 过滤条件 |
| ReadFromStorage | 存储读取方式 |
| PrimaryKey | 主键使用情况 |
| Partition | 分区过滤情况 |
| Files | 涉及文件数 |
| Rows | 预计扫描行数（越小越好） |

**优化要点：**
- 确认分区键被有效使用
- 避免全表扫描（Full scan）
- 检查主键是否命中

### EXPLAIN ANALYZE（ClickHouse 21.1+）

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "EXPLAIN ANALYZE SELECT * FROM users WHERE phone = '13800138000';" --format=JSONEachRow | jq -s '.'
```

比 EXPLAIN 更详细，包含**实际运行时间**、**实际扫描行数**和**执行步骤耗时**。

### 查看表大小和行数

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT
  table AS table_name,
  total_rows AS rows,
  formatReadableSize(total_bytes) AS total_size,
  formatReadableSize(data_bytes) AS data_size,
  formatReadableSize(index_bytes) AS index_size
FROM system.tables
WHERE database = '<database>'
ORDER BY total_bytes DESC;" --format=JSONEachRow | jq -s '.'
```

### 查看数据库中所有表的基本信息

```bash
clickhouse-client -h <host> -u <user> -d <db> -q "
SELECT
  name AS table,
  engine AS table_engine,
  total_rows AS rows,
  formatReadableSize(total_bytes) AS size,
  comment AS table_comment
FROM system.tables
WHERE database = '<database>'
  AND engine NOT LIKE '%View%'
ORDER BY total_bytes DESC;" --format=JSONEachRow | jq -s '.'
```

## 环境变量配置

```bash
export CLICKHOUSE_PASSWORD="yourpassword"
export CLICKHOUSE_HOST="127.0.0.1"
export CLICKHOUSE_USER="app_user"
export CLICKHOUSE_DB="app_db"

clickhouse-client -h "$CLICKHOUSE_HOST" -u "$CLICKHOUSE_USER" -d "$CLICKHOUSE_DB" --password="$CLICKHOUSE_PASSWORD" -q "SELECT 1;" --format=JSONEachRow
```

## 完整示例脚本

```bash
#!/bin/bash
# 查询用户统计数据（带错误处理）

DB_HOST="${CLICKHOUSE_HOST:-127.0.0.1}"
DB_USER="${CLICKHOUSE_USER:-app_user}"
DB_PASS="${CLICKHOUSE_PASSWORD:-}"
DB_NAME="${CLICKHOUSE_DB:-app_db}"

QUERY="
SELECT JSON_OBJECT(
  'timestamp', now(),
  'summary', JSON_OBJECT(
    'total_users', (SELECT COUNT(*) FROM users),
    'active_users', (SELECT COUNT(*) FROM users WHERE status = 'active'),
    'new_today', (SELECT COUNT(*) FROM users WHERE toDate(created_at) = today())
  )
) AS report;
"

clickhouse-client -h "$DB_HOST" -u "$DB_USER" --password="$DB_PASS" -d "$DB_NAME" -q "$QUERY" --format=JSON 2>&1 | jq .
```

## 安全建议

1. **禁止**在命令行中直接写密码（进程列表可见）
2. **使用** `CLICKHOUSE_PASSWORD` 环境变量或配置文件
3. 生产环境**强制**使用 SSL (`--secure` 选项)
4. 配置文件权限设置为 `chmod 600 ~/.clickhouse-client/config.xml`
5. 查询操作使用只读账号
6. 避免使用默认端口和默认用户名/密码

**重要提示:** 使用 `--format` 参数指定输出格式（如 TSV/JSON/JSONEachRow）确保 clickhouse-client 输出纯净数据，是生成有效 JSON 的前提。
