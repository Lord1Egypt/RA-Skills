---
name: DeFi Audit & Smart Contract Bounty Triage
slug: atlas-bounty-triage
version: 1.0.4
description: Smart contract audit and DeFi security triage skill for Solidity, EVM protocols, bug bounty programs, Code4rena, Sherlock, and HackenProof. Maps attack surface, prioritizes vulnerabilities, and generates a structured audit checklist/report.
homepage: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage
changelog: "Conversion SEO v1.0.4: exact-match DeFi audit title, smart contract audit keywords, stronger star/download CTA, and paid ZIP funnel copy."
tags:
  - security
  - audit
  - smart-contract
  - smart-contract-audit
  - defi
  - defi-audit
  - solidity
  - evm
  - vulnerability-scanner
  - bug-bounty
  - code4rena
  - sherlock
  - hackenproof
  - defi-security
  - solidity-audit
  - smart-contract-security
  - defi-bounty
  - audit-checklist
  - latest
  - atlas
metadata:
  AtlasAgentSuite:
    tier: free
    use_cases:
      - smart contract audit triage
      - DeFi protocol audit checklist
      - Solidity vulnerability review
      - EVM security research
      - bug bounty target prioritization
    upsells:
      - "Atlas Starter/Pro ZIP Packs ($49/$150): https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage"
      - "Concierge Install: https://atlasagentsuite.com/concierge.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage"
---

# DeFi Audit & Smart Contract Bounty Triage

A lightweight **smart contract audit** and **DeFi security triage** skill for Solidity/EVM protocols, bug bounty hunters, Code4rena wardens, Sherlock auditors, and HackenProof researchers.

Use this when you need a fast first-pass review of a DeFi protocol or smart contract scope before committing hours to a manual audit.

## Search Keywords / Best Use Cases

- paid security skill pack
- DeFi audit workflow
- DeFi audit checklist
- DeFi audit template
- smart contract audit workflow
- smart contract audit checklist
- smart contract audit template
- smart contract bounty triage
- DeFi bounty triage
- Solidity bug bounty workflow
- Code4rena smart contract audit
- Sherlock smart contract audit
- HackenProof DeFi bounty
- paid DeFi audit pack
- Atlas bounty skill pack
- Solidity audit template
- DeFi audit checklist
- bug bounty report template
- Code4rena audit prep
- Sherlock audit prep
- HackenProof bounty workflow

- smart contract audit
- DeFi audit
- DeFi security audit
- Solidity audit
- EVM audit
- vulnerability scanner
- smart contract vulnerability triage
- bug bounty triage
- Code4rena audit workflow
- Sherlock audit workflow
- HackenProof bounty workflow
- access control review
- oracle manipulation review
- reentrancy checklist
- upgradeable proxy review

## When to Use

- New smart contract audit target assigned
- DeFi contest just opened and you need to prioritize files
- Bug bounty scope includes Solidity/EVM contracts
- You need a structured first-pass vulnerability checklist
- You want to map attack surface before deep manual review

## What It Produces

A structured markdown audit triage report with:

- Target overview
- Protocol type and contract categories
- Attack surface map
- High-priority vulnerability classes
- Contract-by-contract checklist
- Recommended deep-dive order
- Quick-win review items

## Workflow

### Phase 1: Smart Contract Scope Mapping

For each contract in scope:

1. Identify protocol type: lending, AMM, vault, staking, bridge, oracle, governance, NFT, account abstraction
2. Identify external integrations: Chainlink, Uniswap, Curve, ERC20 tokens, bridges, routers, keepers
3. Flag proxy/upgrade patterns: `EIP1967`, `UUPS`, transparent proxy, beacon proxy, clones
4. Identify privileged roles: owner, admin, guardian, pauser, timelock, operator
5. Note novel or high-risk mechanisms: custom accounting, share pricing, liquidation math, rewards, TWAPs

### Phase 2: DeFi Vulnerability Prioritization

Score each vulnerability class by **likelihood × impact**:

