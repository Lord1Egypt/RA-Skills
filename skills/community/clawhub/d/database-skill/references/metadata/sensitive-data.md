---
name: "governance-sensitive-data"
description: "敏感数据识别与分级：自动化扫描库表，识别 PII 和金融数据，进行数据分级打标。"
---

# 敏感数据识别与分级 (Sensitive Data Identification & Classification)

在数据治理中，保护敏感数据是合规和安全的核心要求。本模块通过自动化手段，识别数据库中的敏感信息，并对其进行分类分级。

## 目标

1.  **自动识别**：发现存储在数据库中的敏感字段（如手机号、身份证、密码）。
2.  **分级分类**：根据敏感程度，将数据分为 L1~L4 等级。
3.  **合规落地**：为数据脱敏、加密提供元数据支撑。

## 数据分级标准 (示例)

| 等级 | 描述 | 示例 | 保护要求 |
| :--- | :--- | :--- | :--- |
| **L4 (绝密)** | 泄露导致严重影响 | 密钥、生物特征、密码明文 | 加密存储，严格审计 |
| **L3 (机密)** | 泄露导致较大影响 | 身份证号、银行卡号、手机号 | 脱敏展示，访问审批 |
| **L2 (内部)** | 仅限内部使用 | 员工姓名、部门、职位 | 内部公开，外部保密 |
| **L1 (公开)** | 可对外公开 | 产品信息、公告 | 无特殊限制 |

## 识别方法

### 1. 关键词匹配 (Keyword Matching)

基于字段名 (`column_name`) 和字段注释 (`comment`) 进行正则匹配。

**常用正则规则**：

-   **手机号**: `(phone|mobile|telephone|contact|sj|tel)`
-   **身份证**: `(id_card|identity|id_no|cert_no|sfz)`
-   **邮箱**: `(email|mail|mailbox)`
-   **银行卡**: `(card_no|bank_card|credit_card)`
-   **密码**: `(password|pwd|pass|secret|token|key)`
-   **地址**: `(address|addr|location|gps)`

### 2. 数据采样 (Data Sampling)

如果元数据匹配不准确，可通过 `execute_sql` 对数据进行采样分析（需谨慎操作，仅限只读权限）。

**采样逻辑**：
1.  `SELECT distinct col FROM table LIMIT 100`
2.  对采样数据应用正则校验（如：符合 11 位数字且以 1 开头可能是手机号）。

## 实施流程

### 第一步：获取字段元数据

遍历所有表，获取字段信息。

```python
from toolbox import create_client
import re

client = create_client()
columns = [
    {'name': 'user_phone', 'comment': '用户手机号'},
    {'name': 'password_hash', 'comment': '加密密码'},
    {'name': 'order_id', 'comment': '订单ID'},
]
```

### 第二步：执行敏感识别

编写 Python 函数进行匹配。

```python
SENSITIVE_RULES = {
    'L3': [
        r'phone|mobile|tel',       # 手机号
        r'id_card|identity|sfz',   # 身份证
        r'email|mail',             # 邮箱
        r'bank|credit',            # 银行卡
    ],
    'L4': [
        r'password|pwd|secret',    # 密码/密钥
    ]
}

def classify_column(col_name, col_comment):
    text = f"{col_name} {col_comment}".lower()
    
    # 优先匹配高等级
    for level in ['L4', 'L3']:
        for rule in SENSITIVE_RULES[level]:
            if re.search(rule, text):
                return level, rule
                
    return 'L1', None

# 执行识别
for col in columns:
    level, rule = classify_column(col['name'], col['comment'])
    if level != 'L1':
        print(f"发现敏感字段: {col['name']} ({col['comment']}) -> 等级: {level}, 命中规则: {rule}")
```

### 第三步：输出分级清单

生成敏感数据资产目录，包含：
-   实例/库/表名
-   字段名
-   敏感等级
-   数据类型
-   命中规则

## 后续治理动作

1.  **数据脱敏**：对 L3/L4 级字段，在查询结果中自动脱敏（如：`138****0000`）。
2.  **加密存储**：对 L4 级字段，建议在应用层或数据库层加密存储。
3.  **权限控制**：限制对高敏感等级字段的 `SELECT` 权限。
