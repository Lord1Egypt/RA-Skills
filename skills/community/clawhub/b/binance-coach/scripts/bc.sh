#!/usr/bin/env bash
# bc.sh — BinanceCoach CLI wrapper for OpenClaw skill
#
# Uses python main.py --command "..." for clean non-interactive output.
# No banner, no prompt, no piping hacks.
#
# Usage:
#   bc.sh <command> [args...]
#   bc.sh --path           (print project path and exit)
#   bc.sh --lang nl <cmd>  (run command in Dutch)

set -euo pipefail

# ── Find project root ────────────────────────────────────────────────────────
find_project() {
    # 1. Explicit env override
    if [[ -n "${BINANCE_COACH_PATH:-}" && -f "$BINANCE_COACH_PATH/main.py" ]]; then
        echo "$BINANCE_COACH_PATH"; return
    fi
    # 2. Standard workspace locations
    local candidates=("$HOME/workspace/binance-coach" "$HOME/.binance-coach" "$HOME/binance-coach")
    for dir in "${candidates[@]}"; do
        if [[ -f "$dir/main.py" && -f "$dir/.env" ]]; then echo "$dir"; return; fi
    done
    # 3. Bundled src/ inside skill (no setup needed for read-only commands)
    local skill_dir src_dir
    skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    src_dir="$skill_dir/src"
    if [[ -f "$src_dir/main.py" ]]; then echo "$src_dir"; return; fi
    echo ""
}

PROJECT="$(find_project)"

if [[ "${1:-}" == "--path" ]]; then echo "$PROJECT"; exit 0; fi

if [[ -z "$PROJECT" ]]; then
    echo "❌ BinanceCoach project not found."
    echo "   Run: bc.sh setup  OR  set BINANCE_COACH_PATH"
    exit 1
fi

# ── Parse optional --lang flag ───────────────────────────────────────────────
LANG_ARGS=""
if [[ "${1:-}" == "--lang" ]]; then
    shift; LANG_ARGS="--lang ${1:-en}"; shift
fi

COMMAND="${1:-help}"
shift || true
ARGS=("$@")

# ── Load .env ────────────────────────────────────────────────────────────────
if [[ -f "$PROJECT/.env" ]]; then
    set -o allexport; source "$PROJECT/.env"; set +o allexport
fi

# ── Find Python ──────────────────────────────────────────────────────────────
PYTHON="${PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
    for py in python3 python; do
        if command -v "$py" &>/dev/null; then PYTHON="$py"; break; fi
    done
fi

# ── Run via --command flag (clean non-interactive output) ────────────────────
# Args are joined into a single quoted string passed to --command.
# Each arg is shell-quoted to prevent injection.
run_cmd() {
    local cmd="$1"
    cd "$PROJECT"
    # shellcheck disable=SC2086
    $PYTHON main.py $LANG_ARGS --command "$cmd"
}

# Build a safe command string from a base command + args array
safe_cmd() {
    local base="$1"; shift
    local result="$base"
    for arg in "$@"; do
        # Strip shell metacharacters — use tr to avoid bash parsing issues with backtick in pattern
        local clean
        clean=$(printf '%s' "$arg" | tr -d ';&|$()`{}\\<>')
        result="$result $clean"
    done
    printf '%s' "$result"
}

# ── Dispatch ─────────────────────────────────────────────────────────────────
cd "$PROJECT"

