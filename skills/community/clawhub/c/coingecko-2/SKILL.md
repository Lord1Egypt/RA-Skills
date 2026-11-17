---
name: coingecko
description: "Live Bitcoin & crypto price data via CoinGecko API. Fetch BTC/USD, ETH/USD, multi-asset quotes. Supports both Demo (free) and Pro API keys. No credentials in prompts—only .env isolation."
version: 1.0.0
author: "bronoman & Hermes local (May 2026)"
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [bitcoin, crypto, market-data, api, price-feed]
    category: tools
    requires_tools: [terminal]
required_environment_variables:
  - name: CG_API_KEY
    prompt: "CoinGecko API key (Demo: free, Pro: paid)"
    help: "Get free Demo API at https://www.coingecko.com/en/api/documentation. Demo = rate-limited, always works. Pro = unlimited, requires payment. Key never leaves .env file."
    required_for: "Price queries (fallback to Kraken if absent)"
    password: true
optional_environment_variables:
  - name: CG_FALLBACK_KRAKEN
    prompt: "Use Kraken API as fallback? (true/false)"
    default: "true"
    help: "Kraken public API requires no auth. Set false to disable fallback."
---

# CoinGecko Skill for Hermes Agent

**Skill Path:** `[config]/.hermes/skills/coingecko`

Live cryptocurrency price data integration with private key isolation and fallback redundancy. Fetch Bitcoin, Ethereum, and 10,000+ crypto asset prices using free CoinGecko API or paid Pro tier.

---

## Features Overview

| Feature                           | Status     | Auth Required | Fallback          |
|-----------------------------------|------------|---------------|-------------------|
| Fetch BTC/USD Price               | ✅         | Optional (Demo key works) | Kraken API        |
| Fetch Multi-Asset Prices          | ✅         | Optional      | Kraken API        |
| 24h Price Change                  | ✅         | Optional      | Kraken (limited)  |
| Market Cap & Volume               | ✅ Pro     | Optional      | Kraken (limited)  |
| Format Price Data                 | ✅         | No            | —                 |
| Automatic Price Refresh           | ✅         | No            | —                 |

---

## Security Architecture

CoinGecko API key **never** reaches Hermes chat or logs.  
All price data queries are **read-only** (no signing, no write permissions).  
Credentials stored securely using environment variable isolation.

---

## Core Scripts

All scripts are in:  
`[config]/.hermes/skills/coingecko/scripts/`

- `fetch_price.py` — Fetch live BTC/USD from CoinGecko or Kraken  
- `fetch_multi_asset.py` — Query multiple crypto assets at once  
- `health_check.py` — Verify API connectivity and key validity  

---

## Quick Usage

### Fetch Current BTC/USD Price
```bash
python3 [skill-scripts]/fetch_price.py
# Returns: {"price": 81291.00, "price_str": "$81,291.00", "change_24h": 0.48, ...}
```

### Fetch Multiple Assets
```bash
python3 [skill-scripts]/fetch_multi_asset.py bitcoin ethereum
# Returns: {"bitcoin": {"price": 81291}, "ethereum": {"price": 2432.50}}
```

### Health Check (Verify API Key)
```bash
python3 [skill-scripts]/health_check.py
# Returns: {"api_status": "ok", "key_type": "demo", "rate_limit_remaining": 10}
```

---

## Skill Details

This skill provides **standalone cryptocurrency price data integration** for Hermes. Fetch live Bitcoin and Ethereum prices, query thousands of crypto assets, and integrate market data into any workflow—all with automatic fallback to Kraken API if CoinGecko key is unavailable.

**Key Advantage:** Works as an independent skill. Can be used for trading, research, monitoring, alerts, or any use case that needs live crypto prices. content processors and other downstream systems call this skill as needed.

---

## API Key Types Explained

### Demo Key (Free ✅)
- **Where to get:** https://www.coingecko.com/en/api/documentation
- **Signup:** 2 minutes, email + password
- **Limits:** 10-50 calls/minute (rate-limited but stable)
- **Endpoint:** `https://api.coingecko.com/api/v3/...` with `x_cg_demo_api_key` param
- **Cost:** Free forever
- **Best for:** Low volume trading, Hermes agents, hobby projects, content generation

### Pro Key (Paid 💰)
- **Where to get:** https://www.coingecko.com/en/api/pricing
- **Signup:** 5 minutes via API dashboard
- **Limits:** Unlimited calls (enterprise tier available)
- **Endpoint:** Same as Demo, with `x_cg_pro_api_key` param
- **Cost:** $10-50/month depending on tier
- **Best for:** High-volume data pipelines, trading bots, critical services

**Script handles both automatically** — no code changes needed. Just add key to `.env` and script auto-detects type.

---

## Getting Your API Key (Demo)

1. **Visit:** https://www.coingecko.com/en/api/documentation
2. **Click:** "Get free API key" (top right)
3. **Fill in:** Email + strong password
4. **Verify:** Check your email for verification link
5. **Copy:** Your demo key will appear in dashboard
6. **Configure:** Set up your API key:
   ```
   API_KEY=CG-JptZUWeFoPzfDLKmFPE3bMn3
   ```
7. **Test:** Run health_check.py to verify

---

## Dual-Source Redundancy

If CoinGecko key fails or is rate-limited, script **automatically falls back to Kraken API** (no auth needed):

```
┌─────────────────────────────────────────┐
│ fetch_price.py                          │
│  1. Try CoinGecko (has more data)       │
│     ├─ With Demo key: 10-50 calls/min   │
│     ├─ With Pro key: unlimited          │
│     └─ On rate-limit: timeout ×3, then→├─┐
│  2. Fall back to Kraken (no auth)       │ │
│     ├─ Always works for BTC/USD         │ │
│     ├─ Limited to major pairs           │ │
│     └─ Returns: {"BTC": price, ...}     │ │
│  3. On both fail: Return error          │ │
│                                         │ │
└─────────────────────────────────────────┘ │
  Return: {"price": N, "source": "..."}   ←─┘
```

