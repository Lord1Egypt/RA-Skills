# 数据质量规则库 (Data Quality Rules Reference)

## 6 大质量维度

### 1. 完整性 (Completeness)

| 规则 | SQL 检查 | 阈值建议 |
|------|----------|----------|
| 主键非空 | `COUNT(*) WHERE pk IS NULL` | = 0 |
| 必填字段非空率 | `SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END) / COUNT(*)` | < 1% |
| 关键维度覆盖 | 事实表的维度外键是否都有对应维度行 | = 100% |

```sql
-- 完整性检查示例
SELECT
    'completeness' AS check_type,
    COUNT(*) AS total,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM dwh.dim_customer;
```

### 2. 唯一性 (Uniqueness)

| 规则 | SQL 检查 | 阈值建议 |
|------|----------|----------|
| 主键唯一 | `COUNT(*) vs COUNT(DISTINCT pk)` | 完全一致 |
| 业务键唯一 | `SELECT bk, COUNT(*) HAVING COUNT(*) > 1` | = 0 |
| 复合键唯一 | `SELECT col1, col2, COUNT(*) HAVING COUNT(*) > 1` | = 0 |

### 3. 有效性 (Validity)

| 规则 | SQL 检查 | 阈值建议 |
|------|----------|----------|
| 数据类型正确 | 日期格式解析、数值可转换 | = 100% |
| 值域范围 | `col BETWEEN min AND max` | > 99% |
| 枚举值合法 | `col IN ('A','B','C')` | = 100% |
| 正则匹配 | `REGEXP_CONTAINS(col, r'pattern')` | > 95% |
| 引用完整性 | `fk NOT IN (SELECT pk FROM dim_table)` | = 0 |

### 4. 一致性 (Consistency)

| 规则 | SQL 检查 | 阈值建议 |
|------|----------|----------|
| 跨表一致性 | 同一实体在不同表中的属性是否一致 | > 99% |
| 汇总一致性 | `SUM(fact.amount) = SUM(agg.amount)` |偏差 < 0.1% |
| 跨系统一致性 | 源系统与数仓记录数对比 |偏差 < 1% |

### 5. 及时性 (Timeliness)

| 规则 | SQL 检查 | 阈值建议 |
|------|----------|----------|
| 数据新鲜度 | `MAX(created_at) vs NOW()` | < SLA 阈值 |
| 管道准时率 | 管道在预定时间窗口内完成的比例 | > 99% |
| 延迟交付 | 数据从源系统到数仓的延迟 | < 1h (核心) |

### 6. 准确性 (Accuracy)

| 规则 | SQL 检查 | 阈值建议 |
|------|----------|----------|
| 统计异常 | Z-Score > 3 的行数占比 | < 1% |
| 金额合理性 | `amount < 0 OR amount > 1000000` | < 0.1% |
| 分布漂移 | 当日分布 vs 前 7 日均值的 KL 散度 | < 0.1 |
| 零值/负值检查 | `amount <= 0` | 视业务而定 |

## Great Expectations 规则速查

```yaml
# 完整性
- expect_column_values_to_not_be_null:
    column: customer_id
    mostly: 0.99

# 唯一性
- expect_column_values_to_be_unique:
    column: order_id

# 值集合
- expect_column_values_to_be_in_set:
    column: status
    value_set: ["active", "inactive", "pending"]

# 范围
- expect_column_values_to_be_between:
    column: age
    min_value: 0
    max_value: 150

# 正则
- expect_column_values_to_match_regex:
    column: email
    regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

# 新鲜度
- expect_column_max_to_be_between:
    column: updated_at
    max_value: "{{ now() }}"
    min_value: "{{ now() - timedelta(days=1) }}"
```

## dbt 测试模板

```yaml
# schema.yml
version: 2
models:
  - name: fact_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customer')
              field: customer_sk
      - name: order_amount
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
```

## 异常检测规则

### 数据量异常
```sql
-- 检测当日数据量是否异常偏离
WITH daily_stats AS (
    SELECT
        DATE(created_at) AS dt,
        COUNT(*) AS row_count
    FROM fact_orders
    WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    GROUP BY dt
),
stats AS (
    SELECT AVG(row_count) AS avg_count, STDDEV(row_count) AS std_count
    FROM daily_stats
    WHERE dt < CURRENT_DATE()
)
SELECT
    d.dt,
    d.row_count,
    s.avg_count,
    (d.row_count - s.avg_count) / NULLIF(s.std_count, 0) AS z_score,
    CASE WHEN ABS((d.row_count - s.avg_count) / NULLIF(s.std_count, 0)) > 3
         THEN 'ANOMALY' ELSE 'NORMAL' END AS status
FROM daily_stats d, stats s
WHERE d.dt = CURRENT_DATE();
```

## 质量阈值建议

| 数据类型 | 完整性 | 唯一性 | 有效性 | 及时性 |
|----------|--------|--------|--------|--------|
| 核心交易数据 | 100% | 100% | 99.9% | 4h |
| 客户主数据 | 99% | 100% | 99% | 8h |
| 行为日志 | 95% | — | 95% | 1h |
| 第三方数据 | 90% | — | 90% | 24h |
| 归档数据 | 98% | 100% | 98% | — |

## 检查清单

- [ ] 每个核心表至少覆盖完整性、唯一性、有效性检查
- [ ] 关键业务指标配置了异常检测
- [ ] 定义了故障升级路径（谁/何时/怎么通知）
- [ ] 质量检查嵌入到 ETL 管道中
- [ ] 定期（每周）审查质量报告和趋势
