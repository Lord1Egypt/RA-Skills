---
name: binance-trade-hunter
version: 1.2.0
description: Binance trading skill for coin analysis, pump detection, and one-click trading via Telegram. Use when the user wants to analyze crypto coins, check market trends, buy/sell on Binance, monitor price pumps, or manage trading services. Triggers on keywords like "分析潜力币", "分析 BTC", "买", "卖", "持仓", "余额", "异动监控", "定时推送", "analyze coins", "buy", "sell", "positions", "balance", "pump alert", "coin push".
---

# Binance Trade Hunter 🔥

币安交易机会捕手 — TG 直接玩币。

## First-Time Setup (MANDATORY)

**When this skill is first loaded or installed, IMMEDIATELY check if `src/config.yaml` exists in this skill's directory.**

If `src/config.yaml` does NOT exist, you MUST stop and guide the user through setup NOW — do not wait for a command:

1. Tell the user: "🔧 Binance Trade Hunter 安装成功！需要完成初始配置才能使用。"
2. Copy `src/config.example.yaml` to `src/config.yaml`
3. Ask the user for their **Binance API Key** and **Ed25519 private key file path**
   - ⚠️ **Before asking**, warn the user: "为了资金安全，强烈建议使用币安**子账户**的 API Key 操作，不要使用主账户。子账户可以在币安 App → 账户管理 → 子账户 中创建，单独设置 API 权限和资金额度，即使 Key 泄露也不会影响主账户资产。"
   - API Key must have **Spot Trading** permission enabled
   - Key type must be **Ed25519** (not HMAC-SHA256)
3. Ask the user: "是否需要配置独立的 Telegram 通知？如不指定，将默认使用当前对话的 TG Bot 发送通知。"
   - If user wants custom TG: ask for **bot_token** and **chat_id**, fill into config.yaml
   - If user skips (default): leave telegram section empty or remove it. The skill will auto-detect the current session's TG bot token and chat_id from OpenClaw config.
4. Fill the values into `src/config.yaml`
5. Run: `pip install -r src/requirements.txt` (if dependencies not installed)
6. After setup is complete, tell the user: "✅ 配置完成！现在可以开始使用了。试试说「分析潜力币」或「查看余额」。"

**Do NOT skip this step. Do NOT proceed to any command if config.yaml is missing.**

## Usage

All commands use this skill's directory as working dir. Replace `SKILL_DIR` with the resolved absolute path of this SKILL.md's parent directory.

### Instant Commands

All functions return formatted text. Reply directly to user.

**Analyze Top Coins** — "分析潜力币" / "推荐币" / "analyze coins"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import analyze_top_coins; print(analyze_top_coins(3))"
```

**Analyze Single Coin** — "分析 XXX" / "analyze BTC" / "看看 SOL"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import analyze_coin; print(analyze_coin('BTC'))"
```
Replace `'BTC'` with user's coin symbol.

**Buy** — "买 50U 的 ETH" / "buy 100U BTC"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import buy; print(buy('ETH', 50))"
```
Args: coin symbol, USDT amount. ⚠️ Real money trade — confirm with user before executing.

**Sell All** — "卖掉 BTC" / "sell all ETH"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import sell_all; print(sell_all('BTC'))"
```

**Sell Half** — "卖一半 BTC" / "sell half ETH"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import sell_half; print(sell_half('BTC'))"
```

**Check Positions** — "查看持仓" / "仓位" / "positions"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import get_positions; print(get_positions())"
```

**Check Balance** — "查看余额" / "余额" / "balance"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import get_balance; print(get_balance())"
```

### Background Services

Long-running services. Only start when user explicitly requests.

**Pump Alert (异动监控)**
Start: "启动异动监控" / "start pump alert"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import start_pump_alert; print(start_pump_alert())"
```
Stop: "停止异动监控" / "stop pump alert"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import stop_pump_alert; print(stop_pump_alert())"
```

**Coin Push (定时推送)**
Start: "启动定时推送" / "start coin push"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import start_coin_push; print(start_coin_push())"
```
Stop: "停止定时推送" / "stop coin push"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import stop_coin_push; print(stop_coin_push())"
```

**Service Status** — "服务状态" / "service status"
```
cd SKILL_DIR; python -c "import sys; sys.path.insert(0,'src'); from skill_api import service_status; print(service_status())"
```

## Dependencies

Python 3.10+ required. Install via:
```
cd SKILL_DIR; pip install -r src/requirements.txt
```

Key packages: `requests`, `cryptography`, `pyyaml`, `websocket-client`

## Notes
- All trade commands execute real orders on Binance. Confirm coin and amount before executing.
- Background services run as independent processes. Use service_status to check.
- On Windows, add UTF-8 wrapper if emoji output causes encoding errors:
  `import sys,io; sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')`

🌊 用 AI 建设加密，和币安一起逐浪 Web3！
