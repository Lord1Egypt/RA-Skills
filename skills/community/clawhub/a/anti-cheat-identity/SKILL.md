---
name: anti-cheat-identity
slug: anti-cheat-identity
displayName: 赛事反作弊身份核验器
version: 1.1.2
category: ai-agent
display_name: 赛事反作弊身份核验器
title: 赛事反作弊身份核验器
author: 诺卫(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事反作弊身份核验器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-004域。 适用场景：当需要赛事反作弊身份核验器能力时使用本技能；触发词：赛事、判定器、TH-EVT-004、anti-cheat-identity。
tags: [赛事, 判定器, TH-EVT-004, anti-cheat-identity]
description_zh: "赛事反作弊身份核验器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-004域。"
description_en: "Contest anti-cheating identity verification tool: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-004)."
read_when:
  - UIBC 赛事报名/排位赛前参赛者身份真实性核验
  - 疑似违规账号、代练、身份存疑时零依赖复核
  - 需快速生成 TH-EVT-004 域反作弊决策报告
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
  entry_point: anti-cheat-identity.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: author_id
    type: string
    description: 作者标识
    required: true
  - name: env_hash
    type: string
    description: 环境指纹哈希
    required: true
  - name: prev_env_hashes
    type: string
    description: 历史环境指纹 JSON 数组
    required: false
  - name: submit_count
    type: int
    description: 提交次数
    required: false
  - name: time_gap_min
    type: int
    description: 距上次提交分钟
    required: false
  - name: demo
    type: bool
    description: 内置冒烟案例
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 风险等级+flags+advice 的 JSON IR
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - anti_cheat
  - identity_verify
  - contest
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
- Pre-registration / pre-rank identity verification for UIBC contestants.
- Suspected alt accounts, boosting, or questionable identity → zero-dependency review.
- Fast generation of a TH-EVT-004 anti-cheat decision report without local script setup.

### Usage
- Inputs: `event_id` (unique event ID), `participant_json` (contestant identity JSON), `policy_version`.
- Action: a doc-style tool; no external script directory required.
- Output: standardized JSON IR; inspect `verification_result`, `risk_level`.

### Flow
1. Initialize the call with event info, participant data and scope.
2. Parse and compare per UIBC spec; internal logic judgment.
3. Auto-compute risk factors; emit a TH-EVT-004-structured JSON response.
4. Read the JSON IR; check anti-cheat verdict tags.
5. Per `verification_status`: admit to the event or raise a warning.
6. Archive the verification record into the event security log.

### Evidence & safety
- Evidence: TBD. Version: 1.1.2. Security: no independent scan (TBD).

## 中文

### 何时用
- 适用于 UIBC 赛事报名或排位赛前的参赛者身份真实性核验场景。
- 当检测到潜在违规账号、代练行为或身份信息存疑时，提供零依赖的复核机制。
- 用于需要快速生成符合 TH-EVT-004 域要求的反作弊决策报告，且无需部署本地脚本环境的情况。

### 用法
- **输入参数**：必须传入 `event_id`（赛事唯一标识）、`participant_json`（参赛者身份信息 JSON）及 `policy_version`（政策版本）。
- **动作说明**：技能为文档型工具，不依赖外部脚本目录，直接通过接口调用执行逻辑。
- **输出获取**：读取系统返回的标准化 JSON IR 协议，重点关注 `verification_result`、`risk_level` 等字段以确认核验结论。

### 流程
1. 初始化调用请求，携带赛事信息、参与者身份数据及目标核验范围。
2. 执行文档解析与标准比对，依据 UIBC 赛事规范进行内部逻辑判断。
3. 系统自动计算风险因子并生成符合 TH-EVT-004 域结构的 JSON 响应。
4. 接收返回的 JSON IR 流，检查是否包含反作弊判定标签。
5. 根据 `verification_status` 字段决定是允许参赛还是触发警告提示。
6. 将核验记录归档至赛事安全日志，完成整个身份核验闭环。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
