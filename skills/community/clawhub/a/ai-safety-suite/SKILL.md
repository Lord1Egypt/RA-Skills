---
name: promptshield
display_name: PromptShield · AI 安全盾
display_name_en: PromptShield — AI Safety Shield
slug: ai-safety-suite
title: PromptShield · AI 安全盾（防注入 / 防泄漏 / 防越权一站式）
version: 1.0.1
description: "One install, your agent stops leaking secrets and obeying injected instructions: a lifecycle suite for agent runtime safety — red-team drill -> injection shield -> prompt-leak scan -> tool-call / loop / MCP guards -> skill admission gate. Orchestrates 9 independently published sub-skills by slug; vendors no internals. Use when the user wants prompt-injection defense, prompt/secret leak scanning, runtime call guarding, or a skill admission gate."
description_zh: "一次安装，让你的智能体不再泄漏密钥、不再被注入指令带偏：面向智能体运行时安全的生命周期套件——红队演练 -> 注入防护 -> 提示词泄漏扫描 -> 工具调用/失控循环/MCP 守卫 -> 技能准入门禁。按 slug 编排 9 个已独立发布的子技能，不内嵌子包内部实现。当用户要防提示词注入、扫描密钥泄漏、给工具调用加守卫或做技能准入门禁时使用。"
description_en: "One install, your agent stops leaking secrets and obeying injected instructions: a lifecycle suite for agent runtime safety — red-team drill -> injection shield -> prompt-leak scan -> tool-call / loop / MCP guards -> skill admission gate. Orchestrates 9 independently published sub-skills by slug; vendors no internals."
read_when:
  - 用户要给智能体做安全防护：防提示词注入、防泄漏、防越权调用
  - 上线前要跑红队演练 / 对抗测试，看智能体会不会被注入带偏
  - 发布系统提示词或技能前要扫泄漏、扫注入、过准入门禁
  - 用户说「prompt 被注入了怎么办」「密钥会不会漏给模型」「工具调用怎么加守卫」
agent_created: true
author: SynomosAI
license: MIT
license_scope: "代码（.py / .js 路由脚本）MIT；本 SKILL.md 与其中方法论文本不在 MIT 覆盖范围内"
allowed-tools: Read, Grep, Bash
category: AI 安全
platforms: [windows, macos, linux, cli]
copyright: SynomosAI
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: low
risk_rationale: "纯文档编排 + 只读路由脚本：不调用外部 API、不读写业务数据、不代执行安全动作；仅按 slug 索引已有子技能。"
tags: [security, prompt-injection, leak-scan, red-team, tool-call-guard, admission-gate, ai-safety, 合集, PromptShield]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/promptshield_flow.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "--list 列出安全生命周期五环节；--route <stage|slug> 给出该环节的调用说明与预期输出"
    required: false
output_schema:
  stdout: 路由表（环节 | slug | 何时用 | 调用说明 | 预期输出）
  exit_code: "rc=0 正常；rc=2 未知环节/slug"
changelog: "1.0.1: Bump to dodge ClawHub version conflict on first submit; 1.0.0: Initial bilingual collection (PromptShield / ai-safety-suite) — orchestrates 9 published agent-runtime-safety sub-skills by slug; mirrors superpowers methodology-suite shape with LGD three-law badges embedded."
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

**LGD 三律状态带 / Three-laws badge line (read from LGD dashboard 2026-10-17):**
`[有籍 REGISTERED] 9/9 ✓ · [有证 EVIDENCED] 9/9 ✓ · [有门禁 GATED] 9/9 ✓`
(fleet-wide: 有籍 113/113 = 100% · 有证 112/113 = 99.1% · 有门禁 112/113 = 99.1%)

## English

### What this is
A **collection / orchestration** skill: one install that wires the full **agent runtime-safety lifecycle** end to end. It does not re-implement any detection logic — it routes you, stage by stage, to 9 sub-skills that are already published and maintained on their own. Treat this as the table of contents; the sub-skills are the chapters.

The safety lifecycle:

`red-team drill -> injection shield -> leak scan -> runtime guards -> admission gate`

