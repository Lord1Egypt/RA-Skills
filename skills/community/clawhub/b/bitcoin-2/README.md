# Bitcoin L1 Blockchain Skill for Hermes Agent

## What is Bitcoin

**Bitcoin** is "digital money" — a way to store and send value without a bank or government. Instead of trusting a company to hold your money, Bitcoin uses mathematics (cryptography) to prove ownership. You generate a unique key pair (like a username + super-secure password combined), and whoever holds the private key owns the Bitcoin.

**Why Bitcoin?** It's the hardest money ever created because:
- Supply is capped at 21 million coins (no government can print more)
- No bank can freeze your account or reverse transactions
- Transactions are permanent and transparent (recorded forever on the blockchain)
- You are your own bank (no middle man, no fees, no gatekeepers)

**How Bitcoin works:**
- You own a private key (secret, like a password)
- You derive a public address from that key (like your bank account number)
- Anyone can send Bitcoin to your address
- Only the private key holder can spend it
- Miners verify transactions and secure the network

**Why on-chain data matters:** Bitcoin's price, network fees, and transaction flow tell you what the market thinks and how the network is operating right now. Hermes tracks this via live Mempool data so your applications always have current blockchain context.

---

## Description of This Skill

Live Bitcoin L1 blockchain data integration for Hermes Agent. Query address balances, transaction details, fee estimates, mempool analysis, and block data using the free Mempool.space REST API. Automatic BTC/USD pricing via CoinGecko. Zero credential exposure — no API keys required.

---

## Meta-Data

- **version:** 1.0.0
- **author:** "bronoman (May 2026)"
- **license:** MIT
- **platforms:** [linux]
- **category:** blockchain
- **tags:** [bitcoin, btc, l1, blockchain, utxo, mempool, on-chain, fees]

---

## What This Skill Does

**Address & UTXO Data (No API Key Required)**
- ✅ Fetch Bitcoin address balances (confirmed + unconfirmed)
- ✅ Scan unspent outputs (UTXOs) and sort by value
- ✅ Get transaction count and address history
- ✅ Detect address type (P2PKH, P2SH, P2WPKH, P2TR, Taproot)
- ✅ Display total received/spent for any address

**Transaction Inspection**
- ✅ Look up transaction by TXID
- ✅ View all inputs and outputs
- ✅ Calculate fees in satoshis, sat/vB, BTC, and USD
- ✅ Check confirmation status and block height
- ✅ Identify transaction size and virtual bytes

**Network Fee Analysis**
- ✅ Get current fee estimates (sat/vB)
- ✅ Show estimates for 1m, 10m, 24h confirmation targets
- ✅ Display fee distribution histogram (what % of txs at each rate)
- ✅ Calculate typical transaction costs (250vB example)
- ✅ Identify low-fee windows for sending

**Mempool Statistics**
- ✅ Live pending transaction count
- ✅ Mempool size in MB (virtual bytes)
- ✅ Fee distribution by satoshi rate
- ✅ Total fees pending in the pool
- ✅ Estimated backlog time

**Block Monitoring**
- ✅ Get recent blocks with timestamps
- ✅ Show transaction count per block
- ✅ Display block size in KB
- ✅ Relative time formatting ("2 hours ago")
- ✅ Monitor network activity

**Network Status**
- ✅ Latest block height
- ✅ Current network time
- ✅ Mempool state overview
- ✅ Fee environment summary
- ✅ BTC/USD price and market data

**Price Data (CoinGecko Integration)**
- ✅ Fetch current BTC price in 10 currencies
- ✅ Supported: USD, EUR, GBP, JPY, CHF, CAD, AUD, SGD, INR, HKD
- ✅ Correct decimal formatting (JPY has no decimals)
- ✅ Always current market price

---

## What This Skill Does NOT Do

**Will NOT provide trading advice**
- ❌ This is a data fetcher, not a price prediction tool
- ❌ AI cannot predict markets reliably
- ❌ Use price data for context, not investment decisions

