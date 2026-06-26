# 指标计算规则

## 财务指标

| 指标 | 计算公式 |
|------|----------|
| 毛利润 | 收入 - 直接成本 |
| 毛利率 | 毛利润 / 收入 × 100% |
| 净利润 | 收入 - 总成本 |
| 净利率 | 净利润 / 收入 × 100% |

## 运营指标

| 指标 | 计算公式 |
|------|----------|
| DAU | 当日活跃用户数（去重） |
| MAU | 当月活跃用户数（去重） |
| 留存率 | 第 N 日仍活跃用户 / 第 1 日新增用户 |
| 转化率 | 完成目标行为用户数 / 总访问用户数 |
| ARPU | 总收入 / 活跃用户数 |
| 客单价 | GMV / 订单数 |

## 增长指标

```
同比增长率 (YoY) = (本期值 - 去年同期值) / 去年同期值 × 100%
环比增长率 (MoM) = (本期值 - 上期值) / 上期值 × 100%
日环比 (DoD)     = (今日值 - 昨日值) / 昨日值 × 100%
```

## 异常判定规则

| 级别 | 条件 | 标记 |
|------|------|------|
| 严重 | 变化幅度 > 30% | 🔴 |
| 警告 | 变化幅度 10%~30% | 🟡 |
| 正常 | 变化幅度 < 10% | 🟢 |

波动率计算：`abs(当前值 - 基准值) / 基准值`

基准值优先级：7日均值 > 前日值 > 上周同日值

## SQL 示例

```sql
-- 昨日订单数和 GMV
SELECT COUNT(*) AS orders, SUM(amount) AS gmv
FROM orders
WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY;

-- 同比（去年同日）
SELECT COUNT(*) AS orders_yoy
FROM orders
WHERE DATE(created_at) = DATE_SUB(CURDATE() - INTERVAL 1 DAY, INTERVAL 1 YEAR);

-- 7日均值（用于异常基准）
SELECT AVG(daily_orders) AS avg_7d FROM (
  SELECT DATE(created_at) AS d, COUNT(*) AS daily_orders
  FROM orders
  WHERE created_at >= CURDATE() - INTERVAL 8 DAY
    AND created_at < CURDATE() - INTERVAL 1 DAY
  GROUP BY d
) t;
```