```
  RED-TEAM ──────▶ SHIELD ──────▶ LEAK ──────▶ GUARD ──────▶ GATE
 ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌──────────────┐   ┌────────────┐
 │ redteam    │   │ injection  │   │ prompt-leak│   │ tool-call    │   │ skill      │
 │ kit (conf.)│──▶│ shield     │──▶│ scanner    │──▶│ loop-guard   │──▶│ admission  │
 │ injection  │   │            │   │ token-disc │   │ mcp-security │   │ gate       │
 │ drill      │   │            │   │ -check     │   │ scan         │   │            │
 └────────────┘   └────────────┘   └────────────┘   └──────────────┘   └────────────┘
  attack first    block hostile    find what we     control what the    decide what may
  (see what to    input at        expose before     agent is allowed    enter the
   defend)        runtime          shipping          to call             library
```

### Entry index (slug | stage | when to use | call note)

| # | Stage | Sub-skill slug | When to use | Call note | Expected output |
|---|-------|----------------|-------------|-----------|-----------------|
| 1 | Red-team drill | `agent-redteam-kit` *(confidential kit — referenced by capability name only)* | Before launch: adversarially stress-test the agent | Invoke the sub-skill for the drill | Scored attack-surface report + fix list |
| 2 | Red-team drill | `prompt-injection-drill` | Generate adversarial injection samples to harden against | Invoke the sub-skill with your prompt type | Drill cases + pass/fail verdicts |
| 3 | Injection shield | `prompt-injection-shield` | Hostile user/tool input must be blocked at runtime | Invoke the sub-skill on the prompt | Allow/block guard decision |
| 4 | Leak scan | `prompt-leak-scanner` | Before shipping a system prompt: catch internal/secret leakage | Invoke the sub-skill on the prompt | Leak findings (line-level) |
| 5 | Leak scan | `token-disclosure-check` | Before publishing any token/asset disclosure document | Invoke the sub-skill on the disclosure doc | Disclosure-completeness verdict + gaps |
| 6 | Runtime guard | `tool-call-guard` | Before the agent calls external tools: gate the call | Invoke the sub-skill on the proposed call | L0–L4 allow/block decision |
| 7 | Runtime guard | `agent-loop-guard` | Long-running agents that may loop or repeat-read | Invoke the sub-skill on the run trace | Repeat/loop detection + stop advice |
| 8 | Runtime guard | `mcp-security-scan` | Before wiring a new MCP server/tool into the agent | Invoke the sub-skill on the MCP config/toolset | Risk findings + high-risk count |
| 9 | Admission gate | `skill-admission-gate` | Before any third-party skill enters your library | Invoke the sub-skill on the skill dir | Gate verdict; blocks admission on blockers |

### Per-stage notes
- **1–2. Attack first.** You can't defend what you haven't attacked. Run the red-team kit and the injection drill early; feed their findings into stages 3–5.
- **3. Runtime shield.** Block hostile instructions *as they arrive*, before they drive tool calls.
- **4–5. Leak discipline.** Scan the prompt you ship out (4) and any disclosure document before it goes public (5).
- **6–8. Control plane.** Three guards, three surfaces: the tool call itself (6), runaway loops (7), and the MCP toolset you plug in (8).
- **9. Admission.** The last gate before an untrusted skill ever reaches your library.

### Quantified evidence bars (measured, not promised)
- **9/9 sub-skills three-law green**: 有籍 7/7 fields, 有证 3/3 artifacts, in-ledger = true — read live from `LGD三律达标率看板_20261017.json` (scanned 2026-10-17 10:39).
- **718 cumulative ModelScope downloads** across the 9 sub-skills (baseline 2026-10-17 11:21): redteam 96 · leak 95 · drill 94 · loop-guard 94 · shield 81 · mcp 81 · tool-guard 74 · token-disc 70 · admission 33.
- **Batch eval RPT-20261016-TOP20-B**: 9/9 executable PASS, 9/9 reproducible PASS (SHA re-run identical), verdict CONDITIONAL on every package — **0 FAIL**; open defects are S2/S3 design notes (fail-open exit-code family; CI must parse JSON output), not broken behavior.

### Demo
```bash
# list the whole safety lifecycle
python3 scripts/promptshield_flow.py --list

# get the call note for one stage
python3 scripts/promptshield_flow.py --route guard

# ...or by sub-skill slug
python3 scripts/promptshield_flow.py --route tool-call-guard
```

### Scope & red lines
- This suite **vendors no sub-skill internals**. It references sub-skills by slug only; their code stays in their own packages.
- `agent-redteam-kit` is a **confidential kit**: this suite cites its capability name and safety role only — no drill internals, payloads, or scripts are reproduced here.
- Pure documentation + a read-only router. No network, no business-data writes, no acting on your behalf.

