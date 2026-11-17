---
name: data-grade-checker
slug: data-grade-checker
displayName: 数据分类分级判定器
version: 1.0.2
category: it-ops-security
display_name: 数据分类分级判定器
title: 数据分类分级判定器
author: 诺源(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 数据分类分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-DAT-001域。 适用场景：当需要数据分类分级判定器能力时使用本技能；触发词：合规、判定器、TH-DAT-001、data-grade-checker。
tags: [合规, 判定器, TH-DAT-001, data-grade-checker]
description_zh: "数据分类分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-DAT-001域。"
description_en: "Data classification and grading determination tool: zero-dependency decision support with JSON IR output (domain TH-DAT-001)."
read_when:
  - 新数据源接入系统前自动化合规初筛与风险预判
  - 数据资产盘点/审计快速评估敏感信息密度
  - 按 TH-DAT-001 域标准界定数据属性标签（L1-L4）
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
platforms: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: data-grade-checker.py
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
changelog: "1.0.2: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
- Automated compliance pre-screening / risk prediction before a new data source joins the system.
- Rapidly assess sensitive-info density during data-asset inventory or audit.
- Label data attributes (L1–L4) per TH-DAT-001 domain standards.

### Usage
- Input: pass the data sample and rule scope; no external script to load.
- Output: structured JSON IR, ready to embed in downstream decision chains.
- Doc-style skill: submit task description + data object via context; the internal rule engine reasons automatically.

### Flow
1. Receive the request; parse the raw data to grade.
2. Match the TH-DAT-001 classification & grading rule set.
3. Multi-condition validation and weighting over the internal doc knowledge base.
4. Emit a JSON IR with risk level and compliance verdict.

### Evidence & safety
- Evidence: TBD. Version: 1.0.2. Security: no independent scan (TBD).

## 中文

### 何时用
- 在新数据源接入系统前进行自动化合规初筛与风险预判。
- 在执行数据资产盘点或审计任务时，快速评估敏感信息密度。
- 需要依据 TH-DAT-001 域标准明确界定数据属性标签（L1-L4）的场景。

### 用法
- **输入参数**：直接传入待检数据样本及指定规则范围，无需加载外部脚本文件。
- **输出说明**：返回结构化 JSON IR 结果，默认支持嵌入到下游决策链路中。
- **调用方法**：作为文档型技能，通过指令上下文提交任务描述与数据对象，技能将自动检索内部规则库执行逻辑推理。

### 流程
1. 接收调用请求并解析待判定的原始数据内容。
2. 匹配 TH-DAT-001 域下的分类与分级核心规则集。
3. 基于内部文档知识库进行多条件校验与逻辑加权。
4. 生成包含风险等级与合规结论的 JSON IR 结果。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
