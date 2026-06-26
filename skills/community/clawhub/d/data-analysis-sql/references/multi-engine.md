# 多数据引擎方言速查

## 引擎选择建议

| 场景 | 推荐引擎 |
|------|---------|
| 离线大表批处理（TB级） | Hive / SparkSQL |
| 跨源联邦查询（多数据源） | Presto / Trino |
| 高并发实时 OLAP | ClickHouse |
| 多表 JOIN 的 OLAP 查询 | Doris / StarRocks |
| 云原生大表 Serverless | BigQuery |
| 业务库读写混合 | MySQL / PostgreSQL |
| 湖仓一体 | Iceberg + SparkSQL / Trino |

---

## Hive / SparkSQL

```sql
-- 日期函数
DATE_SUB(CURRENT_DATE, 7)
DATE_ADD(CURRENT_DATE, 1)
DATEDIFF('2024-03-15', '2024-03-01')         -- 返回天数差
MONTHS_BETWEEN('2024-03-15', '2024-01-01')

-- 字符串函数
CONCAT(STRING, ...)                          -- 拼接
CONCAT_WS('-', ARRAY<STRING>)               -- 数组拼接
SPLIT(col, ',')                              -- 字符串切数组
GET_JSON_OBJECT(col, '$.key')               -- JSON 解析
REGEXP_EXTRACT(col, 'pattern(\\d+)', 1)    -- 正则提取

-- 条件函数
IF(condition, true_val, false_val)
NVL(col, default_val)
COALESCE(col1, col2, ...)
CASE WHEN cond THEN val ELSE default END

-- 聚合函数
COLLECT_LIST(col)    -- 聚合为数组（不去重）
COLLECT_SET(col)     -- 聚合为数组（去重）
SUM(IF(status='paid', 1, 0))               -- 条件计数

-- 炸开数组
SELECT EXPLODE(arr_col) AS item FROM ...

-- 类型转换
CAST(col AS STRING)
CAST(col AS DECIMAL(18,2))
CAST(col AS ARRAY<STRING>)

-- 窗口函数（完整语法）
SUM(col) OVER (PARTITION BY x ORDER BY y ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)

-- 近似函数（大数据集加速）
APPROX_COUNT_DISTINCT(col)                  -- 近似去重（误差约2%）
APPROX_PERCENTILE(col, 0.5)                 -- 近似分位数

-- 分区裁剪（必须带分区字段）
WHERE dt = '2024-03-15'                     -- ✅ 好
WHERE dt >= '2024-03-01' AND dt <= '2024-03-15'  -- ✅ 好
WHERE DATE_FORMAT(create_time, 'yyyy-MM-dd') = '2024-03-15'  -- ❌ 索引失效

-- 防止数据倾斜
DISTRIBUTE BY hash(user_id)                 -- 按 hash 打散
SORT BY user_id                             -- reducer 内排序
CLUSTER BY user_id                          -- DISTRIBUTE BY + SORT BY 合并
```

## ClickHouse

```sql
-- 日期函数
toDate(created_at)                          -- DATE
toStartOfDay(created_at)                    -- 当天零点
toStartOfMonth(created_at)                   -- 月初
toStartOfWeek(created_at)                   -- 周一
formatDateTime(created_at, '%Y-%m-%d')     -- 格式化

-- 聚合函数
count()                                      -- 高效 COUNT(*)
uniqExact(user_id)                           -- 精确去重（数据量大时慢）
uniqMerge(uniqState(user_id))                -- 去重状态合并（分布式）
argMax(user_id, time)                       -- 取最大值对应的 user_id
argMin(time, amount)                        -- 取最小值对应的 time

-- 组内拼接
groupArray(100)(product_name)               -- 组内取最多100个拼接成数组
groupBitmap(user_id)                         -- Bitmap 去重

-- 分位计算
quantileExact(0.5)(amount)                  -- 精确中位数
quantileTDigest(0.95)(amount)               -- 近似分位数（误差小）

-- 窗口函数（ClickHouse 20.3+）
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY create_time) AS rn
SUM(amount) OVER (PARTITION BY user_id ORDER BY create_time
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_amount

-- 物化视图（预聚合）
CREATE MATERIALIZED VIEW mv_daily_metric
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(dt)
ORDER BY (dt, platform)
AS SELECT dt, platform, SUM(amount) AS total_amount, COUNT(*) AS order_cnt
FROM dwd_order_detail
GROUP BY dt, platform;

-- JOIN 注意事项
-- ClickHouse 小表放右（大表 LEFT JOIN 小表）
-- GLOBAL JOIN：强制广播
SELECT a.*, b.name FROM A GLOBAL JOIN B ON a.id = b.id;

-- NULL 处理
-- ClickHouse 默认不忽略 NULL，COUNT(DISTINCT x) 会计入 NULL
-- 需显式排除：uniqExact(ifNull(user_id, ''))
```

