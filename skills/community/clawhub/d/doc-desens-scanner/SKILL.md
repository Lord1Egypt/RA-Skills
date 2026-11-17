---
name: doc-desens-scanner
display_name: 文档智能去敏（Desens Scanner）
display_name_en: "Document Desensitization Scanner"
description: "当用户说『这篇文档有敏感信息要发出去』『先脱敏再发』『别把内部路径/密钥/人名露出去』『对外发布前扫一遍隐私』，或要把文档/代码/日志对外前做去敏时使用。扫描 个人标识(PII)·密钥·内部路径·内部项目代号 四类敏感项并打码/留痕，输出去敏版+清单（有证：脱敏动作可审计）。可运行脚本（desens_scan 扫描器）。理论根基：LGD 三律之有证（脱敏留痕，可追责）。触发词：去敏、脱敏、desensitize、脱敏扫描、隐私打码、密钥泄露、内部路径、对外发布前检查、PII。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
category: AI安全
platforms: [windows, macos, linux]
read_when:
  - 文档/代码/日志要对外发布或发给客户前
  - 担心泄露密钥、内部路径、人名、内部项目代号
  - 要做隐私合规的发布前检查
  - 收到「先脱敏」类指令
tags: [去敏, 脱敏, desensitize, 隐私打码, PII, 密钥, 发布前检查]
slug: doc-desens-scanner
title: 文档智能去敏（Desens Scanner）
copyright: SynomosAI
description_zh: "当用户说『这篇文档有敏感信息要发出去』『先脱敏再发』『别把内部路径/密钥/人名露出去』『对外发布前扫一遍隐私』，或要把文档/代码/日志对外前做去敏时使用。扫描 个人标识(PII)·密钥·内部路径·内部项目代号 四类敏感项并打码/留痕，输出去敏版+清单（有证：脱敏动作可审计）。可运行脚本（desens_scan 扫描器）。理论根基：LGD 三律之有证（脱敏留痕，可追责）。触发词：去敏、脱敏、desensitize、脱敏扫描、隐私打码、密钥泄露、内部路径、对外发布前检查、PII。"
description_en: "Scan documents, code and logs for PII, secrets, internal paths and project codenames before external release, with masking suggestions for each finding."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/desens_scan.py
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
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
Use it when the user plans to share a document, piece of code or log externally; when content might contain internal paths or leaked secrets and needs checking; and when a pre-release privacy-compliance self-check is required to make sure no personal identifiers (PII) or other sensitive data goes out.

### Usage
Call the core script `python desens_scan.py` with the target file path, e.g. `python desens_scan.py -i document.txt`. To customize the desensitization rules, add `--target-key [type]` (e.g. pii, key, path). The system reads the input content directly and scans / processes it.

### Workflow
Step 1: the user provides the raw document or code stream as input. Step 2: the engine loads `desens_scan.py` and parses the content in depth, identifying the four sensitive classes: PII, secrets, internal paths and internal codenames. Step 3: automatic masking (redact / replace) runs and a traceable processing record is generated. Step 4: the redacted content plus a full risk list is produced. Step 5: the audit log is attached when delivering the result, satisfying the theoretical root of "evidenced — accountable".

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.1.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
用户计划将文档、代码或日志对外共享时；发现内容可能存在内部路径、密钥泄露风险需要排查时；在发布前执行隐私合规自检，确保不包含个人标识（PII）及其他敏感信息时使用。

### 用法
调用核心脚本命令 `python desens_scan.py`，并传入目标文件路径参数 `[path]`，例如 `python desens_scan.py -i document.txt`。若需自定义脱敏规则，可添加参数 `--target-key [密钥类型]`（如 pii, key, path）；系统将直接读取输入内容进行扫描与处理。

### 流程
第一步：用户提供待处理的原始文档或代码流作为输入。第二步：技能引擎加载 `desens_scan.py` 脚本对内容进行深度解析，识别 PII、密钥、内部路径等四类敏感项。第三步：执行自动脱敏操作（打码/替换）并生成可追溯的处理记录。第四步：输出包含完整风险清单的脱敏版本内容。第五步：交付最终结果时附带审计日志，满足“有证可追责”的理论根基要求。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
