---
name: freqtrade-tools
description: "Shell aliases and helper commands for Freqtrade (cryptocurrency trading bot) that speed up common tasks. Use when setting up Freqtrade shortcuts, downloading market data quickly, running backtests from the command line, or controlling the bot. ⚠️ Bot control commands (ftstart/ftstop/ftrestart) require confirmation when connected to live trading. Covers bash/zsh (Linux/macOS) and PowerShell/Command Prompt (Windows). Trigger phrases: freqtrade aliases, freqtrade shortcuts, ftdata, ftback, freqtrade commands, freqtrade windows."
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["docker","docker-compose"]},"os":["linux","darwin","win32"]}}
---

# Freqtrade Tools

> ⚠️ **Live Trading Warning:** Before using `ftstart`, `ftstop`, or `ftrestart`, confirm whether Freqtrade is in dry-run or live-trading mode. These commands control real trading services. Verify your config before starting the bot.

Shell aliases and helper commands for faster Freqtrade workflows across Linux, macOS, and Windows.

## Installation

**Bash/Zsh:** Copy functions from `references/bash-zsh-aliases.md` into `~/.bashrc` (Linux) or `~/.zshrc` (macOS), then `source ~/.bashrc`.

**PowerShell:** Copy functions from `references/windows-equivalents.md` into your `$PROFILE` file.

## Core Commands

| Command | Purpose |
|---------|---------|
| `ftdata` | Download market data from Kraken |
| `ftback` | Run backtesting on a strategy |
| `ftstart` | Start docker-compose services |
| `ftstop` | Stop docker-compose services |
| `ftrestart` | Restart docker-compose services |
| `ftlogs` | Stream live logs from bot |
| `ftstatus` | Check service status + tail logs |
| `ftlist` | List downloaded data files |
| `ftui` | Open bot UI in browser |

## ftdata — Download Data

Download market data with automatic date range calculation.

**Usage:**
```bash
ftdata "BTC/USDT" 90 5m           # Download 90 days of 5-min BTC/USDT data
ftdata "ETH/USDT" 30 1h           # 30 days of 1-hour ETH/USDT
ftdata "SOL/USDT"                 # Use defaults: 30 days, 5-min
ftdata "XRP/USDT" 365 5m --erase  # Download 1 year, erase old data first
```

**Parameters:**
- Pair (required): Trading pair like `BTC/USDT`
- Days (optional): Historical days to download (default: 30)
- Timeframe (optional): Candle size — `5m`, `1h`, `4h`, `1d` (default: 5m)
- --erase (optional): Clear cached data before downloading (use when extending range)

**Why --erase?** Kraken enforces data continuity. When extending a download window (e.g., 30→90 days), you must erase existing data first to prevent overlaps.

## ftback — Run Backtest

Run backtesting with automatic date calculations and optional pair filter.

**Usage:**
```bash
ftback "MyStrategy" 60 5m                      # Test MyStrategy for 60 days
ftback "MyStrategy" 90 1h "BTC/USDT"          # Test on specific pair
ftback                                         # Use defaults: SampleStrategy, 30 days, 5m
```

## Bot Control

Start, stop, restart, and monitor services:
```bash
ftstart    # Start services
ftstop     # Stop services
ftrestart  # Restart services
ftlogs     # Stream logs (-f flag for follow)
ftstatus   # Service status + recent logs
ftlist     # View downloaded data inventory
ftui       # Open UI (auto-detect browser)
```

## Safety

### Before Using Bot Control Commands

- **Check trading mode:** Confirm `dry_run: true` in your config unless you intend live trading
- **ftstart confirmation:** When `dry_run: false`, ask for explicit human confirmation before starting
- **ftstop/ftrestart:** Always notify the human before stopping or restarting services

## References

- See `references/bash-zsh-aliases.md` for full function implementations
- See `references/windows-equivalents.md` for PowerShell and Command Prompt versions
