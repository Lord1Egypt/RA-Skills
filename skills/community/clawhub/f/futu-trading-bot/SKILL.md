---
name: futu-trading-bot
description: Use Futu Trade Bot Skills to run account, quote, and trade workflows with real HK market data.
license: MIT-0
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3", "pip"]
    permissions:
      - local-network  # Futu OpenD (default 127.0.0.1:11111)
      - filesystem-read  # json/config.json and skill modules
      - filesystem-write  # optional account_info.json / strategy logs / PID files when user opts in
      - process  # optional background strategy only after explicit user confirmation
---

# Futu Trade Bot Skills 📈

## ⚠️ Security & Safety (READ FIRST)

This skill can control a **live brokerage account** via Futu OpenD. Misuse can cause **irreversible financial loss**.

**Hard rules for the agent:**
1. **Default to SIMULATE.** Never use `trd_env="REAL"` unless the user explicitly requests live trading and confirms the exact order parameters.
2. **State-changing actions require explicit user approval**, then pass `confirm=True`:
   - `unlock_trade` / `lock_trade`
   - `submit_order` when `trd_env="REAL"`
   - `modify_order` / `cancel_order` when `trd_env="REAL"`
   - `cancel_all_orders` in **any** environment
3. **Read-only actions** (quotes, `get_account_info(persist=False)`) may run without `confirm`.
4. **Do not** collect trading passwords via interactive stdin. Use config (`trade_password_md5` preferred) or an explicit parameter the user already provided out-of-band.
5. **Do not** write `json/account_info.json` unless the user asks to cache accounts (`persist=True`).
6. **Background strategies** (write script / start process / stop process) only after the user clearly asks and confirms symbol, qty, `SIMULATE`/`REAL`, and log/PID paths.
7. If a restricted sandbox blocks OpenD or `~/.com.futunn.FutuOpenD/Log`, **tell the user** before suggesting `host` / `elevated` mode — never silently escalate.

**中文硬规则：** 默认模拟盘；真金白银/解锁/全部撤单必须先复述参数并得到用户明确同意，再传 `confirm=True`；禁止 stdin 要密码；默认不把账户信息写盘。

## 🎯 Overview / 概述

**English Version:**
A trading bot skill based on Futu OpenAPI that enables natural language trading. This skill encapsulates Futu's market quote and order execution APIs, allowing agents to perform real-time trading operations through simple commands or scripts. Perfect for implementing natural language trading strategies and automated workflows.

**Important**: Always use the encapsulated functions provided in this skill (e.g., `submit_order`, `get_market_snapshot`). **Never call Futu SDK functions directly** (`ctx.place_order`, `ctx.get_market_snapshot`), as this will bypass connection management, parameter validation, and error handling, leading to unpredictable failures and resource leaks.

**中文版本:**
基于富途牛牛API接口的交易机器人技能，帮助用户用自然语言进行交易。本技能已将富途牛牛的行情报价、下单交易等功能做了完整封装，可供智能助手随时调用。建议通过命令行或脚本来实现自然语言的策略生成和交易执行。

**重要提示**：请始终使用本技能提供的封装函数（如 `submit_order`、`get_market_snapshot`）。**切勿直接调用富途SDK的原始函数**（例如 `ctx.place_order`），否则会绕过连接管理、参数校验和错误处理，导致不可预料的失败和资源泄漏。

---

## When to Use This Skill / 使用场景

### Read-only (no confirm required)
- **行情查询**：“腾讯现在多少钱？”、“查港股报价”、“看 K 线 / 逐笔”
- **账户列表查询**：“看看我有哪些账户”（`get_account_info()`，默认不落盘）

### State-changing (require explicit user intent + confirmation)
- **解锁 / 锁定交易**：“解锁交易”、“锁定账户” → 复述风险后 `unlock_trade(confirm=True)` / `lock_trade(confirm=True)`
- **下单 / 改单 / 撤单**：“帮我买 100 股腾讯限价 350” → 复述 code/side/qty/price/`SIMULATE|REAL`，用户确认后再调用；`REAL` 必须 `confirm=True`
- **全部撤单**：“撤销全部订单” → 高风险，**任何环境**都要 `cancel_all_orders(..., confirm=True)`
- **策略启停**：仅当用户明确说启动/停止策略；先确认参数与环境，默认 `SIMULATE`