---

## Security & Privacy

### ✅ What You Can Trust

**API Key Isolation**
- API key never appears in Hermes prompts, memory, or logs
- Only `fetch_price.py` reads from `$CG_API_KEY` environment
- Script returns only **public data** (price, market cap, 24h change)
- Key is **read-only** — CoinGecko API has no write/delete permissions

**No Data Leakage**
- Price data is public (anyone can fetch without a key)
- API key only needed for rate-limit increases
- Hermes Agent never sees the key during operation

**Transparent & Auditable**
- All API calls logged with timestamp and source
- Error messages never contain credential details
- Fallback behavior is deterministic and logged

### ⚠️ What You Must Do

**Protect Credential Files**


**Never Share Your Key**
- Don't paste `.env` in chat, tickets, or public repos
- Don't commit `.env` to git (add to `.gitignore`)
- If key is exposed, regenerate in CoinGecko dashboard (takes 2 minutes)

**Rotate Keys Periodically**
- Even for free keys, rotate every 6-12 months
- Check CoinGecko dashboard for suspicious activity
- If suspicious: regenerate immediately

---

## Troubleshooting

### Symptom: "Connection timeout" or "No such host"

**Cause:** Network unreachable or DNS failure

**Fix:**
```bash
# Test connectivity to CoinGecko
curl -s https://api.coingecko.com/api/v3/ping

# Should return: {"gecko_says":"..."}
# If fails: Check internet connection, firewall, DNS
```

### Symptom: "Invalid API key" or 401 Unauthorized

**Cause:** Key is malformed, expired, or incorrect

**Fix:**
1. Verify your API key is configured (no extra spaces)
2. Check CoinGecko dashboard — key may have expired
3. Regenerate key and update `.env`
4. Test with: `health_check.py`

### Symptom: "Rate limit exceeded" (HTTP 429)

**Cause:** Demo key limit reached (10-50 calls/min)

**Fix:**
1. Wait 1-2 minutes (rate limit resets)
2. Script auto-retries with exponential backoff
3. Upgrade to Pro key for unlimited access
4. Or: Reduce query frequency

### Symptom: Kraken fallback returns "No data"

**Cause:** Kraken doesn't support that trading pair

**Fix:**
- Kraken only supports major pairs (BTC/USD, ETH/USD)
- For altcoins, CoinGecko Demo key is required
- Upgrade to Pro key to avoid rate limits on altcoins

---

## Environment & Credentials Checklist

- [ ] Python venv at `[config]/.hermes/coingecko-env`
- [ ] Dependencies: `requests`, `urllib3`, `python-dotenv`
- [ ] Credential storage contains API key=CG-...` (or empty for Kraken fallback)
- [ ]  ``
- [ ] Manual test: `health_check.py` returns `"api_status": "ok"`
- [ ] Manual test: `fetch_price.py` returns valid BTC price
- [ ] Manual test: `fetch_multi_asset.py bitcoin ethereum` returns multiple prices

---

## Verified Success Record

**Tested (May 11, 2026):**
```
CoinGecko Demo API:
  Price: $81,291.00 (▲ 0.48%)
  Source: CoinGecko API
  Status: ✅ Working

Kraken Fallback:
  Price: $81,313.50
  Source: Kraken (no auth)
  Status: ✅ Working

```

---

## What's New in v1.0

✅ **Initial release** — Full CoinGecko + Kraken integration  
✅ **Dual-source redundancy** — Automatic fallback to Kraken if Demo key rate-limited  
✅ **Content integration-ready** — Bitcoin content generator with live price  
✅ **Zero-exposure design** — API keys stored in `.env` only, never in prompts/logs  
✅ **Demo + Pro support** — Works with both free and paid API tiers  

---

## Author Notes

This skill represents clean, secure, **standalone** cryptocurrency data integration for Hermes Agent. Every operation is:
- **Read-only** (no write permissions to markets or accounts)
- **Redundant** (dual-source fallback to Kraken)
- **Transparent** (all API calls logged with timestamp)
- **Credential-safe** (keys never exposed in prompts or memory)
- **Self-contained** (no dependencies on downstream systems)

The philosophy is simple: **Live market data should be free and accessible**. This skill brings that to Hermes through both free (Demo API) and professional (Pro API) tiers, with automatic fallback so you always get a price.

Downstream systems like the Daily Intelligence Brief call this skill when they need live price data. The skill has no knowledge of or dependency on calling processes, it is purely a data provider.

**Philosophy:** Bitcoin is the hardest money ever created. Hermes should know its price in real-time, always. This skill makes that possible, for any use case.

PRs welcome.

---

## Legal Disclaimer

This CoinGecko skill and associated code is provided for educational, informational, and agent integration purposes only. The code is offered "as is", without any warranty of any kind. Use of this skill is entirely at your own risk.

The author is not responsible or liable for:
- Price accuracy or staleness (CoinGecko/Kraken are responsible for their data)
- Any trading decisions based on prices fetched via this skill
- Any service disruptions from CoinGecko or Kraken
- Any financial losses resulting from use of this skill

CoinGecko and Kraken are third-party services operated by independent companies. This skill is a client integration only. Always verify prices independently before making financial decisions.

This project is an expression of technical exploration. It does not constitute financial advice, investment guidance, or professional software.

By using this skill you agree that you are solely responsible for your own actions and compliance with all applicable laws and regulations regarding cryptocurrency trading, taxation, and financial reporting. This is not financial advice.
