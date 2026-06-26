---
name: "governance-data-quality"
description: "数据质量检查与报告：基于 SQL 或 Pandas 对数据进行批量质量体检，生成健康度报告。"
---

# 数据质量检查与报告 (Data Quality Check & Reporting)

本模块专注于对数据进行**批量质量检查**并**生成质量报告**。与实时监控不同，这里更侧重于定期对全量或分区数据进行“体检”，发现历史遗留问题或系统性缺陷。

## 技术选型建议：SQL vs Pandas

针对“查询量较大”的场景，选择合适的执行策略至关重要：

| 策略 | 适用场景 | 优点 | 缺点 | 建议 |
| :--- | :--- | :--- | :--- | :--- |
| **SQL 下推 (SQL Push-down)** | **大数据量** (千万/亿级)、基础统计指标 | 计算在数据库端完成，网络传输小，速度快 | 复杂逻辑实现困难，消耗数据库 CPU | **推荐首选**，尤其是统计类规则 |
| **Pandas 本地处理** | **小数据量** (万级)、复杂逻辑、跨源校验 | 灵活性极高，支持复杂算法和可视化 | 需拉取全量数据，网络 IO 和内存是瓶颈 | 仅用于小表或**采样后**的分析 |

**最佳实践**：优先使用 **SQL 聚合** 计算指标（如空值率、重复数）；仅在需要深度分析样本分布时，才使用 Pandas 拉取部分数据。

## 质量规则库

定义通用的质量检查规则模板：

| 规则类型 | SQL 模板示例 | 适用场景 |
| :--- | :--- | :--- |
| **完整性 (Completeness)** | `SELECT COUNT(*) FROM {table} WHERE {col} IS NULL` | 检查必填字段 |
| **唯一性 (Uniqueness)** | `SELECT COUNT(*) - COUNT(DISTINCT {col}) FROM {table}` | 检查主键或唯一索引 |
| **准确性 (Accuracy)** | `SELECT COUNT(*) FROM {table} WHERE {col} < 0` | 检查数值范围、枚举值 |
| **一致性 (Consistency)** | `SELECT COUNT(*) FROM {table} WHERE end_time < start_time` | 字段间逻辑校验 |

## 检查流程实施 (SQL 模式)

### 1. 定义检查任务

配置需要检查的表和规则。

```python
dq_tasks = [
    {
        "table": "orders",
        "checks": [
            {"name": "check_null_user", "sql": "SELECT COUNT(*) FROM orders WHERE user_id IS NULL", "desc": "用户ID为空"},
            {"name": "check_neg_amount", "sql": "SELECT COUNT(*) FROM orders WHERE amount < 0", "desc": "金额为负"},
            {"name": "check_duplicate_no", "sql": "SELECT COUNT(*) - COUNT(DISTINCT order_no) FROM orders", "desc": "订单号重复"}
        ]
    }
]
```

### 2. 执行检查并收集指标

使用 `execute_sql` 批量执行，仅获取统计结果。

```python
from toolbox import create_client
import pandas as pd
from datetime import datetime

client = create_client()
def execute_dq_checks(instance_id, db, tasks):
    results = []
    
    for task in tasks:
        table = task['table']
        print(f"正在检查表: {table}...")
        
        # 获取总行数，用于计算错误率
        count_res = execute_sql(client, sql=f"SELECT COUNT(*) as cnt FROM {table}", instance_id=instance_id, database=db)
        total_rows = list(count_res['data']['rows'][0].values())[0] if count_res['success'] else 0
        
        for check in task['checks']:
            # 执行校验 SQL
            res = execute_sql(client, sql=check['sql'], instance_id=instance_id, database=db)
            
            error_count = 0
            if res['success'] and res['data']['rows']:
                # 假设 SQL 返回的第一列就是错误行数
                error_count = list(res['data']['rows'][0].values())[0]
            
            results.append({
                "Check Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Table": table,
                "Rule Name": check['name'],
                "Description": check['desc'],
                "Total Rows": total_rows,
                "Error Rows": error_count,
                "Error Rate": f"{(error_count/total_rows*100):.2f}%" if total_rows > 0 else "0.00%",
                "Status": "PASS" if error_count == 0 else "FAIL"
            })
            
    return pd.DataFrame(results)

# 执行
df_report = execute_dq_checks("inst-xxx", "order_db", dq_tasks)
```

### 3. 生成质量报告

利用 Pandas 将结果格式化为 Markdown 或 HTML 报告。

```python
def generate_report(df_report):
    # 统计概览
    total_checks = len(df_report)
    failed_checks = len(df_report[df_report['Status'] == 'FAIL'])
    score = 100 - (failed_checks / total_checks * 100) if total_checks > 0 else 100
    
    print(f"=== 数据质量体检报告 ===")
    print(f"综合得分: {score:.1f}")
    print(f"检查项总数: {total_checks}")
    print(f"发现问题项: {failed_checks}")
    print("\n=== 详细问题清单 ===")
    
    # 仅打印失败的项
    failures = df_report[df_report['Status'] == 'FAIL']
    if not failures.empty:
        print(failures[['Table', 'Description', 'Error Rows', 'Error Rate']].to_markdown(index=False))
    else:
        print("🎉 完美！未发现数据质量问题。")

# 生成报告
generate_report(df_report)
```

## 报告输出示例

```text
=== 数据质量体检报告 ===
综合得分: 66.7
检查项总数: 3
发现问题项: 1

=== 详细问题清单 ===
| Table  | Description | Error Rows | Error Rate |
|:-------|:------------|:-----------|:-----------|
| orders | 订单号重复   | 5          | 0.05%      |
```
