# CoinGecko Skill for Hermes Agent

## What is Bitcoin & Cryptocurrency

**Bitcoin** is "digital money" — a way to store and send value without a bank or government. Instead of trusting a company to hold your money, Bitcoin uses mathematics (cryptography) to prove ownership. You generate a unique key pair (like a username + super-secure password combined), and whoever holds the private key owns the Bitcoin.

**Why Bitcoin?** It's the hardest money ever created because:
- Supply is capped at 21 million coins (no government can print more)
- No bank can freeze your account or reverse transactions
- Transactions are permanent and transparent (recorded forever on the blockchain)
- You are your own bank (no middle man, no fees, no gatekeepers)

**Other cryptocurrencies** (Ethereum, Solana, other cryptocurrencies, etc.) build on Bitcoin's ideas but with different features. Ethereum added smart contracts (programs that run on the blockchain). other cryptocurrencies added privacy. Each solves different problems.

**Why prices matter:** Bitcoin's price in USD tells you what the market thinks Bitcoin is worth right now. If Bitcoin went from $50K to $75K, that's a 50% increase in value. Hermes tracks this via live price feeds so your applications running on Hermes always has current market context.

---

## Audit Result
Scanning 'coingecko' before publish...
Scan: coingecko (self/community)  Verdict: SAFE
Decision: ALLOWED — Allowed (community source, safe verdict)

---

## Description of This Skill

Live cryptocurrency price data integration for Hermes Agent. Fetch Bitcoin, Ethereum, and 10,000+ crypto assets using free CoinGecko API. Automatic fallback to Kraken if rate-limited. Zero credential exposure — API keys stay in `.env`, never in prompts.

---

## Meta-Data

- **version:** 1.0.0
- **author:** "Hermes local (May 2026)"
- **license:** MIT
- **platforms:** [linux]
- **category:** tools
- **tags:** [bitcoin, crypto, market-data, api, price-feed]

---

## What This Skill Does

**Price Data (No API Key Required for Basic Use)**
- ✅ Fetch current BTC/USD price (free via Kraken if no API key)
- ✅ Get 24-hour price change (shows if price went up or down)
- ✅ Return market cap and trading volume (how much is being traded)
- ✅ Query 10,000+ crypto assets (not just Bitcoin — Ethereum, Solana, etc.)
- ✅ Handle API timeouts gracefully with automatic fallback

**Data Formats**
- ✅ Return prices as dictionaries (for Python code)
- ✅ Format prices with commas and $ sign (for display)
- ✅ Include badges like "▲ 2.1%" or "▼ 1.8%" (for alerts/summaries)
- ✅ Provide raw JSON for programmatic use

**API Key Flexibility**
- ✅ Works with free Demo API key (best for Hermes)
- ✅ Works with paid Pro API key (unlimited rate limit)
- ✅ Auto-detects key type; no code changes needed
- ✅ Falls back to Kraken API (requires no key, always free)

**Security & Privacy**
- ✅ API keys stored securely in environment variables
- ✅ Never appears in Hermes chat, prompts, or logs
- ✅ Read-only access (can fetch prices, cannot trade or move funds)
- ✅ Transparent logging (all API calls timestamped, no credential leaks)
- ✅ Standalone operation (no dependencies on other systems)

---

## What This Skill Does NOT Do

**Will NOT trade crypto**
- ❌ This is a read-only price feed
- ❌ Cannot buy, sell, or move coins
- ❌ Cannot interact with exchanges (only view public prices)

**Will NOT expose API keys**
- ❌ API keys never logged, printed, or shown in chat
- ❌ Keys only passed via `$CG_API_KEY` environment variable
- ❌ No keys in prompts, function arguments, or transcripts

**Will NOT predict prices**
- ❌ This is a data fetcher, not a price prediction tool
- ❌ AI cannot predict markets reliably
- ❌ Use price data for context, not investment decisions

**Will NOT give financial advice**
- ❌ This skill provides data only, not recommendations
- ❌ Always do your own research before trading
- ❌ Consult a financial advisor for investment decisions

---

## Documentation

See `references/DESCRIPTION.md` for technical details, API endpoints, and troubleshooting.

---

## Author Notes

This skill brings live Bitcoin and crypto price data into Hermes without requiring credentials in chat or exposing sensitive keys. The design is simple:

1. **Fetch prices from CoinGecko** (largest crypto data provider, free + paid tiers)
2. **Fall back to Kraken** if rate-limited (free, no auth needed)
3. **Return data only** (never trade, never move funds)
4. **Keep keys safe** (never in logs, only in `.env`)