case "$COMMAND" in
    portfolio)    run_cmd "portfolio" ;;
    dca)          run_cmd "$(safe_cmd dca "${ARGS[@]:-}")" ;;
    market)       run_cmd "$(safe_cmd market "${ARGS[0]:-BTCUSDT}")" ;;
    fg)           run_cmd "fg" ;;
    behavior)     run_cmd "behavior" ;;
    alert)        run_cmd "$(safe_cmd alert "${ARGS[@]}")" ;;
    alerts)       run_cmd "alerts" ;;
    check-alerts) run_cmd "check-alerts" ;;
    learn)        run_cmd "$(safe_cmd learn "${ARGS[0]:-}")" ;;
    project)      run_cmd "$(safe_cmd project "${ARGS[0]:-BTCUSDT}")" ;;
    coach)        run_cmd "coach" ;;
    weekly)       run_cmd "weekly" ;;
    ask)          run_cmd "$(safe_cmd ask "${ARGS[@]}")" ;;
    models)       run_cmd "models" ;;
    model)        run_cmd "$(safe_cmd model "${ARGS[0]:-}")" ;;
    telegram)
        echo "🤖 Starting BinanceCoach Telegram bot..."
        exec $PYTHON main.py --telegram
        ;;
    demo)         exec $PYTHON main.py --demo ;;
    setup)
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        exec bash "$SCRIPT_DIR/setup.sh"
        ;;
    setup-crons)
        # Create or repair OpenClaw scheduled analysis crons
        echo "🕐 BinanceCoach — Cron Setup"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # Check if openclaw CLI is available
        if ! command -v openclaw &>/dev/null; then
            echo "❌ openclaw CLI not found — cron setup requires OpenClaw."
            exit 1
        fi

        # Try to detect Telegram user ID from .env or ask
        TG_CHAT="${TELEGRAM_USER_ID:-}"
        if [[ -z "$TG_CHAT" ]]; then
            echo "   Your Telegram user ID is needed to deliver analysis reports."
            echo "   You can get it from @userinfobot on Telegram."
            echo ""
            read -rp "   Telegram user ID: " TG_CHAT
            [[ -z "$TG_CHAT" ]] && { echo "❌ Telegram user ID required."; exit 1; }
        else
            echo "   Using Telegram ID from .env: $TG_CHAT"
        fi

        # Morning/evening schedule options
        read -rp "   Morning analysis time (default: 09:00): " MORNING_HOUR
        MORNING_HOUR="${MORNING_HOUR:-9}"
        MORNING_HOUR="${MORNING_HOUR//:/}"  # strip colon if user typed "9:00"
        MORNING_HOUR="${MORNING_HOUR%00}"    # strip trailing 00
        MORNING_HOUR="${MORNING_HOUR:-9}"

        read -rp "   Evening analysis time (default: 21:00): " EVENING_HOUR
        EVENING_HOUR="${EVENING_HOUR:-21}"
        EVENING_HOUR="${EVENING_HOUR//:/}"
        EVENING_HOUR="${EVENING_HOUR%00}"
        EVENING_HOUR="${EVENING_HOUR:-21}"

        TZ="${TZ:-Europe/Amsterdam}"

        MORNING_MSG="Run the BinanceCoach morning portfolio analysis: cd ~/workspace/binance-coach && python3 scripts/daily_analysis.py — then send the complete output to the user on Telegram."
        EVENING_MSG="Run the BinanceCoach evening portfolio analysis: cd ~/workspace/binance-coach && python3 scripts/daily_analysis.py — then send the complete output to the user on Telegram."

        # Remove existing BinanceCoach analysis crons to avoid duplicates
        EXISTING=$(openclaw cron list --json 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin) if isinstance(json.load(open('/dev/stdin')) if False else None, list) else []
