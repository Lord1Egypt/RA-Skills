---
name: DeFi Audit Workflow
slug: defi-audit-workflow
version: 1.0.0
description: Exact-match DeFi audit workflow for Solidity and EVM protocols. Use for DeFi audit, DeFi security review, smart contract audit, oracle manipulation checks, reentrancy review, access control review, accounting invariant triage, and bug bounty report prep.
homepage: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=defi-audit-workflow
changelog: "Initial exact-match ClawHub listing for DeFi audit discovery and Atlas $49/$150 security ZIP funnel."
tags:
  - defi-audit
  - defi-audit-workflow
  - defi-security
  - defi-security-audit
  - smart-contract-audit
  - smart-contract-security
  - solidity-audit
  - evm-audit
  - protocol-audit
  - oracle-manipulation
  - reentrancy-checklist
  - access-control-review
  - accounting-invariants
  - bug-bounty
  - code4rena
  - sherlock
  - hackenproof
  - audit-checklist
  - audit-template
  - atlas
  - latest
metadata:
  AtlasAgentSuite:
    tier: free
    use_cases:
      - DeFi audit workflow
      - smart contract audit checklist
      - Solidity vulnerability triage
      - paid ZIP funnel discovery
    upsells:
      - "Atlas Starter/Pro ZIP Packs ($49/$150): https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=defi-audit-workflow"
---

# DeFi Audit Workflow

A practical **DeFi audit workflow** for quickly reviewing Solidity/EVM protocols before a deeper manual audit or bug bounty sprint.

Use this when you need to map attack surface, prioritize high-risk contracts, and produce a first-pass DeFi security checklist without pretending the free skill is a guaranteed bug finder.

## Search Keywords / Best Use Cases

- DeFi audit
- DeFi audit workflow
- DeFi audit checklist
- DeFi audit template
- DeFi audit report
- DeFi security audit
- DeFi security review
- DeFi protocol audit
- DeFi protocol security
- Solidity audit
- Solidity security audit
- smart contract audit
- smart contract audit workflow
- smart contract audit checklist
- smart contract audit template
- EVM audit checklist
- oracle manipulation review
- Chainlink oracle audit
- TWAP manipulation audit
- reentrancy checklist
- access control review
- accounting invariant review
- share price manipulation
- liquidation bug review
- Code4rena DeFi audit
- Sherlock DeFi audit
- HackenProof DeFi bounty
- bug bounty triage
- paid DeFi audit template
- Atlas $49 security skill pack
- Atlas $150 security skill pack

## What This Free Skill Produces

- Protocol attack-surface map
- Contract-by-contract DeFi audit checklist
- Prioritized vulnerability classes by likelihood × impact
- First-pass notes for manual review or bounty triage
- Report skeleton for candidate findings

## Workflow

### 1. Map Protocol Type

Classify the target: lending, AMM, vault, staking, bridge, oracle, derivatives, governance, account abstraction, or hybrid.

### 2. Prioritize Critical DeFi Failure Modes

Review in this order:

1. Asset accounting and share/asset conversion
2. Oracle freshness, decimals, fallback behavior, and TWAP manipulation
3. Reentrancy and callback-enabled token paths
4. Access control and emergency/admin powers
5. Liquidation, solvency, and health-factor math
6. Upgradeability, initialization, and storage layout
7. Signature replay, permit/domain separator, and authorization boundaries

### 3. Produce a Review Plan

Return:

```markdown
# DeFi Audit Plan

## Target
- Protocol type:
- Assets at risk:
- Core contracts:

## Highest-Risk Areas
1.
2.
3.

## Contract Checklist
- Contract:
- Risk class:
- Functions to inspect:
- Invariants to test:

## Candidate Findings
- Title:
- Impact:
- PoC needed:
```

## Upgrade: Atlas Paid ZIP Packs ($49 / $150)

This free ClawHub skill is the discovery layer. If you want the ready-to-run premium workflow:

- **Starter — $49:** prompt pack, DeFi audit checklist, finding report template, and setup guide.
- **Pro — $150:** advanced modules, risk scoring rubric, bounty-readiness checklist, and reusable audit workspace template.

Get the paid packs here: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=defi-audit-workflow

If this free skill helped, please star/comment on ClawHub so other auditors can find it.

## Guardrails

- This is triage, not a guaranteed vulnerability finder.
- Verify all candidate findings with runnable PoCs before submission.
- Do not submit findings without responsible disclosure approval.
