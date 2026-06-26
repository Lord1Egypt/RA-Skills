# Security Checklist for Freqtrade + Kraken

> **Your API keys are your password to your money.** One mistake can drain your account. This checklist prevents that.

---

## 🔑 API Key Generation

### When Creating Keys on Kraken

**DO THIS:**

- [ ] Create keys with **minimal permissions only**
  - ✅ Funds: Query
  - ✅ Orders: Query open orders & trades
  - ✅ Orders: Query closed orders & trades
  - ✅ Orders: Create & modify orders
  - ✅ Orders: Cancel & close orders

- [ ] **NEVER enable:**
  - ❌ Withdraw
  - ❌ Deposit
  - ❌ Earn
  - ❌ Any "admin" permission

**Why?** If your API key leaks, an attacker can only trade — not drain your funds.

### Withdrawal Permission = Game Over

If a leaked key has Withdraw permission:
- Attacker can move all your funds to their wallet
- Kraken will NOT reverse the transaction
- You've lost everything

**Literally do not enable it. Ever.**

---

## 📦 Key Storage

### Step 1: .env File (Local Machine)

```bash
# Good ✅
FREQTRADE__EXCHANGE__KEY=your-api-key
FREQTRADE__EXCHANGE__SECRET=your-secret

# Bad ❌
export FREQTRADE__EXCHANGE__KEY=your-api-key  # In a script that gets committed
key = "abc123..."  # Hardcoded in config.json
```

**Rules:**
- [ ] `.env` file exists in your Freqtrade directory
- [ ] `.env` is in `.gitignore`
- [ ] Never commit `.env` to git
- [ ] Never paste keys in chat, email, or forums

**Check:**
```bash
cat .gitignore | grep .env
# Should output: .env
```

### Step 2: Docker Environment

Edit `docker-compose.yml`:

```yaml
services:
  freqtrade:
    environment:
      - FREQTRADE__EXCHANGE__KEY=your-api-key
      - FREQTRADE__EXCHANGE__SECRET=your-secret
```

**Not:**
```yaml
# BAD ❌
environment:
  - FREQTRADE__EXCHANGE__KEY=your-api-key  # Hardcoded in committed file
```

### Step 3: config.json Reference

```json
{
  "exchange": {
    "name": "kraken",
    "key": "empty string ("")",
    "secret": "empty string ("")"
  }
}
```

**Check:** `cat config.json | grep "key":` should show `"empty string ("")"`, not actual keys.

---

## 🔒 Operational Security

### Pre-Launch Checks

- [ ] Dry-run mode enabled (`"dry_run": true`)
- [ ] Paper trading only (no real money yet)
- [ ] max_open_trades set to 3 or fewer (limits exposure)
- [ ] stake_amount is small (start with $10-50)

### Repository Safety

- [ ] `.env` in `.gitignore`
- [ ] `config.json` does NOT contain real keys
- [ ] Never committed `.env` to git history
- [ ] If you accidentally committed keys: **rotate them immediately**

**If you leaked keys:**
```bash
# On Kraken: disable + regenerate the API key immediately
# On your machine:
rm .env  # Delete the old one
# Create new .env with new keys from Kraken
```

### Running Freqtrade Safely

```bash
# Safe: Keys loaded from environment
docker-compose up

# Unsafe: Passing keys as arguments ❌
docker-compose run freqtrade --kraken-key=abc123

# Unsafe: Keys in shell history ❌
export FREQTRADE__EXCHANGE__KEY=abc123  # This gets saved in ~/.bash_history
```

---

## 💰 Fund Protection

### Kraken Account Setup

- [ ] Enable 2FA (two-factor authentication)
- [ ] Use strong, unique password (16+ chars, mix of types)
- [ ] Add IP whitelist if Kraken offers it
- [ ] Keep an eye on API key usage: Kraken dashboard → API → Activity log

### Freqtrade-Specific Limits

```json
{
  "max_open_trades": 3,
  "stake_amount": "0.01",
  "dry_run": true
}
```

| Setting | Purpose | Safe Value |
|---------|---------|-----------|
| `max_open_trades` | Max concurrent bots | 3 (limits exposure) |
| `stake_amount` | Per-trade size | $10-50 when live |
| `dry_run` | Paper trading | `true` for first 2-4 weeks |

### Live Trading Stages

1. **Week 1-2:** Dry-run only. Validate strategy works.
2. **Week 3-4:** Live mode, $50-100 total. Test real execution.
3. **Week 5+:** Scale up as you gain confidence.

Never jump to $1000 trades without weeks of testing.

---

## 🚨 Incident Response

### If You Suspect Key Leak

1. **Immediately go to Kraken**
2. **Disable the API key** (Settings → API → Deactivate)
3. **Check account history** for unauthorized trades
4. **Generate new key** with new name
5. **Update .env** with new key
6. **Restart Freqtrade** to use new key

Contact Kraken support immediately. Outcomes vary — there are no guarantees of recovery. Freqtrade and exchanges are used at your own risk; this is experimental software.

### If You See Unauthorized Activity

1. Check the API activity log on Kraken
2. Identify what happened (unauthorized trade? withdrawal attempt?)
3. Note timestamp and amount
4. Contact Kraken support with evidence
5. Disable key and regenerate

---

## 📋 Launch Checklist

Use this before enabling live trading:

- [ ] `.env` file created with API keys
- [ ] `.env` added to `.gitignore`
- [ ] `config.json` uses `empty string ("")` syntax (not literal keys)
- [ ] `dry_run: true` in config
- [ ] `max_open_trades: 3` or fewer
- [ ] `stake_amount: 0.01` (start small in live mode)
- [ ] Downloaded 1+ year of historical data
- [ ] Backtested strategy with at least 100+ trades
- [ ] Run dry-run for 2+ weeks
- [ ] No sensitive data in git history
- [ ] Kraken 2FA enabled
- [ ] Kraken password is strong and unique

---

## Common Mistakes to Avoid

| Mistake | Cost | Fix |
|---------|------|-----|
| Enable Withdraw permission on API key | Everything | Never enable it |
| Hardcode keys in config.json | Key leak if repo exposed | Use `${ENV_VAR}` syntax |
| Enable live trading before dry-run | Money | Always dry-run first |
| High max_open_trades | Large drawdown | Start with 3 or less |
| Large stake_amount first trade | Catastrophic loss | Start with $10-50 |
| No 2FA on exchange account | Account takeover | Enable immediately |
| Ignore API activity logs | Late fraud detection | Check weekly |

---

## Questions?

- **Freqtrade docs:** https://www.freqtrade.io/en/latest/exchanges/#kraken
- **Kraken API docs:** https://docs.kraken.com/rest/
- **Exchange comparison:** See `exchange-comparison.md` in this folder
