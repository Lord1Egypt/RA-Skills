---



name: freqtrade-tools
description: "Shell aliases and helper commands for Freqtrade (cryptocurrency trading bot) that speed up common tasks. Use when setting up Freqtrade shortcuts, downloading market data quickly, running backtests from the command line, or controlling the bot. ⚠️ Bot control commands (ftstart/ftstop/ftrestart) target a single named compose project and refuse to run against a live (dry_run: false) bot or delete cached data without explicit confirmation. Covers bash/zsh (Linux/macOS) and PowerShell/Command Prompt (Windows). Trigger phrases: freqtrade aliases, freqtrade shortcuts, ftdata, ftback, freqtrade commands, freqtrade windows."
metadata: {"clawdbot":{"emoji":"\u26a1","requires":{"bins":["docker","docker-compose"]},"os":["linux","darwin","win32"],"version":"1.0.7"}}
---




# Freqtrade Tools

> ⚠️ **Live Trading Warning:** Before using `ftstart`, `ftstop`, or `ftrestart`, confirm whether Freqtrade is in dry-run or live-trading mode. These commands control real trading services. Verify your config before starting the bot.

Shell aliases and helper commands for faster Freqtrade workflows across Linux, macOS, and Windows.

## Installation

## Before You Run: Live Bot Safety

Several shortcuts in this skill control a **live trading bot**. Starting,
stopping, or restarting a bot that holds real exchange credentials can change
your positions.

**Every command goes through a `ft_guard` helper that enforces three things
in code, not just in documentation:**

1. **One explicit target.** Every `docker-compose` call passes `-p "$FT_PROJECT"`.
   Without it, `docker-compose` acts on whatever project happens to be in the
   current directory, so a command could start or stop an unrelated container
   set. Set `FT_PROJECT` if your project is not named `freqtrade`.
2. **Trading-mode detection.** The guard reads `dry_run` from the Freqtrade
   config and refuses to run bot-control commands when `dry_run` is `false`.
   If the config cannot be read, it refuses rather than assuming.
3. **Confirmation for destructive actions.** `ftstart`, `ftstop`, `ftrestart`,
   and `ftdata --erase` require `FT_CONFIRM=yes` before running.

**Confirm before acting on a live bot.** `ftstart`, `ftstop`, and `ftrestart`
take effect immediately. Before running them:

- Confirm the bot and its exchange account explicitly.
- Prefer a separate dry-run container for verification runs.
- `ftdata --erase` deletes cached market data. Confirm before using it.

**Use the PowerShell functions over cmd.exe macros.** The previous `.bat`
templates embedded the `DAYS` value directly into a `powershell -Command`
string, which allows command injection if that value is ever attacker-
controlled. Those templates have been removed; the cmd.exe section now
delegates to the PowerShell functions, which validate their arguments and
apply the guard.

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

- **Check trading mode:** The guard reads `dry_run` from your config and refuses
  to run bot-control commands against a live bot unless you set `FT_CONFIRM=yes`
- **ftstart confirmation:** When `dry_run: false`, ask for explicit human confirmation before starting
- **ftstop/ftrestart:** Always notify the human before stopping or restarting services
- **Target the right project:** Set `FT_PROJECT` if your compose project is not
  named `freqtrade`. `docker-compose -p` is what keeps a command from acting on
  an unrelated container set.
- **Override the config path:** Set `FT_CONFIG` if your Freqtrade config is not
  at `user_data/config.json`

## References

- See `references/bash-zsh-aliases.md` for full function implementations
- See `references/windows-equivalents.md` for PowerShell and Command Prompt versions
