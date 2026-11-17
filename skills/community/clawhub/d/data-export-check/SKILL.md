---
name: data-export-check
description: 数据出境合规自检 — 数据出境前五项义务自检（分级/单独同意/PIA/标准合同或安全评估/留痕），缺项即 FAIL（零依赖） 适用场景：当需要数据出境合规自检能力时使用本技能；触发词：data-export-check。
slug: data-export-check
title: data-export-check
version: 1.0.1
display_name: 数据出境合规自检
display_name_en: Data Export Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, cli]
copyright: SynomosAI
description_zh: "数据出境合规自检 — 数据出境前五项义务自检（分级/单独同意/PIA/标准合同或安全评估/留痕），缺项即 FAIL（零依赖）"
description_en: "Pre-export data compliance self-check across five obligations: grading, separate consent, PIA, standard contract or security assessment, and record-keeping; missing items FAIL (zero-dependency)."
read_when:
  - 企业制定数据跨境传输计划前的合规自检
  - 安全/法务审批个人信息出境业务方案时风险评估
  - 监管预警/内部审计验证《数据安全法》义务落实
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [data-export-check, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/data_export_check.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS; 1=FAIL/warnings; 2=usage error"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. Before an enterprise builds a cross-border data transfer plan, confirm the compliance self-check is done.
2. Security / legal review of business plans involving personal-information export.
3. Regulatory alert or internal audit requiring verification of Data Security Law obligations.

### Usage
Run `data_export_check.py` directly; no extra deps. Customize data type, target region, sensitivity grade via params. Output includes an overall compliance score and a missing-items list.

### Flow
1. Collect data metadata (classification, purpose, target country).
2. Run `data_export_check.py` with the check params.
3. Compare status against the five obligations (grading / consent / PIA / contract-or-assessment / record-keeping).
4. Any missing item → FAIL with a report.
5. Fix gaps or add the required legal documents.
6. All pass → lift the block and proceed with export.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 企业在制定数据跨境传输计划前，需确认是否完成合规性自检。
2. 安全或法务部门在审批涉及个人信息出境的业务方案时进行风险评估。
3. 发生监管预警或内部审计要求验证《数据安全法》相关义务落实情况时。

### 用法
本技能直接调用 Python 脚本 `data_export_check.py`，无需额外安装库包。主入口为内置的自检函数，支持参数自定义输入，包括待导出数据类型、目标区域及敏感等级。返回结果将包含综合合规评分及具体的缺失项清单。

### 流程
1. 收集待出境数据的元信息（包含内容分级、用途描述及目标国家）。
2. 调用 `data_export_check.py` 运行自检逻辑，传入相关检查参数。
3. 系统根据五项义务（分级/同意/PIA/合同评估/留痕）逐项比对现状。
4. 获取执行结果，若任何项缺失则自动判定为 FAIL 并生成报告。
5. 针对 Fail 结果修复遗漏合规措施或补充必要的法律文件。
6. 确认所有检查项通过后方可解除限制并进入正式数据出境操作环节。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
