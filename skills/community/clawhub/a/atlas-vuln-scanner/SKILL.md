---
name: atlas-vuln-scanner
description: Scan Solidity repositories for Atlas smart-contract vulnerability patterns and generate triage-ready security reports.
version: 0.1.0
category: security
tags:
  - solidity
  - smart-contracts
  - defi
  - security
  - bug-bounty
metadata:
  openclaw:
    emoji: "🛡️"
    os:
      - linux
      - macos
    requires:
      bins:
        - python3
    install: "No install required beyond Python 3; run scripts/atlas_vuln_scanner.py locally."
    homepage: "https://atlasagentsuite.com"
---

# Atlas Smart Contract Vulnerability Pattern Scanner

Atlas Vuln Scanner is an OpenClaw/Hermes-ready security skill that turns a Solidity repository into a structured first-pass vulnerability triage report.

It is designed for:
- Solo auditors and bounty hunters doing first-pass repo review
- DeFi teams preparing for audit or launch
- Agent builders who want a reusable smart-contract review workflow

## Value proposition

Run an Atlas-pattern scan against a Solidity repo and get:
- File/line-linked vulnerability flags
- Confidence labels: High / Medium / Low
- Pattern categories: reentrancy, oracle risk, access control, unchecked calls, accounting drift, pause gaps, initialization issues, unsafe casts, gas griefing
- Founder-readable executive summary
- Bounty-style finding candidate template

## Important guardrail

This is a **heuristic triage skill**, not a full audit and not a guaranteed vulnerability detector.

Every output must distinguish:
- **Static heuristic flag** — pattern matched, manual validation required
- **Finding candidate** — evidence is strong enough for deeper review
- **Verified finding** — only after a human or PoC confirms exploitability

Do not submit findings, send protocol messages, publish exploit details, or claim verified severity without explicit human approval.

## Quick start

```bash
python3 scripts/atlas_vuln_scanner.py --target /path/to/solidity/repo --output ./scan-results
```

Run bundled demo:

```bash
python3 scripts/atlas_vuln_scanner.py --target demo/contracts --output demo/results
```

Outputs:
- `scan-report.md` — full pattern scan report
- `finding-candidates.md` — prioritized candidate writeups
- `exec-summary.md` — protocol-founder readable summary
- `scanner-log.json` — machine-readable raw results

## Agent workflow

When using this skill as an agent:

1. Ask for a local path or public GitHub repo URL.
2. Clone/fetch repo if needed.
3. Run the scanner script against Solidity files.
4. Read `scanner-log.json` and `scan-report.md`.
5. Reduce noise: remove obvious mocks/tests/interfaces unless user asked to include them.
6. Write top 3–5 finding candidates with confidence labels.
7. Tell the user what requires manual validation before disclosure.

## Suggested prompt

```text
Use atlas-vuln-scanner on this Solidity repo: <repo/path>. Produce a concise triage report, top candidate findings, and founder-facing summary. Do not submit or disclose anything externally.
```

## ClawHub licensing / monetization note

Public ClawHub docs currently describe ClawHub as a free/open skill registry, not a paid marketplace. Published ClawHub skills are MIT-0 and ClawHub does **not** support native paid skills, per-skill pricing, paywalls, revenue sharing, seller onboarding, Stripe, payouts, or KYC.

Recommended monetization path:
- Publish this skill as a free defensive triage tool on ClawHub for discovery.
- Keep proprietary premium pattern packs, paid report templates, and private/pro scanner workflows external to ClawHub.
- Use the CTA to route interested users to Atlas for the paid Atlas Security Skill Pack, robust scans, and audit prep.

CTA:
> This free ClawHub skill is the elementary Atlas scanner. For deeper DeFi pattern coverage, polished audit-prep reports, and paid validation workflows, get the Atlas Security Skill Pack at https://atlasagentsuite.com.

## Source/caveat notes

Pattern selection is based on Atlas/OpenClaw bounty and audit workflow knowledge plus common DeFi bug classes. Scanner output should be treated as a prioritization layer for human review, not final proof.
