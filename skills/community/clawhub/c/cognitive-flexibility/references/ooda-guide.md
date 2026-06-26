# OODA 模式使用指南

## 概述

OODA 循环（Observe-Orient-Decide-Act）是一种知识驱动的推理模式，适用于复杂问题的分析和解决。

## 适用场景

- ✅ 复杂问题分析
- ✅ 多步骤推理任务
- ✅ 需要证据支持的决策
- ✅ 跨领域知识整合

## 不适用场景

- ❌ 简单查询（使用 OOA 经验模式）
- ❌ 创造性任务（使用 OOCA 创造模式）
- ❌ 探索性研究（使用 OOHA 发现模式）

## 使用流程

### 1. 观察（Observe）

检索相关知识和历史经验。

```python
from scripts.chain_reasoner import OODAReasoner

reasoner = OODAReasoner()
observation = await reasoner.observe(task, tools)
```

### 2. 判断（Orient）

分析情境，评估复杂度和约束。

```python
orientation = await reasoner.orient(observation)
```

### 3. 决策（Decide）

制定推理策略。

```python
decision = await reasoner.decide(orientation)
```

### 4. 行动（Act）

执行推理链，生成答案。

```python
result = await reasoner.act(decision, tools)
```

## 完整示例

```python
from scripts.chain_reasoner import OODAReasoner
from scripts.self_assessor import SelfAssessor

# 创建推理器和评估器
reasoner = OODAReasoner(confidence_threshold=0.7)
assessor = SelfAssessor()

# 执行 OODA 推理
task = "分析用户反馈数据，找出主要问题并提出改进建议"
result = await reasoner.process(task, tools=tools)

# 自我评估
assessment = await assessor.evaluate(result)

# 检查是否需要改进
if assessment["needs_improvement"]:
    reflection = await assessor.reflect(result, assessment)
    # 根据反思改进结果
    improved_result = await improve(result, reflection)
```

## 置信度阈值

| 阈值 | 适用场景 |
|------|---------|
| 0.9+ | 高风险决策 |
| 0.7-0.9 | 标准任务（推荐） |
| 0.5-0.7 | 快速响应 |
| <0.5 | 需要人工介入 |

## 最佳实践

1. **充分观察** - 检索足够的历史经验
2. **深度判断** - 分析任务复杂度和约束
3. **明确策略** - 选择合适的推理深度
4. **验证答案** - 通过自我评估确保质量

## 常见问题

### Q: 什么时候切换认知模式？

A: 当 OODA 模式的置信度<0.5 时，考虑切换：
- 相似任务多 → 切换 OOA 经验模式
- 需要创新 → 切换 OOCA 创造模式
- 探索未知 → 切换 OOHA 发现模式

### Q: 如何提高置信度？

A:
1. 检索更多相关知识
2. 增加推理步骤深度
3. 引入外部验证（web_search）
4. 多次迭代改进

---

_道研出品 · OODA 模式指南 v1.0_
