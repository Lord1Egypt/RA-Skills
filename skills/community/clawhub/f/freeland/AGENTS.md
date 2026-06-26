# Skill Guide

This subtree owns the published Freeland skill definition for OpenClaw and other external agents.

## Key Invariants

- the skill is a user-facing contract for external agents
- endpoint descriptions must stay aligned with the real Freeland API
- product claims must match current provider behavior and deployment shape
- wallet, cards, inbox, Freeman, eSIM, VPN, and invoices must be described honestly
- version bumps and publish steps should accompany meaningful skill changes
- the public ClawHub bundle must remain trust-first and compliance-friendly
- do not publish bypass advice, approval-odds tips, fraud workarounds, geo tricks, or wording that implies evasion

## Publish Command

```bash
pnpm publish:skill:freeland --version X.Y.Z --changelog "..."
```

## Documentation Hooks

If the platform behavior changes, update the canonical skill package as well as current architecture docs and agent entrypoints.
