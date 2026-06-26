---
name: business-rule-engine
version: 1.0.0
description: |
  轻量级业务规则引擎，支持规则定义、规则执行、规则链编排和动态规则加载。
  Lightweight business rule engine supporting rule definition, execution, chain orchestration and dynamic rule loading.
---

# Business Rule Engine | 业务规则引擎

灵活的业务规则管理解决方案，支持复杂的业务逻辑编排和执行。

A flexible business rule management solution supporting complex business logic orchestration and execution.

## 核心功能 | Core Features

- 📋 **规则定义** | Rule Definition - 声明式规则定义语法
- ⚡ **规则执行** | Rule Execution - 高性能规则执行引擎
- 🔗 **规则链** | Rule Chain - 支持规则链编排
- 🔄 **动态加载** | Dynamic Loading - 运行时动态加载规则
- 📊 **规则评估** | Rule Evaluation - 条件表达式和动作执行
- 🧩 **可扩展** | Extensible - 插件式规则扩展

## 快速开始 | Quick Start

### Python API

```python
from business_rule_engine import RuleEngine, Rule

# 创建规则引擎 | Create rule engine
engine = RuleEngine()

# 定义规则 | Define rule
rule = Rule(
    name="discount_rule",
    condition="order_amount > 100 and vip_level >= 2",
    action={"type": "apply_discount", "value": 0.9}
)

# 添加规则 | Add rule
engine.add_rule(rule)

# 执行规则 | Execute rule
result = engine.evaluate({
    "order_amount": 200,
    "vip_level": 3
})
```

## 测试 | Tests

```bash
python -m pytest tests/ -v
```
