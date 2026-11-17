---
name: ai-incident-log
description: ai-incident-log — AI 失控/误操作/幻觉事故一键入账（JSONL 台账）：时间/严重度/模型/动作/复盘字段；--list/--report 一键汇总。 适用场景：当需要AI事故记录器能力时使用本技能；触发词：ai-incident-log。
slug: ai-incident-log
title: ai-incident-log
version: 1.0.1
display_name: AI事故记录器
display_name_en: AI Incident Log
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "ai-incident-log — AI 失控/误操作/幻觉事故一键入账（JSONL 台账）：时间/严重度/模型/动作/复盘字段；--list/--report 一键汇总。"
description_en: "Log AI failures, hallucinations and misoperations into a JSONL incident ledger: time, severity, model, action and retrospective fields; --list/--report for summaries."
read_when:
  - AI 出现严重幻觉/事实错误/逻辑崩坏，需固化事故证据
  - AI 自主决策引发误操作（文件篡改/数据泄露/服务挂起）
  - 要把错误节点沉淀为合规 JSONL 台账供审计追溯
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [ai-incident-log, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/ai_incident_log.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: command
    type: string
    description: add|list|report
    required: true
  - name: severity
    type: int
    description: 严重度 1-3，默认2
    required: false
  - name: model
    type: string
    description: 涉事模型/智能体
    required: false
  - name: action
    type: string
    description: 已采取措施
    required: false
  - name: owner
    type: string
    description: 记录人
    required: false
  - name: file
    type: string
    description: 台账 JSONL 路径
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 事故回执/台账/报告
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - incident_log
  - audit_trail
  - safety
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
1. Model output shows severe hallucination, factual error or logic collapse; evidence must be frozen immediately.
2. Autonomous AI action causes production anomalies (file tampering, data leak, service hang).
3. Retrospective key review info must be turned into a compliant JSONL ledger for audit traceability.

### Usage
1. One-click log: `python ai_incident_log.py --record`, with `--severity critical/high/medium` and model version.
2. Query/summary: `--list` for history; `--report` for a structured summary.
3. Ensure Python env and the main script (and cache dir) exist.

### Flow
1. **Locate anomaly**: identify the trigger moment in logs/monitoring.
2. **Fill fields**: timestamp, severity, model, action description.
3. **Run script**: `--record` mode writes a standardized JSONL entry.
4. **Verify**: `--list` confirms the record; check timestamp and fields.
5. **Report**: `--report` generates a one-click summary for team sync.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 当检测到 AI 模型生成内容出现严重幻觉、事实错误或逻辑崩坏，需即时固化事故证据时；
2. 当因 AI 自主决策引发的误操作（如文件篡改/数据泄露/服务挂起）导致生产环境异常时；
3. 当需要快速沉淀关键复盘信息，将交互过程中的错误节点转化为合规 JSONL 台账用于审计追溯时。

### 用法
1. **一键入账记录**：通过命令行执行 `python ai_incident_log.py --record`，支持传入 `--severity critical/high/medium` 及模型版本等自定义参数；
2. **台账查询与汇总**：调用 `ai_incident_log.py --list` 查看所有历史事故清单，或使用 `--report` 一键生成结构化汇总报告；
3. **环境校验提示**：执行前请确保 Python 环境已配置好，并确认项目根目录下存在主脚本文件。

### 流程
1. **异常定位**：在日志或监控中识别 AI 失控、幻觉或操作错误的触发时刻；
2. **信息填充**：依据实际情况填写时间戳、严重度等级、涉事模型及动作描述等关键要素；
3. **脚本执行**：在终端运行主脚本，选择 `--record` 模式生成标准化的 JSONL 入库文件；
4. **结果核对**：调用 `--list` 接口确认数据已落库，检查时间戳与字段完整性是否匹配；
5. **报告产出**：若需向团队同步，再次运行 `--report` 参数获取一键汇总的分析文档。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
