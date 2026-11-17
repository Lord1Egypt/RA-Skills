---
name: contract-interact-checklist
description: 合约交互风险清单 — 智能合约交互前六项风险自检（审计/地址/授权额度/撤销/私钥/小额试单），未完成即 FAIL（零依赖） 适用场景：当需要合约交互风险清单能力时使用本技能；触发词：contract-interact-checklist。
slug: contract-interact-checklist
title: contract-interact-checklist
version: 1.0.1
display_name: 合约交互风险清单
display_name_en: Contract Interact Checklist
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude, codex, cursor, windsurf, cli]
copyright: SynomosAI
description_zh: "合约交互风险清单 — 智能合约交互前六项风险自检（审计/地址/授权额度/撤销/私钥/小额试单），未完成即 FAIL（零依赖）"
description_en: "Six-item risk checklist before interacting with smart contracts: audit, address, allowance, revocation, private keys, small test transaction; incomplete FAIL (zero-dependency)."
read_when:
  - 智能合约交互前高风险自查（新合约部署前审计/第三方地址验证）
  - 涉及资金授权、大额转账时检查授权额度与撤销机制
  - 私钥保管与小额试单环节提前识别交互风险
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [contract-interact-checklist, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/contract_interact_checklist.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: have
    type: string
    description: 已完成项编号逗号串
    required: false
  - name: approve
    type: string
    description: 授权范围 limited|unlimited
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 智能合约交互前风险清单与放行结论
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - smart_contract
  - risk_checklist
  - web3
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
High-risk self-check before interacting with a smart contract: pre-deployment code audit or third-party address verification. Check allowance and revocation when authorizing funds or large transfers. Surface interaction risk around key custody and small test transactions.

### Usage
Run `contract_interact_checklist.py`; pass the target contract address and operation type (e.g. `--check audit,permission`). Any missing item → FAIL.

### Flow
1. Prepare the target contract address and interaction intent (transfer / approve).
2. Run the script in self-check mode.
3. Verify the six items in order: audit, address, allowance, revocation, private key, test tx.
4. On missing item / dependency failure → FAIL and block the interaction.
5. All pass → emit the go signal.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
适用于智能合约交互前的高风险自查场景，如新合约部署前的代码审计或第三方调用地址验证。当涉及资金授权、大额转账时用于检查授权额度与撤销机制有效性。在私钥保管及小额试单环节，本技能可提前识别交互风险并执行零依赖检查。

### 用法
直接执行 `contract_interact_checklist.py` 脚本。参数需传入目标合约地址及操作类型（例如 `--check audit,permission`）。若任意检测项未完成将返回 FAIL 状态，无需手动干预后续逻辑。

### 流程
1. 准备输入目标合约地址与具体交互意图（如交易/授权）。
2. 运行主脚本进入自检模式。
3. 系统依次验证六项风险：审计、地址、授权额度、撤销、私钥及试单。
4. 检测到未通过或依赖缺失时，自动标记 FAIL 并阻断交互流程。
5. 所有项目通过且无未决风险时，输出通过结果并生成执行许可信号。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
