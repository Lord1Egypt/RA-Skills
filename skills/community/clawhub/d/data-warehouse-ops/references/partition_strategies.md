# 分区策略参考 (Partition Strategies Reference)

## 各平台分区能力对比

| 特性 | BigQuery | Snowflake | Redshift | StarRocks | ClickHouse | Databricks |
|------|----------|-----------|----------|-----------|------------|------------|
| 分区方式 | 时间/整数范围/摄入时间 | 自动微分区 | DISTKEY + SORTKEY | RANGE/LIST | RANGE/LIST | RANGE |
| 分区粒度 | HOUR/DAY/MONTH/YEAR | 自动 | 复合键 | HOUR/DAY/MONTH/YEAR | HOUR/DAY/MONTH | YEAR/MONTH/DAY |
| 最大分区数 | 4000 | 无限制 | 无限制 | 1024 | 建议 < 1000 | 建议 < 10000 |
| 聚簇支持 | CLUSTER BY (4列) | CLUSTER BY (4列) | 复合SORTKEY(8列) | 分桶(BUCKETS) | ORDER BY | Z-ORDER |
| 分区裁剪 | 自动 | 自动(微分区) | 手动(SORTKEY) | 自动 | 自动 | 自动 |
| 成本影响 | 按扫描字节 | 按 credit | 按节点小时 | 免费(开源) | 免费(开源) | 按 DBU |

## BigQuery 分区策略

### 推荐模式
```sql
-- 标准模式：日期分区 + 聚簇
CREATE TABLE dwh.fact_orders (
    order_id STRING,
    customer_id INT64,
    product_id INT64,
    order_date DATE,
    total_amount NUMERIC,
    ...
)
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, product_id;
```

### 分区选择决策树
1. 有日期/时间列？ → `PARTITION BY DATE(timestamp_col)` (DAY 粒度)
2. 数据按摄入时间组织？ → `PARTITION BY _PARTITIONDATE` (摄入时间分区)
3. 只有整数 ID？ → `PARTITION BY RANGE_BUCKET(id, GENERATE_ARRAY(0, 1000000, 1000))`

### 聚簇列选择
- 常用 WHERE 过滤列（除分区列外）
- JOIN 键
- GROUP BY / ORDER BY 列
- 每个聚簇块 50k-500k 行效果最佳

### 注意
- 分区过期设置：`OPTIONS(partition_expiration_days=90)`
- 要求分区过滤：`OPTIONS(require_partition_filter=TRUE)`
- 每日免费 1 TB 扫描配额

## Snowflake 分区策略

### 自动微分区
Snowflake 自动将数据组织为微分区（50-500MB 未压缩），无需手动分区声明。

### 聚簇（可选）
```sql
-- 显式聚簇加速查询
CREATE TABLE dwh.fact_orders
CLUSTER BY (order_date, customer_id);
```

### 聚簇建议
- 高基数列聚簇效果好（数百万 distinct values）
- JOIN 频繁的列
- WHERE 过滤列
- 避免对频繁更新的列聚簇

### 监控
```sql
-- 查看聚簇深度（越小越好）
SELECT SYSTEM$CLUSTERING_INFORMATION('dwh.fact_orders');
-- 查看聚簇比率（> 2 可能需要重新聚簇）
SELECT SYSTEM$CLUSTERING_RATIO('dwh.fact_orders');
```

## Redshift 分区策略

### DISTKEY + SORTKEY
```sql
CREATE TABLE dwh.fact_orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    ...
)
DISTKEY(customer_id)          -- 分散到各节点
COMPOUND SORTKEY(order_date, customer_id);  -- 节点内排序
```

### DISTKEY 选择
- 选择 JOIN 最频繁的列
- 避免严重倾斜的列（某个值占比 > 25%）
- 优先选择过滤频率高的列
- 验证倾斜：`SELECT distkey, COUNT(*) FROM table GROUP BY distkey`

