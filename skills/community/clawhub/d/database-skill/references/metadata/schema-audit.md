---
name: "governance-schema-audit"
description: "库表规范性审计：自动化检查数据库表结构设计规范，如主键、命名、注释、类型等。"
---

# 库表规范性审计 (Schema Standardization Audit)

库表规范性审计通过自动化规则，检查数据库表结构设计是否符合最佳实践和公司规范，旨在提升数据质量、可维护性和性能。

## 审计目标

1.  **规范一致性**：强制命名规范（如：表名全小写、下划线分隔）。
2.  **性能保障**：确保表有主键，索引设计合理。
3.  **可理解性**：确保表和字段有完整的注释。
4.  **数据安全**：避免使用不安全的数据类型或字符集。

## 审计规则库

### 1. 命名规范 (Naming Convention)

-   **表名/字段名**：
    -   必须使用小写字母、数字、下划线。
    -   不能以数字开头。
    -   长度限制（如：MySQL 表名 <= 64 字符）。
    -   禁止使用保留字（如 `order`, `group`, `user`）。

### 2. 结构规范 (Structural Rules)

-   **主键检查**：每张表必须有显式定义的主键 (`PRIMARY KEY`)。
-   **存储引擎**：强制使用 InnoDB。
-   **字符集**：推荐使用 `utf8mb4`。
-   **外键**：生产环境通常禁用外键约束，建议逻辑外键。

### 3. 文档规范 (Documentation Rules)

-   **表注释**：表必须有业务含义注释。
-   **字段注释**：字段注释覆盖率需达到 100%。

### 4. 类型规范 (Data Type Rules)

-   **布尔值**：推荐使用 `TINYINT(1)` 或 `BOOLEAN`。
-   **浮点数**：涉及金额必须使用 `DECIMAL`，禁止 `FLOAT/DOUBLE`。
-   **大字段**：尽量避免使用 `TEXT/BLOB`，如必须使用需单独存储。

## 审计实施流程

### 第一步：获取表结构

使用 `get_table_info` API 获取表的详细定义。

```python
from toolbox import create_client
client = create_client()

# 示例：获取表结构
res = get_table_info(client,
    instance_id="inst-xxx",
    database="order_db",
    table="t_order_main"
)

if res['success']:
    table_info = res['data']
    print(f"正在审计表: {table_info['name']}")
    columns = table_info.get('columns', [])
```

### 第二步：执行规则检查

编写 Python 函数对 `table_info` 进行规则校验。

```python
def audit_table(table_info):
    issues = []
    table_name = table_info.get('name', '')
    columns = table_info.get('columns', [])
    
    # 规则 1: 检查表名规范
    if not table_name.islower():
        issues.append(f"[命名规范] 表名 {table_name} 包含大写字母")
        
    # 规则 2: 检查是否有主键
    has_pk = any(col.get('is_primary_key', False) for col in columns)
    if not has_pk:
        issues.append(f"[结构规范] 表 {table_name} 缺少主键")
        
    # 规则 3: 检查字段注释
    for col in columns:
        if not col.get('comment'):
            issues.append(f"[文档规范] 字段 {col['name']} 缺少注释")
            
    return issues

# 执行审计
issues = audit_table(table_info)
if issues:
    print("发现问题:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("审计通过")
```

## 审计报告

审计结果应生成报告，并通知相关负责人整改。

**报告模板示例**：

| 表名 | 问题级别 | 问题描述 | 建议修复方案 |
| :--- | :--- | :--- | :--- |
| `UserOrders` | High | 表名包含大写字母 | 修改为 `user_orders` |
| `t_log` | High | 缺少主键 | 添加自增主键 `id` |
| `status` | Medium | 缺少注释 | 添加注释 "订单状态: 0-未支付, 1-已支付" |

## 自动化集成

可以将此审计脚本集成到：
1.  **CI/CD 流水线**：SQL 变更前自动检查。
2.  **每日巡检任务**：定期扫描全量库表，生成日报。