This skill is **standalone and independent**. It has no knowledge of DIB, trading systems, or other downstream consumers. Other systems call this skill when they need live price data—the skill just provides the data and exits. Perfect for trading bots, research scripts, price alerts, dashboards, or anything else that needs live crypto prices.

For Hermes users new to Bitcoin:
- Bitcoin price = what the market thinks Bitcoin is worth in USD right now
- Higher price doesn't mean Bitcoin is "better" — just more valuable in fiat currency
- Price changes hourly, so "live data" means you always get current market context
- Any system that uses prices should fetch live data at the moment it's needed, not recycle stale data

**Philosophy:** Bitcoin is global, open, and permissionless. Hermes should know its price without gatekeepers. This skill makes that possible.

---

## Getting Started

### Option 1: Free Demo API (Recommended for Hermes)

1. **Visit:** https://www.coingecko.com/en/api/documentation
2. **Click:** "Get free API key"
3. **Sign up:** Email + password (2 minutes)
4. **Copy key:** Dashboard will show `CG-...` string
5. **Add to .env:**
Set your CoinGecko API key in your Hermes environment:
```bash
Set your API key securely in your environment
echo "Setting API key..."
```
6. **Test:**
   ```bash
   your virtual environment/bin/python3 [config]/skills/coingecko/scripts/health_check.py
   ```

### Option 2: Free Kraken API (No Signup Needed)

If you don't want to sign up for CoinGecko:
1. **Do nothing** — Script auto-falls back to Kraken
2. **No API key needed** — Kraken public API is free
3. **Limitation:** Only BTC/USD, ETH/USD (no altcoins)
4. **Perfect for:** Hermes DIB generation (just needs BTC/USD)

### Option 3: Paid Pro API (For High-Volume Use)

If you run many agents or need unlimited queries:
1. **Visit:** https://www.coingecko.com/en/api/pricing
2. **Choose tier:** $10/month = most use cases
3. **Add key to .env** (same as Demo)
4. **Automatic:** Script detects Pro key and removes rate limits

---

## Common Questions

### Q: Is this secure? Can Hermes be hacked and leak my Bitcoin?

**A:** No. This skill is **read-only** — it can only fetch prices, not move coins. Your actual Bitcoin lives in a wallet (which you control via a private key). This skill has no access to wallets, exchanges, or your actual funds. The API key is only for fetching public prices.

Think of it like checking stock prices on Yahoo Finance — you're viewing data, not accessing your brokerage account.

### Q: Why two APIs (CoinGecko + Kraken)?

**A:** Redundancy. CoinGecko has more data (10,000+ assets) but has rate limits on the free tier. Kraken has fewer assets but works without auth. By using both, Hermes always gets a price even if one is rate-limited.

### Q: Why is the API key password-protected in .env?

**A:** To prevent accidental exposure. If someone steals your computer or reads your `.env` file without permission, they can only see prices — they can't access your actual Bitcoin wallets, exchanges, or funds. The key has no permissions to trade, transfer, or delete.

### Q: What if I don't provide an API key?

**A:** The script falls back to Kraken API (free, no key needed). You'll only get BTC/USD and ETH/USD, but that's enough for your daily DIB. No signup required.

### Q: How often should I rotate my API key?

**A:** For free Demo keys: rotate every 6-12 months as best practice. For Pro keys: same, plus monitor your CoinGecko dashboard for suspicious activity. If you suspect a key is exposed, regenerate immediately in the dashboard (takes 2 minutes).

### Q: Can this script trade Bitcoin for me?

**A:** No. It's read-only. It can only fetch prices. To actually trade, you'd need to use an exchange API (Binance, Kraken, Coinbase) with write permissions, which requires separate authentication and puts your funds at risk. This skill doesn't do that.

---

## Install CoinGecko Skill

**Direct from Hermes skills:**
```bash
hermes skills install coingecko
```

Or manually:
use cd skills, then use cloning in git with the proper repository-url
go to cd coingecko, python3 -m venv env, finally use pip to install ...
---

## Legal Disclaimer

This CoinGecko skill and associated code is provided for educational and informational purposes only. The code is offered "as is", without any warranty of any kind. Use of this skill is entirely at your own risk.

The author is not responsible or liable for:
- Price accuracy or staleness (CoinGecko/Kraken are responsible)
- Any trading decisions based on prices fetched
- Any service disruptions from CoinGecko or Kraken
- Any financial losses resulting from use

CoinGecko and Kraken are third-party services. This skill is a client integration only. Always verify prices independently before making financial decisions.

This does not constitute financial advice, investment guidance, or professional software. By using this skill you agree you are solely responsible for your compliance with applicable laws. This is not financial advice.
>>>>>>> 14d7c26 (feat: add coingecko skill (CoinGecko API integration))