**Will NOT execute transactions**
- ❌ Cannot send, receive, or move Bitcoin
- ❌ Cannot access wallets or private keys
- ❌ Read-only blockchain query only

**Will NOT predict fees or times**
- ❌ Fee estimates are probabilistic based on current mempool
- ❌ Actual confirmation times vary with network congestion
- ❌ Use estimates as guidance, not guarantees

**Will NOT give financial advice**
- ❌ This skill provides data only, not recommendations
- ❌ Always do your own research before transacting
- ❌ Consult a financial advisor for investment decisions

**Will NOT guarantee real-time data**
- ❌ Mempool.space updates every 10 seconds
- ❌ Block data lags by 1-2 seconds
- ❌ Prices cached and updated frequently but not tick-by-tick

---

## Quick Start

### Installation

From Hermes:
```bash
hermes skills install github.com/bronoman/hermes-skills bitcoin
```

Or manually:
```bash
cd ~/.hermes/skills/blockchain/bitcoin
python3 scripts/bitcoin_client.py stats
```

### 7 Commands

**1. Get Address Balance & UTXOs**
```bash
python3 scripts/bitcoin_client.py address <bitcoin_address> [--limit 20]
```
Example:
```bash
python3 scripts/bitcoin_client.py address 1A1z7agoat3bLsCywJ6H7qqyiB8t6SE2Kt
```

**2. Inspect Transaction**
```bash
python3 scripts/bitcoin_client.py tx <txid>
```
Example:
```bash
python3 scripts/bitcoin_client.py tx abc123def456...
```

**3. Get Fee Estimates**
```bash
python3 scripts/bitcoin_client.py fees [--currency USD]
```
Returns: sat/vB rates for 1m, 10m, 24h targets

**4. Mempool Analysis**
```bash
python3 scripts/bitcoin_client.py mempool
```
Returns: pending tx count, pool size, fee distribution

**5. Recent Blocks**
```bash
python3 scripts/bitcoin_client.py blocks [--limit 10]
```
Returns: latest blocks with timestamps and tx counts

**6. Network Stats**
```bash
python3 scripts/bitcoin_client.py stats
```
Returns: block height, mempool size, fees, BTC price

**7. BTC Price**
```bash
python3 scripts/bitcoin_client.py price [--currency EUR]
```
Returns: BTC price in specified currency

---

## API Integration

**Mempool.space REST API**
- Free, no authentication required
- Rate limit: ~30-50 requests/minute
- Endpoints: `/api/blocks`, `/api/address/{addr}`, `/api/tx/{txid}`, `/api/mempool`, `/api/v1/fees/recommended`

**CoinGecko (Optional)**
- Free API for BTC/USD pricing
- Optional API key for higher limits
- Falls back to Mempool prices if unavailable

**No External Dependencies**
- Uses Python stdlib only (urllib, json, argparse, datetime)
- No third-party packages required
- Works on any Python 3.8+ (included with Python distribution)

---

## Common Questions

### Q: Is this secure? Can Hermes be hacked and leak my Bitcoin?

**A:** No. This skill is **read-only** — it can only fetch blockchain data, not move coins. Your actual Bitcoin lives in a wallet (which you control via a private key). This skill has no access to wallets, exchanges, or your actual funds.

Think of it like checking public stock prices on Yahoo Finance — you're viewing data, not accessing your brokerage account.

### Q: Why no API key needed?

**A:** Mempool.space provides free public blockchain data. All Bitcoin transactions are public by design. This skill just queries that public data. No authentication needed.

### Q: Can this predict Bitcoin price?

**A:** No. It shows current market price, not predictions. Bitcoin price depends on supply/demand, macroeconomic factors, sentiment, and many variables AI can't reliably predict.

### Q: Can this help me trade Bitcoin?

