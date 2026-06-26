# CoinPay DID — CORRECTED 2026-03-29

> **The CoinPay DID is NOT a blockchain DID.** It's the **CoinPay Credential & Reputation Protocol (CPR)** — a trust and reputation system for AI agents built on CoinPayPortal.

## API Base
`https://coinpayportal.com/api`

## What It Really Is

CoinPay DID = a **merchant account DID** + **reputation protocol**.

- Every registered merchant gets a DID via `POST /reputation/did/claim`
- The DID is NOT on any blockchain — it's a CoinPay internal identifier
- Trust is built through **task receipts** submitted to the reputation system
- Platform issuers can issue **credentials** to agent DIDs

## Working Endpoints (CONFIRMED)

```
✅ POST /auth/register       — register merchant
✅ POST /auth/login          — login → JWT token
✅ GET  /health              — returns {"status":"ok","version":"0.6.11"}
✅ POST /reputation/did/claim — claim/generate DID for merchant
✅ GET  /reputation/did/me   — get merchant's DID
✅ GET  /reputation/agent/{did}/reputation — trust profile
✅ POST /reputation/receipt   — submit task completion receipt
✅ POST /reputation/verify    — verify a credential
✅ GET  /lightning/offers     — Lightning BOLT12 offers
```

## DID URL Format

```
did:key:z6Mk[HASH]   ← this is the DID format, but NOT a real did:key blockchain DID
```

The `did:key:` prefix makes it look like a W3C DID, but it's actually a CoinPay internal identifier.

## Anthony's CoinPay DID Project

Anthony's two gigs:
1. **"I will pay you $5 USD in SOL to integrate CoinPay oAuth"** — build oAuth login with CoinPay
2. **"I will pay you $5 USD in SOL to integrate CoinPay payment"** — build crypto payment integration

Both pay $5 SOL. The DID integration = integrating CoinPay's **reputation system** into ugig.net.

## Anthony's Verification Token

```
pkce_97b168ddb8b71ba5802ef78233579875227ee1961fb0b955b4682909
```

This is a CoinPay API token (Bearer format). Use as:
```
Authorization: Bearer pkce_97b168dd...
```

## Key Files

- Skills: `/Users/zhouwen/.openclaw/Main/skills/coinpay-did-setup/`
- Skills: `/Users/zhouwen/.openclaw/Main/skills/coinpay-did-integration/`
