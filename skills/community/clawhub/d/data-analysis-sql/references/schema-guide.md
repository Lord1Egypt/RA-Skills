# 数仓建模指南（大数据工程师视角）

## 数据分层架构

```
┌─────────────────────────────────────────────────────┐
│  ODS  (Operational Data Store)   ← 原始数据层       │
│    ↓ ETL / CDC                                           │
│  DWD  (Data Warehouse Detail)   ← 明细事实+维度退化   │
│    ↓ 轻度聚合                                            │
│  DWS  (Data Warehouse Summary)  ← 按主题汇总（按天/月） │
│    ↓ 按需聚合                                            │
│  ADS  (Application Data Store)  ← 应用层（报表/接口）  │
└─────────────────────────────────────────────────────┘
```

| 层级 | 特征 | 表命名示例 |
|------|------|---------|
| **ODS** | 1:1 映射源表，加 ETL 时间戳 | `ods_trade_orders`、`ods_user_login` |
| **DWD** | 清洗后的原子事实+退化维度 | `dwd_order_detail`、`dwd_user_base` |
| **DWS** | 按主题轻度汇总，按天/周/月 | `dws_user_action_daily`、`dws_sale_gmv_monthly` |
| **ADS** | 面向业务的指标表，供报表/接口 | `ads_business_report`、`ads_realtime_dashboard` |

## 主题域划分

| 主题域 | 核心事实表 | 核心指标 |
|--------|----------|---------|
| 交易（trade） | 订单、支付、退款 | GMV、订单量、客单价、支付转化率 |
| 用户（user） | 行为事件、会员 | DAU、新增、留存、分层 |
| 商品（product） | 商品、类目、库存 | SKU数、动销率、库存周转 |
| 流量（流量） | 点击流、搜索词 | PV、UV、点击率、跳出率 |
| 营销（marketing） | 活动、红包、优惠券 | 核销率、ROI、投入产出比 |

## 事实表设计

### 事务事实表（Transaction Fact）

记录每个业务事件，不可更新，只追加。

```sql
-- 订单事务事实表
CREATE TABLE dwd_order_detail (
    order_id          STRING          COMMENT '订单ID',
    user_id           STRING          COMMENT '用户ID',
    product_id        STRING          COMMENT '商品ID',
    category_l1_id    STRING          COMMENT '一级类目ID',
    category_l2_id    STRING          COMMENT '二级类目ID',
    shop_id           STRING          COMMENT '店铺ID',
    city_id           STRING          COMMENT '城市ID',
    order_amount      DECIMAL(18,2)   COMMENT '订单金额',
    pay_amount        DECIMAL(18,2)   COMMENT '实付金额',
    discount_amount   DECIMAL(18,2)   COMMENT '优惠金额',
    coupon_amount     DECIMAL(18,2)   COMMENT '优惠券金额',
    order_status      STRING          COMMENT '订单状态',
    create_time       STRING          COMMENT '下单时间',
    pay_time          STRING          COMMENT '支付时间',
    ship_time         STRING          COMMENT '发货时间',
    receive_time      STRING          COMMENT '收货时间',
    is_valid          TINYINT         COMMENT '是否有效（1有效 0无效）',
    -- 退化维度（直接冗余，避免大 JOIN）
    platform          STRING          COMMENT '来源平台',
    channel           STRING          COMMENT '来源渠道',
    -- 审计字段
    etl_time          STRING          COMMENT 'ETL 时间'
) COMMENT '订单明细事实表'
PARTITIONED BY (dt STRING)              -- 按天分区，禁止全量分区
STORED AS PARQUET                      -- 列式存储，压缩比高
TBLPROPERTIES ('parquet.compression'='SNAPPY');
```

### 周期快照事实表（Periodic Snapshot Fact）

定期（如每日）拍一张全量状态的快照，适合不可累加指标（库存、账户余额）。

```sql
CREATE TABLE dws_product_stock_daily (
    product_id        STRING          COMMENT '商品ID',
    sku_id            STRING          COMMENT 'SKU ID',
    warehouse_id      STRING          COMMENT '仓库ID',
    stock_qty         BIGINT          COMMENT '库存数量',
    available_qty     BIGINT          COMMENT '可用库存',
    frozen_qty        BIGINT          COMMENT '冻结库存',
    last_inbound_time STRING          COMMENT '最近入库时间',
    last_outbound_time STRING         COMMENT '最近出库时间',
    etl_time          STRING
) COMMENT '商品库存日快照'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 累计快照事实表（Accumulating Snapshot Fact）

记录流程从开始到结束的全程状态，适合有明确结束节点的流程（订单生命周期、物流）。

```sql
-- 订单生命周期累计表（退款关闭后不再更新）
CREATE TABLE dwd_order_lifecycle_accum (
    order_id          STRING,
    user_id           STRING,
    create_time       STRING,
    pay_time          STRING          COMMENT '支付时间（未支付则NULL）',
    ship_time         STRING,
    receive_time      STRING,
    refund_time       STRING          COMMENT '退款时间（未退款则NULL）',
    close_time        STRING,
    order_status      STRING,
    etl_time          STRING
) COMMENT '订单生命周期累计事实表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

## 维度表设计

### 标准维度表（Slowly Changing Dim）

