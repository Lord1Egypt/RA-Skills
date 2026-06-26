#!/usr/bin/env python3
"""
BinanceCoach — twice-daily portfolio analysis with position scaling advice.
Sends results via Telegram.
"""
import os, sys, requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load env
load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent))

from binance.spot import Spot
from modules.market    import MarketData
from modules.portfolio import Portfolio
from modules.dca       import DCAAdvisor
from modules.coach_db  import CoachDB

# ── Setup ─────────────────────────────────────────────────────────────────────
api_key    = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")
tg_token   = os.getenv("TELEGRAM_BOT_TOKEN", "")
tg_chat    = os.getenv("TELEGRAM_USER_ID", "")
budget     = float(os.getenv("DCA_BUDGET_MONTHLY", "400"))
risk       = os.getenv("RISK_PROFILE", "moderate")

client    = Spot(api_key=api_key, api_secret=api_secret)
market    = MarketData(client)
portfolio = Portfolio(client, market)
dca       = DCAAdvisor(market, monthly_budget=budget, risk_profile=risk)
db        = CoachDB()

hour    = datetime.now().hour
session = "🌅 Morning" if hour < 15 else "🌆 Evening"
date    = datetime.now().strftime("%Y-%m-%d %H:%M")

# ── Fetch data ────────────────────────────────────────────────────────────────
balances = portfolio.get_balances()
health   = portfolio.calculate_health_score(balances)
fg       = market.get_fear_greed()
fg_score = fg["value"]
fg_label = fg["classification"]

# Save snapshot with real F&G
portfolio.save_snapshot(balances, health, fg=fg)

total    = health["total_usd"]
h_score  = health["score"]
h_grade  = health["grade"]

# Get DCA recs for main holdings
symbols = ["ADAUSDT","BTCUSDT","DOGEUSDT","ETHUSDT","ANKRUSDT","SHIBUSDT"]
recs = {r["symbol"]: r for r in [dca.get_recommendation(s) for s in symbols]}

# ── Position advice ───────────────────────────────────────────────────────────
advice = []

shib = recs.get("SHIBUSDT", {})
ankr = recs.get("ANKRUSDT", {})
doge = recs.get("DOGEUSDT", {})
ada  = recs.get("ADAUSDT",  {})
btc  = recs.get("BTCUSDT",  {})
eth  = recs.get("ETHUSDT",  {})

# SHIB
shib_rsi = shib.get("rsi", 50)
if shib_rsi > 70:
    advice.append(f"⬇️ <b>SHIB</b> — RSI {shib_rsi:.1f} (overbought). Don't add, consider trimming.")
elif shib.get("multiplier", 1) > 1.0:
    advice.append(f"➡️ <b>SHIB</b> — Neutral. Hold position.")

# ANKR — deepest discount
ankr_mult = ankr.get("multiplier", 1)
ankr_disc = ankr.get("price_vs_sma200", 0)
if ankr_mult > 1.1:
    advice.append(f"⬆️ <b>ANKR</b> — ×{ankr_mult:.2f} (SMA200 discount {ankr_disc:.1f}%). Best value in portfolio. Accumulate.")

# DOGE
doge_rsi = doge.get("rsi", 50)
if doge_rsi < 45:
    advice.append(f"⬆️ <b>DOGE</b> — RSI {doge_rsi:.1f} (low). Good speculative entry.")
elif doge_rsi > 65:
    advice.append(f"⬇️ <b>DOGE</b> — RSI {doge_rsi:.1f}. Stretched, skip new buys.")
else:
    advice.append(f"➡️ <b>DOGE</b> — RSI {doge_rsi:.1f}. Neutral, hold.")

# ADA — underwater -69%, strict RSI gate
ada_rsi  = ada.get("rsi", 50)
ada_disc = ada.get("price_vs_sma200", 0)
if ada_rsi < 45:
    advice.append(f"⬆️ <b>ADA</b> — RSI {ada_rsi:.1f} (low). DCA to lower avg entry ($0.891).")
elif ada_rsi > 62:
    advice.append(f"⏸️ <b>ADA</b> — RSI {ada_rsi:.1f}. Already -69% underwater. Wait for RSI &lt;50 before adding.")
else:
    advice.append(f"➡️ <b>ADA</b> — RSI {ada_rsi:.1f}. Hold, no action.")

# BTC
btc_rsi  = btc.get("rsi", 50)
btc_mult = btc.get("multiplier", 1)
if fg_score < 25 and btc_rsi < 65:
    advice.append(f"⬆️ <b>BTC</b> — Extreme Fear + RSI {btc_rsi:.1f}. Small DCA buy OK.")
elif btc_rsi > 70:
    advice.append(f"⏸️ <b>BTC</b> — RSI {btc_rsi:.1f}. Warm, wait for pullback.")
else:
    advice.append(f"➡️ <b>BTC</b> — RSI {btc_rsi:.1f}. Neutral, hold or small add.")

# ETH
eth_rsi = eth.get("rsi", 50)
if eth_rsi < 45:
    advice.append(f"⬆️ <b>ETH</b> — RSI {eth_rsi:.1f}. Good DCA entry.")
elif eth_rsi > 70:
    advice.append(f"⏸️ <b>ETH</b> — RSI {eth_rsi:.1f}. Warm, hold.")

# Market-wide override
if fg_score < 20:
    advice.append(f"\n💎 <b>Market at Extreme Fear ({fg_score})</b> — Historically strong buy zone. Focus on quality (BTC/ETH/ANKR).")
elif fg_score > 75:
    advice.append(f"\n⚠️ <b>Market at Extreme Greed ({fg_score})</b> — Scale DOWN memes (SHIB/DOGE/FLOKI). Take partial profits.")

# No stablecoins warning
stable_pct = sum(b.get("usd_value",0) for b in balances if b.get("asset","") in {"USDT","USDC","BUSD","FDUSD"}) / total * 100
if stable_pct < 5:
    advice.append(f"\n🔴 <b>0% stablecoins</b> — No dry powder. Even $50-100 USDC gives you ammo if market drops further.")

advice_text = "\n".join(advice) if advice else "✅ No position changes needed."

# ── Build & send message ──────────────────────────────────────────────────────
msg = f"""{session} <b>BinanceCoach Analysis</b>
📅 {date}

💼 <b>Portfolio: ${total:,.2f}</b>
🏥 Health: {h_score}/100 ({h_grade})
😱 F&amp;G: {fg_score}/100 — {fg_label}

📐 <b>Position Advice:</b>
{advice_text}

<i>Snapshot saved to coach.db.</i>"""

if tg_token:
    try:
        requests.post(
            f"https://api.telegram.org/bot{tg_token}/sendMessage",
            json={"chat_id": tg_chat, "text": msg, "parse_mode": "HTML"},
            timeout=10,
        )
        print(f"✅ Sent: {session} {date}")
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
        print(msg)
else:
    print(msg)