## Doris / StarRocks

```sql
-- 日期函数
DATE_FORMAT(create_time, '%Y-%m-%d')        -- 格式化
DATE_SUB(create_time, INTERVAL 7 DAY)       -- 日期偏移
DAYS_SUB(create_time, 7)                    -- 简写形式
DATE_TRUNC(create_time, 'MONTH')           -- 月初

-- 窗口函数（全面支持）
SUM(amount) OVER (PARTITION BY user_id ORDER BY dt
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_amount

-- 聚合函数
GROUP_CONCAT(DISTINCT category ORDER BY sales DESC SEPARATOR ',')  -- 组内拼接
ARRAY_AGG(col ORDER BY col2)                -- 数组聚合

-- Lateral View（UDTF 展开）
SELECT user_id, tag
FROM (
    SELECT user_id, SPLIT(content, ',') AS tags FROM user_profile
) t
LATERAL VIEW EXPLODE(tags) tag_table AS tag;

-- Bitmap 函数（高效 UV 计算）
SELECT BITMAP_COUNT(BITMAP_OR(user_bitmap)) AS uv
FROM dws_user_bitmap_daily;

-- 物化视图（自动改写）
CREATE MATERIALIZED VIEW mv_sale_daily
AS SELECT dt, platform, SUM(pay_amount) AS gmv
FROM dwd_order_detail
GROUP BY dt, platform;
```

## Presto / Trino

```sql
-- 日期函数
DATE_TRUNC('month', created_at)             -- 月初
DATE_ADD('day', 7, created_at)              -- 加7天
DATE_DIFF('day', start_date, end_date)     -- 天数差
FORMAT_DATETIME(created_at, '%Y-%m-%d')

-- 字符串函数
SPLIT(col, ',')[2]                          -- 取数组第2个（1-indexed）
JSON_EXTRACT_scalar(col, '$.key')           -- JSON 提取标量
REGEXP_EXTRACT(col, 'pattern(\d+)', 1)     -- 正则
TRIM, LTRIM, RTRIM
LOWER, UPPER, INITCAP

-- 数组函数
ARRAY[1, 2, 3]                              -- 构造数组
CONCAT(arr1, arr2)                          -- 数组合并
ARRAY_JOIN(arr, ',')                        -- 数组转字符串
CARDINALITY(arr)                            -- 数组长度
FILTER(arr, x -> x > 3)                    -- 数组过滤

-- 聚合
ANY_VALUE(col)                              -- 任意值（不聚合报错时用）
ARRAY_AGG(col ORDER BY created_at)          -- 数组聚合（有序）
MAP_AGG(key, value)                        -- 构造 MAP

-- APPROX 函数
APPROX_DISTINCT(col)                        -- 近似去重
APPROX_PERCENTILE(col, 0.99)                -- 近似分位

-- 窗口函数
RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
LAG(col, 1) OVER (PARTITION BY user_id ORDER BY dt) AS prev_val
FIRST_VALUE(col) OVER (PARTITION BY user_id ORDER BY dt
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_val

-- UNION vs UNION ALL：Presto 无需特别优化，UNION ALL 更快
```

## BigQuery