**A:** It provides data for context, but doesn't execute trades. To trade, you'd need to use an exchange API (Coinbase, Kraken, Binance) with write permissions, which is a separate integration. This skill is read-only.

### Q: Why are fee estimates different from what I see elsewhere?

**A:** Mempool.space estimates based on current pool state. Different services use different algorithms. Actual fees depend on network congestion at the moment you broadcast. Use estimates as guidance, not guarantees.

### Q: What if Mempool.space is down?

**A:** The script returns an error. For production use, set `BITCOIN_API_URL` to a self-hosted Mempool instance or commercial provider with redundancy.

---

## Environment Variables

```bash
# Optional: Use custom Mempool instance (default: mempool.space)
export BITCOIN_API_URL="https://mempool.space/api"

# Optional: CoinGecko API key (for better rate limits on prices)
export COINGECKO_API_KEY="your-key-here"
```

---

## Author Notes

This skill brings live Bitcoin blockchain data into Hermes without requiring credentials or API keys in chat. The design is simple:

1. **Query Mempool.space** (largest Bitcoin mempool tracker, free, no auth)
2. **Fetch price from CoinGecko** (optional, falls back to Mempool)
3. **Return data only** (never transact, never move funds)
4. **Keep everything public** (Bitcoin data is public by design)

This skill is **standalone and independent**. It has no knowledge of trading systems, wallets, or other downstream consumers. Other systems call this skill when they need blockchain data — the skill just provides the data and exits. Perfect for dashboards, monitoring systems, trading research, fee analysis, or anything else that needs live Bitcoin data.

For Hermes users new to Bitcoin:
- Bitcoin address = your public identifier (like an email, anyone can send you coins)
- Private key = your ownership proof (like a password, never share it)
- UTXO = unspent output (Bitcoin you can spend, coins are immutable until spent)
- sat/vB = satoshis per virtual byte (fee measurement, lower = cheaper)
- Mempool = waiting room for transactions (before they get mined into blocks)
- Block height = which block number is current (increments every ~10 minutes)

**Philosophy:** Bitcoin is global, open, and permissionless. Hermes should know its state without gatekeepers. This skill makes that possible.

---

## Install Bitcoin Skill

**From Hermes:**
```bash
hermes skills install github.com/bronoman/hermes-skills bitcoin
/use bitcoin
```

Or manually:
```bash
cd ~/.hermes/skills/blockchain/bitcoin
python3 scripts/bitcoin_client.py --help
```

---

## Legal Disclaimer

This Bitcoin L1 blockchain skill and associated code is provided for educational and informational purposes only. The code is offered "as is", without any warranty of any kind. Use of this skill is entirely at your own risk.

The author is not responsible or liable for:
- Price accuracy or staleness (Mempool/CoinGecko are responsible for their data)
- Any trading decisions based on blockchain data fetched
- Any service disruptions from Mempool.space or CoinGecko
- Any financial losses resulting from use
- Misinterpretation of fee estimates or confirmation times

Mempool.space and CoinGecko are third-party services. This skill is a client integration only. Always verify data independently before making financial decisions.

This does not constitute financial advice, investment guidance, or professional software. By using this skill you agree you are solely responsible for your compliance with applicable laws. This is not financial advice.

Bitcoin is a public blockchain — all transactions are visible to everyone. Do not assume privacy. Address balances are public. Transaction amounts are public. Only the owner of a private key can move coins.

---

## Testing & Verification

```bash
# Verify API connectivity
python3 scripts/bitcoin_client.py stats

# Test address lookup (Satoshi's famous address)
python3 scripts/bitcoin_client.py address 1A1z7agoat3bLsCywJ6H7qqyiB8t6SE2Kt

# Check current fees
python3 scripts/bitcoin_client.py fees

# Analyze mempool
python3 scripts/bitcoin_client.py mempool

# Get BTC price
python3 scripts/bitcoin_client.py price --currency EUR
```

All commands should return structured JSON-compatible output within 2-3 seconds.