### SORTKEY 选择
- 第 1 列：最常做范围过滤的日期列
- 后续列：按查询频率降序排列
- 复合 SORTKEY 最多 8 列
- 定期 VACUUM 和 ANALYZE

### 自动表优化 (ATO)
```sql
-- 开启 Redshift 自动优化
ALTER TABLE dwh.fact_orders ALTER SORTKEY AUTO;
ALTER TABLE dwh.fact_orders ALTER DISTSTYLE AUTO;
```

## StarRocks 分区策略

### 分区 + 分桶
```sql
CREATE TABLE dwh.fact_orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    amount DECIMAL(18,2)
)
PARTITION BY RANGE(order_date) (
    PARTITION p202401 VALUES LESS THAN ("2024-02-01"),
    PARTITION p202402 VALUES LESS THAN ("2024-03-01"),
    PARTITION p202403 VALUES LESS THAN ("2024-04-01")
)
DISTRIBUTED BY HASH(order_id) BUCKETS 32;
```

### 动态分区
```sql
-- 自动创建和删除分区
ALTER TABLE dwh.fact_orders
SET (
    "dynamic_partition.enable" = "true",
    "dynamic_partition.time_unit" = "MONTH",
    "dynamic_partition.start" = "-3",   -- 保留最近 3 个月
    "dynamic_partition.end" = "1",      -- 提前创建未来 1 个月
    "dynamic_partition.prefix" = "p",
    "dynamic_partition.buckets" = "32"
);
```

### 分桶键选择
- 高基数列（distinct values 多）
- 分布均匀的列
- 常用于等值 JOIN 的列
- 建议 2 的幂次方

## ClickHouse 分区策略

### 分区 + 排序键
```sql
CREATE TABLE dwh.fact_orders (
    order_id UInt64,
    customer_id UInt64,
    order_date Date,
    amount Decimal(18,2)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(order_date)
ORDER BY (customer_id, order_date);
```

### 最佳实践
- 分区粒度：MONTH 最常用（不要过细）
- ORDER BY 即主键索引 → 按查询频率排序
- TTL 自动清理：`TTL order_date + INTERVAL 12 MONTH DELETE`
- 分区数不要超过 1000

## Databricks (Delta Lake) 分区策略

### 分区 + Z-Ordering
```sql
CREATE TABLE dwh.fact_orders
USING DELTA
PARTITIONED BY (order_year, order_month)
LOCATION '/mnt/dwh/fact_orders';

-- Z-Ordering 加速多维过滤
OPTIMIZE dwh.fact_orders ZORDER BY (customer_id, product_id);
```

### 最佳实践
- 分区列基数适中（每分区至少 1GB 数据）
- 避免小文件问题 — 使用 Auto Optimize
- Z-Ordering 列选高基数过滤列
- 定期 OPTIMIZE：`OPTIMIZE dwh.fact_orders`

## 分区策略选择决策树

```
是否有时间维度？
├── 是 → 按时间分区 (DAY/MONTH)
│   ├── 查询总是带时间过滤？ → 时间分区 + 聚簇其他列
│   └── 高频写入 + 实时查询？ → HOUR 粒度分区
├── 否 → 按业务键
│   ├── 按地区/租户分区 (多租户隔离)
│   └── 不分区，仅聚簇高频查询列
└── 特殊场景
    ├── 增量 ETL → 使用摄入时间分区
    └── 数据归档 → 按年分区 + TTL 自动删除
```

## 分区策略检查清单

- [ ] 分区列是否常用于 WHERE 过滤？
- [ ] 分区粒度是否合适（不过粗也不过细）？
- [ ] 是否设置了分区过期/自动清理策略？
- [ ] 聚簇列是否覆盖了主要的 JOIN 和 GROUP BY 操作？
- [ ] 是否避免了高基数键分区（如 user_id）？
- [ ] 是否设置了 require_partition_filter 防止意外全表扫描？
- [ ] 是否监控了分区数据倾斜？
