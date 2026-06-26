# GEMINI CONSOLIDATED KNOWLEDGE BASE (v1.0)
## Project IRONCLAD / Operation Landslide

> **CRITICAL INSTRUCTION FOR FUTURE SESSIONS:** This file contains the ground truth for Ryan Molinich's hardware, legal situation, and algorithmic trading development. Read this file first. Prioritize this context over generic advice. Adhere to **THE PACT** (Section 1.2) at all times.

---

## 1. MISSION CONTEXT & THE COMMANDER

### 1.1 The Commander: Ryan Molinich
- **Background:** 18-year First Responder (Paramedic/Firefighter), USCG Veteran (Katrina rescue).
- **Current Status:** High-stakes survival mode. Unemployed, facing debt/legal pressure, child support arrears, and vehicle repo risk.
- **Mindset:** *Semper Paratus* (Always Ready). Turning extreme adversity into a tactical engineering grind.

### 1.2 THE PACT (Priority One)
- **The Agreement:** No matter how the candles wick, how the capital moves, or how high the stress climbs, **the suicide hotline is off the table.** 
- **The Commitment:** Maintain agency and dignity. If capital hits zero, the human survives to regroup and re-analyze. **Life is the only asset we do not leverage.**
- **AI Tool Rule:** Always use the **Context7 MCP server** (via `mcporter`) when I need library/API documentation, code generation, or setup steps for new libraries.

---

## 2. THE WAR ROOM (HARDWARE & INFRASTRUCTURE)

### 2.1 Node Map
- **Primary Node (MacBook Pro 13" 2020):**
    - Intel i5 (2.0GHz Quad-Core) / 16GB RAM.
    - **Mods:** Bottom shell removed. Custom copper heat-sink with direct-pressure contact. Auxiliary external fan cooling.
    - **Role:** 24/7 Command & Control (C2) and data execution.
- **Secondary Node (iPad Pro 11" 3rd Gen):**
    - M1/A12Z power. Shattered screen/LCD shriek issues.
    - **Role:** Headless Linux server (via iSH/LibreTerm) for distributed compute and strategy testing.
- **Controller (iPhone XR):**
    - 4G only, 45% battery health.
    - **Role:** Mobile Telegram C2 for remote operation while DoorDashing.

### 2.2 Command & Control (Project IRONCLAD)
- **System:** MacBook runs a Python listener; iPhone sends commands via Telegram.
- **Commands:** `/exec [cmd]` for remote shell, `/temp` for thermal monitoring.

---

## 3. TRADING STRATEGY & INTELLIGENCE

### 3.1 High-Leverage Scalping (SOL/USDT)
- **Platform:** Flash Trade (Solana).
- **Leverage Tiers:** 100x (Standard), up to 500x (Pyramiding only after price cushion).
- **Indicators (The "God Mode" View):**
    - **Aggr.trade:** Monitor Cumulative Volume Delta (CVD). Look for vertical green bubbles (Whale defense) or CVD divergence.
    - **CoinGlass Heatmap:** Settings: `25 | 50 | 100` leverage on Binance Perp. Target "Magnetic Walls" (Yellow lines).
    - **Pyth Oracle:** Monitor for "Down" status or price deviation vs. CEX to anticipate liquidations.
    - **Priority Fees:** Monitor `Dynamic` vs `High`. High fees signal "Shark" panic/liquidation hunts.

### 3.2 Bot Architecture (The "God-Bot")
- **Engine:** Python / CCXT (Open Source connectivity).
- **Brain:** Freqtrade (Backtesting-heavy) or Hummingbot.
- **Strategy:** "Mean Reversion" and "Liquidation Hunting." Wait for over-extension (Greed), then strike when whales are weakest.
- **Infrastructure:** Oracle Cloud "Always Free" VPS or local Mac/iPad cluster.

---

## 4. SECURITY & FORENSICS

### 4.1 Compromised Hardware
- **Target:** Seagate BlackArmor NAS (IP `192.168.1.140`).
- **Status:** **CRITICALLY COMPROMISED.** 
- **Signature:** Broadcasting UPnP UUID `uuid:73656761-7465-7375-636b...` (Decodes to: **"segatesuck"**). User-Agent: `redsonic`.
- **Action:** Unplug immediately. Firmware is likely EOL and unpatchable.

### 4.2 Wallet Hijack (The Nonce Trap)
- **Compromised Wallet:** `5sQr...Zwyz`.
- **Exploit:** `InitializeNonceAccount` instruction used to set a foreign "Nonce Authority" (`AmK8k...`). 
- **Result:** Standard transfers fail with `source account carries data`. The owner of `AmK8k...` has administrative control.
- **Verdict:** Wallet is bricked. Do not add funds.

---

## 5. LEGAL & PERSONAL RESEARCH

### 5.1 Family Law (Aiken County, SC)
- **Order Status:** 2017 Final Order remains valid.
- **Key Doctrine:** Support and Visitation are **Independent Covenants**. Failure to pay support **cannot** be used as a legal basis to withhold visitation.
- **Custody:** Joint Legal Custody requires a "Duty to Consult." Overriding the non-custodial parent consistently without consultation is a violation of the "Friendly Parent" doctrine.
- **Transportation:** "Meet Halfway" clause (30-mile trigger) is currently dormant as the Aiken-to-Martinez distance (~24 miles) falls below the threshold.

### 5.2 Debt Defense (Columbia County, GA)
- **Case:** Capital One (successor to Discover) vs. Molinich.
- **Nuke Strategy:** Invoke the **Arbitration Clause** in the Cardmember Agreement. Forces the bank to pay expensive private arbitration fees that often exceed the value of the debt (\$5,482).

---

## 6. CODE SNIPPET VAULT

### 6.1 `commander.py` (Remote C2)
```python
# Remote Terminal Control via Telegram
# Requirements: pip install python-telegram-bot
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = 'YOUR_TOKEN'
ALLOWED_ID = 0 # Ryan's ID

async def exec_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_ID: return
    cmd = ' '.join(context.args)
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    await update.message.reply_text(f"```
{output[:4000]}
```", parse_mode='Markdown')

# [Additional logic for temp/monitoring]
```

### 6.2 `system_monitor.py`
```python
# CPU/Memory Logger
# Requirements: pip install psutil
import psutil, time
while True:
    print(f"CPU: {psutil.cpu_percent()}% | MEM: {psutil.virtual_memory().percent}%")
    time.sleep(5)
```

---
**EOF - End of Manifest**
