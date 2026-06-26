---
name: browser-use-agent
description: |-
  Browser-Use：把 LLM 变成网页操作员的异步 Python 库（Python 3.11+）。Agent 步循环采集 DOM + 截图 → LLM 一次调用产出 thinking / evaluation / next_goal / action[] → 经 CDP 执行。
  Browser-Use: an async Python library (3.11+) that turns an LLM into a web operator. The Agent loop collects DOM + screenshot, makes one LLM call emitting thinking / evaluation / next_goal / action[], and executes via CDP. Built on cdp-use; no Playwright.
license: MIT-0
compatibility: AI engineering knowledge skill — host AI consumes seed.yaml directly. No installation required.
metadata:
  version: "v0.1.0"
  blueprint_id: "finance-bp-133"
  blueprint_source: "browser-use/browser-use"
  blueprint_commit: "f3878b0e074a53119defe6cbc625687a1343ba8e"
  category: ai-engineering
  doramagic_url: "https://doramagic.ai/zh/crystal/browser-use-agent"
  openclaw:
    skillKey: browser-use-agent
    category: ai-engineering
    primaryEnv: knowledge
---
# 这个 skill 适合什么用户？能做哪些任务？

## 概览

Browser-Use 是把 LLM 变成网页操作员的异步 Python 库（github.com/browser-use/browser-use）。Agent 步循环：(1) 通过 14 个 watchdog 围绕 bubus.EventBus 采集 BrowserStateSummary（带数字索引的 DOM、截图、tab 列表、页面状态）；(2) 一次 LLM 调用同时产出 thinking + evaluation_previous_goal + memory + next_goal + action[]；(3) 经 CDP 原语在双层 page-change 守卫下执行动作。

CD...

**Doramagic 晶体页**: https://doramagic.ai/zh/crystal/browser-use-agent

## 知识规模

- **40 条约束** (4 fatal + 36 non-fatal)
- 上游源码: `browser-use/browser-use` @ commit `f3878b0e`
- 蓝图 ID: `finance-bp-133`

## 用法

Host AI（Claude Code / Cursor / OpenClaw）读 `references/seed.yaml`，按其中的：
- `intent_router` 匹配用户意图
- `architecture` 理解项目架构
- `constraints` 应用 anti-pattern 约束
- `business_decisions` 参考核心设计决策

## FAQ 摘要

### 这个 skill 适合什么用户？能做哪些任务？
适合做网页自动化的工程师：表单填写、信息抓取、回归测试、跨站点数据采集等。Agent 把视觉理解 + 操作规划合并到一次 LLM 调用，比传统 Playwright 脚本更适合非确定性页面。访问 doramagic.ai/r/browser-use 查看完整用例。

### 需要准备什么环境？依赖什么？
Python 3.11+，Chromium 系浏览器（local_browser_watchdog 自动启动或通过 cdp_url 接管），至少一个 LLM provider 配置（默认 ChatBrowserUse项目自家微调模型）。要求 async event loop——Agent / BrowserSession 接口是 async-native。

### 会踩哪些坑？这个 skill 怎么防护？
本 skill 内置 40 条约束（4 条 fatal）。典型踩坑：(1) alert/confirm/beforeunload 自动接受，破坏性确认（如 'Delete this'）也会通过；(2) Agent(sensitive_data=...) 不配 Browser(allowed_domains=[...]) 是 fail-OPEN（只 warning 不 raise），合规场景必须显式

---

完整文档: 见 `references/seed.yaml` (v6.1 schema). 浏览页: https://doramagic.ai/zh/crystal/browser-use-agent
