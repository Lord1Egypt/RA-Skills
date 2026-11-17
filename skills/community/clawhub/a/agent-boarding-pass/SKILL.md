---
name: agent-boarding-pass
description: agent-boarding-pass — 给任何 AI 智能体签发一张可验证的『登机牌』：身份 + 证据哈希 + 权限白名单 + 有效期，SHA-256 防篡改；一条命令验真（指纹重算 + 过期校验）。可整张贴进 system prompt / 仓库 / 工单。 适用场景：当需要智能体登机牌能力时使用本技能；触发词：agent-boarding-pass。
slug: agent-boarding-pass
title: agent-boarding-pass
version: 1.0.1
display_name: 智能体登机牌
display_name_en: Agent Boarding Pass
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "agent-boarding-pass — 给任何 AI 智能体签发一张可验证的『登机牌』：身份 + 证据哈希 + 权限白名单 + 有效期，SHA-256 防篡改；一条命令验真（指纹重算 + 过期校验）。可整张贴进 system prompt / 仓库 / 工单。"
description_en: "Issue verifiable boarding passes for AI agents: identity + evidence hashes + permission allowlist + expiry, SHA-256 tamper-evident, one-command verification."
read_when:
  - 向外部 AI 智能体授予临时访问权限或验证其身份
  - 敏感数据交互需确认通信方在权限白名单内
  - 给第三方协作系统签发含身份凭证/证据哈希/有效期的安全票据
  - 一条命令重算指纹+过期校验验真
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [agent-boarding-pass, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/agent_boarding_pass.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: agent
    type: string
    description: 签发模式：智能体标识
    required: false
  - name: verify
    type: string
    description: 验真模式：登机牌 JSON（内联/@文件/路径）
    required: false
  - name: evidence
    type: list
    description: 证据键值（键以 l1-/l2-/l3- 开头）
    required: false
  - name: allow
    type: list
    description: 允许动作白名单
    required: false
  - name: ttl
    type: int
    description: 有效时长小时，默认72
    required: false
  - name: out
    type: string
    description: 登机牌输出路径
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 登机牌 JSON 或验真结论
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - identity
  - agent_credential
  - verification
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
- Granting temporary access to an external AI agent or verifying its identity.
- Sensitive-data exchange where the counterparty must be on a permission allowlist.
- Issuing a security ticket with full identity credentials, evidence hashes and expiry to third-party collaboration systems.

### Usage
Core script: `agent_boarding_pass.py` (in the skill dir).
- `--agent-id`: target agent unique identifier (identity binding).
- `--permissions`: allowlist JSON string defining permitted operations.
- `--expiry-hrs`: validity window (default 24h).
Run it to produce a text block with a SHA-256 tamper-evident fingerprint — embeddable in a system prompt or attachable to a ticket.

### Flow
1. Confirm agent identity and business permission needs.
2. Run `agent_boarding_pass.py` to compute evidence hashes and fingerprint.
3. Verify the pass contains expiry, allowlist and SHA-256 signature fields.
4. Inject the credential into a system prompt or upload to repo/ticket as trust anchor.
5. The receiving agent recomputes the fingerprint and checks expiry before executing.
6. Only after permission match and non-expiry is access granted.

### Evidence & safety
- Evidence: TBD.
- Version: 1.0.1
- Security: no independent scan (TBD).

## 中文

### 何时用
- 需要向外部 AI 智能体授予临时访问权限或验证其身份时。
- 涉及敏感数据交互，需确保通信方属于特定权限白名单的场景。
- 生成包含完整身份凭证、证据哈希及有效期的安全票据给第三方协作系统。

### 用法
- 核心调用脚本：`agent_boarding_pass.py`（位于技能包目录）。
- `--agent-id`: 目标智能体唯一标识符。
- `--permissions`: 权限白名单 JSON。
- `--expiry-hrs`: 凭证有效期（默认 24 小时）。

### 流程
1. 确认智能体身份标识及业务权限需求参数。
2. 调用 `agent_boarding_pass.py` 执行凭证生成逻辑，计算证据哈希与指纹。
3. 验证生成的登机牌包含有效期、白名单及 SHA-256 签名字段。
4. 将凭证文本注入系统提示词或上传至仓库/工单系统作为信任依据。
5. 接收方智能体执行任务前进行指纹重算与过期校验。
6. 确认权限匹配且未过期后，允许访问敏感数据或执行指定操作。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
