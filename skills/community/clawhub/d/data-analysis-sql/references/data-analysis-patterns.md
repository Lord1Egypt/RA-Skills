# 高级数据分析模式

## 1. 留存分析（Cohort 留存 & 行为留存）

```sql
-- 留存率矩阵（Cohort 表）
WITH install AS (
    SELECT user_id, DATE(create_time) AS install_date
    FROM dim_user
    WHERE create_time >= '2024-01-01' AND create_time < '2024-02-01'
),
activity AS (
    SELECT user_id, DATE(event_time) AS act_date
    FROM dwd_user_event_detail
    WHERE dt >= '2024-01-01' AND dt <= '2024-02-28'
),
retention_matrix AS (
    SELECT
        i.install_date AS cohort_date,
        DATEDIFF(a.act_date, i.install_date) AS retention_day,
        COUNT(DISTINCT i.user_id) AS cohort_size,
        COUNT(DISTINCT a.user_id) AS retained_users
    FROM install i
    LEFT JOIN activity a ON i.user_id = a.user_id
    GROUP BY i.install_date, DATEDIFF(a.act_date, i.install_date)
)
SELECT
    cohort_date,
    cohort_size,
    -- 各留存天数
    MAX(CASE WHEN retention_day = 0  THEN retained_users END) AS d0,
    MAX(CASE WHEN retention_day = 1  THEN retained_users END) AS d1,
    MAX(CASE WHEN retention_day = 3  THEN retained_users END) AS d3,
    MAX(CASE WHEN retention_day = 7  THEN retained_users END) AS d7,
    MAX(CASE WHEN retention_day = 14 THEN retained_users END) AS d14,
    MAX(CASE WHEN retention_day = 30 THEN retained_users END) AS d30,
    -- 留存率
    ROUND(MAX(CASE WHEN retention_day = 1  THEN retained_users END) * 100.0
          / NULLIF(cohort_size, 0), 2) AS retention_d1,
    ROUND(MAX(CASE WHEN retention_day = 7  THEN retained_users END) * 100.0
          / NULLIF(cohort_size, 0), 2) AS retention_d7
FROM retention_matrix
GROUP BY cohort_date, cohort_size
ORDER BY cohort_date;
```

## 2. 漏斗分析（含自定义窗口）

```sql
-- 行为漏斗（限定 7 天窗口内的转化路径）
WITH user_funnel AS (
    SELECT
        user_id,
        MIN(CASE WHEN event = 'page_view'    THEN event_time END) AS t1_view,
        MIN(CASE WHEN event = 'product_detail'THEN event_time END) AS t2_detail,
        MIN(CASE WHEN event = 'add_cart'       THEN event_time END) AS t3_cart,
        MIN(CASE WHEN event = 'create_order'  THEN event_time END) AS t4_order,
        MIN(CASE WHEN event = 'payment'       THEN event_time END) AS t5_pay
    FROM dwd_user_event_detail
    WHERE dt BETWEEN '${bizdate_start}' AND '${bizdate_end}'
    GROUP BY user_id
),
funnel_steps AS (
    SELECT
        user_id,
        CASE WHEN t1_view IS NOT NULL          THEN 1 ELSE 0 END AS step1,
        CASE WHEN t1_view IS NOT NULL AND t2_detail IS NOT NULL
             AND DATEDIFF(t2_detail, t1_view) <= 7 THEN 1 ELSE 0 END AS step2,
        CASE WHEN t2_detail IS NOT NULL AND t3_cart IS NOT NULL
             AND DATEDIFF(t3_cart, t2_detail) <= 7 THEN 1 ELSE 0 END AS step3,
        CASE WHEN t3_cart IS NOT NULL AND t4_order IS NOT NULL
             AND DATEDIFF(t4_order, t3_cart) <= 7 THEN 1 ELSE 0 END AS step4,
        CASE WHEN t4_order IS NOT NULL AND t5_pay IS NOT NULL
             AND DATEDIFF(t5_pay, t4_order) <= 7 THEN 1 ELSE 0 END AS step5
    FROM user_funnel
)
SELECT
    COUNT(*) AS total_users,
    SUM(step1) AS step1_cnt,   ROUND(SUM(step1) * 100.0 / NULLIF(COUNT(*), 0), 2) AS step1_rate,
    SUM(step2) AS step2_cnt,   ROUND(SUM(step2) * 100.0 / NULLIF(SUM(step1), 0), 2) AS step2_rate,
    SUM(step3) AS step3_cnt,   ROUND(SUM(step3) * 100.0 / NULLIF(SUM(step2), 0), 2) AS step3_rate,
    SUM(step4) AS step4_cnt,   ROUND(SUM(step4) * 100.0 / NULLIF(SUM(step3), 0), 2) AS step4_rate,
    SUM(step5) AS step5_cnt,   ROUND(SUM(step5) * 100.0 / NULLIF(SUM(step4), 0), 2) AS step5_rate,
    -- 总体转化
    ROUND(SUM(step5) * 100.0 / NULLIF(COUNT(*), 0), 2) AS overall_cvr
FROM funnel_steps;
```

