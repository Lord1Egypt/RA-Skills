# 🤖 Crypto Trading Bot

Automated crypto scalping bot for Binance Futures USDT-M

> ⚠️ **WARNING**: Futures trading is HIGH RISK. Never invest more than you can afford to lose.

---

## 📋 Requirements

- VPS with Ubuntu/Debian
- Python 3.8+
- Binance Futures account
- Telegram bot (optional, for notifications)

---

## 🚀 Quick Setup

### Step 1: Clone & Enter Folder

```bash
git clone https://github.com/mail-eth/crypto-trading-bot.git
cd crypto-trading-bot
```

### Step 2: Get Your API Keys

#### Binance API
1. Go to [Binance](https://www.binance.com) → Login
2. API Management → Create New Key
3. Enable **Futures** trading
4. Permissions: Read & Write
5. Copy **API Key** and **Secret Key**

#### Telegram Bot (Optional)
1. Open Telegram → Search **@BotFather**
2. Send `/newbot`
3. Follow instructions → Copy **Bot Token**

#### Telegram Chat ID
1. Open Telegram → Search **@userinfobot**
2. Send `/start`
3. Copy your **Chat ID** (numbers only)

---

### Step 3: Create Env Files

```bash
# Create binance.env
nano binance.env
```
Paste this (replace with your keys):
```
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_secret_here
```

Save (Ctrl+X → Y → Enter)

```bash
# Create telegram.env
nano telegram.env
```
Paste this (replace with your values):
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

Save (Ctrl+X → Y → Enter)

---

### Step 4: Verify Setup

```bash
bash setup.sh
```

You should see:
```
✅ binance.env: Found
✅ telegram.env: Found
✅ Balance: $XXX.XX
```

---

### Step 5: Run Bot

```bash
# Run scalper strategy
bash run_cycle.sh

# Or run Bollinger Bands strategy
bash run_mean_reversion.sh

# Run system QA check
bash run_qa.sh
```

---

## ⚙️ Auto-Run (Cron)

To run automatically every 5 minutes:

```bash
# Edit crontab
crontab -e
```

Add these lines:
```
*/5 * * * * cd /path/to/crypto-trading-bot && bash run_cycle.sh >> /var/log/trading.log 2>&1
*/5 * * * * cd /path/to/crypto-trading-bot && bash run_mean_reversion.sh >> /var/log/trading-bb.log 2>&1
0 */1 * * * cd /path/to/crypto-trading-bot && bash run_qa.sh >> /var/log/trading-qa.log 2>&1
```

Save (Ctrl+X → Y → Enter)

---

## 📊 Strategies

### Scalper Strategy
- **Entry**: RSI < 30 + below EMA21 + Volume spike
- **Exit**: TP +2% or SL -0.5%
- **Best for**: Trending markets

### Bollinger Bands Strategy
- **Entry**: Price touches lower BB = BUY
- **Exit**: TP +2% or SL -0.5%
- **Best for**: Range-bound markets

---

## ⚠️ Risk Management

| Setting | Value |
|---------|-------|
| Position Size | 20% of balance |
| Leverage | 5x |
| Stop Loss | -0.5% |
| Take Profit | +2% |
| Max Positions | 1 |

---

## 🔧 Troubleshooting

### "Missing BINANCE_API_KEY"
```bash
# Check if env file exists
cat binance.env
# Should show: BINANCE_API_KEY=xxx
```

### "Invalid signature"
- Check your API secret is correct
- Make sure Futures is enabled on your Binance API

### "Cannot place order"
- Check API has **Read & Write** permissions
- Verify system time: `timedatectl`
- Try: `sudo timedatectl set-ntp true`

---

## 📁 Files

| File | Description |
|------|-------------|
| `futures_auto_trade.py` | Scalper strategy |
| `mean_reversion.py` | Bollinger Bands strategy |
| `qa_audit.py` | System health check |
| `run_cycle.sh` | Run scalper |
| `run_mean_reversion.sh` | Run Bollinger |
| `run_qa.sh` | Run QA check |
| `setup.sh` | Verify credentials |
| `README.md` | This file |

---

## 🆘 Support

- Create an Issue on GitHub
- Check log files: `/var/log/trading*.log`

---

## ⚠️ Disclaimer

This bot trades futures which involves significant risk. Past performance does not guarantee future results. Use at your own risk.
