# Bash/Zsh Aliases for Freqtrade

Add these functions to your `.bashrc`, `.zshrc`, or source this file directly.

## Safety helper (required)

Every command below calls `ft_guard` first. It does three things:

1. **Targets one project explicitly.** `docker-compose` without `-p` acts on
   whatever project happens to be in the current directory. `ft_guard` resolves
   a single project name and passes it to every `docker-compose` call, so a
   command can never start or stop an unrelated container set.
2. **Detects the trading mode.** It reads `dry_run` from the Freqtrade config
   and refuses to run live-control commands against a live bot unless you
   confirm.
3. **Confirms destructive actions.** `--erase` deletes cached market data and
   `ftstop`/`ftrestart` interrupt a running bot. Both require confirmation.

Set `FT_PROJECT` to your Freqtrade project name (it defaults to `freqtrade`).
Set `FT_CONFIRM=yes` to skip the interactive prompts in non-interactive shells
where you have already confirmed the action yourself.

```bash
# The compose project name. Override with FT_PROJECT if yours differs.
FT_PROJECT="${FT_PROJECT:-freqtrade}"

# Resolve the Freqtrade config that holds dry_run.
FT_CONFIG="${FT_CONFIG:-user_data/config.json}"

# Read dry_run out of the config. Prints "true", "false", or "unknown".
ft_dryrun() {
  if [ ! -f "$FT_CONFIG" ]; then
    echo "unknown"
    return
  fi
  python3 - "$FT_CONFIG" <<'PY' 2>/dev/null || echo "unknown"
import json, sys
try:
    with open(sys.argv[1]) as fh:
        print("true" if json.load(fh).get("dry_run") else "false")
except Exception:
    print("unknown")
PY
}

# Guard for bot-control commands. Requires an explicit target and, against a
# live bot, an explicit confirmation.
ft_guard() {
  local action="$1"
  local dry
  dry="$(ft_dryrun)"

  if [ "$dry" = "false" ]; then
    echo "REFUSING: $FT_PROJECT is configured with dry_run: false (LIVE trading)."
    echo "Confirm the target project and mode, then set FT_CONFIRM=yes to proceed."
    return 1
  fi

  if [ "$dry" = "unknown" ]; then
    echo "REFUSING: could not read dry_run from $FT_CONFIG."
    echo "Check the config path (override with FT_CONFIG) and confirm the bot is in dry-run."
    return 1
  fi

  if [ "$action" = "destructive" ] && [ "${FT_CONFIRM:-}" != "yes" ]; then
    echo "CONFIRM REQUIRED: this command affects a running bot or deletes cached data."
    echo "Re-run with FT_CONFIRM=yes once you have confirmed the target: $FT_PROJECT"
    return 1
  fi
  return 0
}
```

## ftdata — Download Data

```bash
ftdata() {
  PAIR=${1:-"BTC/USDT"}
  DAYS=${2:-30}
  TIMEFRAME=${3:-"5m"}

  # Validate PAIR (alphanumeric + /)
  if [[ ! "$PAIR" =~ ^[A-Za-z0-9/]+$ ]]; then
    echo "Error: invalid pair format. Use alphanumeric and / only (e.g., BTC/USDT)"; return 1
  fi

  # Validate DAYS (positive integer) — it is interpolated into a command line
  if [[ ! "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ]; then
    echo "Error: invalid days. Use a positive integer (e.g., 30)"; return 1
  fi

  # Validate TIMEFRAME (alphanumeric + m/h/d)
  if [[ ! "$TIMEFRAME" =~ ^[0-9]+(m|h|d)$ ]]; then
    echo "Error: invalid timeframe format. Use format like 5m, 1h, 1d"; return 1
  fi

  # Handle --erase flag safely
  ERASE_FLAG=""
  if [[ "$4" == "--erase" ]]; then
    if ! ft_guard destructive; then return 1; fi
    ERASE_FLAG="--erase"
  fi

  START_DATE=$(date -d "$DAYS days ago" +%Y%m%d 2>/dev/null || \
    date -v-${DAYS}d +%Y%m%d)
  docker-compose -p "$FT_PROJECT" run --rm freqtrade download-data \
    --exchange kraken \
    --pairs "$PAIR" \
    --timerange "${START_DATE}-" \
    --timeframe "$TIMEFRAME" \
    $ERASE_FLAG
}
```

