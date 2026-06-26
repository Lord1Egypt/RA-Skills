# QuestDB使用指南

## 简介

QuestDB是一款高性能时序数据库，支持SQL查询，适合量化因子数据的存储与分析。本指南基于视频第2集内容整理。

---

## 下载与安装

### 官网下载

1. 访问 https://questdb.com 或 GitHub releases
2. 根据系统选择对应版本（Windows/Mac/Linux）
3. 下载文件约3MB（很轻量）

### 各系统安装

#### Windows（本地）

```bash
# 1. 解压到本地目录，如 D:\questdb
# 2. Shift+右键打开PowerShell窗口
# 3. 启动命令
java -p questdb.jar -m io.questdb.server.ServerMain -d D:\questdb\data
```

#### Mac/Linux

```bash
# 解压
tar -xzf questdb-7.x.x.tar.gz
cd questdb-7.x.x

# 启动
./questdb.sh start

# 或指定数据目录
java -p questdb.jar -m io.questdb.server.ServerMain -d /path/to/data
```

---

## Web控制台

启动后访问：http://localhost:9000

可执行SQL查询、查看数据、导入导出CSV

---

## 核心连接方式

| 方式 | 端口 | 用途 |
|------|------|------|
| HTTP | 9000 | Web控制台、REST API |
| PGwire | 8812 | PostgreSQL兼容协议 |
| TCP ILP | 9009 | InfluxDB行协议（高速写入） |

---

## Python连接与写入

### 使用pandas写入

```python
import pandas as pd
from sqlalchemy import create_engine

# 连接QuestDB（PGwire协议）
engine = create_engine('postgresql://admin:quest@localhost:8812/qdb')

# 写入DataFrame
df.to_sql('factor_wide_table', engine, if_exists='append', index=False)

# 查询
query = "SELECT * FROM factor_wide_table WHERE symbol = '000001.SZ'"
result = pd.read_sql(query, engine)
```

### 使用QuestDB ILP协议高速写入

```python
from questdb.ingress import Sender

# 高性能写入（推荐用于实盘数据）
with Sender('localhost', 9009) as sender:
    sender.row('factor_wide_table',
        symbols={'symbol': '000001.SZ', 'trade_date': '2025-01-01'},
        columns={'obv': 123456.78, 'mfi': 65.4, 'close': 15.20}
    )
    sender.flush()
```

---

## 核心SQL操作

### 创建表

```sql
-- 因子宽表
CREATE TABLE factor_wide_table (
    symbol STRING,
    trade_date TIMESTAMP,
    obv DOUBLE,
    mfi DOUBLE,
    emv DOUBLE,
    mom DOUBLE,
    rsi DOUBLE,
    close DOUBLE,
    volume DOUBLE,
    ret DOUBLE
) TIMESTAMP(trade_date) PARTITION BY DAY;

-- 创建索引加速查询
CREATE INDEX ON factor_wide_table(symbol);
```

### 基础查询

```sql
-- 按日期范围查询
SELECT * FROM factor_wide_table
WHERE trade_date BETWEEN '2025-01-01' AND '2025-12-31'
AND symbol = '000001.SZ';

-- 按因子值排序选股
SELECT symbol, trade_date, mfi, rsi
FROM factor_wide_table
WHERE trade_date = '2025-01-02'
ORDER BY mfi DESC
LIMIT 20;
```

### 聚合分析

```sql
-- 计算因子IC值
SELECT
    symbol,
    AVG(ret) as avg_ret,
    CORR(mfi, ret) as ic_mfi
FROM factor_wide_table
WHERE trade_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY symbol;

-- 周度统计
SELECT date_trunc('week', trade_date) as week,
    AVG(mfi) as avg_mfi
FROM factor_wide_table
SAMPLE BY 1w;
```

---

## 数据导入

### CSV导入

```sql
-- 从控制台导入
IMPORT TABLE factor_wide_table FROM 'C:/data/factor.csv' WITH HEADER true;
```

### Python批量写入

```python
# 批量处理后写入
chunks = pd.read_csv('factor_data.csv', chunksize=10000)
for chunk in chunks:
    chunk.to_sql('factor_wide_table', engine, if_exists='append', index=False)
```

---

## 注意事项

1. **免费版限制**：免费版完全够用，无需付费
2. **数据目录**：建议指定固定目录存放数据
3. **启动速度**：首次启动较慢，后续会缓存加速
4. **Docker支持**：有官方Docker镜像可快速部署