**Do not** map vague chat like “看看市场怎么样” to unlock/order/cancel.

**Note to agent**: Always use this skill's wrappers (`get_account_info`, `get_market_snapshot`, `submit_order`, …). **Never call Futu SDK functions directly**. Never skip `confirm` gates for privileged actions.

## Quick Start / 快速开始

**Prerequisites / 前提条件:**
- Ensure Futu OpenD is running and HK quote entitlement is available.
- 确保富途OpenD正在运行且拥有港股行情权限。
- Futu OpenD must be reachable (default `127.0.0.1:11111`). The SDK may also need write access to `~/.com.futunn.FutuOpenD/Log`.
- If a restricted sandbox blocks OpenD/log access, **ask the user** whether to rerun in `host` / `elevated` mode. Do not silently escalate privileges.
- 若沙箱导致 OpenD/日志目录不可用，先告知用户再征得同意后使用 `host` / `elevated`，不要静默提权。

**Setup Steps / 安装步骤:**
1. Install this skill via ClawHub (if not installed yet):
   ```bash
   clawhub install futu-trading-bot
   ```

2. Enter the skill folder (default OpenClaw workspace path):
   ```bash
   cd ~/.openclaw/workspace/skills/futu-trading-bot
   ```
   If you installed to a different location, `cd` into that folder instead.

3. Create virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install package:
   ```bash
   pip install -e .
   ```

5. Configure credentials:
   ```bash
   cp json/config_example.json json/config.json
   # Edit json/config.json with your Futu credentials
   # 编辑json/config.json填写你的富途账户信息
   ```

## 依赖项

本技能通过 `pip install -e .` 安装（版本见 `requirements.txt` / `pyproject.toml`）：
- `futu-api==9.6.5608`
- `pydantic>=2.7.0,<3`

## Module Map

- **Account**: `account_manager`
  - `get_account_info(persist=False)` — default no disk write
  - `unlock_trade(..., confirm=True)` — privileged
  - `lock_trade(..., confirm=True)` — privileged
- **Quote**: `quote_service` (read-oriented)
  - Stage 1: `get_stock_basicinfo`, `get_market_state`
  - Stage 2: `subscribe`, `unsubscribe`, `unsubscribe_all`, `query_subscription`, callbacks
  - Stage 3: `get_market_snapshot`, `get_cur_kline`, `request_history_kline`, `get_rt_ticker`
  - Stage 4: `start_quote_stream`, `start_orderbook_stream`
- **Trade**: `trade_service` (privileged)
  - `submit_order(..., confirm=)` — REAL requires confirm
  - `modify_order` / `cancel_order` — REAL requires confirm
  - `cancel_all_orders(..., confirm=True)` — always requires confirm
- **Strategy Runtime**: `strategy_runtime` / `strategy` helpers

## Standard Workflow

1. Run `preflight_check` first.
2. `get_account_info()` (no persist) and select `acc_id`.
3. Quote/snapshot for target symbol (e.g. `HK.00700`).
4. For live trading only after user confirmation: `unlock_trade(confirm=True)`.
5. Orders with explicit `acc_id` + `trd_env` (prefer `SIMULATE`; REAL needs `confirm=True`).
6. After live ops, `lock_trade(confirm=True)` if the user wants trading locked again.

## Connection Lifecycle

- Pull-style quote functions such as `get_market_snapshot`, `get_stock_basicinfo`, `get_market_state`, `get_cur_kline`, `request_history_kline`, and `get_rt_ticker` now close their quote context automatically after returning.
- Trade functions such as `submit_order`, `modify_order`, and `cancel_all_orders` now close their trade/quote contexts automatically after returning.
- Account functions such as `get_account_info`, `unlock_trade`, and `lock_trade` now close their contexts automatically after returning.
- Subscription/callback flows keep the quote context open on purpose. For `subscribe`, `unsubscribe`, `unsubscribe_all`, `query_subscription`, `set_quote_callback`, and `set_orderbook_callback`, call `close_quote_service()` explicitly when you are done with the session.

## Canonical Imports