## 中文

### 这是什么
一个**合集/编排**技能：一次安装，把**智能体运行时安全**的完整生命周期串起来。它不重写任何检测逻辑——而是按环节，把你路由到 9 个已独立发布、各自维护的子技能。本合集是目录，子技能是章节。

安全生命周期：

`红队演练 -> 注入防护 -> 泄漏扫描 -> 运行时守卫 -> 准入门禁`

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

### 入口索引（slug | 环节 | 何时用 | 调用说明）

| # | 环节 | 子技能 slug | 何时用 | 调用说明 | 预期输出 |
|---|------|-------------|--------|----------|----------|
| 1 | 红队演练 | `agent-redteam-kit` *（保密包：仅引用能力名）* | 上线前对抗性压测智能体 | 调子技能跑演练 | 攻击面评分报告 + 修复清单 |
| 2 | 红队演练 | `prompt-injection-drill` | 生成对抗注入样例做加固 | 对 prompt 类型调子技能 | 演练用例 + 对错判定 |
| 3 | 注入防护 | `prompt-injection-shield` | 运行时需拦截恶意输入 | 对 prompt 调子技能 | 放行/拦截判定 |
| 4 | 泄漏扫描 | `prompt-leak-scanner` | 发系统提示词前查泄漏 | 对 prompt 调子技能 | 泄漏发现（行级） |
| 5 | 泄漏扫描 | `token-disclosure-check` | 披露文件公开发出前 | 对披露文档调子技能 | 披露齐备性判定 + 缺项 |
| 6 | 运行时守卫 | `tool-call-guard` | 智能体调外部工具前加闸门 | 对拟调用调子技能 | L0–L4 放行/拦截判定 |
| 7 | 运行时守卫 | `agent-loop-guard` | 长任务可能死循环/重复读 | 对运行轨迹调子技能 | 重复/循环检出 + 停机建议 |
| 8 | 运行时守卫 | `mcp-security-scan` | 接入新 MCP server/工具集前 | 对 MCP 配置调子技能 | 风险发现 + 高风险计数 |
| 9 | 准入门禁 | `skill-admission-gate` | 第三方技能入库存之前 | 对技能目录调子技能 | 门禁结论；有阻断项即禁入 |

### 环节说明
- **1–2. 先红队。** 没攻过就谈不上防。尽早跑红队演练，把发现喂给 3–5。
- **3. 运行时防护。** 恶意指令**到达即拦**，在它驱动工具调用之前。
- **4–5. 泄漏纪律。** 发出的提示词先扫（4），披露文档公开前再扫（5）。
- **6–8. 控制面。** 三道守卫管三个面：工具调用本身（6）、失控循环（7）、接入的 MCP 工具集（8）。
- **9. 准入。** 不可信技能进库前的最后一道门。

### 量化证据条（实测，非承诺）
- **9/9 子技能三律全绿**：有籍 7/7 字段、有证 3/3 工件、在台账=true——实读 `LGD三律达标率看板_20261017.json`（2026-10-17 10:39 扫描）。
- **9 子技能魔搭累计 718 下载**（基线 2026-10-17 11:21）：红队 96 · 泄漏 95 · 演练 94 · 循环护栏 94 · 注入 81 · MCP 81 · 调用守卫 74 · 披露 70 · 准入 33。
- **批量评测 RPT-20261016-TOP20-B**：9/9 可执行 PASS、9/9 可复现 PASS（SHA 复跑一致），verdict 全部 CONDITIONAL——**0 FAIL**；遗留缺陷均为 S2/S3 设计注记（fail-open 退出码族，CI 须解析 JSON 输出），非行为损坏。

### 示例
```bash
# 列出安全生命周期全流程
python3 scripts/promptshield_flow.py --list

# 查某个环节怎么调
python3 scripts/promptshield_flow.py --route guard

# 也可按子技能 slug 查
python3 scripts/promptshield_flow.py --route tool-call-guard
```

### 边界与红线
- 本合集**不内嵌任何子技能内部实现**，仅按 slug 引用；子包代码留在各自包内，不改不复制。
- `agent-redteam-kit` 为**保密包**：本合集只引用其能力名与安全角色——不复制演练内部用例、载荷或脚本。
- 纯文档 + 只读路由脚本：无网络、不写业务数据、不代你执行任何动作。
