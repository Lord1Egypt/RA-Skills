---
name: fin-ai-classifier
slug: fin-ai-classifier
displayName: 金融 AI 应用分级判定器
version: 1.0.2
category: it-ops-security
display_name: 金融 AI 应用分级判定器
display_name_en: Financial AI Application Tiering Classifier
title: 金融 AI 应用分级判定器
author: 诺丰(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 金融 AI 应用分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-FIN-002域。 适用场景：当需要金融 AI 应用分级判定器能力时使用本技能；触发词：合规、判定器、TH-FIN-002、fin-ai-classifier。
tags: [合规, 判定器, TH-FIN-002, fin-ai-classifier, 金融AI, 分级]
description_zh: "金融 AI 应用分级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-FIN-002域。"
description_en: "Financial AI application tiering determination tool: zero-dependency decision support with JSON IR output (domain TH-FIN-002)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
platforms: [windows, macos, linux]
read_when:
  - 要对金融 AI 应用做快速合规分级（I/II/III 级），严格遵循 TH-FIN-002 官方规则
  - 处理高风险金融算法决策工具的准入审查或监管报送
  - 需要自动输出 JSON IR 报告接入统一监管标准接口
  - 用户说「这个 AI 放贷/荐股算几级」「金融 AI 要不要备案」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: fin-ai-classifier.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.2: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. When a fast compliance tier assessment of a financial AI application is needed, strictly following the official rules (TH-FIN-002 domain).
2. When handling admission reviews or regulatory filings involving high-risk financial algorithmic decision tools.
3. When the system must automatically output JSON IR reports to a unified regulatory standard interface.

### Usage
Because this skill is document-type with no script dependency, no external file needs to be loaded — trigger it directly from a workflow node. When calling, state clearly the financial AI application name under classification, its core function description and its domain. Key parameters: `application_id`, `feature_description` and `domain_scope` (defaults to TH-FIN-002); the system matches the rule base automatically and returns a JSON IR result.

### Workflow
1. The user or system workflow initiates the call, passing the financial application identifier and feature profile.
2. The internal engine retrieves the official rule sources and compliance metric set within the TH-FIN-002 domain.
3. Based on the input, it auto-computes the application's risk grade and dependency level.
4. The engine produces a technical-level response conforming to the JSON IR standard.
5. The result is returned for upper-layer systems to parse, for later decisions or regulatory filing interfaces.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.2
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed. This is AI-assisted decision support, not legal advice.

## 中文

### 何时用
1. 当需对金融 AI 应用的合规性进行快速分级评估，且需严格遵循官方规则（TH-FIN-002 域）时。
2. 在处理涉及高风险金融算法决策工具的准入审查或监管报送场景时。
3. 当系统需要自动化输出 JSON IR 格式的报告以接入统一监管标准接口时。

### 用法
由于本技能为文档型且无脚本依赖，调用方式无需加载外部文件，直接通过工作流节点触发。调用时需明确待分类的金融 AI 应用名称、核心功能描述及所属领域。关键参数支持传入 `application_id`、`feature_description` 与 `domain_scope`（默认为 TH-FIN-002），系统将依据规则库进行自动匹配并返回 JSON IR 结果。

### 流程
1. 用户或系统工作流发起调用请求，传入待评级的金融应用标识及功能特征。
2. 内部引擎检索 TH-FIN-002 域内的官方规则源与合规指标集合。
3. 基于输入数据对应用的风险等级与依赖程度进行自动化匹配计算。
4. 引擎生成符合 JSON IR 标准的技术级响应数据。
5. 返回结果供上层系统解析，用于后续决策或监管报送接口对接。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。本工具为 AI 辅助决策支持，非法律意见。
