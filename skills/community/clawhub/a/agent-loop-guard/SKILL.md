---
name: agent-loop-guard
display_name: 失控循环护栏（Agent Loop Guard）
display_name_en: "Agent Loop Guard"
description: >-
  Guard against runaway agent loops: step limits, repeated-action detection, budget alerts and controlled-intervention patterns for stuck, looping or burning agents.

  当用户说『agent卡死了』『一直在重复同样动作』『跑飞了烧光token』『怎么给agent设步数上限』，或 agent 出现无限循环/重复调用/原地打转时使用。把 agent 的运行当『受控进程』：监控步数上限·重复动作·状态无进展，触发即熔断并产出诊断。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：agent卡死、无限循环、重复动作、跑飞、步数上限、loop guard、token烧光、失控循环。
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - agent 疑似陷入无限循环或重复调用同一工具
  - token/费用异常飙升，怀疑 agent 跑飞
  - 想给 agent 设最大步数 / 无进展熔断
  - 用户抱怨「它一直在绕圈」
tags: [失控循环, loop guard, 步数上限, agent监控, token控制, 熔断, 可靠性, AI工程]
slug: agent-loop-guard
title: 失控循环护栏（Agent Loop Guard）
copyright: SynomosAI
description_zh: "当用户说『agent卡死了』『一直在重复同样动作』『跑飞了烧光token』『怎么给agent设步数上限』，或 agent 出现无限循环/重复调用/原地打转时使用。把 agent 的运行当『受控进程』：监控步数上限·重复动作·状态无进展，触发即熔断并产出诊断。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：agent卡死、无限循环、重复动作、跑飞、步数上限、loop guard、token烧光、失控循环。"
description_en: "Guard against runaway agent loops: step limits, repeated-action detection, budget alerts and controlled-intervention patterns for stuck, looping or burning agents."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/loop_guard.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: trace
    type: string
    description: 运行轨迹文本（内联）
    required: true
  - name: max_steps
    type: int
    description: 最大步数，默认30
    required: false
  - name: repeat
    type: int
    description: 重复容忍次数，默认3
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 循环检测结论与风险等级
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - loop_detection
  - trace_analysis
  - safety
permissions:
  network: false
  filesystem: true
  subprocess: false
  scope: project-dir-only   # 只处理调用者指定目录，不越界、不跟随符号链接
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
1. The user says the agent "froze", "ran away" or "burned through tokens".
2. The system detects repeated calls of the same action with no real progress.
3. The user asks how to set a "step limit" or suspects the flow is out of control.
4. Internal monitoring accumulates "no gate" risk (LGD state).

### Usage
- Core script: `loop_guard.py` (root of the skill dir).
- Key flags: `--check_loop` for loop detection; `--enable_firewall` for circuit-breaking.
- Config: env vars `LGD_MAX_STEPS=10` and `TOKEN_BUDGET_LIMIT` activate automated monitoring.

### Flow
1. **Trigger watch**: scan conversation/log streams for "stuck" signals.
2. **State capture**: current step count, token burn rate, action-sequence fingerprint.
3. **Rule match**: run loop-detection; test circuit-break conditions.
4. **Intervention**: on confirmed infinite loop or stall, fire a system-level circuit break.
5. **Diagnosis**: structured report with root cause, remaining-token estimate, fix suggestions.
6. **Recovery**: on user instruction, lift the limit and enter a new controlled monitoring cycle.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 当用户明确提及 Agent"卡死"、"跑飞"或"烧光 token"等异常状态时。
2. 当系统检测到 Agent 处于重复调用同一动作的循环，且任务执行无实质性进展时。
3. 当用户询问如何设置"步数上限"或质疑当前流程失控时。
4. 当内部监控算法识别到"无门禁"状态持续累积风险时。

### 用法
- **核心脚本**：直接执行 `loop_guard.py`（位于根目录）。
- **关键命令**：`--check_loop` 循环检测；`--enable_firewall` 开启熔断保护。
- **配置说明**：设定环境变量 `LGD_MAX_STEPS=10` 与 `TOKEN_BUDGET_LIMIT` 激活自动化监控。

### 流程
1. **触发监听**：在对话流或 Agent 日志中实时扫描"卡死"及异常行为信号。
2. **状态采集**：收集当前执行步骤、Token 消耗速率及动作序列指纹数据。
3. **规则比对**：运行检测算法，验证是否满足熔断条件。
4. **干预决策**：确认无限循环或状态停滞，立即触发系统级熔断。
5. **诊断生成**：输出根因分析、Token 剩余量评估及修复建议的结构化报告。
6. **执行恢复**：等待用户指令后解除限制，进入新一轮受控监控周期。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/agent-loop-guard
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/agent-loop-guard/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
