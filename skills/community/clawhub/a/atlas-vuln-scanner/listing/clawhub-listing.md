# ClawHub Listing Draft — Atlas Smart Contract Vulnerability Pattern Scanner

## Title
Atlas Smart Contract Vulnerability Pattern Scanner

## Short tagline
Turn Solidity repos into triage-ready vulnerability reports using Atlas DeFi audit patterns.

## Category
Security / Smart Contracts / DeFi / Bug Bounty

## ClawHub availability
Free / MIT-0 ClawHub skill.

Public ClawHub docs state that ClawHub does not currently support paid skills, per-skill pricing, paywalls, revenue sharing, seller onboarding, Stripe, payouts, or KYC. Do not include native price metadata in `SKILL.md`.

## Description
Atlas Vuln Scanner is an agent-ready OpenClaw skill for first-pass Solidity security review. Point it at a local repo and it produces a structured vulnerability triage package: file/line flags, confidence labels, candidate finding writeups, and a founder-readable executive summary.

It is built for auditors, bounty hunters, and DeFi teams who want a fast pre-audit pass before spending deeper manual review time.

## What users get
- OpenClaw/Hermes-compatible `SKILL.md`
- Runnable local scanner script
- Demo vulnerable contract
- Markdown scan report output
- Bounty-style finding candidate template
- Executive summary template for protocol teams
- Responsible disclosure and anti-hallucination guardrails

## Core patterns covered
- Reentrancy / external-call order
- Access-control gaps
- Oracle spot-price / staleness risk
- Unchecked low-level and token calls
- Accounting/share math drift
- Unsafe casts and unchecked arithmetic
- Delegatecall/arbitrary execution
- Pause coverage gaps
- Initializer/upgradeability issues
- Timestamp and gas-griefing heuristics

## Guardrail
This is a heuristic triage workflow, not a replacement for a full audit. Outputs require manual validation before severity claims, disclosure, or bounty submission.

## External monetization CTA
Use ClawHub as free distribution/discovery. For paid work, route users externally:

Need help validating the scanner output? Atlas can turn candidate flags into a paid robust scan, audit-prep packet, or bounty submission review.

Suggested external offers:
- $500–$2,500+ robust scan / audit-prep report
- Custom private/pro scanner workflow
- Atlas Security Skill Pack outside ClawHub if paid distribution is required

## Publish command
```bash
clawhub login

clawhub publish /Users/natemacdaddy/.hermes/workspace/atlas-security-skills/atlas-vuln-scanner \
  --slug atlas-vuln-scanner \
  --name "Atlas Smart Contract Vulnerability Pattern Scanner" \
  --version 0.1.0 \
  --tags latest,security,smart-contracts \
  --changelog "Initial release"
```
