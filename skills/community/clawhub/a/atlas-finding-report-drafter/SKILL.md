---
name: Atlas Finding Report Drafter
slug: atlas-finding-report-drafter
version: 1.0.0
description: Smart contract audit finding report writer — drafts structured, severity-ranked exploit scenarios and audit findings for Solidity/EVM protocols. Takes raw vulnerability notes from triage and produces submission-ready audit write-ups with proof-of-concept narrative, impact analysis, and severity scoring. Use for DeFi audit report writing, Code4Arena finding submission, Sherlock finding write-up, HackenProof report drafting, and severity ranking for audit findings.
homepage: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_content=atlas-finding-report-drafter
changelog: "v1.0.0: initial release — exploit scenario writing and audit finding report drafting"
tags:
  - security
  - audit
  - smart-contract
  - smart-contract-audit
  - finding-report
  - finding-report-writer
  - exploit-scenario
  - exploit-scenario-writing
  - proof-of-concept
  - poc-writeup
  - severity-scoring
  - severity-ranking
  - finding-severity
  - audit-finding
  - audit-report
  - defi-security
  - solidity-audit
  - solidity-finding
  - evm-audit
  - code4rena
  - code4arena-finding
  - code4arena-writeup
  - sherlock-audit
  - sherlock-finding
  - hackenproof
  - hackenproof-finding
  - finding-writeup
  - audit-writeup
  - audit-report-drafter
  - vulnerability-report
  - vulnerability-writeup
  - security-audit-report
  - critical-finding
  - high-finding
  - medium-finding
  - atlas
metadata:
  AtlasAgentSuite:
    tier: free
    use_cases:
      - smart contract audit finding write-up
      - exploit scenario narrative drafting
      - finding severity ranking and scoring
      - Code4Arena submission write-up
      - Sherlock audit finding draft
      - HackenProof finding report
      - audit finding proof of concept
    upsells:
      - "Full Atlas Bounty Ops: https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-finding-report-drafter"
      - "Concierge Install: https://atlasagentsuite.com/concierge.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-finding-report-drafter"
---

# Atlas Finding Report Drafter

A focused **exploit scenario writer** and **audit finding report drafter** for Solidity/EVM smart contract audits. Takes raw vulnerability observations from Phase 1–3 of the audit workflow and converts them into polished, submission-ready finding write-ups with properly scored severity, impact narrative, and proof-of-concept scenarios.

Use this after `atlas-smart-contract-auditor` has completed triage and flagged candidate vulnerabilities. This skill is where the finding gets its structure, severity score, and PoC narrative.

## Search Keywords / Best Use Cases

- smart contract audit finding write-up
- audit finding report
- finding report template
- exploit scenario writeup
- exploit scenario example
- proof of concept writeup
- proof of concept smart contract
- severity scoring smart contract audit
- finding severity ranking
- critical severity smart contract
- high severity finding
- Code4Arena finding writeup
- Code4Arena submission format
- Sherlock finding writeup
- Sherlock audit finding
- HackenProof finding report
- audit report drafting
- vulnerability report drafting
- security audit report template
- finding report example
- audit finding PoC
- smart contract poc example
- severity CVSS Web3
- likelihood impact scoring
- smart contract exploit narrative
- audit finding structure
- Code4Arena warden report
- Sherlock warden report
- audit finding markdown

## When to Use

- `atlas-smart-contract-auditor` has flagged a candidate vulnerability and you need to write it up
- A bug bounty contest just ended and you have raw notes to convert into findings
- You found a vulnerability and need a structured write-up for submission
- You want to score and rank multiple findings by severity before submission
- You need a PoC narrative written for a Solidity/EVM finding
- You want to standardize your finding format across a team or contest

## What It Produces

A complete, submission-ready audit finding with:
- Finding title and summary
- Severity score (Likelihood × Impact) with justification
- Affected contract(s) and function(s)
- Vulnerability class and CWE mapping
- Technical root cause description
- Exploit scenario narrative (step-by-step)
- Proof-of-concept code or transaction example
- Impact analysis (funds at risk, protocol effect)
- Remediation / fix recommendation
- Supporting references (real-world precedent, CVEs, past contest winners)

## Workflow

### Phase 1: Gather Finding Components

Before drafting, collect or confirm the following for each finding:

```
- Affected contract(s) and function signature(s)
- Exact source code snippet (or file:line reference)
- Vulnerability class (e.g., Reentrancy, Oracle Manipulation, Access Control)
- Observed behavior vs. expected behavior
- Estimated funds / users / protocol scope at risk
- Any external integrations involved (tokens, oracles, other contracts)
- Whether a fix exists / has been deployed
```

### Phase 2: Severity Scoring

Score each finding using **Likelihood × Impact**. Be strict — overestimate severity is a common rookie mistake that gets findings downgraded in review.

```text
SEVERITY MATRIX

Critical: Likelihood Low × Impact Critical
  → Funds permanently lost, protocol invariant broken, no workaround
  → Example: signature verification bypass enabling fund theft

High: Likelihood Medium × Impact High
  → Exploitable under realistic conditions, measurable fund exposure
  → Example: oracle manipulation draining a lending pool

Medium: Likelihood High × Impact Medium  OR  Likelihood Low × Impact Medium
  → Requires unusual conditions or partial user action
  → Example: rounding dust accumulation, griefable DOS

Low: Likelihood High × Impact Low
  → Aesthetic or minor edge case with no real impact
  → Example: Event不看不懂, minor input validation gap

Informational: No direct exploit path, worth noting
  → Example: code quality issues, missing zero-address checks
```