" 2>/dev/null || true)

        # Use cron list to find and remove existing ones
        EXISTING_IDS=$(openclaw cron list 2>/dev/null | grep -E "BinanceCoach (Morning|Evening) Analysis" | awk '{print $1}' || true)
        if [[ -n "$EXISTING_IDS" ]]; then
            echo ""
            echo "   Found existing BinanceCoach analysis crons — removing to recreate..."
            while IFS= read -r cid; do
                [[ -z "$cid" ]] && continue
                openclaw cron rm "$cid" 2>/dev/null && echo "   ✅ Removed $cid" || true
            done <<< "$EXISTING_IDS"
        fi

        echo ""
        echo "   Creating morning cron (${MORNING_HOUR}:00)..."
        openclaw cron add \
            --name "BinanceCoach Morning Analysis" \
            --cron "0 ${MORNING_HOUR} * * *" \
            --tz "$TZ" \
            --session isolated \
            --message "$MORNING_MSG" \
            --announce \
            --to "telegram:${TG_CHAT}" 2>&1 | grep -E '"id"|"name"|error' | head -5
        echo "   ✅ Morning analysis cron created"

        echo ""
        echo "   Creating evening cron (${EVENING_HOUR}:00)..."
        openclaw cron add \
            --name "BinanceCoach Evening Analysis" \
            --cron "0 ${EVENING_HOUR} * * *" \
            --tz "$TZ" \
            --session isolated \
            --message "$EVENING_MSG" \
            --announce \
            --to "telegram:${TG_CHAT}" 2>&1 | grep -E '"id"|"name"|error' | head -5
        echo "   ✅ Evening analysis cron created"

        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ Crons active! You'll receive portfolio analysis:"
        echo "   🌅 Every morning at ${MORNING_HOUR}:00"
        echo "   🌆 Every evening at ${EVENING_HOUR}:00"
        echo ""
        echo "   To rebuild crons anytime: bc.sh setup-crons"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ;;
    update)
        echo "🔄 BinanceCoach update — review before applying"
        echo "   Changelog: https://clawhub.ai/skills/binance-coach"
        echo "   Source:    https://github.com/UnrealBNB/BinanceCoachAI"
        echo ""
        echo "   This will:"
        echo "   • Fetch updated skill files from ClaWHub/GitHub (network access)"
        echo "   • Run pip install to update Python dependencies from PyPI"
        echo "   • Your .env and alert data are preserved"
        echo ""
        printf "   Proceed with update? [y/N] "
        read -r confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Update cancelled."; exit 0; }
        echo ""
        echo "🔄 Updating BinanceCoach skill..."
        # Step 1: Update skill files via ClaWHub
        if command -v clawhub &>/dev/null; then
            clawhub update binance-coach && echo "✅ Skill updated from ClaWHub"
        else
            echo "⚠️  clawhub CLI not found — skipping registry update"
        fi
        # Step 2: Copy new bundled src to workspace (preserve .env and data/)
        SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
        SRC_DIR="$SKILL_DIR/src"
        if [[ -d "$SRC_DIR" && -f "$SRC_DIR/main.py" && -d "$PROJECT" ]]; then
            # Back up .env and data/
            TMP_ENV=$(mktemp)
            cp "$PROJECT/.env" "$TMP_ENV" 2>/dev/null || true
            # Copy new source (excludes .env and data/)
            rsync -a --exclude='.env' --exclude='data/' "$SRC_DIR/" "$PROJECT/" 2>/dev/null || \
            cp -r "$SRC_DIR/." "$PROJECT/"
            # Restore .env
            [[ -f "$TMP_ENV" ]] && cp "$TMP_ENV" "$PROJECT/.env"
            rm -f "$TMP_ENV"
            echo "✅ Source updated at $PROJECT"
        else
            echo "⚠️  Bundled src not found — re-run setup to reinstall"
        fi
        # Step 3: Re-install deps in case requirements changed
        pip3 install --break-system-packages -q -r "$PROJECT/requirements.txt" 2>/dev/null || true
        echo "✅ BinanceCoach updated successfully"
        echo "   Your .env and alert data are preserved."
        ;;
    snapshot)       run_cmd "snapshot" ;;
    history)        run_cmd "$(safe_cmd history "${ARGS[0]:-7}")" ;;
    dca-history)    run_cmd "$(safe_cmd dca-history "${ARGS[0]:-}")" ;;
    confirm)        run_cmd "$(safe_cmd confirm "${ARGS[@]}")" ;;
    import-orders)  run_cmd "import-orders" ;;
    journal)        run_cmd "$(safe_cmd journal "${ARGS[0]:-}")" ;;
    journal-add)    run_cmd "$(safe_cmd journal-add "${ARGS[@]}")" ;;
    journal-delete) run_cmd "$(safe_cmd journal-delete "${ARGS[0]:-}")" ;;
    journal-perf)   run_cmd "journal-perf" ;;
    pnl)            run_cmd "$(safe_cmd pnl "${ARGS[0]:-}")" ;;
    pnl-export)     run_cmd "pnl-export" ;;
    rebalance)      run_cmd "rebalance" ;;
    targets)        run_cmd "targets" ;;
    targets-set)    run_cmd "$(safe_cmd targets-set "${ARGS[@]}")" ;;
    yield)          run_cmd "yield" ;;
    news)         run_cmd "news ${ARGS[0]:-}" ;;
    listings)     run_cmd "listings ${ARGS[0]:-}" ;;
    launchpool)   run_cmd "launchpool" ;;
    news-check)   run_cmd "news-check" ;;
    watch)
        INTERVAL="${ARGS[0]:-60}"
        echo "👁  Starting BinanceCoach watcher (interval: ${INTERVAL}s)..."
        echo "    Ctrl+C to stop, or run: bc.sh watch-stop"
        run_cmd "watch ${INTERVAL}"
        ;;
    watch-bg)
        INTERVAL="${ARGS[0]:-60}"
        LOG_FILE="$PROJECT/data/watcher.log"
        nohup bash "${BASH_SOURCE[0]}" watch "$INTERVAL" >> "$LOG_FILE" 2>&1 &
        BG_PID=$!
        echo "👁  Watcher started in background (PID: $BG_PID)"
        echo "    Logs: $LOG_FILE"
        echo "    Stop: bc.sh watch-stop"
        ;;
    watch-stop)   run_cmd "watch-stop" ;;
    watch-status) run_cmd "watch-status" ;;
    help|--help|-h)
        echo "BinanceCoach — commands:"
        echo "  portfolio            Portfolio health score & analysis"
        echo "  dca [SYMBOLS]        Smart DCA recommendations"
        echo "  market [SYMBOL]      Market context (price/RSI/SMA/F&G)"
        echo "  fg                   Fear & Greed index"
        echo "  behavior             Behavioral bias analysis"
        echo "  alert SYM COND VAL   Set price/RSI alert"
        echo "  alerts               List active alerts"
        echo "  check-alerts         Check if any alert triggered"
        echo "  learn [TOPIC]        Educational lessons"
        echo "  project [SYMBOL]     12-month DCA projection"
        echo "  journal [COIN]         Show decision journal (filter by COIN optional)"
        echo "  journal-add COIN BUY/SELL PRICE [AMOUNT] [notes]"
        echo "                         Log a buy or sell decision"
        echo "                         e.g.: journal-add ADA buy 0.262 100 \"oversold -49% SMA200\""
        echo "  journal-delete ID      Delete a journal entry by its id"
        echo "  journal-perf           Journal performance vs current prices (unrealised P&L)"
        echo "  pnl [SYMBOL]           P&L from Binance trade history (FIFO, 365 days)"
        echo "  pnl-export             Export P&L to timestamped CSV for Koinly / CoinTracking"
        echo "  rebalance            Portfolio rebalancing suggestions"
        echo "  targets              Show target allocation"
        echo "  targets-set C% ...   Set targets: targets-set BTC 40 ETH 30 BNB 20 ADA 10"
        echo "  yield                Stablecoin yield optimizer"
        echo "  news [N]             Latest Binance news & announcements (default: 5)"
        echo "  listings [N]         New coin listings (default: 5)"
        echo "  launchpool           Active launchpools & HODLer airdrops"
        echo "  news-check           Check for new unseen announcements (heartbeat use)"
        echo "  watch [SECS]         Watch for new announcements, notify Telegram (default: 60s)"
        echo "  watch-bg [SECS]      Same but runs in background (nohup)"
        echo "  watch-stop           Stop the running watcher"
        echo "  watch-status         Check if watcher is running"
        echo "  coach                AI coaching summary (needs Anthropic key)"
        echo "  weekly               AI weekly brief (needs Anthropic key)"
        echo "  ask <question>       Ask Claude (needs Anthropic key)"
        echo "  models / model <id>  Claude model management"
        echo "  telegram             Start standalone Telegram bot"
        echo "  demo                 Demo mode (no API keys needed)"
        echo "  setup                First-time setup wizard"
        echo "  setup-crons          Create/repair OpenClaw scheduled analysis crons"
        echo "  update               Update to latest version from ClaWHub"
        ;;
    *)
        echo "❌ Unknown command: $COMMAND"
        echo "   Run: bc.sh help"
        exit 1
        ;;
esac
