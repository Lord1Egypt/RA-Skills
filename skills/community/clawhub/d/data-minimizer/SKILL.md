---
name: data-minimizer
description: data-minimizer — 把文本里的手机号/邮箱/证件号/长号/指定人名一键打码后交给 AI，输出脱敏文本+脱敏报告；支持 --names 自定义人名、--json。 适用场景：当需要给AI前脱敏器能力时使用本技能；触发词：data-minimizer。
slug: data-minimizer
title: data-minimizer
version: 1.0.1
display_name: 给AI前脱敏器
display_name_en: Data Minimizer
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "data-minimizer — 把文本里的手机号/邮箱/证件号/长号/指定人名一键打码后交给 AI，输出脱敏文本+脱敏报告；支持 --names 自定义人名、--json。"
description_en: "Mask phone numbers, emails, ID numbers, long digits and names before handing text to AI; outputs masked text plus masking report; supports --names and --json."
read_when:
  - 发送含手机号/邮箱/证件号/长号的文本给外部 AI 模型前
  - 文档处理流程涉及隐私合规，需对人名及敏感标识匿名化
  - 工作流需同时获取脱敏文本与脱敏报告以备审计
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [data-minimizer, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/data_minimizer.py
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
Before sending text containing phone numbers, emails, ID numbers or long digit strings to an external AI model. When document processing involves privacy compliance and named entities must be anonymized. When the workflow needs both the cleaned text and a masking report for audit.

### Usage
Run `python data_minimizer.py --input_text <text> --output_format json`. `--names` takes a custom name list (e.g. `['Zhang San']`); `--json` enables structured output.

### Flow
1. Prepare the raw text; confirm it contains sensitive info to protect.
2. Configure params; add `--names` for custom-name masking.
3. Run the script; it scans for sensitive data.
4. On completion, replace detected items with masks and generate the report.
5. Read the final output; JSON mode returns a structured result for downstream use.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
当您需要将包含手机号、邮箱、证件号或长号码的文本发送给外部 AI 模型前；当文档处理流程涉及隐私合规，需对指定人名及敏感标识进行匿名化处理时；当您希望在工作流中同时获取脱敏后的干净文本及详细的脱敏报告记录以备审计。

### 用法
执行命令：`python data_minimizer.py --input_text <待处理内容> --output_format json`。支持参数说明：`--names` 用于传入需要脱敏的自定义人名列表（如 `['张三']`），`--json` 用于启用 JSON 结构化输出模式以返回报告数据。

### 流程
1. 准备待处理的原始文本内容，确认其中包含需保护的敏感信息。
2. 根据需求配置参数，若涉及特定人名脱敏请添加 `--names` 列表。
3. 在终端执行命令启动脚本，系统将读取输入并开始扫描敏感数据。
4. 等待处理完成，系统自动将识别到的敏感项进行掩码替换并生成报告。
5. 获取最终输出，若开启了 JSON 模式则直接获得结构化结果用于后续调用。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
