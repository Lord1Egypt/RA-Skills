---
name: "governance-data-profiling"
description: "数据探查：自动化分析数据分布、统计特征、空值率等，帮助理解数据内容和质量。"
---

# 数据探查 (Data Profiling)

数据探查是对现有数据进行统计分析和结构化审查的过程。通过自动化探查，可以快速了解数据的分布特征、值域范围和潜在问题，为数据清洗和建模提供依据。

## 探查目标

1.  **数据分布分析**：了解数值型字段的极值、均值，枚举型字段的分布。
2.  **结构一致性**：验证数据是否符合预期的格式（如日期格式、邮箱格式）。
3.  **异常发现**：识别离群值（Outliers）和不符合业务逻辑的数据。

## 核心指标

| 指标类型 | 具体指标 | 适用字段类型 | 业务含义 |
| :--- | :--- | :--- | :--- |
| **基础统计** | 行数 (Count), 空值率 (Null%) | 所有 | 数据完整性概览 |
| **基数分析** | 唯一值数 (Cardinality), 唯一值率 | 字符串, ID | 识别主键或枚举字段 |
| **数值分布** | Min, Max, Avg, Median, StdDev | 数值型 | 了解业务规模和波动 |
| **枚举分布** | Top N 值及占比 | 类别型 | 了解业务构成（如各城市订单占比） |
| **长度分析** | 最大/最小/平均长度 | 字符串 | 优化存储空间定义 |

## 自动化探查流程

### 1. 单表探查 (Single Table Profiling)

针对单张表，生成全字段的探查报告。

```python
from toolbox import create_client
import pandas as pd

client = create_client()
def profile_table(instance_id, db, table):
    # 1. 获取表结构
    schema = get_table_info(client, instance_id=instance_id, database=db, table=table)
    if not schema['success']:
        return
        
    columns = schema['data']['columns']
    
    # 2. 构建探查 SQL
    # 为了性能，建议使用采样或分批查询，这里演示全量聚合
    selects = ["COUNT(*) as total_rows"]
    for col in columns:
        col_name = col['name']
        col_type = col['type'].lower()
        
        # 基础统计：空值数
        selects.append(f"COUNT(CASE WHEN {col_name} IS NULL THEN 1 END) as {col_name}_nulls")
        # 基数统计：唯一值数
        selects.append(f"COUNT(DISTINCT {col_name}) as {col_name}_distinct")
        
        # 数值型特定统计
        if any(t in col_type for t in ['int', 'decimal', 'float', 'double']):
            selects.append(f"MAX({col_name}) as {col_name}_max")
            selects.append(f"MIN({col_name}) as {col_name}_min")
            selects.append(f"AVG({col_name}) as {col_name}_avg")
            
    sql = f"SELECT {', '.join(selects)} FROM {table}"
    
    # 3. 执行查询
    res = execute_sql(client, sql=sql, instance_id=instance_id, database=db)
    if res['success']:
        return res['data']['rows'][0]
```

### 2. 深度探查 (Deep Profiling)

对于关键字段，进行更深入的频率分布分析。

**示例：统计用户所在城市分布**

```python
sql = """
SELECT city, COUNT(*) as cnt, COUNT(*)*100.0/(SELECT COUNT(*) FROM users) as pct
FROM users
GROUP BY city
ORDER BY cnt DESC
LIMIT 20
"""
res = execute_sql(client, sql=sql, instance_id="inst-xxx", database="user_db")
```

## 探查报告应用

1.  **元数据增强**：将探查出的“最大长度”、“枚举值列表”回写到元数据管理系统。
2.  **开发辅助**：开发人员在写 SQL 前，先查看探查报告，避免因数据倾斜导致的性能问题。
3.  **存储优化**：发现定义了 `VARCHAR(1000)` 但实际最大长度仅 20 的字段，建议缩减。
