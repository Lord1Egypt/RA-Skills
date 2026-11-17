---
name: agent-output-registry
slug: agent-output-registry
title: agent-output-registry
display_name: AI 产出有籍登记器（LGD-I 有籍）
display_name_en: "Agent Output Registry (LGD-I Registered)"
description: "当用户要『给 AI 产出溯源 / IP 归属 / 防篡改 / 审计留痕』，或担心『AI 生成内容说不清来源、被改了认不出、权属扯不清』时用。给每条 AI 产出发一张『籍』(户口)：SHA-256 指纹 + 模型/版本/提示哈希 + 时间戳 + 权属，写入本地台账；支持 verify 证完整性、lookup 查归属、report 列全部。这是 LGD-I 有籍的落地执行器——把抽象的『有籍』变成每条产出可查的户口。触发词：AI 产出溯源、AI 内容登记、IP 归属、产出指纹、防篡改、审计留痕、有籍、产出户口。"
version: 1.0.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
read_when:
  - 用户要追溯某条 AI 产出的来源、模型、版本、提示
  - 用户担心 AI 内容被篡改、权属不清、审计无据
  - 做 AI 资产管理、合规留痕、知识产权保护
  - 要落地「凡造必登」的有籍原则
tags: [LGD, 有籍, 溯源, IP归属, 防篡改, 审计留痕, AI产出, 户口, 指纹]
copyright: SynomosAI
description_zh: "当用户要『给 AI 产出溯源 / IP 归属 / 防篡改 / 审计留痕』，或担心『AI 生成内容说不清来源、被改了认不出、权属扯不清』时用。给每条 AI 产出发一张『籍』(户口)：SHA-256 指纹 + 模型/版本/提示哈希 + 时间戳 + 权属，写入本地台账；支持 verify 证完整性、lookup 查归属、report 列全部。这是 LGD-I 有籍的落地执行器——把抽象的『有籍』变成每条产出可查的户口。触发词：AI 产出溯源、AI 内容登记、IP 归属、产出指纹、防篡改、审计留痕、有籍、产出户口。"
description_en: "Register every AI output with a household-register entry (LGD-I): SHA-256 fingerprint + model/version/prompt provenance for IP attribution, tamper evidence and audit trails."
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/output_registry.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: command
    type: string
    description: 子命令：add|verify|lookup|report
    required: true
  - name: out
    type: string
    description: 登记库路径（add 必填）
    required: false
  - name: model
    type: string
    description: 产出所用模型
    required: false
  - name: version
    type: string
    description: 版本号
    required: false
  - name: prompt
    type: string
    description: 提示词摘要
    required: false
  - name: issuer
    type: string
    description: 签发方
    required: false
  - name: license
    type: string
    description: 许可
    required: false
  - name: id
    type: string
    description: 登记 ID（verify/lookup 必填）
    required: false
output_schema:
  stdout: 登记记录 / 校验结论 / 台账报告
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - output_registry
  - provenance
  - audit_trail
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
1. Verify the integrity/authenticity of AI-generated text, code or data against later tampering.
2. Compliance scenarios: copyright protection, model attribution, audit trails — record IP source and timestamps.
3. The user worries AI output has unclear provenance or can't be recognized after modification.

### Usage
1. `python output_registry.py --register` — submit output with model version hash, prompt fingerprint and ownership.
2. `python output_registry.py --verify <record_id>` — check the SHA-256 fingerprint hasn't been tampered with.
3. `python output_registry.py --lookup <content_hash>` — find owner, generation time and logs.
4. `python output_registry.py --report` — list all registered records and the full index.

### Flow
1. After an AI task, compute the SHA-256 fingerprint of the final output as the unique ID.
2. `register`: write model version, prompt hash and timestamp into the local ledger.
3. `lookup` by record ID for attribution.
4. Periodic `verify`: check entries stay intact and hash-consistent.
5. `report` exports the full audit list for external compliance review.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 当需要验证 AI 生成内容（文本、代码或数据）的完整性与真实性，防止后续被篡改时。
2. 在涉及版权保护、模型归属权确认或审计留痕的合规场景中，需明确产出的 IP 来源与时间戳时。
3. 面对用户担忧 AI 输出内容模糊来源、或被修改后难以识别风险的情况。

### 用法
1. 执行 `python output_registry.py --register` 提交产出，需传入模型版本哈希、提示词指纹及权属信息。
2. 使用 `python output_registry.py --verify <record_id>` 验证指定记录号的 SHA-256 指纹是否未被篡改。
3. 调用 `python output_registry.py --lookup <content_hash>` 检索某条产出内容的归属者、生成时间及详细日志。
4. 通过 `python output_registry.py --report` 输出当前台账中的所有注册记录及完整索引列表。

### 流程
1. AI 任务执行完毕，提取最终输出内容并计算 SHA-256 指纹作为唯一标识。
2. 调用脚本执行 `register` 动作，将模型版本、提示词哈希与时间戳写入本地台账。
3. 如需溯源，通过 `lookup` 命令输入记录 ID 查询具体权属信息。
4. 定期使用 `verify` 检查台账条目是否保持完整性及哈希一致性。
5. 最终利用 `report` 导出完整审计清单，供外部系统或合规审核使用。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
