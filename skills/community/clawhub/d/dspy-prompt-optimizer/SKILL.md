---
name: dspy-prompt-optimizer
description: |-
  DSPy：把 LLM 程序写成可组合 Module + 声明式 Signature 的 Python 框架。通过 14 个 teleprompter（optimizer）从 train + dev 集自动编译 prompt 与 few-shot demo。
  DSPy: a Python framework for building LLM programs as composable Modules with declarative Signatures. 14 teleprompter (optimizer) classes auto-compile prompts and few-shot demos from train + dev sets. LM access is unified via LiteLLM; 2-tier cache (LRU + diskcache).
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-137"
  blueprint_source: "stanfordnlp/dspy"
  blueprint_commit: "da4ae1941d551fdc09d7d1bfbb6f7c01b96063a8"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/dspy-prompt-optimizer"
  openclaw:
    skillKey: dspy-prompt-optimizer
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

DSPy 是把 LLM 程序写成可组合 Module + 声明式 Signature 的 Python 框架（github.com/stanfordnlp/dspy）。可插拔 Adapter 格式化消息和解析响应；LM 客户端层包装 LiteLLM 提供统一 provider 访问；14 个 teleprompter （optimizer）类从 train + dev 集自动编译 prompt 和 few-shot demo。

下层是 2 层缓存（LRUCache 内存 + diskcache FanoutCache 磁盘）和 3 层遥测（Settings.trace、Module.hist...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/dspy-prompt-optimizer

## 知识规模

- **44 条约束** (8 fatal + 36 non-fatal)
- 上游源码: `stanfordnlp/dspy` @ commit `da4ae194`
- 蓝图 ID: `finance-bp-137`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要把 LLM 流水线工程化的研究员和工程师：用 Signature 替代手写prompt、用 teleprompter（如 MIPROv2、BootstrapFewShot）从数据自动优化 prompt + few-shot。覆盖 RAG / agent / 分类 / 抽取等用例。访问 doramagic.ai/r/dspy 查看完整说明。

### 需要准备什么环境？依赖什么？
Python 3.10+，至少一个 LM provider 通过 LiteLLM 访问（默认接受 'provider/model' 字符串如 'openai/gpt-4o-mini'）；可写磁盘用于 ~/.dspy_cache（或 DSPY_CACHEDIR 覆盖）。MIPROv2 离散搜索可选 optuna（懒加载）；asyncify 可选 anyio。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 44 条约束（8 条 fatal）。CRITICAL 安全坑：(1) 默认 Cache(restrict_pickle=False) + diskcache pickle.load 在被污染的 ~/.dspy_cache shard 上 = RCE，无用户 opt-in；(2) MIPROv2 估算 LM 调用数但不在超预算时中止（静默失控成本）；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/dspy-prompt-optimizer
