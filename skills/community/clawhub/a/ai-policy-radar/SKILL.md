---
name: ai-policy-radar
display_name: AI法规动态雷达（Policy Radar）
display_name_en: "AI Policy Radar"
description: "当用户说『最近AI出了什么新规』『EU AI Act/脆监会/NMPA有没有新动作』『法规更新我得跟上』『帮我盯AI政策』，或要持续跟踪 AI 监管动态（EU AI Act / 中国 NMPA / 美国 FDA / GDPR 等）时使用。扫描法规库/更新日志，按主题（风险分级/透明度/数据/准入）归类变动并留痕（有证），输出「本月新增了什么、对你有何影响」。可运行脚本（policy_radar 扫描器）。理论根基：LGD 三律之有证（法规变动留痕可溯）。与 eu-ai-act-companion 互补（它管单法导航，本技能管跨法动态监测）。触发词：AI法规、政策雷达、监管动态、EU AI Act更新、合规追踪、policy radar、法规监测。"
version: 1.0.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Task
category: AI合规
platforms: [windows, macos, linux]
read_when:
  - 要持续跟踪 AI 监管新规
  - 不确定 EU AI Act / NMPA / FDA 近期有无变动
  - 做合规月报/动态监测
  - 收到「盯一下政策」类指令
tags: [AI法规, policy radar, 监管动态, 合规追踪, 有证]
slug: ai-policy-radar
title: AI法规动态雷达（Policy Radar）
copyright: SynomosAI
description_zh: "当用户说『最近AI出了什么新规』『EU AI Act/脆监会/NMPA有没有新动作』『法规更新我得跟上』『帮我盯AI政策』，或要持续跟踪 AI 监管动态（EU AI Act / 中国 NMPA / 美国 FDA / GDPR 等）时使用。扫描法规库/更新日志，按主题（风险分级/透明度/数据/准入）归类变动并留痕（有证），输出「本月新增了什么、对你有何影响」。可运行脚本（policy_radar 扫描器）。"
description_en: "Track AI regulatory movements (EU AI Act, China NMPA, US FDA, GDPR and more): a monitoring radar with source pointers so rule changes do not blindside your roadmap."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
standards_ref: ["EU AI Act"]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/policy_radar.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: dir
    type: string
    description: 政策文档目录
    required: true
  - name: since
    type: string
    description: 起始日期过滤
    required: false
output_schema:
  stdout: 政策要点雷达摘要
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - policy_monitoring
  - compliance
  - research
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
1. The user wants the latest AI regulatory developments, especially updates on the EU AI Act, China NMPA or GDPR.
2. Cross-jurisdiction compliance tracking with focus on clustered changes (risk tiers, data access, etc.).
3. Ongoing monitoring of regulatory trends with a sourced monthly report.

### Usage
1. Natural-language trigger: "policy radar", "AI regulatory monitoring", "watch AI policy" → auto-invoke `policy_radar.py`.
2. Parametric: `python policy_radar.py --region=EU,NMPA --topic=risk`.
3. Direct file scan: `python policy_radar.py -f regulations.log --log=true`.

### Flow
1. **Trigger & load**: read `policy_radar.py` core code on user command.
2. **Scan**: auto-scan regulation update logs across EU, China, US jurisdictions.
3. **Classify & trace**: group changes by theme (risk, transparency) with sourced records (LGD "has evidence").
4. **Impact analysis**: map recent rules to user's business/compliance.
5. **Report**: structured output with the monthly new list and suggested actions.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 用户希望获取 AI 领域最新法规动态，特别是针对 EU AI Act、中国 NMPA 或 GDPR 等特定法案的更新询问。
2. 当需要跨法域进行合规追踪，且关注多主题（如风险分级、数据准入）的集中变更时。
3. 用户要求持续跟踪监管趋势并获取带有来源依据的月度新增报告时。

### 用法
1. **自然语言唤起**：直接使用触发词"政策雷达"、"AI 法规监测"或"帮我盯 AI 政策"，系统将自动调用 `policy_radar.py`。
2. **参数化指令**：若需指定扫描范围，使用格式 `[区域]-[主题]` 进行限定，例如：`python policy_radar.py --region=EU,NMPA --topic=risk`。
3. **脚本运行模式**：针对特定法规库或更新日志文件直接运行命令，示例为 `python policy_radar.py -f regulations.log --log=true`。

### 流程
1. **触发与加载**：接收用户指令后，读取 `policy_radar.py` 核心代码。
2. **扫描识别**：自动扫描法规库更新日志，提取关于欧盟、中国及美国等主要法域的新规变动。
3. **分类与留痕**：依据 LGD 三律之有证原则，将变动按风险、透明度等主题归类并保留来源可追溯记录。
4. **影响分析**：结合现有知识库，推演近期法规对用户业务或合规的具体影响。
5. **输出报告**：生成结构化文本，包含本月新增清单及对目标的关联建议。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
