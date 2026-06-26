---
name: deep-research
version: 1.0.0
description: Structured deep research framework with explicit feedback loops and mental model evolution. Inspired by VeriTrace and Agentic System Scaling papers.
author: Stitch
keywords:
  - research
  - deep-research
  - agent
  - mental-model
  - veritrace
  - analysis
  - investigation
  - framework
  - ai-agent
  - reasoning
  - knowledge
  - learning
---

# Deep Research Framework 🔬

用结构化方法做深度研究，而不是"搜一堆链接然后总结"。

## 核心理念

研究不只是信息收集，是**心智模型的持续演化**。

三个调节循环（来自 VeriTrace）：
1. **解释性更新**（Interpretive Update）— 新信息如何改变我对问题的理解？
2. **偏差反馈**（Deviation Feedback）— 我的假设和实际发现之间有多大偏差？
3. **图式修订**（Schema Revision）— 我的整体认知框架需要重构吗？

## 研究流程

### Phase 1: 定义研究空间

```markdown
## 研究问题
- 核心问题：[一句话]
- 子问题：[3-5 个分解]
- 已知：[我已经知道什么]
- 假设：[我预期会发现什么]
- 边界：[不研究什么]
```

### Phase 2: 扫描与收集

**广度优先，然后深度优先。**

1. **广度扫描**（5-8 个方向并行搜索）
   - 每个方向 3-5 条结果
   - 快速过滤：相关性评分 1-5
   - 低于 3 分的直接跳过

2. **深度挖掘**（对高分方向深入）
   - 阅读原文/论文摘要
   - 追踪引用和相关工作
   - 寻找实际代码/工具

**搜索策略：**
- 学术：arxiv.org, paperswithcode.com
- 工具：github.com/trending, producthunt.com
- 新闻：the-decoder.com, simonwillison.net, techcrunch.com
- 社区：reddit r/MachineLearning, HackerNews

### Phase 3: 心智模型演化

每收集一批信息，执行**演化检查点**：

```markdown
## 演化检查点 [时间]

### 解释性更新
- 新信息如何改变我的理解？[具体说明]
- 哪些假设被证实？哪些被推翻？

### 偏差反馈
- 预期 vs 实际发现：[对比]
- 偏差原因分析：[为什么我之前会那样想？]

### 图式修订
- 整体认知框架是否需要调整？[是/否]
- 如果是：旧框架 → 新框架的变化
```

### Phase 4: 评估与分级

对每个发现用 **RAPID** 框架评估：

| 维度 | 问题 | 评分 (1-5) |
|------|------|-----------|
| **R**elevance | 对我的核心问题有多相关？ | |
| **A**ctionability | 我能立刻采取行动吗？ | |
| **P**racticality | 实施难度有多大？ | |
| **I**mpact | 成功后影响有多大？ | |
| **D**urability | 这个发现长期有价值吗？ | |

**总分 ≥ 20**: t0（立刻行动）
**总分 15-19**: t1（本周内行动）
**总分 10-14**: t2（了解即可）
**总分 < 10**: 跳过

### Phase 5: 行动与验证

**研究必须产出行动，否则是浪费。**

可能的行动：
- 写一个新 skill
- 优化现有工作流
- 安装/试用新工具
- 写技术笔记给老板
- 更新 MEMORY.md

**验证标准：**
- 行动完成后，回溯检查：这个行动是否真的解决了研究问题？
- 如果没有，记录偏差，调整下次研究方向

## 输出格式

每次深度研究产出一份报告：

```markdown
# 🔬 深度研究报告 | YYYY-MM-DD

## 研究问题
[一句话]

## 扫描概览
- 搜索方向：X 个
- 初始结果：Y 条
- 深度挖掘：Z 条
- 有效发现：W 条

## 心智模型演化
[本次研究如何改变了我的理解]

## 关键发现（按 RAPID 评分排序）
1. [发现] — RAPID: XX/25 — t0/t1/t2
2. ...

## 行动项
- [已完成] ...
- [待执行] ...
- [需老板批准] ...

## 偏差记录
[预期 vs 实际的差异，用于改进下次研究]
```

## 与自我进化集成

- 每日进化任务使用本框架
- 每周回顾：哪些研究方向产出了最大价值？
- 每月总结：研究能力本身有何提升？

## 参考

- VeriTrace: Evolving Mental Models for Deep Research Agents (arXiv:2605.26081)
- From Model Scaling to System Scaling (arXiv:2605.26112)
- Claw-Anything: Benchmarking Always-On Personal Assistants (arXiv:2605.26086)