```sql
-- 日期函数
DATE_TRUNC(create_time, MONTH)             -- 月初
DATE_ADD(create_time, INTERVAL 7 DAY)      -- 加7天
DATE_DIFF(end_date, start_date, DAY)       -- 天数差（DAY/WEEK/MONTH/YEAR）
FORMAT_DATE('%Y-%m', create_time)          -- 格式化

-- 字符串
CONCAT('user_', user_id)
SPLIT(col, ',')                            -- 数组
REGEXP_EXTRACT(col, r'pattern(\d+)')      -- 正则
JSON_VALUE(payload, '$.key')               -- JSON 提取

-- 聚合
ARRAY_AGG(col ORDER BY created_at LIMIT 100)  -- 有序数组聚合
STRING_AGG(DISTINCT tag, ',')              -- 字符串聚合去重

-- 窗口函数
SUM(amount) OVER (PARTITION BY user_id ORDER BY dt
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7d
RANK() OVER (PARTITION BY dept ORDER BY salary DESC)
LAG(col, 1, 0) OVER (...)                  -- 默认填充值

-- APPROX 函数
APPROX_COUNT_DISTINCT(user_id)             -- 近似去重
APPROX_QUANTILES(col, 100)[OFFSET(50)]     -- 分位数

-- BigQuery 特有的 TIMESTAMP 类型
CAST(created_at AS TIMESTAMP)
CURRENT_TIMESTAMP()
TIMESTAMP_DIFF(end_time, start_time, SECOND)

-- 强烈推荐：分区 + 聚簇
CREATE TABLE dwd_order_detail
PARTITION BY DATE(create_time)
CLUSTER BY user_id, platform
AS SELECT ...;
```

## MySQL / PostgreSQL

```sql
-- MySQL 日期
DATE_FORMAT(created_at, '%Y-%m-%d')
DATE_SUB(CURDATE(), INTERVAL 7 DAY)
DATEDIFF(end_date, start_date)
IFNULL(col, 0)

-- PostgreSQL 日期
TO_CHAR(created_at, 'YYYY-MM-DD')
created_at - INTERVAL '7 days'
EXTRACT(DAY FROM created_at)
COALESCE(col, 0)
GREATEST(a, b)                              -- 最大值（忽略NULL）
LEAST(a, b)                                 -- 最小值

-- PostgreSQL 特有
ARRAY_AGG(col ORDER BY col2)               -- 有序数组聚合
STRING_AGG(col, ',')                       -- 字符串聚合
JSON_AGG(row)                              -- JSON 聚合
UNNEST(ARRAY[1,2,3])                       -- 数组展开
GENERATE_SERIES(1, 10)                      -- 序列生成

-- 递归 CTE（树形结构）
WITH RECURSIVE tree AS (
    SELECT id, name, parent_id, 1 AS level
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, t.level + 1
    FROM categories c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;

-- 窗口函数（标准）
ROW_NUMBER() OVER (PARTITION BY dept ORDER BY hiredate)
LAG(col, 1) OVER (PARTITION BY dept ORDER BY hiredate)
```

## SQL 改写规则（引擎迁移对照）

| 场景 | Hive/Spark → ClickHouse | Hive/Spark → Presto | MySQL → BigQuery |
|------|------------------------|---------------------|------------------|
| 日期减7天 | `DATE_SUB(dt, 7)` | `DATE_ADD('day', -7, dt)` | `DATE_SUB(dt, INTERVAL 7 DAY)` |
| 条件聚合 | `SUM(IF(status='paid',1,0))` | `SUM(CASE WHEN status='paid' THEN 1 END)` | 同 Presto |
| 去重计数 | `COUNT(DISTINCT col)` | `APPROX_DISTINCT(col)`（大表） | `APPROX_COUNT_DISTINCT(col)` |
| NULL 处理 | `NVL(col, 0)` | `COALESCE(col, 0)` | `IFNULL(col, 0)` |
| 字符串拼接 | `CONCAT(a, b)` | `CONCAT(a, b)` 或 `a \|\| b` | `CONCAT(a, b)` |
| 分组 TOP-K | `ROW_NUMBER() OVER PARTITION` | 同 | 同 |