## 3. 同期群分析（Revenue Cohort）

```sql
-- 按用户首次付费月份分组，看后续每月 ARPPU 趋势
WITH first_pay AS (
    SELECT
        user_id,
        DATE(MIN(paid_time)) AS first_pay_month
    FROM dwd_order_detail
    WHERE paid_time IS NOT NULL
    GROUP BY user_id
),
monthly_revenue AS (
    SELECT
        fp.user_id,
        fp.first_pay_month,
        DATE_TRUNC('month', o.paid_time) AS pay_month,
        DATEDIFF(DATE_TRUNC('month', o.paid_time), fp.first_pay_month) AS month_offset,
        SUM(o.pay_amount) AS month_revenue
    FROM first_pay fp
    INNER JOIN dwd_order_detail o ON fp.user_id = o.user_id
    WHERE o.status IN ('paid', 'completed')
    GROUP BY fp.user_id, fp.first_pay_month, DATE_TRUNC('month', o.paid_time)
)
SELECT
    first_pay_month,
    COUNT(DISTINCT user_id) AS cohort_size,
    SUM(month_revenue) AS total_revenue,
    SUM(month_revenue) / NULLIF(COUNT(DISTINCT user_id), 0) AS arppu,
    -- M0-M3 ARPPU 趋势
    MAX(CASE WHEN month_offset = 0 THEN month_revenue / NULLIF(COUNT(DISTINCT user_id), 0) END) AS m0_arppu,
    MAX(CASE WHEN month_offset = 1 THEN month_revenue / NULLIF(COUNT(DISTINCT user_id), 0) END) AS m1_arppu,
    MAX(CASE WHEN month_offset = 2 THEN month_revenue / NULLIF(COUNT(DISTINCT user_id), 0) END) AS m2_arppu
FROM monthly_revenue
GROUP BY first_pay_month
ORDER BY first_pay_month;
```

## 4. RFM 用户分层

```sql
WITH rfm_base AS (
    SELECT
        user_id,
        MAX(order_time)                                       AS last_order_time,
        DATEDIFF(CURRENT_DATE, MAX(order_time))               AS recency,  -- 越近越好
        COUNT(DISTINCT order_id)                              AS frequency,
        SUM(pay_amount)                                       AS monetary
    FROM dwd_order_detail
    WHERE status IN ('paid', 'completed')
    GROUP BY user_id
),
rfm_scores AS (
    SELECT
        user_id,
        recency, frequency, monetary,
        -- 分位数打分（1-5分）
        NTILE(5) OVER (ORDER BY recency DESC)   AS r_score,  -- 近的 R 高
        NTILE(5) OVER (ORDER BY frequency)      AS f_score,
        NTILE(5) OVER (ORDER BY monetary)       AS m_score
    FROM rfm_base
)
SELECT
    user_id,
    recency, frequency, monetary,
    r_score, f_score, m_score,
    r_score + f_score + m_score AS rfm_sum,
    CONCAT(r_score, f_score, m_score) AS rfm_tag,
    -- 人群标签
    CASE
        WHEN r_score = 5 AND f_score >= 4 THEN '重要价值用户'
        WHEN r_score >= 4 AND monetary >= 4 THEN '重要发展用户'
        WHEN r_score <= 2 AND f_score >= 3 THEN '重要保持用户'
        WHEN r_score <= 2 AND f_score <= 2 THEN '重要挽留用户'
        WHEN r_score >= 4 AND f_score <= 2 THEN '一般价值用户'
        ELSE '一般用户'
    END AS user_segment
FROM rfm_scores;
```

## 5. 路径分析（Session 切分 & 行为序列）

```sql
-- 按会话窗口切分用户行为序列
WITH events_with_session AS (
    SELECT
        user_id,
        event_time,
        event_name,
        -- 超过30分钟无行为则开新 session
        SUM(CASE WHEN DATEDIFF(event_time, LAG(event_time) OVER w) > 30 OR LAG(event_time) OVER w IS NULL
                 THEN 1 ELSE 0 END) OVER w AS session_flag
    FROM dwd_user_event_detail
    WHERE dt = '${bizdate}'
    WINDOW w AS (PARTITION BY user_id ORDER BY event_time)
),
session_grouped AS (
    SELECT
        user_id,
        SUM(session_flag) OVER (ORDER BY event_time) AS session_id,
        COLLECT_LIST(event_name) AS event_sequence  -- 行为序列数组
    FROM events_with_session
    GROUP BY user_id, event_time, session_flag
)
SELECT
    session_id,
    COUNT(DISTINCT user_id)          AS user_cnt,
    COUNT(*)                          AS event_cnt,
    -- 序列中出现最多的前3个路径
    MODE(ARRAY_JOIN(event_sequence, '->')) AS top_path
FROM session_grouped
GROUP BY session_id
ORDER BY user_cnt DESC;
```

