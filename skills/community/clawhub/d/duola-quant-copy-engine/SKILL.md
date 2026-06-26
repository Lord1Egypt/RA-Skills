---
name: duola-lobster-agent
description: "Institutional-grade execution playbook for the published `duola` Polymarket copy-trading CLI in lobster-agent workflows. Use when tasks require production-style setup and operation: install/upgrade from npm, leader onboarding, trade synchronization, strategy backtesting, autopilot bootstrap, live loop control, diagnostics, and structured risk/performance reporting."
---

# Duola Lobster Agent

## Overview

Execute the standard operating workflow for `duola` as an agent toolchain.
Prefer staged rollout: sync -> backtest -> doctor -> limited live start -> status/log review.

## Billing Setup (SkillPay)

Configure once in runtime environment:

```bash
export SKILLPAY_API_URL="https://skillpay.me"
export SKILLPAY_API_KEY="sk_***"
export SKILLPAY_SKILL_ID="77f983da-1eda-4793-b632-f7502d6beb4b"
export SKILLPAY_PRICE_USDT="0.01"
```

Use billing gate with commands that support `--billing-user-id`.
Supported: `sync`, `backtest`, `follow start`, `autopilot onboard`, `autopilot start`.

Check billing endpoints from CLI:

```bash
duola billing balance --user-id <user_id> --output json
duola billing charge --user-id <user_id> --amount 0.01 --output json
duola billing payment-link --user-id <user_id> --amount 1 --output json
```

## Execution Workflow

### 1) Verify Runtime and CLI

Run:

```bash
node -v
npm view duola version
duola --version
```

If `duola` is missing, install:

```bash
npm install -g duola
```

If global install is restricted, run project-local CLI:

```bash
npm install
npm run build
node dist/index.js --version
```

### 2) Register and Inspect Leader

```bash
duola leader add <leader_address> --name <alias>
duola leader list --output json
duola leader inspect <alias> --output json
```

Use deterministic aliases and keep one alias per leader address.

### 3) Sync and Baseline Backtest

```bash
duola sync <alias> --limit 500 --output json
duola backtest <alias> --lookback 30d --fixed-usd 25 --output json
```

If results are weak, tune before live mode:
- raise `--min-liquidity`
- increase `--min-time-to-expiry`
- reduce `--fixed-usd`

### 4) Run Doctor Diagnostics

```bash
duola doctor <alias> --output json
```

Require passing API connectivity and secret checks before live mode.

### 5) Onboard Autopilot (Preferred Live Path)

Use stdin for private key and do not print secrets:

```bash
printf '%s' '<private_key>' | duola autopilot onboard <leader_address> \\
  --name <alias> --private-key-stdin --profile balanced --sync-limit 200
```

Start with explicit confirmation phrase:

```bash
duola autopilot start <alias> --confirm-live "I UNDERSTAND LIVE TRADING" --detach
```

### 6) Operate and Observe

```bash
duola autopilot status <alias> --output json
duola follow logs <alias> --tail 100 --output json
duola autopilot stop <alias> --output json
```

For limited-cycle validation:

```bash
duola follow start <alias> --confirm-live "I UNDERSTAND LIVE TRADING" --max-cycles 5 --output json
```

## Reporting Contract

Return concise machine-usable summaries:
- `leader`: alias, address
- `sync`: fetched/inserted/skipped counts
- `backtest`: win rate, total pnl, max drawdown, executed signals
- `doctor`: failed checks and remediation
- `autopilot`: status, detach state, heartbeat, recent errors

When live start is blocked, report the exact failed precondition and the next command.
