# Business Rule Engine | 业务规则引擎

<p align="center">
  ⚡ Lightweight business rule engine for dynamic logic execution
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>
## English

### Overview

Business Rule Engine is a lightweight, flexible solution for managing and executing business rules. It supports declarative rule definition, rule chains, dynamic loading, and extensible rule evaluation.

### Installation

```bash
pip install -r requirements.txt
```

### Features

| Feature | Description |
|---------|-------------|
| Rule Definition | Declarative rule definition syntax |
| Rule Execution | High-performance rule execution engine |
| Rule Chain | Orchestrate multiple rules in sequence |
| Dynamic Loading | Load rules at runtime |
| Rule Evaluation | Complex condition expressions and actions |
| Extensibility | Plugin-based rule extensions |

### Quick Start

```python
from business_rule_engine import RuleEngine, Rule

# Create rule engine
engine = RuleEngine()

# Define a simple rule
rule = Rule(
    name="senior_discount",
    condition="age >= 60",
    action={"type": "discount", "value": 0.8}
)

# Add rule to engine
engine.add_rule(rule)

# Evaluate data against rules
result = engine.evaluate({"age": 65, "order_total": 100})
print(result)  # {'senior_discount': {'matched': True, 'action': {'type': 'discount', 'value': 0.8}}}
```

### Rule Chain Example

```python
from business_rule_engine import RuleChain

# Create rule chain
chain = RuleChain()

# Add rules in sequence
chain.add_rule(Rule("check_inventory", "stock > 0"))
chain.add_rule(Rule("apply_discount", "is_member == True"))
chain.add_rule(Rule("calculate_total", "price * quantity"))

# Execute chain
context = {"stock": 10, "is_member": True, "price": 50, "quantity": 2}
result = chain.execute(context)
```

### JSON Rule Definition

```python
import json

# Define rules in JSON
rules_json = '''
[
    {
        "name": "vip_discount",
        "condition": "vip_level >= 3 and order_amount > 500",
        "action": {"type": "discount", "value": 0.7}
    },
    {
        "name": "new_user_bonus",
        "condition": "is_new_user == True",
        "action": {"type": "bonus", "value": 50}
    }
]
'''

# Load rules from JSON
engine = RuleEngine()
engine.load_rules_from_json(rules_json)

# Evaluate
result = engine.evaluate({
    "vip_level": 4,
    "order_amount": 600,
    "is_new_user": False
})
```

---

<a name="中文"></a>
## 中文

### 概述

业务规则引擎是一个轻量级、灵活的解决方案，用于管理和执行业务规则。支持声明式规则定义、规则链、动态加载和可扩展的规则评估。

### 安装

```bash
pip install -r requirements.txt
```

### 功能特性

| 特性 | 说明 |
|------|------|
| 规则定义 | 声明式规则定义语法 |
| 规则执行 | 高性能规则执行引擎 |
| 规则链 | 顺序编排多个规则 |
| 动态加载 | 运行时加载规则 |
| 规则评估 | 复杂条件表达式和动作执行 |
| 可扩展性 | 插件式规则扩展 |

### 快速开始

```python
from business_rule_engine import RuleEngine, Rule

# 创建规则引擎
engine = RuleEngine()

# 定义简单规则
rule = Rule(
    name="senior_discount",
    condition="age >= 60",
    action={"type": "discount", "value": 0.8}
)

# 添加规则到引擎
engine.add_rule(rule)

# 评估数据
result = engine.evaluate({"age": 65, "order_total": 100})
print(result)  # {'senior_discount': {'matched': True, 'action': {'type': 'discount', 'value': 0.8}}}
```

### 规则链示例

```python
from business_rule_engine import RuleChain

# 创建规则链
chain = RuleChain()

# 顺序添加规则
chain.add_rule(Rule("check_inventory", "stock > 0"))
chain.add_rule(Rule("apply_discount", "is_member == True"))
chain.add_rule(Rule("calculate_total", "price * quantity"))

# 执行规则链
context = {"stock": 10, "is_member": True, "price": 50, "quantity": 2}
result = chain.execute(context)
```

### JSON规则定义

```python
import json

# 用JSON定义规则
rules_json = '''
[
    {
        "name": "vip_discount",
        "condition": "vip_level >= 3 and order_amount > 500",
        "action": {"type": "discount", "value": 0.7}
    },
    {
        "name": "new_user_bonus",
        "condition": "is_new_user == True",
        "action": {"type": "bonus", "value": 50}
    }
]
'''

# 从JSON加载规则
engine = RuleEngine()
engine.load_rules_from_json(rules_json)

# 评估
result = engine.evaluate({
    "vip_level": 4,
    "order_amount": 600,
    "is_new_user": False
})
```

## 测试 | Testing

```bash
python -m pytest tests/test_rule_engine.py -v
```

## 许可证 | License

MIT License
