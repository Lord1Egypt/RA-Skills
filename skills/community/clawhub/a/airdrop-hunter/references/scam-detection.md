# Scam Detection Guide

## Overview

This document provides guidelines for detecting and warning about Web3 scams.

---

## 1. Fake Claim Websites

### Phishing Patterns

```
🚨 RED FLAGS:
- Contains "claim", "free", "reward", "airdrop" in domain
- Hyphenated knockoffs: scroll-airdrop.io, arbitrum-claims.com
- Random numbers: airdrop2026.xyz, claim-now123.net
- Unusual TLDs: .xyz, .top, .click, .work (when not official)
- Subdomain tricks: claim.official-project.xyz
```

### Verification Steps

1. Check project's official Twitter bio for website
2. Compare domains character by character
3. Search "[project name] scam" on Twitter
4. Verify on project's official docs/GitHub

### Warning Format

```markdown
⚠️ PHISHING ALERT

🚨 Suspicious Domain: [domain]
✅ Official Domain: [verified domain]

DO NOT:
- Visit the suspicious link
- Connect your wallet
- Sign any transactions
```

---

## 2. Social Engineering Scams

### Common Patterns

| Type | Example | Red Flag |
|------|---------|----------|
| DM Scam | "You won airdrop, click here" | Unsolicited claim link |
| Impersonation | Fake support account | Slightly different handle |
| Urgency | "Claim within 1 hour or lose" | Artificial deadline |
| Gas Request | "Pay 0.01 ETH to claim" | Legit claims are free |

### Warning Format

```markdown
⚠️ SOCIAL SCAM ALERT

🚨 Pattern Detected: [type]
📩 Example: "You won [X] airdrop, click link to claim"

✅ REMEMBER:
- Official projects NEVER send claim links via DM
- Official projects NEVER ask for private keys
- Official projects NEVER require upfront gas payment for claims

ACTION: Block and report the sender
```

---

## 3. Fake Token Scams

### Detection Criteria

| Check | Legitimate | Scam |
|-------|------------|------|
| Exchange Listing | Binance, OKX, Bybit | Only DEX |
| Verification | CoinGecko/CMC listed | Not listed |
| Contract | Verified on official site | Random address |
| Liquidity | High, locked | Low, unlocked |

### Warning Format

```markdown
⚠️ FAKE TOKEN ALERT

🚨 Counterfeit Token: "[TICKER]" on DEX
❌ This is NOT the official token

✅ OFFICIAL TOKEN:
- Listed on: [Binance, OKX, Bybit]
- Contract: [official address]
- Verify at: [official website]

DO NOT buy the DEX version
```

---

## Quick Verification Checklist

```
□ Domain matches official Twitter bio
□ Contract address matches official docs
□ Token listed on major exchanges (if launched)
□ No upfront payment required for claims
□ Official announcement exists
□ Community sentiment is positive
```

---

## Emergency Response

If user encounters suspected scam:

1. **STOP** - Do not click any links
2. **VERIFY** - Check official channels
3. **REPORT** - Alert community
4. **PROTECT** - Never share private keys
