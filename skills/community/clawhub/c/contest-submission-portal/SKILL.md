---
name: contest-submission-portal
slug: contest-submission-portal
displayName: 赛事作品提交合规校验器
version: 1.1.2
category: ai-agent
display_name: 赛事作品提交合规校验器
title: 赛事作品提交合规校验器
author: 诺声(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事作品提交合规校验器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-001域。 适用场景：当需要赛事作品提交合规校验器能力时使用本技能；触发词：赛事、判定器、TH-EVT-001、contest-submission-portal。
tags: [赛事, 判定器, TH-EVT-001, contest-submission-portal]
description_zh: "赛事作品提交合规校验器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-001域。"
description_en: "Contest submission compliance validator: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-001)."
read_when:
  - UIBC 赛事作品提交前的合规预检
  - 按 TH-EVT-001 域规范做标准化决策支持
  - 输出可直接解析的 JSON IR 衔接后续系统/上报平台
classification:
  skillhub: ["community-events"]
  iso_25010: ["Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
platforms: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: contest-submission-portal.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: demo
    type: bool
    description: 内置冒烟案例
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 提交合规校验 JSON IR（Pass/Fail+违规详情）
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - contest
  - compliance
  - submission
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.2: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
Pre-submission compliance check for UIBC contest entries in a zero-dependency environment. Standardized decision support for TH-EVT-001 domain rules, with parseable JSON IR output for downstream systems / reporting platforms.

### Usage
No external script call. Provide the work's metadata, the domain tag (TH-EVT-001) and the check mode. As a doc-style skill, structured JSON data drives the internal rule engine; the output is a standardized JSON IR.

### Flow
1. Prepare the submission info as a standard JSON object.
2. Tag the request with the TH-EVT-001 domain rule.
3. Run the zero-dependency UIBC-spec parsing and compliance check.
4. Emit a JSON IR with status code, violation details and fix suggestions.
5. Per the Pass/Fail flag, confirm submission eligibility or trigger the fix loop.

### Evidence & safety
- Evidence: TBD. Version: 1.1.2. Security: no independent scan (TBD).

## 中文

### 何时用
本技能适用于在零依赖环境下执行 UIBC 赛事作品提交前的合规预检。当需要针对 TH-EVT-001 域内的具体规范进行标准化决策支持时，特别是在确保输出结果为可直接解析的 JSON IR 格式以衔接后续系统或上报平台的情况下。

### 用法
无需调用任何外部脚本文件，通过定义输入参数来激活技能逻辑。请提供包含元数据的"作品原始信息"、"适用领域标签（指定 TH-EVT-001）"及"校验模式"。作为文档型技能，用户可仅通过传入结构化的 JSON 数据触发内部规则引擎，输出将自动以标准化 JSON IR 格式返回。

### 流程
1. 用户准备待提交作品信息并将其转换为符合预期的标准 JSON 对象。
2. 在系统请求中明确指定 TH-EVT-001 域规则标签。
3. 技能内部执行基于 UIBC 赛事规范的零依赖解析与合规性校验。
4. 生成包含状态码、违规详情及修正建议的 JSON IR 响应。
5. 依据返回结果中的 Pass/Fail 标记确认提交资格或触发作品修正流程。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
