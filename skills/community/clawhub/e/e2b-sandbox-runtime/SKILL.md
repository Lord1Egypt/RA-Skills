---
name: e2b-sandbox-runtime
description: |-
  E2B：在隔离 micro-VM 里执行 AI 生成代码的云端 runtime。Python / TS SDK 通过 Connect-RPC 调用 envd 守护进程（Rust + protobuf）。
  E2B: cloud-side runtime for executing AI-generated code in isolated micro-VMs. Python and TypeScript SDKs are pure RPC clients over Connect-RPC against an envd daemon (Rust + protobuf).
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-141"
  blueprint_source: "e2b-dev/E2B"
  blueprint_commit: "557b723cc12f48af6c3657518a0b326b46ebff6d"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/e2b-sandbox-runtime"
  openclaw:
    skillKey: e2b-sandbox-runtime
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

E2B 是在隔离 micro-VM 里执行 AI 生成代码的云端 runtime（github.com/e2b-dev/E2B）。Python / TypeScript SDK 是纯 RPC 客户端，通过 Connect-RPC 对接 envd 守护进程（Rust + protobuf，托管在独立的 e2b-dev/infra repo）。

SDK 接口为 2x2：{Sandbox, AsyncSandbox} × {Template, AsyncTemplate}。Sandbox / AsyncSandbox 各带四个子模块作为实例属性：files: Filesystem / comman...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/e2b-sandbox-runtime

## 知识规模

- **42 条约束** (3 fatal + 39 non-fatal)
- 上游源码: `e2b-dev/E2B` @ commit `557b723c`
- 蓝图 ID: `finance-bp-141`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合需要让 LLM 安全执行任意代码的工程师：AI 助手跑 Python / shell、数据分析 sandbox、教学环境。每个 sandbox 是隔离 micro-VM，泄露面限制在单个 sandbox 内。Jupyter 内核 / 富输出场景应改用 e2b-code-interpreter。访问 doramagic.ai/r/e2b 查看完整用例。

### 需要准备什么环境？依赖什么？
Python 3.9+ 或 Node 18+。`E2B_API_KEY` 给 SDK runtime（创建 / 控制 sandbox）；`E2B_ACCESS_TOKEN` 给 CLI 鉴权（template build / dashboard）。可选 `E2B_DOMAIN`（默认 e2b.app）。出站 HTTPS 到 *.e2b.app。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 42 条约束（3 条 fatal）。典型踩坑：(1) TS 用户忘 kill()——TS Sandbox 没有 Symbol.dispose 也没自动清理，sandbox 持续计费到超时；(2) 通过 envs={...} 传 API key 会被 commands.list() 泄露给持有 sandbox 句柄的人；

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/e2b-sandbox-runtime
