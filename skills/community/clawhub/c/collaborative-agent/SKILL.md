---
name: collaborative-agent
description: ARC多智能体协作：规划/执行/审查/总结/研究/批评，迭代评审
compatibility: opencode
metadata:
  private: true
---
# Skill: collaborative-agent

# ARC 式多智能体协作框架

## 归属管理
- 归属核心：`think-expand`（想核心）
- 上级负责：复杂决策任务由think-expand分解后委托协作框架执行

## 功能范围
- 多角色协作：规划者/执行者/审查者/总结者/研究者/批评者
- 迭代式同行评审：产出→评审→反馈→优化
- 任务分解：复杂任务自动拆分为子任务
- 依赖管理：子任务按依赖顺序执行
- 结果综合：多步结果整合为结构化报告

## 原理
源自 ARC (AutoResearchClaw 2026) 研究：
- 多智能体同行评审协作
- 自我强化循环
- 集成已有能力：ScriptDB / VSAEngine / SkillEvolver / CognitiveReasoner

## 用法

```python
import sys; sys.path.insert(0, r'D:\coze-local\db')
from collaborative_agent import ARCWorkflow, AgentRole

# 创建协作工作流
wf = ARCWorkflow()

# 添加任务（自动分配角色）
wf.add_task("研究Transformer优化方案", role="researcher")
wf.add_task("制定实现计划", role="planner", depends_on=[0])
wf.add_task("实现并测试", role="executor", depends_on=[1])
wf.add_task("审查代码质量", role="reviewer", depends_on=[2])
wf.add_task("生成总结报告", role="summarizer", depends_on=[3])

# 执行所有任务
results = wf.run_all()

# 获取最终报告
report = wf.get_report()
```

## 触发场景
- 复杂问题需要分步骤处理（规划→执行→审查→总结）
- 需要多角度分析的研究任务
- 需要质量审查的代码/内容生成
- 需要从多来源综合信息的任务

## 集成
- 内部自动调用 `capability_executor.detect_and_execute()` 执行已注册能力
- 使用 `CognitiveReasoner` 提供语言/数值反馈
- 使用 `SkillEvolver` 记录失败并进化

Base directory: file:///C:/Users/pc/.config/opencode/skills/collaborative-agent


## B站学习
> 学习时间: 2026-06-01 20:57

- **安逸Ai丶**: Agent中为什么需要 tracing 和 observability？
  - 关键词: Agent中为什么需要, tracing, observability
- **银色海豚KK**: OpenClaw v2026.5.28 更新快报 | ClawPDF Claude Opus 4.8 Agent协作
  - 关键词: OpenClaw, v2026, 28, 更新快报, ClawPDF

## B站学习
> 学习时间: 2026-06-01 21:01

- **安逸Ai丶**: Agent中为什么需要 tracing 和 observability？
- **银色海豚KK**: OpenClaw v2026.5.28 更新快报 | ClawPDF Claude Opus 4.8 Agent协作
- **智能体老王**: AI给自己写工具？字节团队出品 MUSE-Autoskill 让Agent实现技能自进化，推动skills成为可复用的知识资产

## 融合来源: collaborative-agent-1fe479
> 融合时间: 自动合并

> 学习时间: 2026-06-01 21:07
- **WJ_UPC**: 20221216_王钧_Advances in Collaborative Neurodynamic Optimization
- **树欲静心不止**: 250908- Coding Agent实战心得：从工具到伙伴的协作之道 / Coding Agent Mastery: Collaborative Devel
- **UncleScto**: 3D LMI Gocator with HANWHA collaborative robot
> 融合时间: 自动合并
> 学习时间: 2026-06-02 07:52
- **dailyrain**: 3GC Collaborative and Creative Content Generation in Game Design
- **dailyrain**: 3GC Collaborative and Creative Content Generation in Game Design
- **Tracy春雪**: The Teachers&#x27; Room - Collaborative Writing 1 - Planning

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:20

- **安逸Ai丶**: Agent中为什么需要 tracing 和 observability？
  https://www.bilibili.com/video/BV1BwVd6xEd8
- **AIlazy俊**: 66K 星的 Caveman：让 Agent 少废话，还能省 tokens
  https://www.bilibili.com/video/BV1hdV96rEiV
- **智能体老王**: AI给自己写工具？字节团队出品 MUSE-Autoskill 让Agent实现技能自进化，推动skills成为可复用的知识资产
  https://www.bilibili.com/video/BV1QPVf6QEF1

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:33

- **安逸Ai丶**: Agent中为什么需要 tracing 和 observability？
  https://www.bilibili.com/video/BV1BwVd6xEd8
- **AIlazy俊**: 66K 星的 Caveman：让 Agent 少废话，还能省 tokens
  https://www.bilibili.com/video/BV1hdV96rEiV
- **智能体老王**: AI给自己写工具？字节团队出品 MUSE-Autoskill 让Agent实现技能自进化，推动skills成为可复用的知识资产
  https://www.bilibili.com/video/BV1QPVf6QEF1
