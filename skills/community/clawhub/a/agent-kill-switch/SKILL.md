---
name: agent-kill-switch
description: agent-kill-switch — 部署智能体前生成『制动卡』：停止条件/断权动作/责任人/恢复条件；--check 校验制动卡字段齐全，缺项 rc=1 不许上线。 适用场景：当需要智能体紧急制动卡能力时使用本技能；触发词：agent-kill-switch。
slug: agent-kill-switch
title: agent-kill-switch
version: 1.0.1
display_name: 智能体紧急制动卡
display_name_en: Agent Kill Switch
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "agent-kill-switch — 部署智能体前生成『制动卡』：停止条件/断权动作/责任人/恢复条件；--check 校验制动卡字段齐全，缺项 rc=1 不许上线。"
description_en: "Generate a kill card before deploying an agent: stop conditions, revocation actions, owner, recovery conditions; --check validates completeness and blocks launch on missing fields."
read_when:
  - 智能体上线前安全准入评审需制动卡完整性校验
  - 敏感数据/资金处理/高危任务部署前
  - 缺失「停止条件」或「恢复条件」等风控要素时
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [agent-kill-switch, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/agent_kill_switch.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: agent
    type: string
    description: 生成模式：智能体名
    required: false
  - name: check
    type: string
    description: 校验模式：制动卡 JSON
    required: false
  - name: conditions
    type: list
    description: 停止条件（多条）
    required: false
  - name: revoke
    type: string
    description: 断权动作（撤 key/断网/停容器）
    required: false
  - name: owner
    type: string
    description: 责任人
    required: false
  - name: recovery
    type: string
    description: 恢复条件
    required: false
  - name: out
    type: string
    description: 输出路径
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 制动卡 JSON 或校验结论
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - kill_switch
  - safety
  - incident_response
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
1. Pre-launch security admission review: mandatory kill-card field completeness check.
2. Before deploying agents handling sensitive data, funds or high-risk tasks.
3. When stop conditions / recovery conditions are missing from the system config.

### Usage
1. Core script: `agent_kill_switch.py` — `python agent_kill_switch.py --check`.
2. Params: `--input-config` (kill-card file path), `--skip-check` (local testing only).
3. Verdict: rc=0 fields complete and validated; rc=1 missing fields — launch blocked.

### Flow
1. **Define the kill card**: config with stop conditions, revocation actions, owner, recovery conditions.
2. Ensure `agent_kill_switch.py` is available.
3. Run `python agent_kill_switch.py --check --input-config <file>` in the deploy tool.
4. Watch output: rc=1 → kill card missing or invalid.
5. Fix config per error messages until all required fields are present.
6. Re-run check (rc=0) → sign deployment release.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 在智能体上线前的安全准入评审阶段，需强制进行制动卡字段完整性验证。
2. 涉及敏感数据操作、资金处理或高危任务执行的关键业务场景部署前。
3. 当系统配置缺失「停止条件」或「恢复条件」等关键风控要素时。

### 用法
1. 核心脚本：`agent_kill_switch.py`，调用方式为 `python agent_kill_switch.py --check`。
2. 参数说明：`--input-config`（制动卡文件路径），`--skip-check`（仅用于本地测试跳过验证）。
3. 结果判断：字段齐全且通过校验返回 `0`，缺项失败返回 `1` 不许上线。

### 流程
1. **定义制动卡**：编写包含停止条件、断权动作、责任人、恢复条件的配置数据。
2. **导入脚本路径**：确保环境已安装 `agent_kill_switch.py`。
3. **执行检查命令**：`python agent_kill_switch.py --check --input-config <file>`。
4. **获取校验反馈**：rc=1 则判定制动卡缺失或无效。
5. **修正配置数据**：根据报错提示补全缺失字段。
6. **确认上线授权**：rc=0 后生成部署签名放行。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
