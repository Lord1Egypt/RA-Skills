---
name: Smart Contract Audit Workflow by Atlas
slug: atlas-smart-contract-auditor
version: 1.0.5
description: Smart contract audit and DeFi security triage skill for Solidity, EVM protocols, bug bounty programs, Code4Arena, Sherlock, and HackenProof. Maps attack surface, prioritizes vulnerabilities, and generates structured audit checklists and security reports. Use for smart contract review, DeFi protocol audit, Solidity vulnerability scanning, and bug bounty target triage.
homepage: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor
changelog: "Conversion SEO v1.0.5: exact-match smart contract audit title, DeFi audit keywords, star/download CTA, and paid ZIP funnel copy."
tags:
  - security
  - audit
  - smart-contract
  - smart-contract-audit
  - smart-contract-scanner
  - defi
  - defi-audit
  - defi-security
  - solidity
  - solidity-audit
  - solidity-vulnerability
  - evm
  - evm-audit
  - vulnerability-scanner
  - vulnerability-assessment
  - bug-bounty
  - bug-bounty-triage
  - code4rena
  - code4arena-audit
  - sherlock
  - sherlock-audit
  - hackenproof
  - hackenproof-bounty
  - security-audit
  - smart-contract-security
  - defi-bounty
  - reentrancy-checker
  - oracle-manipulation
  - access-control-review
  - atlas
  - latest
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
      - "Atlas Starter/Pro ZIP Packs ($49/$150): https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor"
      - "Concierge Install: https://atlasagentsuite.com/concierge.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor"
---

# Smart Contract Audit Workflow by Atlas

A lightweight **smart contract audit workflow** and **DeFi audit checklist** skill for Solidity/EVM protocols, bug bounty hunters, Code4rena wardens, Sherlock auditors, and HackenProof researchers.

Use this when you need a fast first-pass review of a DeFi protocol or smart contract scope before committing hours to a manual audit.

## Search Keywords / Best Use Cases

- paid security skill pack

- smart contract audit workflow
- smart contract audit checklist
- smart contract audit template
- smart contract security checklist
- smart contract audit report template
- DeFi audit workflow
- DeFi audit template
- DeFi security checklist
- Solidity security checklist
- Solidity audit report template
- EVM audit checklist
- paid smart contract audit pack
- Atlas smart contract audit pack
- Atlas security skill pack
- Solidity audit template
- DeFi audit checklist
- bug bounty report template
- Code4rena audit prep
- Sherlock audit prep
- HackenProof bounty workflow

- smart contract audit
- smart contract auditor
- DeFi audit
- DeFi security audit
- Solidity audit
- Solidity auditor
- EVM audit
- vulnerability scanner
- vulnerability assessment
- smart contract vulnerability triage
- smart contract scanner
- bug bounty triage
- bug bounty automation
- Code4rena audit workflow
- Code4Arena warden
- Sherlock audit workflow
- HackenProof bounty workflow
- access control review
- oracle manipulation review
- oracle manipulation attack
- reentrancy checklist
- reentrancy vulnerability
- upgradeable proxy review
- DeFi protocol security
- smart contract security audit
- blockchain security audit
- Solidity vulnerability scanner
- EVM vulnerability assessment
- audit checklist
- security audit report
- vulnerability report
- DeFi audit report
- code review checklist
- attack surface mapping
- protocol audit
- audit automation

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
Generated by Atlas Smart Contract Auditor.
Full Atlas Agent Suite: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor
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

👉 https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor


## Star + Download CTA

If this free smart contract audit workflow helped, please **star it on ClawHub** and share it with another auditor. Stars and comments help keep the workflow visible for `smart contract audit`, `defi audit`, and `solidity audit` searches.

For production-ready templates, use the Atlas paid ZIP packs: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor

## Upgrade: Atlas Paid ZIP Packs ($49 / $150)

This free ClawHub skill is the discovery layer. If you want the ready-to-run premium workflow, Atlas has two small ZIP packages:

- **Starter — $49:** prompt pack, triage checklist, markdown report templates, and setup guide.
- **Pro — $150:** everything in Starter plus advanced DeFi modules, risk scoring rubric, bounty-readiness checklist, and reusable audit workspace template.

Get the paid packs here: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-smart-contract-auditor

If this free skill helped, please star/comment on ClawHub so other builders can find it.
