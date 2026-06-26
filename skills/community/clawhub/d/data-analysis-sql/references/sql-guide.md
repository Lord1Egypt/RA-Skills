# SQL 编写规范与大数据引擎指南

## 通用规范

- **关键字大写**：`SELECT`、`FROM`、`WHERE`、`JOIN`、`GROUP BY`
- **每个子句占一行**，禁止多子句写在一行
- **禁止 `SELECT *`**，必须明确列出字段，并加注释
- **表别名**用简短有意义的字母（`a/b/o/u`），避免无意义别名
- **字段别名**用 `AS alias_name`，不要省略 AS
- **CTE 优先**：超过 2 层嵌套子查询 → 改用 CTE（`WITH ... AS`）

## 标准查询结构

```sql
SELECT
    -- 时间维度
    DATE(create_time)                          AS dt,
    -- 主键 & 维度
    user_id,
    platform,
    city_level,
    -- 原子指标
    COUNT(DISTINCT order_id)                   AS order_cnt,
    COUNT(DISTINCT user_id)                    AS buyer_cnt,
    SUM(order_amount)                          AS gmv,
    SUM(pay_amount)                            AS revenue,
    -- 派生指标（先算原子，再派生）
    SUM(order_amount) / NULLIF(COUNT(DISTINCT order_id), 0) AS avg_order_amount,
    -- 留存率 / 转化率
    ROUND(100.0 * sign_user_cnt / NULLIF(view_user_cnt, 0), 2) AS cvr
FROM dwd_order_detail
WHERE dt = '${bizdate}'
  AND is_valid = 1                             -- 过滤无效数据
  AND order_status NOT IN ('cancelled', 'refunded')
GROUP BY DATE(create_time), user_id, platform, city_level
HAVING SUM(order_amount) > 0
ORDER BY dt DESC, gmv DESC
LIMIT 100;
```

## CTE 规范（大宽表必备）

```sql
WITH base_orders AS (
    -- Step 1: 从 DWD 拉明细，加通用维度
    SELECT
        o.order_id,
        o.user_id,
        o.order_amount,
        o.pay_amount,
        o.create_time,
        u.city_level,
        u.gender,
        u.age_group,
        p.category_name
    FROM dwd_order_detail o
    INNER JOIN dim_user u ON o.user_id = u.user_id
    INNER JOIN dim_product p ON o.product_id = p.product_id
    WHERE o.dt = '${bizdate}'
      AND o.is_valid = 1
),
order_agg AS (
    -- Step 2: 按用户+类目聚合
    SELECT
        user_id,
        category_name,
        city_level,
        COUNT(DISTINCT order_id)   AS order_cnt,
        SUM(order_amount)           AS gmv,
        MAX(create_time)           AS last_order_time
    FROM base_orders
    GROUP BY user_id, category_name, city_level
),
user_stats AS (
    -- Step 3: 计算人均
    SELECT
        category_name,
        city_level,
        COUNT(DISTINCT user_id)           AS buyer_cnt,
        SUM(gmv)                           AS total_gmv,
        AVG(gmv)                           AS avg_gmv_per_user
    FROM order_agg
    GROUP BY category_name, city_level
)
SELECT * FROM user_stats
ORDER BY total_gmv DESC;
```

## 窗口函数进阶

```sql
-- 累计窗口（用于累计值 / 累计占比）
SUM(amount) OVER (
    PARTITION BY user_id
    ORDER BY dt
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW   -- 累计到当前行
) AS cum_amount

-- 滑动窗口（近7天平均）
AVG(amount) OVER (
    PARTITION BY user_id
    ORDER BY dt
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW           -- 含今日共7天
) AS rolling_7d_avg

-- 首次/末次出现时间
FIRST_VALUE(event_time) OVER (PARTITION BY session_id ORDER BY event_time) AS session_start,
LAST_VALUE(event_time)  OVER (PARTITION BY session_id ORDER BY event_time
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS session_end

-- 占比 / 排名
SUM(amount)   OVER (PARTITION BY dt)                      AS dt_total,    -- 每日合计
amount / SUM(amount) OVER (PARTITION BY dt)               AS dt_share,    -- 每日占比
PERCENT_RANK() OVER (PARTITION BY dept ORDER BY salary)  AS pct_rank,    -- 百分位排名
```

## 关键业务模式

### 1. 订单状态拆解（全链路）

```sql
SELECT
    DATE(create_time)                              AS dt,
    COUNT(*)                                        AS total_orders,
    SUM(CASE WHEN status = 'pending'  THEN 1 END)  AS pending_cnt,
    SUM(CASE WHEN status = 'paid'     THEN 1 END)  AS paid_cnt,
    SUM(CASE WHEN status = 'shipped' THEN 1 END)  AS shipped_cnt,
    SUM(CASE WHEN status = 'completed'THEN 1 END)  AS completed_cnt,
    SUM(CASE WHEN status = 'cancelled'THEN 1 END) AS cancelled_cnt,
    -- 支付转化率
    ROUND(SUM(CASE WHEN status IN ('paid','shipped','completed') THEN 1 END) * 100.0
          / NULLIF(COUNT(*), 0), 2)                AS pay_rate
FROM dwd_order_detail
WHERE dt = '${bizdate}'
GROUP BY DATE(create_time);
```

