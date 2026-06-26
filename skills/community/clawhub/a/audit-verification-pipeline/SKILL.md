---
name: audit-verification-pipeline
description: 审计finding三级验收流水线：自身forge test验证 → GitHub CI → 审查员评审。确保提交真实可靠的验证级产出。
version: 1.0
created: 2026-03-31
tags: [audit, foundry, verification, quality]
---

# Audit Verification Pipeline

## 触发条件

### 触发场景

| 场景 | 对应能力 | 说明 |
|------|----------|------|
| 写完 PoC 准备验证 | Level 1: Self-Verification | forge build + forge test 确认攻击效果 |
| 准备提交 finding 到外部平台 | Level 3: Pre-submission checklist | 提交前必须完成三级验收 |
| forge test 结果不确定 | Quality Self-Assessment | 判断 PASS 是否等于 finding 真实 |
| 判断 finding 严重度 | Severity Assessment Guide | 防止高估（Medium→Low 惯例） |
| 推送审计代码到 GitHub | Level 2: GitHub CI | CI 必须配置防止跳过验证 |

### 决策流程

```
发现可疑代码 → 写 PoC → forge build → forge test
  ├─ PASS + 攻击效果确认 → 质量自评 → 提交宝总决策 → (是) 提交外部平台
  ├─ PASS + 无攻击效果 → 丢弃（FALSE POSITIVE）
  └─ FAIL → 修复（最多3轮）→ 仍失败 → 丢弃
```

### 反触发（不使用此技能的场景）

- **没有 PoC 代码时**：纯代码审查或白板分析不需要 forge 验证
- **非 Solidity 项目**：此流水线基于 Foundry，不适用于 Rust/Go/Python 审计
- **理论级发现**：没有可运行 PoC 的发现标记为理论级，不进入验收流程
- **宝总明确说"先看看"时**：探索阶段不触发正式验收

---

## Overview

三级验收流水线，确保每个审计finding经过确定性验证后才作为交付物。

**核心原则**: 代码生成虽具概率性，但验证是确定性的。没有forge test PASS的finding不是交付物。

## Three-Level Acceptance

```
Level 1: Self-Verification (forge test PASS)
Level 2: GitHub CI (automated, prevents skipping)
Level 3: Auditor Review (novelty, severity, quality)
```

Serial dependency: L1 → L2 → L3. Skipping levels = no verification.

## Level 1: Self-Verification

### Step-by-step

```
1. Read source code → identify suspicious pattern
2. Write finding description (draft)
3. Write Foundry PoC (.t.sol)
4. forge build → fix compilation errors (expect 2-3 rounds)
5. forge test → check result:
   - PASS + attack effect confirmed → REAL
   - PASS + attack effect = 0 → FALSE POSITIVE
   - FAIL (PoC bug) → fix PoC, retry
   - FAIL (code correct) → FALSE POSITIVE, discard
6. Quality self-assessment
7. Present to 宝总 for Level 3 decision
```

### PoC Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.x;

import "forge-std/Test.sol";
import "../src/TargetContract.sol";

contract POC_FindingName is Test {
    TargetContract target;

    function setUp() public {
        // Deploy contracts
        // Setup state
    }

    function test_attack_succeeds() public {
        // Step 1: Setup attack prerequisites
        // Step 2: Execute attack
        // Step 3: Assert attack effect (NOT just that tx succeeds)
        assertGt(attackerProfit, 0, "Attack must produce profit");
    }
}
```

### Common Pitfalls

1. **vm.roll vs vm.warp**: `vm.roll` changes block number only, use `vm.warp` for timestamp
2. **StaleMessage**: Some protocols check message freshness, set correct timestamp
3. **NotTolled/Payable**: Auth functions may require fee payment (e.g., `kiss()`)
4. **Unicode in Solidity**: Replace `—`, `→` etc. with ASCII
5. **Library paths**: Check actual file location, not assumed paths
6. **Virtual shares/balance**: Protocol-specific virtual accounting can absorb rounding (Morpho lesson)
7. **PASS ≠ correct**: PoC passing doesn't mean finding is real — verify attack EFFECT, not just mechanism

### Quality Self-Assessment Template

```
【提交前质量自评】
- Finding ID: [F-XX]
- Verification: [ ] Compiled [ ] forge test PASS [ ] Attack effect verified
- Severity: [H/M/L/I] — Rationale: [why this severity]
- Novelty: [New / Known / Duplicate] — Source if known: [link]
- Known limitations: [any caveats]
```

## Level 2: GitHub CI (TODO)

### Required Workflow

```yaml
# .github/workflows/audit-test.yml
name: Audit PoC Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: foundry-rs/foundry-toolchain@v1
      - run: forge test --match-path "test/POC_*.t.sol" -vv
      - run: forge build
```

### Purpose

Prevents Level 1 from being skipped due to session termination or memory loss.
Every push must pass forge test before PR can be submitted.

## Level 3: Auditor Review

### What auditors check (that forge test cannot)

1. **Novelty**: Is this a known finding? Check previous audit reports
2. **Severity accuracy**: Is Medium really Medium? (Sablier lesson: 2/5 overstated)
3. **Impact quantification**: Precise loss calculation, not qualitative
4. **Report quality**: Clear reproduction steps, code references, remediation
5. **Protocol economics**: DeFi-specific game theory, incentive analysis

### Pre-submission checklist

- [ ] forge test PASS (Level 1)
- [ ] CI green on push (Level 2)
- [ ] Checked previous audit reports for duplicates
- [ ] Severity assessment justified with numbers
- [ ] Impact quantified (not just "funds lost")
- [ ] Report follows platform submission format
- [ ] Presented to 宝总 for approval

## Severity Assessment Guide

| Severity | Criteria |
|----------|----------|
| HIGH | Direct fund loss, DoS of core function, permission escalation |
| MEDIUM | Indirect loss, constrained DoS, griefing with economic cost |
| LOW | Best practice violation, defense-in-depth, theoretical with no practical exploit |
| INFO | Code quality, documentation, no security impact |

**Common overestimation**: If impact requires multiple unlikely conditions, downgrade one level.
**Common underestimation**: If impact is systemic (affects all users), upgrade one level.

## Lessons from Retrospective Verification (2026-03-31)

- 135 findings submitted, 0 verified → Cantina ban
- 29 findings retroactively verified: 28 real (96.6%), 1 FP (3.4%)
- Code analysis capability is solid; verification layer was missing
- False positive example: Morpho F-01 (virtual shares absorb rounding)
- Severity overestimation example: Sablier F-03, F-05 (Medium → Low)
- PoC compilation errors are normal, expect 2-3 rounds of fixes
- forge test PASS ≠ finding correct, verify attack EFFECT not just mechanism
