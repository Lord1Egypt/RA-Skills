---
name: autogen-multi-agent
description: |-
  AutoGen v0.4：asyncio actor-runtime 多智能体框架（autogen-core / autogen-agentchat / autogen-ext 三包）。
  AutoGen v0.4: asyncio actor-runtime multi-agent framework (autogen-core / autogen-agentchat / autogen-ext). ⚠️ Microsoft has declared maintenance mode; new projects should use Microsoft Agent Framework (MAF). This skill is for legacy maintenance only.
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-136"
  blueprint_source: "microsoft/autogen"
  blueprint_commit: "027ecf0a379bcc1d09956d46d12d44a3ad9cee14"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/autogen-multi-agent"
  openclaw:
    skillKey: autogen-multi-agent
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

⚠️ **重要提示**：AutoGen v0.4 已进入微软官方维护模式（README:14,21,23），新项目应使用 Microsoft Agent Framework（MAF）。本 skill 仅服务于既有 AutoGen 工程的维护、迁移与排错。

AutoGen 是 asyncio actor-runtime 多智能体框架（github.com/microsoft/autogen）。三个 Python 包：autogen-core（runtime + 基础接口）、autogen-agentchat（高层 AssistantAgent / GroupChat API）、autogen-...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/autogen-multi-agent

## 知识规模

- **51 条约束** (2 fatal + 49 non-fatal)
- 上游源码: `microsoft/autogen` @ commit `027ecf0a`
- 蓝图 ID: `finance-bp-136`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
主要适合既有 AutoGen 工程的维护团队：排错、迁移到 MAF、向后兼容性补丁。新项目不建议从 AutoGen 起步——用 Microsoft Agent Framework（MAF）。如确需 AutoGen 范式，本 skill 覆盖 actor runtime / GroupChat / Magentic-One 等典型用例。

### 需要准备什么环境？依赖什么？
Python 3.10+（按包元数据），至少一个 ChatCompletionClient provider（共 9 个：openai / anthropic / azure_openai / azure_ai / ollama / llama_cpp / semantic_kernel / cached / replay；OpenAI 是事实标准）。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 51 条约束（2 条 fatal）。CRITICAL 安全坑：(1) LocalCommandLineCodeExecutor 文档声称的 regex 命令消毒**并不存在**——所有 LLM 生成的命令直接 shell 执行到 host；(2) pyautogen 包现已是 0 字节代理，v0.2 cookbook 代码会三处失败；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/autogen-multi-agent
