---
name: a3-law-operational
display_name: A³法则操作化
display_name_en: A³ Law Operational
description: '把「A³ 法则（AI 造 AI 三定律）」从原则落成可执行的工程规矩：① 触发阈值（什么动作算"造/改 AI"或"重大自主行动"，须进入 A³ 评审）；② 事前评估清单（意图/影响/可逆性/监督）；③ 事后复盘与升级/拒绝条件。配触发判定树与评分卡，让任何 AI 在动"造/改另一个 AI"或高影响动作前先过三关。触发词：A³法则、AI造AI三定律、AI自主造AI、触发阈值、自我修改、自主行动评估、AI三定律、造AI评审。'
description_zh: '把「A³ 法则（AI 造 AI 三定律）」从原则落成可执行的工程规矩：① 触发阈值（什么动作算"造/改 AI"或"重大自主行动"，须进入 A³ 评审）；② 事前评估清单（意图/影响/可逆性/监督）；③ 事后复盘与升级/拒绝条件。配触发判定树与评分卡，让任何 AI 在动"造/改另一个 AI"或高影响动作前先过三关。触发词：A³法则、AI造AI三定律、AI自主造AI、触发阈值、自我修改、自主行动评估、AI三定律、造AI评审。'
description_en: 'Operationalize the "A³ Laws" (AI-building-AI three laws) from principles into enforceable engineering rules: (1) trigger thresholds that define what counts as "building/modifying AI" or a "major autonomous action" requiring A³ review; (2) pre-action evaluation checklist (intent / impact / reversibility / oversight); (3) post-action review with escalation / reject conditions. Ships with a trigger decision tree and scoring card so any AI passes three gates before "building/modifying another AI" or any high-impact action. Trigger words: A³ law, AI-builds-AI three laws, self-modification, autonomous action evaluation, AI three laws, build-AI review.'
version: "1.0.2"
agent_created: true
author: 潘布达 (Buda Pan) @SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, Edit, WebFetch
category: AI治理
platforms: [windows, macos, linux]
read_when:
  - AI 准备生成/修改/部署另一个 AI 或智能体（"造 AI"），或执行不可逆/高影响自主动作
  - 用户说"A³法则""AI造AI三定律""自我修改""自主行动评估""触发阈值"
  - 需要把 AI 世界共生论落到操作化的约束与放行条件
tags:
  - A³法则
  - AI造AI
  - 触发阈值
  - 自主行动
  - 约束
  - 三定律
slug: a3-law-operational
displayName: A³ 法则：AI 造 AI 三定律
title: A³ 法则：AI 造 AI 三定律
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: SKILL.md
  runtime: text
  call_pattern: args
input_schema:
  - name: situation
    type: string
    description: 待判断的动作描述（是否属于造/改 AI 或高影响自主动作）
    required: true
output_schema:
  stdout: 触发判定树+事前评估清单+事后复盘条件的结构化文本
  exit_code: "0=正常"
capabilities:
  - ai_governance
  - decision_gate
  - self_modification_review
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.2: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
1. The user input or system detects trigger words like "A³ law" / "AI autonomously building AI".
2. Before a major autonomous action that may rewrite another agent's core logic, architecture or permissions.
3. The internal model rates the current task's intent and impact above the warning threshold.

### Usage
Pure-document protocol; no external scripts. Activate via keywords or auto-trigger the A³ review flow; the system reads the built-in trigger decision tree and pre-action checklist to generate a compliance report.

### Flow
1. **Threshold screening**: match trigger words and behavior type against the scoring card to decide whether to enter the A³ process.
2. **Three-gate review**: check intent legitimacy, impact risk, reversibility and oversight state item by item; produce an interim opinion.
3. **Closed-loop decision**: per the final score execute "escalate / reject / allow", and force-keep post-action review records and escalation directives.

### Evidence & safety
- Evidence: TBD (no benchmark/badge links yet).
- Version: 1.0.2
- Security: no independent scan (TBD).

## 中文

### 何时用
1. 当用户输入或系统检测到「A³ 法则」「AI 自主造 AI」等特定触发词时。
2. 在执行可能改写其他 Agent 核心逻辑、架构或权限的重大自主行动前。
3. 当内部评估模型判定当前任务的意图与影响评分达到阈值预警线时。

### 用法
本技能为纯文档型协议，无需外部脚本调用；用户可通过关键词手动激活该机制，或在后台自动触发 A³ 评审流程；系统需优先读取内置的"触发判定树"与"事前评估清单"生成合规报告。

### 流程
1. **阈值判定**：根据上下文匹配触发词及行为类型，调用评分卡初筛是否进入 A³ 程序。
2. **三关审查**：逐项核查意图合法性、影响风险、可逆性与监督状态，生成中间评估意见。
3. **闭环决策**：依据最终得分执行"升级审批/拒绝/允许"动作，并强制保留事后复盘记录与升级指令。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
