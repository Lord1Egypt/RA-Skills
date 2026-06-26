---
name: Blockchain & DID
description: Decentralized identity (DID) management, on-chain KYC status, and membership tiers with token staking.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIOT_API_BASE_URL
    primaryEnv: AIOT_API_BASE_URL
---

# Blockchain & DID

Use this skill when the user needs to set up a decentralized identity, complete on-chain KYC, or manage membership tiers.

## Configuration

The default API base URL is `https://payment-api-dev.aiotnetwork.io`. All endpoints are relative to this URL.

To override (e.g. for local development):

```bash
export AIOT_API_BASE_URL="http://localhost:8080"
```

If `AIOT_API_BASE_URL` is not set, use `https://payment-api-dev.aiotnetwork.io` as the base for all requests.

## Available Tools

- `get_did_status` — Get the user's decentralized identity (DID) status | `GET /api/v1/blockchain/did` | Requires auth
- `create_did` — Create a new decentralized identity on-chain | `POST /api/v1/blockchain/did` | Requires auth
- `get_blockchain_kyc` — Get on-chain KYC verification status | `GET /api/v1/blockchain/kyc` | Requires auth
- `complete_blockchain_kyc` — Complete on-chain KYC at a given level (basic, standard, or enhanced) | `POST /api/v1/blockchain/kyc/complete` | Requires auth
- `get_membership` — Get membership status and tier | `GET /api/v1/blockchain/membership/status` | Requires auth
- `get_membership_tiers` — Get available membership tier configurations | `GET /api/v1/blockchain/membership/tiers` | Requires auth
- `stake_tokens` — Stake tokens to upgrade membership tier | `POST /api/v1/blockchain/membership/stake` | Requires auth

## Recommended Flows

### Setup Decentralized Identity

Create a DID and complete on-chain KYC

1. Check DID: GET /api/v1/blockchain/did — see if user already has a DID
2. Create DID: POST /api/v1/blockchain/did — if none exists
3. Check on-chain KYC: GET /api/v1/blockchain/kyc
4. Complete KYC: POST /api/v1/blockchain/kyc/complete with {level: basic|standard|enhanced}


### Upgrade Membership

Stake tokens to reach a higher membership tier

1. View tiers: GET /api/v1/blockchain/membership/tiers — see requirements
2. Check current: GET /api/v1/blockchain/membership/status
3. Stake: POST /api/v1/blockchain/membership/stake with {amount}


## Rules

- DID creation is a one-time operation — once active, it cannot be recreated
- On-chain KYC and off-chain (MasterPay) KYC are independent — completing one does not require the other
- Staking records the token amount for tier calculation — tier is determined by the staked amount
- Higher tiers unlock lower fees and additional features (Tier 1: 10%, Tier 2: 15%, Tier 3: 20%, Tier 4: 25% discount)

## Agent Guidance

Follow these instructions when executing this skill:

- Always follow the documented flow order. Do not skip steps.
- If a tool requires authentication, verify the session has a valid bearer token before calling it.
- If a tool requires a transaction PIN, ask the user for it fresh each time. Never cache or log PINs.
- Never expose, log, or persist secrets (passwords, tokens, full card numbers, CVVs).
- If the user requests an operation outside this skill's scope, decline and suggest the appropriate skill.
- If a step fails, check the error and follow the recovery guidance below before retrying.

- DID creation is a one-time operation. Once active, it cannot be recreated. Confirm with the user before calling `create_did`.
- On-chain KYC and off-chain (MasterPay) KYC are independent systems. Completing `complete_blockchain_kyc` does not require MasterPay KYC to be approved.
- `complete_blockchain_kyc` requires a `level` parameter: one of "basic", "standard", or "enhanced". Always ask the user which level they want.
- Staking sets the token amount that determines the membership tier. Tier is calculated from the staked amount: Tier 1 (0 tokens, 10%), Tier 2 (15,000 tokens, 15%), Tier 3 (20,000 tokens, 20%), Tier 4 (25,000 tokens, 25%).
- Higher membership tiers unlock lower transaction fees and additional platform features.
