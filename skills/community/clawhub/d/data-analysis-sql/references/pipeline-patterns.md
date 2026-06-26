# ETL 管线设计模式

## 数据同步策略

### 全量同步（Full Load）

适用场景：表数据量小（<100万）、历史数据需要全部刷新。

```sql
-- 全量拉取（每次重写全表）
INSERT OVERWRITE TABLE ods_trade_orders PARTITION(dt = '${bizdate}')
SELECT
    order_id, user_id, order_amount, order_status,
    create_time, pay_time, update_time
FROM source_db.trade_orders;
```

### 增量同步（Incremental）

适用场景：大表（>1000万）、只同步新增/变更数据。

```sql
-- 增量同步（只取变化数据）
INSERT OVERWRITE TABLE ods_trade_orders PARTITION(dt = '${bizdate}')
SELECT
    order_id, user_id, order_amount, order_status,
    create_time, pay_time, update_time
FROM source_db.trade_orders
WHERE update_time >= DATE_SUB('${bizdate_cutoff}', 1)   -- 覆盖前一天的尾数据
  AND update_time < '${bizdate_cutoff}';
```

### CDC（Change Data Capture）

适用场景：需要捕获所有变更（INSERT/UPDATE/DELETE），延迟敏感业务。

| CDC 方案 | 适用数据库 | 说明 |
|---------|-----------|------|
| Debezium + Kafka | MySQL/PostgreSQL | 监听 binlog，实时捕获变更 |
| Canal | MySQL | 阿里开源，监听 binlog |
| Maxwell | MySQL | 轻量级 binlog 解析 |
| Flink CDC | MySQL/PG/MongoDB | Flink 实时读取 CDC |

```sql
-- CDC 数据落地后打标（区分 INSERT/UPDATE/DELETE）
SELECT
    order_id,
    user_id,
    order_amount,
    -- 变更类型标记（Debezium 格式示例）
    CASE
        WHEN __ Oppenheimer__ = 'd' THEN 'DELETE'
        WHEN __ Oppenheimer__ = 'u' AND before IS NOT NULL THEN 'UPDATE'
        ELSE 'INSERT'
    END AS cdc_op,
    before.order_status AS old_status,
    after.order_status  AS new_status
FROM cdc_orders_stream;
```

## 任务调度模式

### 依赖拓扑设计

```
ods_order_detail   ──→ dwd_order_detail  ──→ dws_user_action_daily  ──→ ads_trade_report
        ↓                    ↓                     ↓
    ods_user          dwd_user_base           dws_sale_gmv_daily
        ↓
    dwd_user_behavior ──→ dws_user_cohort
```

**调度原则：**
- ODS → DWD：小时级或日级，依赖上游 ODS 任务完成
- DWD → DWS：日级，一般 DWD 任务完成后启动
- ADS：最晚启动，依赖所有下游 DWS 汇总完成
- 独立主题可并行：如 DWD 订单宽表和 DWD 用户宽表可并行构建

### 故障恢复策略

| 故障场景 | 恢复策略 |
|---------|---------|
| 上游 ODS 数据缺失 | 等待上游补数据，重跑 ODS 后重刷下游 |
| 中间层 DWD 失败 | 直接重跑 DWD，全量覆盖 |
| ADS 报表失败 | 重跑 ADS，只重刷指标层（上游 DWD 已就绪） |
| 历史分区补数据 | 使用回溯窗口（如最近7天）按批次重刷，不影响当天任务 |

### 时间戳设计（任务幂等）

```sql
-- 每条数据带 ETL 时间戳，支持幂等重跑
SELECT
    order_id,
    dt                                           AS bizdate,       -- 业务日期
    '${etl_time}'                               AS etl_time,       -- ETL 执行时间
    '${bizdate}'                                AS partition_date  -- 分区字段
FROM ods_order_raw;
```

## 全量 vs 增量 vs 拉链

