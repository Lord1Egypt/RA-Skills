---
name: ai-decision-log
description: ai-decision-log — AI 参与的决策一键留痕（JSONL）：决策/模型/证据/人审人/时间；--report 统计模型使用与人审覆盖，无人审的决策重点标出。 适用场景：当需要AI决策留痕器能力时使用本技能；触发词：ai-decision-log。
slug: ai-decision-log
title: ai-decision-log
version: 1.0.1
display_name: AI决策留痕器
display_name_en: AI Decision Log
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "ai-decision-log — AI 参与的决策一键留痕（JSONL）：决策/模型/证据/人审人/时间；--report 统计模型使用与人审覆盖，无人审的决策重点标出。"
description_en: "One-command JSONL logging for AI-involved decisions: decision, model, evidence, human reviewer and time; --report surfaces model usage and human-review coverage gaps."
read_when:
  - AI 决策涉及关键业务风险，需留模型/证据链/时间戳
  - 要统计模型使用与人审覆盖率，找出无人审盲区
  - 合规预警：无人审 AI 决策超阈值需立即标记
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [ai-decision-log, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/ai_decision_log.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: command
    type: string
    description: add|list|report
    required: true
  - name: decision
    type: string
    description: 决策内容（add 用）
    required: false
  - name: model
    type: string
    description: 所用模型
    required: false
  - name: evidence
    type: string
    description: 证据摘要/@文件
    required: false
  - name: reviewer
    type: string
    description: 人审人
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
  stdout: 追加回执/台账列表/决策报告
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - decision_log
  - audit_trail
  - governance
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
- **Decision audit trail**: AI-generated plans/judgments touch key business risk; keep model, evidence chain and timestamp as legal basis.
- **Coverage stats**: periodically compare automated model usage vs human-review coverage to find blind spots.
- **Compliance alert**: un-reviewed AI decisions cross a threshold → flag high-priority risk immediately.

### Usage
Main script: `ai_decision_log.py`.
- Input: `--decision-data` (decision content/JSON), `--time-stamp` (force timestamp).
- Output/report: `.jsonl` default; `--generate-report` triggers stats on "no human review" ratio and highlights anomalies.
- Run via CLI or integrate into existing workflow APIs.

### Flow
1. **Prepare**: context, model version, evidence materials.
2. **Run**: `python ai_decision_log.py` with the params above.
3. **Auto-log**: structured JSONL record with model + human-reviewer IDs.
4. **Report**: per `--generate-report`, produce coverage/risk stats.
5. **Review**: scan "no-review" entries for compliance gaps.
6. **Close loop**: backfill or notify owners for uncovered decisions.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
- **决策留痕审计**：当 AI 生成的方案或判断涉及关键业务风险，需要保留完整的模型、证据链及时间戳作为法律依据时。
- **覆盖率统计与优化**：需定期评估模型在自动化流程中的实际使用率，并与人工复核覆盖数据对比分析，以发现盲区。
- **合规性检查预警**：在业务流程中检测到无人工审核的 AI 决策超过阈值，需立即生成报告并标记高优先级风险。

### 用法
主要调用脚本为 `ai_decision_log.py`。
- **输入参数**：`--decision-data` 指定待记录的决策原始内容或 JSON 对象；`--time-stamp` 强制设定决策发生的具体时间戳。
- **输出与报告**：默认输出为 `.jsonl` 文件，添加 `--generate-report` 标记可触发统计模块，用于计算"无人审"比例及重点高亮异常案例。
- **执行方式**：通过命令行运行或集成到现有工作流的 API 调用接口中。

### 流程
1. **数据准备**：收集当前决策所需的上下文信息、模型版本号及证据材料。
2. **脚本启动**：在执行环境中输入 `python ai_decision_log.py` 并注入上述参数。
3. **自动记录**：系统捕获决策过程，结构化写入 JSONL 日志文件，包含模型与人工标识。
4. **报告生成**：根据 `--generate-report` 配置，生成决策覆盖率及风险统计报表。
5. **重点审查**：扫描日志中"无人审"标记的条目，确认是否满足合规要求。
6. **闭环处理**：若发现未覆盖决策，立即触发补录流程或通知相关责任人进行人工复核。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
