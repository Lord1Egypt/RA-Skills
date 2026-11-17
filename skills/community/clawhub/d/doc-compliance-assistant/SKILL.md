---
name: doc-compliance-assistant
description: 文档合规处理助手 — 清洗+合规扫描一体：编码探测/BOM/换行/空白归一化后，一次扫描 PII（邮箱/手机号/身份证）、密钥（GitHub/AWS/OpenAI/私钥）、URL 内嵌口令，输出脱敏命中报告。当你要发布/外发/归档文档前做合规自检时使用；触发词：doc-compliance、文档合规、发前扫描、PII 扫描、密钥泄漏检查。
slug: doc-compliance-assistant
title: doc-compliance-assistant
version: 1.0.0
display_name: 文档合规处理助手
display_name_en: Doc Compliance Assistant
agent_created: true
author: SynomosAI contributors
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内
allowed-tools: Read, Glob, Grep, Bash, Write
category: 安全与合规
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "文档合规处理助手 — 清洗+合规扫描一体：编码探测/BOM/换行/空白归一化后，一次扫描 PII（邮箱/手机号/身份证）、密钥（GitHub/AWS/OpenAI/私钥）、URL 内嵌口令，输出脱敏命中报告。"
description_en: "Document processing with compliance built-in: normalize encoding/BOM/line-endings/whitespace, then scan in one pass for PII (email/CN-mobile/CN-ID), secrets (GitHub/AWS/OpenAI tokens, private keys, URL basic-auth), and IPs — emits a masked-hit report before the document leaves your machine."
read_when:
  - 文档/Markdown/草稿要外发、贴 Issue、归档或入库前做合规自检
  - 怀疑配置/日志/导出文件里混进了邮箱、手机号、身份证、API Key
  - 需要批量归一化 BOM/CRLF/尾部空白同时拿到一份命中清单
  - 想要机器可读 JSON 命中报告（--json）接入 CI 或 pre-commit
