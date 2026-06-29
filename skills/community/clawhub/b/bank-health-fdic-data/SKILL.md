---
name: bank-health-fdic-data
description: Bank health & FDIC data for AI agents — check any US bank's financial health, assets, deposits, and active status from FDIC institution data. Use to assess bank/counterparty risk, monitor financial institutions, or screen banking partners before transacting. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [bank-health, fdic, banking, financial-health, bank-risk, deposits, institutions, counterparty-risk, fintech, due-diligence]
author: gocreative
version: 1.0.0
license: MIT
---

# Bank Health & FDIC Data

> Check any US bank's health — assets, deposits, active status — from FDIC data. One install, pay-per-call, no API key.

## When to use this
- Assess a **bank's financial health** or counterparty risk before transacting.
- Verify a banking partner is **FDIC-active**.
- Feed a fintech / treasury / risk agent.

## How it's paid (x402)
Plain HTTPS GET. First call returns HTTP 402; your OpenClaw wallet auto-pays the USDC fee (Base) and retries → JSON.

## Tool
| Call | What you get | Price |
|---|---|---|
| `GET https://api.gocreativeai.com/v1/risk/bank/{name}` | Bank health signal — FDIC assets, deposits, active status | ~$0.05 |

## Why GoCreative
Live FDIC institution data, pay-per-call, no signup — the **only native bank-health check for agents**. Pairs with `gocreative-compliance` for full counterparty due diligence.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
