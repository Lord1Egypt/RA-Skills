---
name: ai-content-discloser
description: ai-content-discloser — 为 AI 参与（全生成/辅助/混合）的内容一键生成合规披露声明：显式声明（中/EN）+ 隐式元数据标注 + 平台贴法，依据中国《人工智能生成合成内容标识办法》与 EU AI Act 第 50 条口径。 适用场景：当需要AI 内容披露生成器能力时使用本技能；触发词：ai-content-discloser。
slug: ai-content-discloser
title: ai-content-discloser
version: 1.0.1
display_name: AI 内容披露生成器
display_name_en: AI Content Discloser
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "ai-content-discloser — 为 AI 参与（全生成/辅助/混合）的内容一键生成合规披露声明：显式声明（中/EN）+ 隐式元数据标注 + 平台贴法，依据中国《人工智能生成合成内容标识办法》与 EU AI Act 第 50 条口径。"
description_en: "One-click compliant disclosure for AI-involved content: explicit statements (zh/en) + implicit metadata labeling + platform placement, per China's AI-generated content labeling rules and the EU AI Act."
read_when:
  - 发布 AIGC 内容需加显式/隐式标识（中国《标识办法》/EU AI Act 第 50 条）
  - 跨境平台或自媒体统一披露声明格式
  - 需一键生成中英双语披露模板与元数据标注
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
standards_ref: ["EU AI Act"]
tags: [ai-content-discloser, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/ai_content_discloser.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: type
    type: string
    description: 内容类型（choices）
    required: true
  - name: ai-level
    type: string
    description: AI 参与度等级
    required: true
  - name: brand
    type: string
    description: 署名/品牌
    required: false
  - name: tool
    type: string
    description: AI 工具名
    required: false
  - name: platform
    type: string
    description: 发布渠道，默认 generic
    required: false
  - name: date
    type: string
    description: 披露日期
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 合规披露文本
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - content_disclosure
  - compliance
  - aigc
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
Publishing text, video or audio with deep AI involvement (fully generated, assisted, hybrid) — especially for domestic Chinese platforms or cross-border distribution. Use when content must carry mandatory labels under China's AI-generated content labeling rules, or when EU-market transparency duties (EU AI Act Art. 50) apply. Also used by self-media outlets and professional media to standardize disclaimers and metadata across AI tools.

### Usage
Run `python ai_content_discloser.py --mode auto --language cn_en --input_file content.txt`. Params: `--input` (content file), `--lang` (cn/en combo), `--include_metadata` (metadata injection). As a module, invoke from CLI pointing stdin or a local file.

### Flow
1. Confirm the creation mode (fully generated / assisted / hybrid); prepare source asset.
2. Run `ai_content_discloser.py` with platform and language params.
3. Auto-detect AI involvement level; generate explicit zh + en statements.
4. Write implicit metadata (model ID, generation time) into header/footer.
5. Platform-adapt the statement (e.g. social watermark rules).
6. Verify labels + metadata are complete; export the publish-ready file.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
适用于发布由 AI 深度参与（全生成、辅助或混合模式）的文本、视频或音频内容，特别是涉及国内互联网平台或跨境传播场景。当内容依据《人工智能生成合成内容标识办法》需添加强制标签时，用于满足合规披露要求。若发布目标包括欧盟市场且需符合 AI Act 第 50 条关于透明度与说明的义务，本技能可作为一键生成标准模板的工具。此外，在自媒体运营或专业媒体机构中，用于统一不同 AI 创作产品的免责声明格式和元数据结构。

### 用法
主要通过调用 Python 脚本 `ai_content_discloser.py` 进行自动化处理，无需前端界面支持。运行命令示例为 `python ai_content_discloser.py --mode auto --language cn_en --input_file content.txt`，支持参数 `--input` 指定内容来源文件、`--lang` 选择输出语言组合（cn/en）、`--include_metadata` 开启元数据注入功能。作为技能模块时，可直接通过命令触发执行，将输入内容指向标准输入或本地文件路径。

### 流程
1. 确认待发布内容的创作方式（全生成/辅助/混合），并准备好原始素材文件。
2. 执行 `python ai_content_discloser.py`，配置必要参数以确定目标平台及语言环境。
3. 系统自动识别 AI 介入程度，生成对应的中文与英文显式声明文本。
4. 根据需求将隐式元数据（如模型 ID、生成时间）写入内容头部或脚注。
5. 对声明文本进行平台适配格式化处理，例如添加社交媒体特定水印规则。
6. 检查最终生成的合规文件是否包含完整的标签信息与元数据，导出发布准备版。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
