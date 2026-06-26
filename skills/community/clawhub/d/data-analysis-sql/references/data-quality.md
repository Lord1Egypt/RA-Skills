# 数据质量检测与监控

## 质量维度

| 维度 | 含义 | 监控指标 |
|------|------|---------|
| **完整性** | 数据是否缺失 | 空值率、记录缺失率、主键重复率 |
| **准确性** | 数据值是否正确 | 枚举值分布、超出合理范围值、偏离度 |
| **一致性** | 多表/多系统数据是否一致 | 跨表核验、业务逻辑冲突 |
| **及时性** | 数据是否按时产出 | 任务完成时间、数据延迟 |
| **唯一性** | 主键/业务键是否重复 | 重复率 |
| **有效性** | 数据格式是否符合规范 | 格式校验、正则匹配 |

## 端到端探查流程

```
Step 1: 数据量核查     → COUNT(*) 对比昨日/上周同期，差异超过阈值告警
Step 2: 空值率检测     → 每列空值率，超过 50% 告警（业务允许除外）
Step 3: 主键唯一性     → COUNT(*) vs COUNT(DISTINCT pk)，重复率>0 则告警
Step 4: 枚举值分布     → 每列枚举值占比，极端偏斜告警
Step 5: 数值合理性     → 超出 min/max/avg±3σ 范围的值占比
Step 6: 跨表核验       → 事实表 SUM 与维度表 COUNT 交叉核验
Step 7: 日期连续性     → 分区字段是否连续，缺失分区告警
```

## 核心监控 SQL 模板

### 1. 数据量 & 空值率检测

```sql
-- ODS 层每日空值率监控
SELECT
    '${bizdate}' AS bizdate,
    '${table_name}' AS table_name,
    COUNT(*) AS total_rows,
    -- 核心字段空值率
    ROUND(SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS order_id_null_pct,
    ROUND(SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS user_id_null_pct,
    ROUND(SUM(CASE WHEN order_amount IS NULL THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS order_amount_null_pct,
    ROUND(SUM(CASE WHEN order_status IS NULL THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS order_status_null_pct,
    -- 金额合理范围
    ROUND(SUM(CASE WHEN order_amount < 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS negative_amount_pct,
    ROUND(SUM(CASE WHEN order_amount > 999999 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 4) AS extreme_amount_pct
FROM ${ods_table}
WHERE dt = '${bizdate}';
```

### 2. 主键唯一性检测

```sql
-- 主键重复率检测
SELECT
    '${bizdate}' AS bizdate,
    'dwd_order_detail' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_order_cnt,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_rows,
    ROUND((COUNT(*) - COUNT(DISTINCT order_id)) * 100.0 / NULLIF(COUNT(*), 0), 4) AS duplicate_rate_pct,
    CASE
        WHEN COUNT(*) - COUNT(DISTINCT order_id) > 0 THEN '⚠️ 主键重复'
        ELSE '✅ 正常'
    END AS alert_flag
FROM dwd_order_detail
WHERE dt = '${bizdate}';
```

### 3. 枚举值 & 异常分布检测

```sql
-- 订单状态分布 + 异常状态检测
SELECT
    '${bizdate}' AS bizdate,
    order_status,
    COUNT(*) AS cnt,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct,
    -- 异常标记
    CASE
        WHEN order_status NOT IN ('pending','paid','shipped','completed','cancelled','refunded')
        THEN '⚠️ 非法枚举值'
        ELSE '✅ 正常'
    END AS flag
FROM dwd_order_detail
WHERE dt = '${bizdate}'
GROUP BY order_status
ORDER BY cnt DESC;
```

### 4. 核心指标波动告警

```sql
-- 核心指标日环比/周同比监控
WITH metrics AS (
    SELECT
        dt,
        SUM(order_cnt)         AS order_cnt,
        SUM(gmv)              AS gmv,
        SUM(pay_amount)       AS revenue,
        COUNT(DISTINCT user_id) AS buyer_cnt
    FROM dws_trade_metrics_daily
    WHERE dt >= DATE_SUB('${bizdate}', 7)
    GROUP BY dt
),
with_lag AS (
    SELECT
        dt,
        order_cnt, gmv, revenue, buyer_cnt,
        LAG(order_cnt, 1) OVER (ORDER BY dt) AS order_cnt_d1,
        LAG(gmv, 7)      OVER (ORDER BY dt) AS gmv_d7,
        LAG(buyer_cnt, 7) OVER (ORDER BY dt) AS buyer_cnt_d7
    FROM metrics
)
SELECT
    dt,
    order_cnt, order_cnt_d1,
    ROUND((order_cnt - order_cnt_d1) * 100.0 / NULLIF(order_cnt_d1, 0), 2) AS mom_pct,
    ROUND((gmv - gmv_d7) * 100.0 / NULLIF(gmv_d7, 0), 2) AS wow_pct,
    CASE
        WHEN ABS((gmv - gmv_d7) / NULLIF(gmv_d7, 0)) > 0.30 THEN '🔴 GMV异常（波动>30%）'
        WHEN ABS((buyer_cnt - buyer_cnt_d7) / NULLIF(buyer_cnt_d7, 0)) > 0.20 THEN '🟡 DAU异常（波动>20%）'
        ELSE '✅ 正常'
    END AS alert_flag
FROM with_lag
WHERE dt = '${bizdate}';
```

### 5. 分区完整性检测

```sql
-- 检查最近7天分区是否完整
WITH date_series AS (
    SELECT DATE_SUB('${bizdate}', n) AS dt
    FROM (
        SELECT EXPLODE(SEQUENCE(0, 6)) AS n
    ) t
)
SELECT
    d.dt,
    CASE WHEN t.cnt IS NOT NULL AND t.cnt > 0 THEN '✅ 有数据'
         WHEN t.cnt = 0 THEN '⚠️ 空分区'
         ELSE '🔴 分区缺失' END AS partition_status,
    t.cnt AS row_count
FROM date_series d
LEFT JOIN (
    SELECT dt, COUNT(*) AS cnt
    FROM ods_order_detail
    WHERE dt BETWEEN DATE_SUB('${bizdate}', 6) AND '${bizdate}'
    GROUP BY dt
) t ON d.dt = t.dt
ORDER BY d.dt;
```

### 6. 跨表核验（数据一致性）

```sql
-- ODS → DWD 数据一致性：订单数、金额应完全一致
SELECT
    '${bizdate}' AS bizdate,
    'ods_vs_dwd' AS check_scope,
    'order_cnt' AS metric,
    SUM(a.cnt) AS ods_cnt,
    SUM(b.cnt) AS dwd_cnt,
    SUM(a.cnt) - SUM(b.cnt) AS diff,
    CASE WHEN SUM(a.cnt) - SUM(b.cnt) = 0 THEN '✅ 一致' ELSE '🔴 不一致' END AS flag
FROM (
    SELECT COUNT(*) AS cnt FROM ods_order_detail WHERE dt = '${bizdate}'
) a
CROSS JOIN (
    SELECT COUNT(*) AS cnt FROM dwd_order_detail WHERE dt = '${bizdate}'
) b;
```

## 数据质量告警规则配置

| 告警级别 | 触发条件 | 处理 |
|---------|---------|------|
| 🔴 P0 阻塞 | 核心指标波动 > 30%，或主键重复率 > 0% | 立刻停止下游任务，查因修复 |
| 🟡 P1 警告 | 空值率 > 5%，或枚举值出现未知值 | 发告警，DT 排查，业务确认 |
| 🟢 P2 提示 | 数据量较上周同期波动 > 10% | 记录，观察是否持续 |