**Scoring prompts to answer:**
1. Under what conditions can this be triggered? (Likelihood)
2. What is the worst outcome if triggered? (Impact)
3. Does the attacker need special positioning? (Likelihood)
4. Are there any required prerequisites? (Likelihood)
5. Can the impact be measured in tokens / USD? (Impact)

### Phase 3: Exploit Scenario Narrative

Write the exploit scenario as a **step-by-step story** a non-technical reviewer can follow. Include attacker motivation at each step.

```markdown
## Exploit Scenario

**Attacker Profile:** [Single user / flash loan / admin key compromise / bot]

**Preconditions:** [Attacker has X tokens / specific state / block number]

**Step 1:** [Action] — [Why this matters]
**Step 2:** [Action] — [How state changes]
**Step 3:** [Action] — [The critical moment]
**Post-state:** [What attacker gained] — [What protocol lost]

**Total Profit:** [$X in tokens / Y% pool drained / etc.]
```

### Phase 4: Proof of Concept

Write a minimal, self-contained Solidity proof of concept or Hardhat test that demonstrates the vulnerability. Keep it under 50 lines.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "src/VulnerableContract.sol";

contract PoC is Test {
    VulnerableContract public victim;
    address attacker = makeAddr("attacker");

    function testExploit() external {
        vm.deal(attacker, 1 ether);
        victim = new VulnerableContract();

        // Step 1: Setup
        vm.startPrank(attacker);

        // Step 2: Trigger
        victim.withdraw(1 ether);

        // Step 3: Profit
        assertGt(attacker.balance, 1 ether); // Profit confirmed
        vm.stopPrank();
    }
}
```

### Phase 5: Finding Report Draft

Assemble the complete finding using this structure:

```markdown
# [Finding Title]

## Summary
[2–3 sentence executive summary: what happened, why it matters, how bad]

## Severity
**[Critical / High / Medium / Low / Informational]**

*Likelihood:* [Low / Medium / High]  
*Impact:* [Critical / High / Medium / Low]  
*Justification:* [Why this severity is appropriate — compare to similar known issues]

## Affected Components
- **Contract:** `<ContractName>`
- **Function(s):** `<function signatures>`
- **File(s):** `<file paths and line numbers>`
- **Chain(s):** `<EVM chain(s)>`

## Vulnerability Classification
- **Class:** `<Vulnerability Class>`
- **CWE:** `<CWE ID if applicable>`
- **Root Cause:** `<One sentence root cause>`

## Technical Description
[Detailed technical explanation. Include code snippets. Be precise about what the code does vs. what it should do. Use line references.]

## Exploit Scenario
[Step-by-step narrative from Phase 3 above]

## Proof of Concept
```solidity
[Minimal PoC from Phase 4 above]
```

## Impact Analysis
[Quantify the impact. What funds are at risk? How many users affected? What protocol functionality is broken? Reference similar historical exploits if applicable.]

## Remediation
[Code-level recommendation for how to fix. If a fix was already deployed, note the commit or version.]

## References
- [Link to relevant CVEs, past contest winning findings, or audit reports]
- [Solidity docs, EIP, or security standards referenced]

---
*Finding drafted with Atlas Finding Report Drafter.*
*Full Atlas Agent Suite: https://atlasagentsuite.com/skills.html*
```

## Severity Score Reference Table

| Rating | Likelihood | Impact | Example |
|--------|-----------|--------|---------|
| Critical | Low | Critical | Signature bypass, immutable contract bug |
| High | Medium | High | Oracle manipulation draining pool |
| High | Low | High | Admin key theft draining treasury |
| Medium | High | Medium | Griefing DOS on user entry |
| Medium | Medium | Medium | Rounding dust accumulation |
| Low | High | Low | Eventlog inconsistency |
| Informational | Any | Low | Code quality observation |

## Guardrails

- **Be precise with severity.** Over-scoring is as harmful as under-scoring. Judges and lead auditors will downgrade findings that don't justify their severity with concrete evidence.
- **PoC must be minimal and runnable.** Don't paste the entire protocol. Isolate the vulnerability in the fewest lines possible.
- **Don't invent facts.** If you don't know the exact dollar amount at risk, say "at risk of >X tokens" — don't fabricate a specific USD figure without basis.
- **Reference past wins.** When unsure whether something is a valid finding, check the PATTERNS.md from the audit skill — similar patterns have won High/Medium in real contests.
- **This skill does not replace manual verification.** Draft the finding, but verify the exploit path before submission.

## Get the Full Atlas Agent Suite

The full Atlas Bounty Ops workflow adds:

- Contest monitoring for Code4rena, Sherlock, HackenProof
- Real-time finding severity scoring across full audit scope
- Automated PoC generation templates per vulnerability class
- Scheduled daily briefings on new vulnerability patterns
- Full Atlas Finding Report Drafter + Smart Contract Auditor bundled
- Revenue ops and marketing agents for audit professionals

👉 https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-finding-report-drafter