---
name: api3-feed-manager-readonly
description: Read-only Api3 feed discovery, readiness, coverage, and purchase-planning skill for downstream agent projects. Use when an agent needs to discover or verify decentralized data feeds, inspect funding/runway state, prepare browser or contract plans, or produce exact transaction details without ever holding signer material or submitting onchain transactions.
metadata:
  clawdis:
    homepage: https://github.com/daav3/agentic-lending-project
    author: daav3
    requires:
      bins:
        - node
      config:
        - request.ensure-feeds.json
---

# Api3 Feed Manager (Read-only)

This variant is for discovery, verification, readiness checks, and exact execution planning **without signer-backed execution**.

## What it can do

- discover the best Api3 feed for an asset or pair
- verify whether a feed exists and appears active
- inspect funding/runway state
- classify whether activation is needed
- generate browser-assisted funding plans
- generate exact contract-call payloads for later human or executor use
- audit coverage across chains

## What it will not do

- accept signer material
- submit transactions
- trigger browser purchase flows automatically
- claim a feed was funded unless a fresh post-action check proves it

## Use this when

- you want a safer default package for general users
- you need transaction details without giving the skill wallet authority
- you want a companion to the full executor variant so users can choose

## Operating rules

1. Default to discovery and verification first.
2. Return exact next-step details when execution would be required.
3. Keep the distinction between `not-needed`, `executable`, `browser-assisted`, and `unsupported`.
4. Treat any generated calldata or browser plan as review material for a separate executor or human operator.

## Available commands

- `resolve`
- `discover`
- `ensure-active`
- `prepare-activation`
- `browser-plan`
- `contract-plan`
- `queue-plan`
- `purchase-inputs`
- `prepare-contract-call`
- `coverage-audit`
- `coverage-matrix`
- `supported-chains`

## Notes

- This package is intentionally split from the executor-capable variant to reduce false surprise in security review.
- If a user wants real execution, direct them to the executor variant instead of expanding this package's authority.