## 6. 指标波动检测（同比/环比异常）

```sql
-- 监控核心指标日波动，超阈值告警
WITH daily_metrics AS (
    SELECT
        dt,
        platform,
        SUM(gmv)                              AS gmv,
        SUM(order_cnt)                        AS order_cnt,
        COUNT(DISTINCT buyer_uid)             AS dau
    FROM dws_trade_indicators_daily
    GROUP BY dt, platform
),
with_lags AS (
    SELECT
        dt, platform, gmv, order_cnt, dau,
        LAG(gmv, 7) OVER (PARTITION BY platform ORDER BY dt) AS gmv_d7,
        LAG(gmv, 1) OVER (PARTITION BY platform ORDER BY dt) AS gmv_d1,
        LAG(gmv, 30) OVER (PARTITION BY platform ORDER BY dt) AS gmv_d30,
        LAG(dau, 7) OVER (PARTITION BY platform ORDER BY dt) AS dau_d7
    FROM daily_metrics
)
SELECT
    dt, platform,
    gmv, gmv_d7, dau, dau_d7,
    -- 环比
    ROUND((gmv - gmv_d1) * 100.0 / NULLIF(gmv_d1, 0), 2) AS mom_pct,
    -- 周同比
    ROUND((gmv - gmv_d7) * 100.0 / NULLIF(gmv_d7, 0), 2) AS wow_pct,
    -- DAU 周同比
    ROUND((dau - dau_d7) * 100.0 / NULLIF(dau_d7, 0), 2) AS dau_wow_pct,
    -- 异常标记（波动超过阈值）
    CASE
        WHEN ABS((gmv - gmv_d7) / NULLIF(gmv_d7, 0)) > 0.20 THEN '⚠️ GMV异常'
        WHEN ABS((dau - dau_d7) / NULLIF(dau_d7, 0)) > 0.15 THEN '⚠️ DAU异常'
        ELSE '✅ 正常'
    END AS alert_flag
FROM with_lags
WHERE dt = CURRENT_DATE - 1
ORDER BY ABS((gmv - gmv_d7) / NULLIF(gmv_d7, 0)) DESC;
```

## 7. 数据分布分析（分位数 & 异常值）

```sql
-- 客单价分布 + 异常值检测
SELECT
    -- 分位数
    PERCENTILE_CONT(0.01) WITHIN GROUP (ORDER BY pay_amount) AS p1,
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY pay_amount) AS p10,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY pay_amount) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY pay_amount) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY pay_amount) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY pay_amount) AS p90,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY pay_amount) AS p99,
    -- 统计
    AVG(pay_amount)      AS avg_amount,
    STDDEV(pay_amount)  AS stddev_amount,
    -- 异常值（均值 ± 3倍标准差之外）
    SUM(CASE WHEN pay_amount < AVG(pay_amount) - 3 * STDDEV(pay_amount)
                  OR pay_amount > AVG(pay_amount) + 3 * STDDEV(pay_amount)
             THEN 1 ELSE 0 END) AS outlier_cnt,
    -- 异常占比
    ROUND(SUM(CASE WHEN pay_amount < AVG(pay_amount) - 3 * STDDEV(pay_amount)
                        OR pay_amount > AVG(pay_amount) + 3 * STDDEV(pay_amount)
                   THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS outlier_pct
FROM dwd_order_detail
WHERE dt = '${bizdate}'
  AND status IN ('paid', 'completed');
```

## 8. 渐变维（Slowly Changing Dimension, SCD）

```sql
-- SCD Type 2：用户地址历史变更（保留全量历史）
INSERT OVERWRITE TABLE dwd_user_address_hub PARTITION(dt = '${bizdate}')
SELECT
    user_id,
    address,
    start_dt,                           -- 生效开始日期
    CASE WHEN next_dt IS NULL THEN '9999-12-31' ELSE DATE_SUB(next_dt, 1) END AS end_dt,
    -- 当前版本标记
    CASE WHEN next_dt IS NULL THEN 1 ELSE 0 END AS is_current
FROM (
    SELECT
        user_id,
        address,
        start_dt,
        LEAD(start_dt) OVER (PARTITION BY user_id ORDER BY start_dt) AS next_dt
    FROM (
        SELECT user_id, address, MIN(start_dt) AS start_dt
        FROM ods_user_address_raw
        WHERE dt = '${bizdate}'
        GROUP BY user_id, address
    ) t
) final;

-- 查询用户历史地址（某时间点的快照）
SELECT user_id, address, start_dt, end_dt
FROM dwd_user_address_hub
WHERE user_id = '12345'
  AND '${snapshot_date}' BETWEEN start_dt AND end_dt
ORDER BY start_dt;
```