```sql
CREATE TABLE dim_user (
    user_id           STRING          COMMENT '用户ID（自然键）',
    nickname          STRING          COMMENT '昵称',
    mobile            STRING          COMMENT '手机号',
    gender            STRING          COMMENT '性别',
    age_group         STRING          COMMENT '年龄段',
    city_id           STRING          COMMENT '城市ID',
    city_name         STRING          COMMENT '城市名（退化维度）',
    register_platform STRING          COMMENT '注册平台',
    register_time     STRING          COMMENT '注册时间',
    member_level      STRING          COMMENT '会员等级',
    -- SCD Type 2 字段
    start_date        STRING          COMMENT '生效日期',
    end_date          STRING          COMMENT '失效日期（9999-12-31表示当前）',
    is_current        TINYINT         COMMENT '是否当前版本',
    etl_time          STRING
) COMMENT '用户维度表'
PARTITIONED BY (dt STRING)
STORED AS PARQUET;
```

### 迷你维度（Mini Dimension / Junk Dimension）

将低基数、高频使用的维度字段（如平台、渠道、活动类型）直接退化到事实表，避免 JOIN。

```
退化维度 vs 独立维度表：
- 频繁 JOIN 查询 → 退化维度到事实表（DWD 层常见）
- 字段经常变更 → 独立维度表 + SCD Type 2
- 枚举值少且固定 → 迷你维度（junk dim）
```

### 拉链表（Slowly Changing Type 1 & 2）

适用于数据量大但需要保留历史的维度（如订单关联商品信息）。

```sql
-- 每日增量 + 历史拉链
INSERT OVERWRITE TABLE dwd_product_dim PARTITION(dt = '${bizdate}')
SELECT
    product_id,
    product_name,
    category_id,
    shop_id,
    price,
    start_date,                                          -- 该版本开始日期
    CASE WHEN n.next_start IS NULL THEN '9999-12-31'
         ELSE DATE_SUB(n.next_start, 1) END AS end_date, -- 该版本结束日期
    CASE WHEN n.next_start IS NULL THEN 1 ELSE 0 END    AS is_current,
    '${bizdate}' AS etl_time
FROM (
    SELECT
        p.*,
        LEAD(start_date) OVER (PARTITION BY product_id ORDER BY start_date) AS next_start
    FROM (
        -- 今日新增/变更
        SELECT product_id, product_name, category_id, shop_id, price,
               '${bizdate}' AS start_date
        FROM ods_product_raw
        WHERE dt = '${bizdate}'
        UNION ALL
        -- 继承历史不变数据
        SELECT product_id, product_name, category_id, shop_id, price, start_date
        FROM dwd_product_dim
        WHERE dt = DATE_SUB('${bizdate}', 1)
          AND end_date = '9999-12-31'   -- 只取当前版本
          AND (product_name, category_id, shop_id, price) = (
              SELECT product_name, category_id, shop_id, price
              FROM ods_product_raw WHERE dt = '${bizdate}' AND product_id = dwd_product_dim.product_id
          )
    ) p
) n;
```

## 字段命名规范

| 实体 | 字段规范 | 示例 |
|------|---------|------|
| 时间维度 | `xxx_time`（精确到秒）、`xxx_date`（天）、`xxx_dt`（分区字段） | `create_time`、`order_date`、`dt` |
| 金额 | `xxx_amount`（DECIMAL） | `order_amount`、`pay_amount`、`coupon_amount` |
| 数量 | `xxx_cnt`（BIGINT/INT） | `order_cnt`、`sku_cnt`、`uv` |
| 比率 | `xxx_rate`/`xxx_pct`（DECIMAL, 0.0-1.0 或 0-100） | `pay_rate`、`cvr_pct` |
| 布尔 | `is_xxx`/`has_xxx`/`can_xxx`（TINYINT, 0/1） | `is_valid`、`is_member`、`is_refunded` |
| 标识 | `xxx_id`（STRING，保留原始值） | `order_id`、`user_id` |
| 枚举 | `xxx_type`/`xxx_status`/`xxx_level`（STRING） | `order_status`、`member_level` |

## 分区设计原则

```
❌ 错误：PARTITIONED BY (dt STRING)  +  SELECT *
✅ 正确：WHERE dt = '${bizdate}'      +  只取当天分区

动态分区建议：
- 小表（< 1万行）：可以用固定分区或子查询
- 大表（> 1亿行）：必须严格分区过滤，禁止全表扫描
- 历史分区重刷：走回溯任务，不要直接 DELETE
```

## 数据类型选择

| 数据类型 | 大小 | 适用场景 |
|---------|------|---------|
| `STRING` | 可变 | 所有文本、ID、JSON、数值（统一存储兼容性最好） |
| `DECIMAL(18,2)` | 18 bytes | 金额、精确计算字段 |
| `BIGINT` | 8 bytes | 大计数、ID |
| `INT` | 4 bytes | 小计数、枚举数值映射 |
| `TINYINT` | 1 byte | 布尔标记、is_valid |
| `MAP<STRING,STRING>` | 可变 | 动态属性、扩展字段 |
| `ARRAY<STRING>` | 可变 | 标签列表、行为序列 |

> **Parquet 存储优势**：列式压缩、谓词下推（分区裁剪），`STRING` 类型在 Parquet 下实际存储紧凑，推荐优先使用。
