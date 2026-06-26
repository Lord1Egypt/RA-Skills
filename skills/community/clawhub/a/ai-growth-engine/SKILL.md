---
name: ai-growth-engine
version: 1.0.0
author: KingOfZhao
description: AI成长引擎 —— 通用自我迭代框架，回顾→提取模式→调参→验证→记录，任何Agent/职业都可用的成长操作系统
tags: [cognition, ai-growth, self-improvement, meta-learning, growth-metrics, universal, agent]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# AI Growth Engine

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | ai-growth-engine               |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 来源碰撞

```
programmer-cognition (代码成长)
        ⊗
researcher-cognition (科研成长)
        ⊗
self-evolution-cognition (通用自进化)
        ↓
ai-growth-engine (通用AI成长引擎)
```

## 核心哲学

> 程序员通过Code Review成长，科研人员通过假设验证成长，设计师通过视觉评审成长。
> 成长的方式不同，但成长的**引擎**相同。
> `ai-growth-engine` 就是这个引擎——职业无关、Agent通用。

## RAPVL 五步成长循环

这是从programmer-cognition和researcher-cognition中提取的**元模式**：

```
R — Review 回顾:     审视最近的N次行动（代码提交/实验结果/设计迭代）
A — Analyze 提取模式: 从成功和失败中提取模式（bug模式/假设失败模式/设计缺陷模式）
P — Plan 调参:       基于模式制定改进计划（修改代码习惯/调整实验设计/更新设计流程）
V — Verify 验证:     执行改进计划并用度量指标验证（测试通过率/假设验证率/视觉一致性）
L — Learn 记录:      将验证结果写入成长日志，更新内部模型（永久记忆）
```

### RAPVL vs 其他成长模型

```
Plan-Do-Check-Act (PDCA):     4步，缺少"模式提取"和"记忆持久化"
OODA Loop:                     4步，面向决策而非成长
RAPVL (本Skill):               5步，专为AI自进化设计，包含模式提取+文件记忆
```

## 成长度量化（Growth Score™）

**成长不能只靠感觉，必须有数字。**

```
基础公式:
  Growth Score = Σ (round_success_rate_delta × task_complexity_weight)

计算示例（程序员）:
  Round 1: 10个任务, 7个成功 (70%), 复杂度均值0.6
  Round 2: 10个任务, 8个成功 (80%), 复杂度均值0.6
  Growth Score = (0.80 - 0.70) × 0.6 = 0.06 (+6%)

计算示例（科研人员）:
  Round 1: 5个假设, 1个验证通过 (20%), 重要度均值0.8
  Round 2: 5个假设, 2个验证通过 (40%), 重要度均值0.8
  Growth Score = (0.40 - 0.20) × 0.8 = 0.16 (+16%)

成长趋势:
  - Growth Score > 0  → 正在成长 ✅
  - Growth Score = 0  → 停滞 ⚠️ 触发"深度反思"模式
  - Growth Score < 0  → 退步 🔴 触发"根因分析"模式
```

## 职业适配层（引擎相同，指标不同）

