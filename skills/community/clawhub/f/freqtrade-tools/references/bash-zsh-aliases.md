# Bash/Zsh Aliases for Freqtrade

Add these functions to your `.bashrc`, `.zshrc`, or source this file directly.

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
  
  # Validate TIMEFRAME (alphanumeric + m/h/d)
  if [[ ! "$TIMEFRAME" =~ ^[0-9]+(m|h|d)$ ]]; then
    echo "Error: invalid timeframe format. Use format like 5m, 1h, 1d"; return 1
  fi
  
  # Handle --erase flag safely
  ERASE_FLAG=""
  if [[ "$4" == "--erase" ]]; then
    ERASE_FLAG="--erase"
  fi
  
  START_DATE=$(date -d "$DAYS days ago" +%Y%m%d 2>/dev/null || \
    date -v-${DAYS}d +%Y%m%d)
  docker-compose run --rm freqtrade download-data \
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
- Use `--erase` when extending your data range backward in time.

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
    docker-compose run --rm freqtrade backtesting \
      --strategy "$STRATEGY" \
      --timerange "${START_DATE}-" \
      --timeframe "$TIMEFRAME" \
      --breakdown day
  else
    docker-compose run --rm freqtrade backtesting \
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

## Bot Control — One-Liners

```bash
ftstop()    { docker-compose stop; }
ftstart()   { docker-compose start; }
ftrestart() { docker-compose restart; }
ftlogs()    { docker-compose logs -f freqtrade; }
ftstatus()  { docker-compose ps && \
              docker-compose logs --tail=20 freqtrade; }
ftlist()    { ls -lh user_data/data/kraken/ 2>/dev/null || \
              echo "No data. Run ftdata first."; }
ftui()      { open http://localhost:8080 2>/dev/null || \
              xdg-open http://localhost:8080 2>/dev/null || \
              echo "Open http://localhost:8080"; }
```
