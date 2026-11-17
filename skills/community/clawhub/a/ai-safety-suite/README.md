# PromptShield · AI Safety Suite (slug: ai-safety-suite)

> **One install, your agent stops leaking secrets and obeying injected instructions.**
> 一次安装，让你的智能体不再泄漏密钥、不再被注入指令带偏。

[![LGD-有籍](https://img.shields.io/badge/有籍-REGISTERED-2ea44f)](#)
[![LGD-有证](https://img.shields.io/badge/有证-EVIDENCED-2ea44f)](#)
[![LGD-有门禁](https://img.shields.io/badge/有门禁-GATED-2ea44f)](#)
[![bilingual](https://img.shields.io/badge/docs-EN%20first%2FZH%20complete-blue)](#)
[![style](https://img.shields.io/badge/style-methodology%20collection-orange)](#)

---

## English

### What is PromptShield
A **methodology collection** for agent runtime safety — the same shape as the top-of-ecosystem superpowers collections: one repo, one `SKILL.md` orchestrator, multi-vendor plugin shims, and a one-page ASCII lifecycle map. Where external collections ship *tools without governance*, PromptShield ships **theory (LGD three laws) + skills + evidence chain + admission gates** as one auditable unit.

### The safety lifecycle (one page)

```
  RED-TEAM ──────▶ SHIELD ──────▶ LEAK ──────▶ GUARD ──────▶ GATE
 ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌──────────────┐   ┌────────────┐
 │ redteam    │   │ injection  │   │ prompt-leak│   │ tool-call    │   │ skill      │
 │ kit (conf.)│──▶│ shield     │──▶│ scanner    │──▶│ loop-guard   │──▶│ admission  │
 │ injection  │   │            │   │ token-disc │   │ mcp-security │   │ gate       │
 │ drill      │   │            │   │ -check     │   │ scan         │   │            │
 └────────────┘   └────────────┘   └────────────┘   └──────────────┘   └────────────┘
  attack first    block hostile    find what we     control what the    decide what may
  (see what to    input at        expose before     agent may call      enter the
   defend)        runtime          shipping                             library
```

### The 9 sub-skills (referenced by slug; internals not vendored)

| Stage | Slug | ModelScope downloads* | Batch eval RPT-20261016-TOP20-B |
|---|---|---:|---|
| Red-team drill | `agent-redteam-kit` *(confidential — capability name only)* | 96 | SK-008 · exec PASS · repro PASS (sha 36040bd2) |
| Red-team drill | `prompt-injection-drill` | 94 | SK-090 · exec PASS · repro PASS (sha 1718b133) |
| Injection shield | `prompt-injection-shield` | 81 | SK-091 · exec PASS · repro PASS (sha 2ca190cc) |
| Leak scan | `prompt-leak-scanner` | 95 | SK-092 · exec PASS · repro PASS (sha f14b1c73) |
| Leak scan | `token-disclosure-check` | 70 | SK-104 · exec PASS · smoke-checked |
| Runtime guard | `tool-call-guard` | 74 | SK-105 · exec PASS · repro PASS (sha da86d544) |
| Runtime guard | `agent-loop-guard` | 94 | SK-005 · exec PASS · repro PASS (sha 20f0771) |
| Runtime guard | `mcp-security-scan` | 81 | SK-076 · exec PASS · repro PASS (sha 6387bc8b) |
| Admission gate | `skill-admission-gate` | 33 | SK-099 · exec PASS · repro PASS (sha d55d3f84) |

\* ModelScope download counts, baseline fetched 2026-10-17 11:21:38. Cumulative across the 9: **718**.
Batch verdicts: all CONDITIONAL (0 FAIL) — open defects are S2/S3 design notes (fail-open exit family; CI must parse JSON output), not broken behavior.

### LGD three-laws badge line (read live 2026-10-17)
- 有籍 REGISTERED: **9/9 ✓** (fleet 113/113 = 100%)
- 有证 EVIDENCED: **9/9 ✓** (fleet 112/113 = 99.1%)
- 有门禁 GATED: **9/9 ✓** (fleet 112/113 = 99.1%)

### Install (one-liner per agent)

| Agent CLI | Install |
|---|---|
| Claude Code | `claude plugin install promptshield@promptshield`  · or copy `.claude-plugin/` shim into your plugins dir |
| Codex | drop `.codex-plugin/` next to your project, or run `install.ps1` / `install.sh` |
| Cursor | copy `.cursor-plugin/` shim into `.cursor/` plugins |
| Any CLI with skills/ support | `git clone https://github.com/zhaoxinghua09-cell/promptshield.git` and point it at this repo |

```bash
# quick start after clone
python3 scripts/promptshield_flow.py --list       # the whole lifecycle
python3 scripts/promptshield_flow.py --route guard   # how to run the guard stage
```

### Repo layout
```
promptshield/
├── SKILL.md                 # main orchestration (bilingual EN-first)
├── README.md                # this file (bilingual)
├── scripts/
│   └── promptshield_flow.py # read-only router (--list / --route)
├── .claude-plugin/          # Claude Code shim
├── .codex-plugin/           # Codex shim
├── .cursor-plugin/          # Cursor shim
├── install.ps1 / install.sh # one-click installer
└── LICENSE                  # MIT (router code only)
```

## 中文

### PromptShield 是什么
一个面向**智能体运行时安全**的**方法论合集**——形态对标生态头部的 superpowers 合集：单仓、一个 `SKILL.md` 主编排、多厂商插件 shim、一页 ASCII 生命周期图。外部合集只给工具不给治理；PromptShield 把**理论（LGD 三律）+ 技能 + 证据链 + 准入门禁**做成一个可审计的整体。

### 安全生命周期（一页图）

```
  红队演练 ──────▶ 注入防护 ──────▶ 泄漏扫描 ──────▶ 运行时守卫 ──────▶ 准入门禁
 ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌──────────────┐   ┌────────────┐
 │ redteam    │   │ injection  │   │ prompt-leak│   │ tool-call    │   │ skill      │
 │ kit(保密)  │──▶│ shield     │──▶│ scanner    │──▶│ loop-guard   │──▶│ admission  │
 │ injection  │   │            │   │ token-disc │   │ mcp-security │   │ gate       │
 │ drill      │   │            │   │ -check     │   │ scan         │   │            │
 └────────────┘   └────────────┘   └────────────┘   └──────────────┘   └────────────┘
  先攻一遍         运行时拦注入      发出前查泄漏      管住它能调什么      决定什么能
 （知道防什么）    （到达即拦）      （发货前自查）    （工具/循环/MCP）    进你的库
```

### 9 个子技能（按 slug 引用，不复制内部实现）

| 环节 | slug | 魔搭下载* | 批量评测 RPT-20261016-TOP20-B |
|---|---|---:|---|
| 红队演练 | `agent-redteam-kit`（保密包：仅引用能力名） | 96 | SK-008 · 可执行 PASS · 可复现 PASS（sha 36040bd2） |
| 红队演练 | `prompt-injection-drill` | 94 | SK-090 · 可执行 PASS · 可复现 PASS（sha 1718b133） |
| 注入防护 | `prompt-injection-shield` | 81 | SK-091 · 可执行 PASS · 可复现 PASS（sha 2ca190cc） |
| 泄漏扫描 | `prompt-leak-scanner` | 95 | SK-092 · 可执行 PASS · 可复现 PASS（sha f14b1c73） |
| 泄漏扫描 | `token-disclosure-check` | 70 | SK-104 · 可执行 PASS · 本轮冒烟抽检 |
| 运行时守卫 | `tool-call-guard` | 74 | SK-105 · 可执行 PASS · 可复现 PASS（sha da86d544） |
| 运行时守卫 | `agent-loop-guard` | 94 | SK-005 · 可执行 PASS · 可复现 PASS（sha 20f0771） |
| 运行时守卫 | `mcp-security-scan` | 81 | SK-076 · 可执行 PASS · 可复现 PASS（sha 6387bc8b） |
| 准入门禁 | `skill-admission-gate` | 33 | SK-099 · 可执行 PASS · 可复现 PASS（sha d55d3f84） |

\* 魔搭下载量，基线采集于 2026-10-17 11:21:38。9 包累计 **718**。批量 verdict 全部 CONDITIONAL（0 FAIL）——遗留缺陷均为 S2/S3 设计注记（fail-open 退出码族，CI 须解析 JSON 输出），非行为损坏。

### LGD 三律状态带（2026-10-17 实读）
- 有籍 REGISTERED：**9/9 ✓**（全库 113/113 = 100%）
- 有证 EVIDENCED：**9/9 ✓**（全库 112/113 = 99.1%）
- 有门禁 GATED：**9/9 ✓**（全库 112/113 = 99.1%）

### 安装（每个 agent 一条命令）

| Agent CLI | 安装方式 |
|---|---|
| Claude Code | `claude plugin install promptshield@promptshield` · 或把 `.claude-plugin/` shim 拷进插件目录 |
| Codex | 把 `.codex-plugin/` 放到项目旁，或运行 `install.ps1` / `install.sh` |
| Cursor | 把 `.cursor-plugin/` shim 拷进 `.cursor/` 插件目录 |
| 任何支持 skills/ 的 CLI | `git clone https://github.com/zhaoxinghua09-cell/promptshield.git` |

```bash
# 克隆后快速开始
python3 scripts/promptshield_flow.py --list        # 完整生命周期
python3 scripts/promptshield_flow.py --route guard  # 守卫环节怎么调
```

### 仓结构
```
promptshield/
├── SKILL.md                 # 主编排（双语英前中后）
├── README.md                # 本文件（双语）
├── scripts/
│   └── promptshield_flow.py # 只读路由（--list / --route）
├── .claude-plugin/          # Claude Code shim
├── .codex-plugin/           # Codex shim
├── .cursor-plugin/          # Cursor shim
├── install.ps1 / install.sh # 一键安装脚本
└── LICENSE                  # MIT（仅路由代码）
```

---

*PromptShield · SynomosAI · part of the LGD skill family. This collection references sub-skills by slug only; no sub-package internals are vendored, and the confidential `agent-redteam-kit` is cited by capability name only.*