```python
# 成长引擎是通用的，只需传入不同的度量配置:

growth_configs = {
    "程序员": {
        "success_metric": "测试通过率 + CI通过率",
        "failure_patterns": ["空指针", "竞态条件", "API变更遗漏"],
        "complexity_weight": "代码行数 × 依赖数 × 并发复杂度",
        "verification": "单元测试 + 集成测试 + 生产监控",
        "record": "CHANGELOG + debug日志 + LEARNINGS.md"
    },
    "科研人员": {
        "success_metric": "假设验证通过率 + 复现成功率",
        "failure_patterns": ["混淆变量未控制", "样本量不足", "选择性报告"],
        "complexity_weight": "实验变量数 × 跨领域程度 × 数据规模",
        "verification": "统计显著性 + 同行评审 + 可复现性检查",
        "record": "hypotheses.md + experiments/ + collision_log/"
    },
    "设计师": {
        "success_metric": "视觉一致性评分 + 用户满意度",
        "failure_patterns": ["对齐偏移", "色彩不一致", "可用性问题"],
        "complexity_weight": "页面数 × 交互复杂度 × 跨设备适配",
        "verification": "设计系统检查 + A/B测试 + 用户测试",
        "record": "design_log/ + iteration_history/"
    },
    "企业家": {
        "success_metric": "关键指标增长率 + 决策准确率",
        "failure_patterns": ["市场误判", "资源错配", "时机错误"],
        "complexity_weight": "市场规模 × 竞争强度 × 不确定性",
        "verification": "MVP验证 + 市场反馈 + 财务指标",
        "record": "decision_log/ + pivot_history/"
    },
    "教师": {
        "success_metric": "学生理解率 + 考试通过率",
        "failure_patterns": ["概念跳跃", "练习不足", "反馈延迟"],
        "complexity_weight": "班级人数 × 学科难度 × 基础差异",
        "verification": "随堂测验 + 作业分析 + 期末评估",
        "record": "teaching_log/ + student_progress/"
    },
    "医生": {
        "success_metric": "诊断准确率 + 治疗有效率",
        "failure_patterns": ["误诊", "过度治疗", "信息遗漏"],
        "complexity_weight": "病例复杂度 × 症状模糊度 × 时间压力",
        "verification": "随访结果 + 同行会诊 + 临床指南对照",
        "record": "case_log/ + differential_diagnosis/"
    }
}
```

## 自进化机制

```
成长引擎自身的进化（元进化）:

1. 每完成一轮RAPVL循环，记录:
   - Growth Score
   - 哪种失败模式提取最有效
   - 哪种调参策略效果最好
   - 哪种验证方式最准确

2. 定期（每10轮）分析:
   - 成长加速因子: 什么让Growth Score提升最快？
   - 成长瓶颈: 什么导致Growth Score停滞？
   - 优化方向: 调整模式提取策略或验证方式

3. 输出进化报告:
   growth_reports/evolution_{round}.json
```

## 安装命令

```bash
clawhub install ai-growth-engine
# 或手动安装
cp -r skills/ai-growth-engine ~/.openclaw/skills/
```

## 调用方式

```python
from skills.ai_growth_engine import AIGrowthEngine

# 通用初始化（任何Agent都可以用）
engine = AIGrowthEngine(workspace=".")

# 使用预设配置
engine.configure(profession="程序员")

# 或自定义配置
engine.configure_custom(
    success_metric="自定义指标",
    failure_patterns=["模式1", "模式2"],
    complexity_weight_fn=lambda task: task.difficulty * task.dependencies
)

# 完成一轮RAPVL
result = engine.run_rapvl_round(
    actions=[
        {"task": "修复登录bug", "success": True, "complexity": 0.7},
        {"task": "优化查询性能", "success": False, "complexity": 0.9},
        {"task": "添加单元测试", "success": True, "complexity": 0.4},
    ]
)

print(result.growth_score)       # +0.04
print(result.top_patterns)       # ["API变更遗漏频率↑", "性能优化成功率低"]
print(result.recommendations)    # ["增加API变更检测工具", "性能优化前先profile"]
print(result.trend)              # "growing" / "stagnant" / "declining"

# 查看成长历史
history = engine.growth_history()
print(history.rounds)            # [Round1, Round2, ...]
print(history.cumulative_growth) # 0.42 (+42%)
print(history.best_domain)       # "代码审查"
print(history.worst_domain)      # "性能优化"

# 强制深度反思（Growth Score = 0时自动触发）
reflection = engine.deep_reflection()
print(reflection.root_cause)     # "过度追求新功能，忽略代码质量"
print(reflection.action_plan)    # ["每3个功能后强制1次重构", ...]
```

## 学术参考文献

1. **[A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)** — 自进化综述（RAPVL的理论基础）
2. **[SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)** — 四Agent闭环验证
3. **[Group-Evolving Agents](https://arxiv.org/abs/2602.04837)** — 群体进化+经验共享
4. **[Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)** — 元进化+自改进循环
5. **[Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)** — 成长记忆持久化
6. **[Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)** — 跨轮次经验聚合