**Usage Examples:**
```bash
ftdata "BTC/USDT" 90 5m           # Download 90 days of 5-min BTC/USDT data
ftdata "ETH/USDT" 30 1h           # 30 days of 1-hour ETH/USDT
ftdata "SOL/USDT"                 # Use defaults: 30 days, 5-min
ftdata "XRP/USDT" 365 5m --erase  # Download 1 year, erase old data first
```

**Critical Notes:**
- Call with ONE pair at a time. Multiple pairs cause errors.
- Use `--erase` when extending your data range backward in time. It deletes
  cached data, so it requires confirmation and a verified dry-run target.
- Set `FT_PROJECT` if your compose project is not named `freqtrade`.

## ftback — Run Backtest

```bash
ftback() {
  STRATEGY=${1:-"SampleStrategy"}
  DAYS=${2:-30}
  TIMEFRAME=${3:-"5m"}
  PAIRS=${4:-}

  # Validate STRATEGY (alphanumeric, underscore, hyphen only)
  if [[ ! "$STRATEGY" =~ ^[A-Za-z0-9_-]+$ ]]; then
    echo "Error: invalid strategy name. Use alphanumeric, underscore, or hyphen only"; return 1
  fi

  # Validate DAYS (positive integer) — it is interpolated into a command line
  if [[ ! "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ]; then
    echo "Error: invalid days. Use a positive integer (e.g., 30)"; return 1
  fi

  # Validate TIMEFRAME (alphanumeric + m/h/d)
  if [[ ! "$TIMEFRAME" =~ ^[0-9]+(m|h|d)$ ]]; then
    echo "Error: invalid timeframe format. Use format like 5m, 1h, 1d"; return 1
  fi

  # Validate PAIRS if provided (alphanumeric + /)
  if [[ -n "$PAIRS" ]] && [[ ! "$PAIRS" =~ ^[A-Za-z0-9/,]+$ ]]; then
    echo "Error: invalid pairs format. Use alphanumeric, /, and comma only"; return 1
  fi

  START_DATE=$(date -d "$DAYS days ago" +%Y%m%d 2>/dev/null || \
    date -v-${DAYS}d +%Y%m%d)
  if [ -z "$PAIRS" ]; then
    docker-compose -p "$FT_PROJECT" run --rm freqtrade backtesting \
      --strategy "$STRATEGY" \
      --timerange "${START_DATE}-" \
      --timeframe "$TIMEFRAME" \
      --breakdown day
  else
    docker-compose -p "$FT_PROJECT" run --rm freqtrade backtesting \
      --strategy "$STRATEGY" \
      --timerange "${START_DATE}-" \
      --timeframe "$TIMEFRAME" \
      --pairs "$PAIRS" \
      --breakdown day
  fi
}
```

**Usage Examples:**
```bash
ftback "MyStrategy" 60 5m                      # Test MyStrategy for 60 days
ftback "MyStrategy" 90 1h "BTC/USDT"          # Test on specific pair
ftback                                         # Use defaults: SampleStrategy, 30 days, 5m
```

## Bot Control

These act on a running bot. Each one targets exactly one project and refuses
to run against a live (`dry_run: false`) bot unless `FT_CONFIRM=yes` is set.

```bash
ftstop()    { ft_guard destructive || return 1; docker-compose -p "$FT_PROJECT" stop; }
ftstart()   { ft_guard destructive || return 1; docker-compose -p "$FT_PROJECT" start; }
ftrestart() { ft_guard destructive || return 1; docker-compose -p "$FT_PROJECT" restart; }
ftlogs()    { docker-compose -p "$FT_PROJECT" logs -f freqtrade; }
ftstatus()  { docker-compose -p "$FT_PROJECT" ps && \
              docker-compose -p "$FT_PROJECT" logs --tail=20 freqtrade; }
ftlist()    { ls -lh user_data/data/kraken/ 2>/dev/null || \
              echo "No data. Run ftdata first."; }
ftui()      { open http://localhost:8080 2>/dev/null || \
              xdg-open http://localhost:8080 2>/dev/null || \
              echo "Open http://localhost:8080"; }
```

`ftlogs`, `ftstatus`, `ftlist`, and `ftui` are read-only and need no
confirmation. `ftstop`, `ftstart`, and `ftrestart` do.