classification:
  skillhub: ["security", "productivity"]
  clawhub: ["security", "productivity"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "本地读文件+正则扫描+写归一化副本，最小权限；不联网、不回传任何命中内容（命中即掩码）；密钥不落地不打印明文。"
tags: [doc-compliance, pii-scan, secret-scan, 合规, 文档处理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/doc_compliance.py
  runtime: python3
  call_pattern: args
input_schema:
  file:
    type: string
    description: "输入文本/Markdown 文件路径"
    required: true
  out:
    type: string
    description: "--clean 时写入归一化副本的路径"
    required: false
  clean:
    type: bool
    description: "同时输出归一化副本（BOM 剥离/CRLF→LF/去尾部空白/Tab→4 空格）"
    required: false
  json:
    type: bool
    description: "机器可读 JSON 输出"
    required: false
  list-rules:
    type: bool
    description: "打印全部扫描规则并退出"
    required: false
output_schema:
  stdout: 命中报告（人类可读表格 或 --json 结构化 IR）
  exit_code: rc=0 干净 / rc=1 有命中 / rc=2 用法错误
capabilities:
  - document
  - compliance
  - desensitization
permissions:
  network: false
  filesystem: true
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.0: initial bilingual release (EN-first, ZH after); pure stdlib; 9 scanner rules"
---

# doc-compliance-assistant

## English

**doc-compliance-assistant** v1.0.0 · LGD-Powered security/productivity family · zero-dependency

### The pain
You finish a draft, a config dump, a log export — and then you wonder: *did I accidentally paste a phone number, a bearer token, or an internal IP into something I'm about to send out?* Anthropics' official docx/pdf skills are pure format converters; they never look at content. This skill fuses normalization and compliance into one pass so you don't ship a document and *then* find the leak.

### When to use
- Before a document / Markdown draft / log export / config dump is shared, posted to an issue, archived, or committed.
- You suspect PII or credentials leaked into a text file (email, CN mobile, CN ID card, GitHub/AWS/OpenAI tokens, private key blocks, URLs with embedded basic-auth, IPs).
- You want BOM / CRLF / trailing-whitespace normalization **and** a hit list in the same run.
- You need a machine-readable JSON report (`--json`) to wire into CI or a pre-commit hook.

### Usage
```bash
python scripts/doc_compliance.py --file path/to/draft.md
python scripts/doc_compliance.py --file path/to/draft.md --json
python scripts/doc_compliance.py --file path/to/draft.md --clean --out normalized.txt
python scripts/doc_compliance.py --list-rules
```
- rc=0 clean · rc=1 findings (any) · rc=2 usage error
- Hits are **masked** in output (`con***com`, `ghp***bcd`) — never printed in plaintext.

### Workflow
1. Trigger: identify a pre-send / pre-commit document review (see When to use).
2. Execute: run `doc_compliance.py` per Usage. Default is scan-only; add `--clean --out` to also emit a normalized copy.
3. Verify: read the masked hit list. If `findings_secret > 0`, treat as a block until the source file is scrubbed.
4. Deliver: present the report; the cleaned copy is a convenience, not an auto-redaction — the tool does **not** rewrite secrets inside your text, it only flags them.

### Example
```
$ python scripts/doc_compliance.py --file examples/sample-input.md
file: examples/sample-input.md ｜ encoding: utf-8 ｜ chars: 306
findings: 5 (secret=2 pii=2 info=1)
  - [PII] email line=3 match=con***com
  - [PII] cn_mobile line=3 match=138***000
  - [secret] aws_access_key line=5 match=AKI***PLE
  - [secret] github_token line=6 match=ghp***bcd
  - [info] ipv4 line=9 match=192***.10
```

### Design boundary
This is a **local, offline** scanner. It does not call any API, does not upload content, and does not auto-redact. It is a stop-gate, not a DLP pipeline. For regulated pipelines pair it with a real DLP; this skill exists so the cheap 80% case (obvious secrets / PII) never leaves the editor unwatched.

### Disclaimer
Security aid only. Regex scanners have false negatives; treat a clean run as "no obvious patterns", not "this document is safe".

## 中文

**doc-compliance-assistant** v1.0.0 · LGD-Powered 安全合规家族 · 零依赖

### 痛点
草稿、配置导出、日志文件写完了，转头就犯嘀咕：我是不是把手机号、Bearer Token、内网 IP 不小心贴进了马上要发出去的东西里？anthropics 官方 docx/pdf 件只做格式转换，从不看内容。本技能把归一化和合规扫描压成一遍，避免"发出去之后才发现泄漏"。

### 何时用
- 文档 / Markdown 草稿 / 日志导出 / 配置 dump 外发、贴 Issue、归档、提交前。
- 怀疑文本里混进了 PII 或凭证（邮箱、手机号、身份证、GitHub/AWS/OpenAI Token、私钥块、URL 内嵌 basic-auth、IP）。
- 需要 BOM / CRLF / 尾部空白归一化**同时**拿到一份命中清单。
- 想要机器可读 JSON 报告（`--json`）接 CI 或 pre-commit。

### 用法
```bash
python scripts/doc_compliance.py --file path/to/draft.md
python scripts/doc_compliance.py --file path/to/draft.md --json
python scripts/doc_compliance.py --file path/to/draft.md --clean --out normalized.txt
python scripts/doc_compliance.py --list-rules
```
- rc=0 干净 · rc=1 有命中 · rc=2 用法错误
- 命中在输出里**掩码显示**（`con***com`、`ghp***bcd`），绝不打印明文。

### 流程
1. 触发：识别外发/提交前文档复核任务（见「何时用」）。
2. 执行：按「用法」运行 `doc_compliance.py`。默认只扫描；加 `--clean --out` 同时输出归一化副本。
3. 校验：读掩码命中清单。若 `findings_secret > 0`，视为阻断，直到源文件被清干净。
4. 交付：呈现报告；归一化副本是便利输出，**不是**自动脱敏——工具只标记，不替你改原文里的密钥。

### 实例
```
$ python scripts/doc_compliance.py --file examples/sample-input.md
file: examples/sample-input.md ｜ encoding: utf-8 ｜ chars: 306
findings: 5 (secret=2 pii=2 info=1)
  - [PII] email line=3 match=con***com
  - [PII] cn_mobile line=3 match=138***000
  - [secret] aws_access_key line=5 match=AKI***PLE
  - [secret] github_token line=6 match=ghp***bcd
  - [info] ipv4 line=9 match=192***.10
```

### 设计边界
本地、离线扫描。不调任何 API、不上传内容、不自动脱敏。它是一道闸门，不是 DLP 流水线。受监管流水线请叠真 DLP；本技能存在的意义是把"明显密钥/PII"这便宜的 80% 挡在编辑器里。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

### 免责
本工具为安全辅助。正则扫描有误报漏报；rc=0 表示"未命中明显模式"，不等于"文档绝对安全"。
