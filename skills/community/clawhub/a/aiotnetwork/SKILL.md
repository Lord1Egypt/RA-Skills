---
name: AIOT Network
description: Meta-skill that indexes all AIOT platform skills and routes agent requests to the correct sub-skill.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIOT_API_BASE_URL
    primaryEnv: AIOT_API_BASE_URL
---

# AIOT Network

This is the routing index for the AIOT platform. Use it to determine which sub-skill handles a given user request, then delegate to that skill.

## Configuration

The default API base URL is `https://payment-api-dev.aiotnetwork.io`. All sub-skills use this as the base for API requests.

To override (e.g. for local development):

```bash
export AIOT_API_BASE_URL="http://localhost:8080"
```

If `AIOT_API_BASE_URL` is not set, use `https://payment-api-dev.aiotnetwork.io` as the base for all requests.

## Skill Index

| Skill | Install Slug | Use Cases |
|-------|-------------|-----------|
| Account & Authentication | `aiotnetwork-account-auth` | sign up, log in, manage sessions, reset their password, or link a Web3 wallet |
| KYC & Identity | `aiotnetwork-kyc-identity` | complete identity verification, upload KYC documents, or check verification status |
| Card Management | `aiotnetwork-card-management` | create virtual cards, view card details, or manage card lifecycle (lock, unlock, cancel) |
| Payments & Banking | `aiotnetwork-payments-banking` | top up a wallet, send money, make international remittances, or convert currencies |
| Crypto Wallet | `aiotnetwork-crypto-wallet` | deposit cryptocurrency into their wallet or withdraw to an external address |
| Blockchain & DID | `aiotnetwork-blockchain-did` | set up a decentralized identity, complete on-chain KYC, or manage membership tiers |

## Cross-Skill Dependencies

Some operations span multiple skills. Follow these dependency chains in order:

1. **Account → KYC → Card**: User must sign up (account-auth), complete KYC (kyc-identity), then create cards (card-management).
2. **Account → Payments**: User must be authenticated (account-auth) before any payment operation (payments-banking).
3. **Account → Crypto**: User must be authenticated (account-auth) before depositing or withdrawing crypto (crypto-wallet).
4. **Account → Blockchain DID**: User must be authenticated (account-auth) before creating a DID or staking (blockchain-did).
5. **KYC → Wallet KYC → Card**: MasterPay KYC (kyc-identity) must be approved, then wallet KYC submitted, before card creation (card-management).

## Agent Guidance

- When a user request matches a single skill, delegate directly to that skill.
- When a request spans multiple skills, follow the dependency chains above and execute skills in order.
- If the user has not completed a prerequisite (e.g., no account, KYC not approved), guide them through the prerequisite skill first.
- Each sub-skill contains its own detailed tool definitions, flows, rules, and guidance — always refer to the sub-skill for implementation details.

## Installation

To install all AIOT platform skills at once, run:

```bash
bash scripts/install.sh
```

Or install individual skills:

```bash
clawhub install aiotnetwork-account-auth
```
```bash
clawhub install aiotnetwork-kyc-identity
```
```bash
clawhub install aiotnetwork-card-management
```
```bash
clawhub install aiotnetwork-payments-banking
```
```bash
clawhub install aiotnetwork-crypto-wallet
```
```bash
clawhub install aiotnetwork-blockchain-did
```