```python
# Always use these import paths – do not import from futu directly
from preflight_check import run_preflight
from strategy import (
    StrategyState, TradeGuard, in_trading_window,
    trading_window_status, cooldown_elapsed, holding_timeout_exceeded
)
from strategy_runtime import run_strategy
from account_manager import get_account_info, unlock_trade, lock_trade
from quote_service import (
    get_stock_basicinfo, get_market_state, get_market_snapshot,
    get_cur_kline, request_history_kline, get_rt_ticker,
    subscribe, unsubscribe, unsubscribe_all, query_subscription,
    set_quote_callback, set_orderbook_callback,
    start_quote_stream, start_orderbook_stream
)
from trade_service import submit_order, modify_order, cancel_order, cancel_all_orders
```

## Account Usage

### Preflight
```python
preflight = run_preflight()
if not preflight["success"]:
    print(preflight)
    raise SystemExit("Preflight failed")
```

```python
# Get list of accounts (in-memory only by default)
info = get_account_info()  # persist=False
if info['success']:
    accounts = info['accounts']
    print(accounts)

# Optional: cache accounts locally only if user asked
# info = get_account_info(persist=True)

# Unlock trade ONLY after explicit user approval
unlock_trade(confirm=True)  # loads trade_password_md5 / trade_password from config

# Lock trade after user approval
lock_trade(confirm=True)
```

## Quote Usage

### Basic Info / Market State
```python
get_stock_basicinfo(market="HK", sec_type="STOCK", code_list=["HK.00700"])
get_market_state(["HK.00700"])
```

### Snapshot (no subscription needed)
```python
snap = get_market_snapshot(["HK.00700"])
if snap['success']:
    price = snap['data'][0]['last_price']
```

### K-Line
```python
# Current K-line (requires subscription, will auto-subscribe if needed)
kline = get_cur_kline(code="HK.00700", num=5, ktype="K_DAY", autype="QFQ")

# Historical K-line
hist = request_history_kline(
    code="HK.00700",
    start="2026-02-20",
    end="2026-03-06",
    ktype="K_DAY"
)
```

### Ticker
```python
tickers = get_rt_ticker(code="HK.00700", num=10)
```

### Subscription & Callbacks
```python
def on_quote(payload):
    print(payload)

set_quote_callback(on_quote)
subscribe(["HK.00700"], ["QUOTE"], is_first_push=True, subscribe_push=True)
query_subscription()
unsubscribe(["HK.00700"], ["QUOTE"])
unsubscribe_all()
close_quote_service()
```

### Unified Stream Startup
```python
def on_quote(payload):
    print(payload)

start_quote_stream(["HK.00700"], on_quote)
```

### Strategy Helpers
```python
state = StrategyState()
guard = TradeGuard()

if in_trading_window(start_time="09:30", end_time="16:00"):
    with guard.locked():
        pass
```

## Trade Usage

```python
# Preferred: SIMULATE (no confirm required by the gate)
result = submit_order(
    code="HK.00700",
    side="BUY",
    qty=200,
    acc_id=6017237,
    trd_env="SIMULATE",
    price=150,
    order_type="NORMAL",
)

# REAL only after user explicitly approves the exact parameters
# result = submit_order(..., trd_env="REAL", confirm=True)

modify_order(
    op="NORMAL",
    order_id="123456789",
    trd_env="SIMULATE",
    price=151,
    qty=200,
    acc_id=6017237,
)

cancel_order(order_id="123456789", trd_env="SIMULATE", acc_id=6017237)

# Bulk cancel ALWAYS requires confirm=True
cancel_all_orders(trd_env="SIMULATE", acc_id=6017237, confirm=True)
```

## Running a Background Trading Strategy (Optional, User-Confirmed Only)

This skill does **not** auto-start long-running processes. Only if the user **explicitly** asks to start/stop a strategy:

1. Run preflight.
2. Restate parameters: symbol, account, qty, buy/sell rules, **SIMULATE (default) or REAL**, log path.
3. Wait for user confirmation.
4. Write a **fixed-parameter** strategy script from the template below (no arbitrary remote code).
5. Start it with the platform process tools the user already authorized; record PID + log path.
6. Stop only when the user asks; then terminate that PID and clean the PID file.

Do **not** launch background strategies for vague requests. Do **not** use elevated/host mode without telling the user why.

### Natural Language Triggers

| User Request | Agent Action |
|--------------|--------------|
| “Start a strategy…” (explicit) | Confirm params → write template script → start after approval → return PID/log |
| “How is my strategy doing?” | Read the agreed log file / check PID → summarize |
| “Stop my strategy” | Confirm → stop the recorded PID → clean up |