| 策略 | 原理 | 适用场景 | 数据量影响 |
|------|------|---------|-----------|
| **全量** | 每天全量覆盖 | 小表、历史无意义 | 存储线性增长 |
| **增量** | 每天只写新增/变更 | 大表、只关心当前状态 | 存储线性增长（有限） |
| **拉链** | UPDATE + INSERT，保留历史 | 需追溯历史状态（用户、商品、订单） | 存储固定（无增长） |
| **快照** | 每日拍全量快照 | 状态不可回溯的业务（库存） | 存储×天数增长 |

## 拉链更新实现

```sql
-- 拉链合并逻辑（每日增量合并历史）
INSERT OVERWRITE TABLE dwd_order_zipper PARTITION(dt = '${bizdate}')
SELECT
    order_id, user_id, product_id, order_amount, order_status,
    start_date,           -- 来自历史（不变）
    end_date,             -- 来自历史或今日关闭
    is_current
FROM (
    -- Step 1：历史数据照抄，关闭今日变更的记录
    SELECT
        order_id, user_id, product_id, order_amount, order_status,
        start_date,
        CASE WHEN order_id IN (
            SELECT order_id FROM ods_order_changes
            WHERE dt = '${bizdate}' AND change_type = 'UPDATE'
        ) THEN DATE_SUB('${bizdate}', 1)   -- 昨日关闭
        ELSE end_date END AS end_date,
        0 AS is_current                    -- 历史版本均非当前
    FROM dwd_order_zipper
    WHERE dt = DATE_SUB('${bizdate}', 1)
      AND is_current = 1                   -- 只取当前版本

    UNION ALL

    -- Step 2：今日新增/变更数据（新版本）
    SELECT
        order_id, user_id, product_id, order_amount, order_status,
        '${bizdate}'                        AS start_date,
        '9999-12-31'                        AS end_date,
        1                                   AS is_current
    FROM ods_order_changes
    WHERE dt = '${bizdate}'
) merged;
```

## 数据回溯重刷

```sql
-- 回溯重刷最近 N 天数据
-- 适用于 ODS 结构变更、DWD 口径调整

-- 批量生成重刷日期列表（Shell 示例）
-- for bizdate in $(seq 1 7 | xargs -I {} date -d "-{} days" +%Y-%m-%d); do
--   echo "重刷 bizdate=$bizdate"
--   spark-sql -f dwd_order_detail.sql -d bizdate=$bizdate
-- done

-- 数仓重刷原则：先重 ODS → 再重 DWD → 最后重 DWS/ADS
-- ADS 依赖最重，放最后统一重刷
```

## 数据漂移处理（Data Skew）

```sql
-- 症状：个别 reducer 处理数据量是平均值的 10 倍以上
-- 原因：热点 key 过度集中（如 null 值、大用户）

-- 方案1：加随机前缀打散
SELECT
    CONCAT(
        IF(RAND() < 0.5, 'a', 'b'),   -- 随机前缀
        user_id
    ) AS skewed_key,
    order_amount
FROM orders

-- 方案2：自定义 distribute/sort（Spark SQL）
SELECT /*+ REPARTITION(100, hash(user_id)) */ *
FROM orders

-- 方案3：过滤 NULL + 单独处理
SELECT * FROM orders WHERE user_id IS NOT NULL
UNION ALL
SELECT * FROM orders WHERE user_id IS NULL DISTRIBUTE BY RAND();
```

## UDF / UDTF 开发规范

```sql
-- 注册 UDF（永久函数）
CREATE FUNCTION my_md5 AS 'com.udf.StringMD5'
LOCATION 'hdfs:///user/hive/udf/my-udf.jar';

-- 注册临时 UDF（当前 session 有效）
CREATE TEMPORARY FUNCTION my_concat AS 'com.udf.StringConcat';

-- UDTF（表生成函数）：一行输入，多行输出
-- 示例：自定义分词 UDTF
SELECT user_id, word
FROM (
    SELECT user_id, my_tokenizer(content) AS words
    FROM user_content
)
LATERAL VIEW EXPLODE(words) t AS word;
```
