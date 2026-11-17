---
name: contract-clause-check
description: 合同高危条款扫描器 — 签合同前扫必备条款（违约/争议/管辖）与高危表述（最终解释权/自动续期/高违约金），缺项即 FAIL（零依赖） 适用场景：当需要合同高危条款扫描器能力时使用本技能；触发词：contract-clause-check。
slug: contract-clause-check
title: contract-clause-check
version: 1.0.1
display_name: 合同高危条款扫描器
display_name_en: Contract Clause Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, cli]
copyright: SynomosAI
description_zh: "合同高危条款扫描器 — 签合同前扫必备条款（违约/争议/管辖）与高危表述（最终解释权/自动续期/高违约金），缺项即 FAIL（零依赖）"
description_en: "Scan contracts for missing essential clauses (breach, dispute, jurisdiction) and dangerous terms (final-interpretation rights, auto-renewal, heavy penalties); missing items FAIL (zero-dependency)."
read_when:
  - 合同签署前合规预审，识别潜在法律风险
  - 高价值交易/长期协议的违约与管辖争议条款检测
  - 审核高危表述（最终解释权/自动续期/高违约金）与必备保护条款
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [contract-clause-check, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/contract_clause_check.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: text
    type: string
    description: 合同文本（要点）
    required: true
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 高危条款扫描清单
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - contract_review
  - legal_compliance
  - risk_screening
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
Pre-signature compliance review to surface potential legal risk. Detect breach / jurisdiction-dispute clauses in high-value or long-term agreements. Check for dangerous wording (final-interpretation rights, auto-renewal) and missing protective clauses.

### Usage
Run `python contract_clause_check.py`; pass the contract file path or text via `--input`. Zero-dependency mode emits the report directly.

### Flow
1. Prepare input: confirm the draft or final contract text.
2. Load the script; parse key legal terms.
3. Scan breach, dispute-jurisdiction and auto-renewal clauses.
4. Check missing protective clauses and abnormal wording.
5. On risk-scoring: any high-risk hit → FAIL.
6. Emit a structured report with concrete risk points and suggested revisions.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
适用于合同签署前的合规性预审场景，旨在识别潜在法律风险。
当业务涉及高价值交易或长期协议时，用于检测违约与管辖争议条款。
在审核合同中是否存在高危表述（如最终解释权、自动续期）及必备保护条款时使用。

### 用法
通过运行入口脚本 `python contract_clause_check.py` 进行调用。
命令行参数需指定待扫描的合同文件路径或文本内容，例如 `--input` 参数。
技能在内部零依赖模式下处理逻辑，无需额外环境配置即可直接生成报告。

### 流程
1. 准备输入数据，确认待审核的合同草稿或最终文本。
2. 执行脚本加载与初始化，解析合同中的关键法律术语。
3. 扫描违约、争议管辖及自动续期等高危条款。
4. 检查缺失的必备保护条款及异常表述是否达标。
5. 根据风险评分判定结果，检出高危项即返回 FAIL 状态。
6. 输出包含具体风险点列表与修改建议的结构化报告。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