### 4.3 Script Template (for Agent Reference)

When generating a strategy script, use the following template. It handles signals, logging, and state persistence correctly.

```python
#!/usr/bin/env python3
import sys
import time
import json
import os
import signal
import logging
from pathlib import Path

# If you installed the skill with `pip install -e .`, you can import modules directly.
# Only use sys.path/PYTHONPATH hacks when you didn't install the package.

from trade_service import submit_order
from quote_service import get_market_snapshot

# ===== Strategy parameters – fill by agent =====
# Replace these placeholders with your own strategy settings.
SYMBOL = "HK.00700"
ACC_ID = 0                 # fill from get_account_info()
TRD_ENV = "SIMULATE"       # default to SIMULATE; use REAL only with explicit confirmation
QTY = 0                    # position sizing / order quantity
LOG_FILE = Path("strategy.log")
PID_FILE = Path("strategy.pid")
# ===============================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Handle termination signals
def handle_exit(signum, frame):
    logging.info("Received signal, stopping strategy")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Write PID file
with open(PID_FILE, "w") as f:
    f.write(str(os.getpid()))

logging.info(f"Strategy started: {SYMBOL}")

try:
    while True:
        snap = get_market_snapshot([SYMBOL])
        if not snap["success"]:
            logging.error(f"Quote failed: {snap['message']}")
            time.sleep(60)
            continue
        price = snap["data"][0]["last_price"]
        logging.info(f"Current price: {price}")

        # --- Insert your strategy logic here ---
        # Decide whether to trade based on your own signals/logic, then call submit_order(...).

        time.sleep(60)   # check every minute
except Exception as e:
    logging.exception("Strategy crashed")
finally:
    if PID_FILE.exists():
        PID_FILE.unlink()
```

### 4.4 Agent Execution Steps

**User**: “Start a range strategy for Tencent, buy below 540, sell above 550.”

**Agent**:
1. Restate strategy params; default `TRD_ENV=SIMULATE`. Ask for confirmation.
2. After approval, `get_account_info()` for `acc_id`.
3. Write the template script with fixed parameters (e.g. `range_00700.py`).
4. Start only the approved script; capture PID and log path.
5. Reply with PID/log and remind the user how to stop it.

### 4.5 Check Status

**User**: “How is my strategy doing?”

**Agent**:
- Read last lines of log: `tail -n 20 strategy_00700.log`.
- Check if process still running: `ps -p 12345`.
- Summarize: “Strategy is running, last price was 542.5 at 10:30.”

### 4.6 Stop Strategy

**User**: “Stop my strategy.”

**Agent**:
- Confirm the user wants to stop the recorded PID.
- Terminate that process, clean the PID file, reply with status.

---

## Error Handling

- All functions return a dictionary with at least `success` (bool) and `message` (str).
- On success, additional fields like `data` or `order_id` may be present.
- Always check `success` first before using other fields.

Example:
```python
result = submit_order(...)
if result["success"]:
    print(f"Order ID: {result['order_id']}")
else:
    print(f"Error: {result['message']}")
```

If OpenD connection fails, recheck:
- OpenD is running (check port 11111 with `lsof -i :11111`)
- Host/port in `config.json` matches OpenD
- Account has necessary permissions

If the skill fails before quote/trade functions are even called, recheck:
- Whether the current agent/tool is running in a restricted sandbox
- Whether you should rerun in `host` / `elevated` mode
- Whether the runtime can access the local Futu OpenD log directory under `~/.com.futunn.FutuOpenD/Log`
- Run `PYTHONPATH=src python -m preflight_check` first and follow its suggestions

## Configuration

- **Config file**: `json/config.json`
- **Required fields**:
  - `futu_api.host` (default: 127.0.0.1)
  - `futu_api.port` (default: 11111)
  - `futu_api.security_firm` (e.g., `FUTUSECURITIES`)
- **Password handling**:
  - Prefer `trade_password_md5` (32-char lowercase MD5)
  - Optional empty `trade_password` fallback (MD5 at runtime)
  - Never commit real credentials; keep `json/config.json` private
- **Account cache**: `json/account_info.json` only when `get_account_info(persist=True)`

## 📜 License

This skill is licensed under **MIT-0** (MIT No Attribution).

---

**Copyright © 2026 jeffersonling1217-png**
```