### 2. 用户生命周期打标

```sql
SELECT
    user_id,
    first_login_dt,
    last_login_dt,
    login_days_30d,
    CASE
        WHEN login_days_30d IS NULL               THEN '未注册'
        WHEN login_days_30d = 0 AND first_login_dt = CURRENT_DATE THEN '新注册'
        WHEN login_days_30d = 0                   THEN '沉默用户'
        WHEN login_days_30d BETWEEN 1 AND 7        THEN '低活'
        WHEN login_days_30d BETWEEN 8 AND 20       THEN '中活'
        WHEN login_days_30d > 20                   THEN '高活'
        WHEN DATEDIFF(CURRENT_DATE, last_login_dt) > 30 THEN '流失用户'
    END AS user_lifecycle_stage
FROM dws_user_lifecycle_daily
WHERE dt = CURRENT_DATE - 1;
```

### 3. 商品 TOP-N 分析（分组 TopK）

```sql
SELECT * FROM (
    SELECT
        category_name,
        product_name,
        sales_cnt,
        sales_amount,
        ROW_NUMBER() OVER (PARTITION BY category_name ORDER BY sales_amount DESC) AS rn
    FROM dwd_product_sales_detail
    WHERE dt = '${bizdate}'
) t
WHERE rn <= 10   -- 每类目 TOP10
ORDER BY category_name, rn;
```

### 4. 连续活跃用户检测（窗口 + 技巧）

```sql
-- 找出连续活跃>=7天的用户
WITH daily_active AS (
    SELECT DISTINCT user_id, dt FROM events WHERE dt BETWEEN '2024-01-01' AND '2024-01-31'
),
with_next AS (
    SELECT
        user_id, dt,
        LEAD(dt, 1) OVER (PARTITION BY user_id ORDER BY dt) AS next_dt
    FROM daily_active
),
streaks AS (
    SELECT
        user_id, dt,
        DATEDIFF(next_dt, dt) AS gap
    FROM with_next
    WHERE next_dt IS NOT NULL
)
SELECT user_id, MIN(dt) AS streak_start, COUNT(*) + 1 AS consecutive_days
FROM streaks
WHERE gap = 1
GROUP BY user_id
HAVING COUNT(*) + 1 >= 7;
```

## 性能优化（大数据场景）

| 场景 | 诊断 | 解决方案 |
|------|------|---------|
| 大表 JOIN 笛卡尔积 | 结果行数远超预期 | 确认 JOIN 键唯一性，加 DISTINCT 或预聚合 |
| 全表扫描 | WHERE 无分区字段 | 必须带分区字段过滤（`dt = '...'`） |
| 数据倾斜 |个别 reducer 处理数据量是平均10x+ | 加 `DISTRIBUTE BY hash(field)` + `SORT BY` 打散，或加随机前缀 |
| 大 DISTINCT | 只用一个 reducer 去重 | 改用 `GROUP BY col` 去重，或两阶段去重 |
| 嵌套子查询层叠 | 查询计划深、无法下推 | 改用 CTE，逐层物化中间结果 |
| 窗口函数 OOM | 全局窗口未加 PARTITION | 必须按维度 PARTITION，加 `ROWS BETWEEN` 限制窗口 |
| COUNT(DISTINCT) 慢 | 全局去重开销大 | 近似：`APPROX_DISTINCT()`（Presto/Hive），或精确：`GROUP BY + COUNT(*)` |
| JOIN 顺序不当 | 小表驱动大表 | 确保 JOIN 顺序，小表放左，大表放右 |

**大数据黄金规则**：能用 `WHERE dt = '...'` 过滤的，绝不靠 JOIN 过滤；能预聚合的，绝不实时算。

## NULL 处理规范

```sql
-- 聚合中的 NULL：COUNT(DISTINCT col) 会忽略 NULL，SUM/AVG 也会忽略
-- 显式处理
IFNULL(amount, 0)                  -- MySQL
COALESCE(amount, 0)                -- 通用

-- 字符串拼接防 NULL
CONCAT(IFNULL(first_name,''), IFNULL(last_name,''))  -- MySQL
CONCAT_WS('', first_name, last_name)                 -- 自动忽略 NULL

-- JOIN 中 NULL 不匹配
-- LEFT JOIN 时，右表关联键为 NULL 不会匹配，建议用 NVL / IFNULL 预处理
IFNULL(a.user_id, -1) = IFNULL(b.user_id, -1)

-- 分母防零
revenue / NULLIF(order_cnt, 0)
CASE WHEN order_cnt = 0 THEN NULL ELSE revenue / order_cnt END
```
