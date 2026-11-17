---
name: ai-vendor-checklist
description: ai-vendor-checklist — 10 项 AI 采购尽调清单（数据权属/训练退出/留存/资质/事故通报/子处理者/出境/模型卡/审计/迁移退出）；--template 出清单，--score 打分低于线 rc=1。 适用场景：当需要AI供应商尽调清单能力时使用本技能；触发词：ai-vendor-checklist。
slug: ai-vendor-checklist
title: ai-vendor-checklist
version: 1.0.1
display_name: AI供应商尽调清单
display_name_en: AI Vendor Checklist
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "ai-vendor-checklist — 10 项 AI 采购尽调清单（数据权属/训练退出/留存/资质/事故通报/子处理者/出境/模型卡/审计/迁移退出）；--template 出清单，--score 打分低于线 rc=1。"
description_en: "Ten-item AI procurement due-diligence checklist: data ownership, training opt-out, retention, qualifications, incident notice, sub-processors, cross-border transfer, model cards, audit and exit; --template and --score modes."
read_when:
  - AI 供应商采购前合规尽调（数据权属/出境/训练退出）
  - 法务审合同条款需十项标准化风险清单
  - 供应链中断/法律纠纷风险快速评估是否达监管红线
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [ai-vendor-checklist, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/ai_vendor_checklist.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: mode
    type: string
    description: template|score
    required: true
  - name: vendor
    type: string
    description: 供应商名
    required: false
  - name: score
    type: string
    description: 10 项打分 0/1 逗号串
    required: false
  - name: threshold
    type: float
    description: 通过阈值默认0.8
    required: false
  - name: out
    type: string
    description: 模板输出路径
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 尽调模板或评分结论
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - vendor_due_diligence
  - checklist
  - procurement
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
Pre-procurement compliance due diligence on AI vendors — especially data ownership, cross-border transfer and training opt-out. Generate a standardized ten-item risk list for legal review of contract terms. Quickly assess whether a vendor meets regulatory red lines when supply-chain disruption or legal-dispute risk surfaces. Used in standardized onboarding review of AI partners.

### Usage
Run `python ai_vendor_checklist.py` (root dir). `--template` generates the standard list; `--score <0/1 csv>` runs quantitative scoring. Vendor data can be passed via JSON input.

### Flow
1. Prepare the vendor's procurement requirements and baseline qualifications.
2. Run `ai_vendor_checklist.py` with the desired mode/data interface.
3. Auto-traverse the 10 compliance dimensions (ownership, training opt-out, retention, qualifications, incident notice, sub-processors, cross-border, model cards, audit, exit).
4. Output the list or score; below threshold → rc=1.
5. Human review of risk items / compliance gaps.
6. Decide: sign, trigger audit, or execute migration/exit.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
本技能适用于 AI 供应商采购前的合规性尽职调查，特别是在涉及数据权属界定、跨境数据传输及模型训练退出权限等敏感场景时。当需要生成标准化的十项风险清单以辅助法务部门审核合同条款时调用本技能。在检测到潜在的供应链中断或法律纠纷风险，需快速评估供应商是否满足监管红线（rc=1）时使用。适用于企业内部对 AI 技术合作伙伴进行背景调查及安全准入评审的标准化流程中。

### 用法
执行本地 Python 脚本文件 `ai_vendor_checklist.py`，位于项目根目录。核心调用命令为 `python ai_vendor_checklist.py --template` 用于生成标准清单，或搭配 `--score <数值>` 参数进行定量打分评估。若需处理具体厂商信息，可通过 JSON 输入传递给脚本读取。

### 流程
1. 准备目标 AI 供应商的采购需求及基础资质文件作为输入源。
2. 调用 `ai_vendor_checklist.py` 脚本并指定所需参数或数据接口连接。
3. 系统解析输入数据，自动遍历数据权属、训练退出等 10 项合规指标。
4. 输出生成的清单内容或评分结果，若得分低于阈值则自动设置 rc=1。
5. 人工审核输出的报告是否包含必要风险条目或合规缺口信息。
6. 根据审查结果决定是否签署合同、触发审计或执行迁移退出流程。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