```text
HIGH PRIORITY
- Reentrancy: external calls + state changes + callbacks
- Access control: missing modifiers, wrong role assumptions, admin bypass
- Oracle manipulation: stale price, TWAP manipulation, decimal mismatch, fallback oracle bugs
- Accounting bugs: share price drift, rounding loss, fee math, collateral/debt mismatch
- Liquidation bugs: bad health factor math, stale collateral values, griefable liquidation paths
- Upgradeability bugs: unprotected initializer, storage collision, implementation takeover

MEDIUM PRIORITY
- Fee-on-transfer / rebasing token edge cases
- ERC777 / callback-enabled token surprises
- Sandwich / MEV-sensitive pricing
- DOS via unbounded loops or griefable state
- Signature replay / permit domain separator issues

LOW PRIORITY BUT CHECK
- Input validation gaps
- Event/reporting mismatch
- Gas griefing
- Minor precision loss without exploitable value extraction
```

### Phase 3: Contract-by-Contract Checklist

```markdown
## Contract: <Name>

### External Calls / Reentrancy
- [ ] External calls happen after state updates?
- [ ] Reentrancy guard exists where callbacks are possible?
- [ ] ERC777 / ERC721 receiver / flash loan callbacks considered?

### Access Control
- [ ] Privileged functions use correct modifier?
- [ ] Timelock/owner/admin boundaries are clear?
- [ ] Emergency functions cannot steal user funds?

### Oracle / Pricing
- [ ] Oracle freshness checked?
- [ ] Decimal normalization correct?
- [ ] Fallback oracle cannot be manipulated?
- [ ] TWAP window long enough for protocol value at risk?

### Accounting
- [ ] Shares/assets conversion handles rounding direction correctly?
- [ ] Fee calculations cannot drain or brick accounting?
- [ ] Deposits/withdrawals preserve invariants?

### Upgradeability
- [ ] Initializers protected?
- [ ] Storage layout compatible?
- [ ] Implementation cannot be selfdestructed or hijacked?
```

### Phase 4: Audit Triage Report

```markdown
# Smart Contract Audit Triage: <Target>

## Target Overview
- Protocol type:
- Chain(s):
- Contracts in scope:
- Highest-value assets:

## Attack Surface Summary
- External integrations:
- Oracle dependencies:
- Upgrade pattern:
- Privileged roles:

## Top Vulnerability Classes to Review
1. [HIGH] <class> — <why this target is exposed>
2. [HIGH] <class> — <why this target is exposed>
3. [MEDIUM] <class> — <why this target is exposed>

## Recommended Deep-Dive Order
1. <contract> — focus on <vulnerability class>
2. <contract> — focus on <vulnerability class>
3. <contract> — focus on <vulnerability class>

## Quick Wins Checklist
- [ ] Reentrancy review
- [ ] Access control review
- [ ] Oracle manipulation review
- [ ] Upgradeability review
- [ ] Accounting invariant review

---
Generated by Atlas Smart Contract Audit & DeFi Bounty Triage.
Full Atlas Agent Suite: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage
```

## Guardrails

This is a **triage and audit workflow**, not a guaranteed vulnerability finder. It helps prioritize manual review and produce better audit notes. Always verify candidate findings with a proof of concept before submission.

## Get the Full Atlas Agent Suite

The full Atlas Bounty Ops workflow includes:

- Contest monitoring for Code4rena, Sherlock, HackenProof
- Target scoring and prioritization
- Daily vulnerability pattern promotion
- Finding writeup templates
- Scheduled research briefings
- Revenue ops and marketing agents

👉 https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage


## Star + Download CTA

If this free DeFi audit and bounty triage workflow helped, please **star it on ClawHub** and leave a short comment. Stars/comments help other wardens find it for `defi audit`, `smart contract audit`, and `bug bounty` searches.

For production-ready templates, use the Atlas paid ZIP packs: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage

## Upgrade: Atlas Paid ZIP Packs ($49 / $150)

This free ClawHub skill is the discovery layer. If you want the ready-to-run premium workflow, Atlas has two small ZIP packages:

- **Starter — $49:** prompt pack, triage checklist, markdown report templates, and setup guide.
- **Pro — $150:** everything in Starter plus advanced DeFi modules, risk scoring rubric, bounty-readiness checklist, and reusable audit workspace template.

Get the paid packs here: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage

If this free skill helped, please star/comment on ClawHub so other builders can find it.
