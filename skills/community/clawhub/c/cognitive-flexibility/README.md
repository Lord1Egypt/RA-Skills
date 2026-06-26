# Cognitive Flexibility Skill

让 AI 像人类一样灵活运用知识的 Skill。

## 安装

```bash
# Skill 已内置，无需额外安装
# 确保在 OpenClaw 环境中使用
```

## 快速开始

### 基本使用

```python
from scripts.cognitive_controller import CognitiveController

# 创建控制器
controller = CognitiveController(confidence_threshold=0.7)

# 执行任务（自动选择模式）
task = "分析用户反馈数据，找出主要问题"
result = await controller.process(task, tools=tools)

print(f"模式：{result['mode']}")
print(f"答案：{result['answer']}")
print(f"置信度：{result['assessment']['overall_score']:.2f}")
```

### 手动选择模式

```python
from scripts.chain_reasoner import OODAReasoner
from scripts.pattern_matcher import PatternMatcher

# OODA 推理模式
reasoner = OODAReasoner()
result = await reasoner.process(task, tools=tools)

# OOA 经验模式
matcher = PatternMatcher()
result = await matcher.match(task, tools=tools)
```

## 运行测试

```bash
cd skills/cognitive-flexibility
python tests\test_cognitive_skills.py
```

## 文档

- [SKILL.md](SKILL.md) - Skill 元数据和使用说明
- [IMPLEMENTATION-REPORT.md](IMPLEMENTATION-REPORT.md) - 实施报告
- [references/ooda-guide.md](references/ooda-guide.md) - OODA 模式使用指南

## 认知模式

| 模式 | 名称 | 适用场景 | 状态 |
|------|------|---------|------|
| **OOA** | 经验模式 | 熟悉场景 | ✅ 已实现 |
| **OODA** | 推理模式 | 复杂问题 | ✅ 已实现 |
| **OOCA** | 创造模式 | 创新需求 | ⏳ 开发中 |
| **OOHA** | 发现模式 | 探索未知 | ⏳ 开发中 |

## 实施进度

- [x] P0: OODA Reasoner 实现
- [x] P0: Pattern Matcher 实现
- [x] P0: Self Assessor 实现
- [x] P1: Cognitive Controller 实现
- [x] P2: 测试用例创建
- [ ] P2: 集成到道子主循环
- [ ] P2: OOCA/OOHA 模式实现

---

_道研出品 · Cognitive Flexibility Skill v1.0_
