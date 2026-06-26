---
name: crewai-multi-agent
description: |-
  CrewAI 多智能体框架：role-goal-backstory 声明智能体，sequential / hierarchical 双流程，ReAct 与 OpenAI native function-calling 双 tool 循环，统一 Memory + 5 个原生 LLM provider + Lit
  CrewAI multi-agent framework: role-goal-backstory agent declaration, sequential / hierarchical execution processes, dual tool-call loops (ReAct + OpenAI native function-calling), unified Memory layer, 5 native LLM providers + LiteLLM fallback.
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-134"
  blueprint_source: "joaomdmoura/crewAI"
  blueprint_commit: "cb46a1c4babef8c51db6499d7a81f2c36b01bdef"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/crewai-multi-agent"
  openclaw:
    skillKey: crewai-multi-agent
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

CrewAI 是构建多智能体 LLM 应用的 Python 框架（github.com/joaomdmoura/crewAI）。核心特征：role-goal-backstory 智能体声明，两种执行流程（sequential / hierarchical 含 auto- 或自定义 manager），双 tool-call 循环（ReAct 文本解析 vs OpenAI 原生 function-calling，运行时特征探测选择），统一 Memory 层（Memory + MemorySlice + RecallFlow，自适应深度召回），可插拔 LLM provider 路由（5 个原生 SD...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/crewai-multi-agent

## 知识规模

- **56 条约束** (5 fatal + 51 non-fatal)
- 上游源码: `joaomdmoura/crewAI` @ commit `cb46a1c4`
- 蓝图 ID: `finance-bp-134`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要多 agent 协作完成复杂任务的工程师：研究 + 写作 + 校对、数据采集 + 分析 + 报告、销售线索挖掘 + 跟进等。两种流程满足不同需求：sequential 适合明确流水线，hierarchical 适合需要 manager 调度的开放任务。访问 doramagic.ai/r/crewai 查看完整用例。

### 需要准备什么环境？依赖什么？
Python（版本见 pyproject.toml），至少一个 LLM provider（Memory 默认 OpenAI gpt-4o-mini；Crew agent 各自挑 llm）。Memory 启用时默认 OpenAIEmbeddingFunction 嵌入 + lancedb 向量库。如需走非原生 SDK 模型，安装 LiteLLM。空气墙 / 数据驻留场景必须 ENV 关闭遥测。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 56 条约束（5 条 fatal）。典型踩坑：(1) aggregate_raw_outputs_from_task_outputs 无 token cap，长任务链溢出 LLM 上下文；(2) tool 重复使用检测只比 last_used_tool，A→B→A→B 振荡漏检；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/crewai-multi-agent
