#!/bin/bash
# BinanceCoach — twice-daily portfolio analysis with position scaling advice

# Auto-detect skill location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BC="bash ${SCRIPT_DIR}/bc.sh"
ENV_FILE="$HOME/workspace/binance-coach/.env"
PYTHON="/opt/homebrew/bin/python3"

if [ -f "$ENV_FILE" ]; then
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
fi

TG_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TG_CHAT="${TELEGRAM_USER_ID:-}"
HOUR=$(date +%H)
SESSION=$([ "$HOUR" -lt 15 ] && echo "🌅 Morning" || echo "🌆 Evening")
DATE=$(date '+%Y-%m-%d %H:%M')

send_tg() {
    if [ -n "$TG_TOKEN" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
            -d "chat_id=${TG_CHAT}" \
            -d "parse_mode=HTML" \
            --data-urlencode "text=$1" > /dev/null
    fi
}

# Fetch raw output
PORTFOLIO=$($BC portfolio 2>&1) || true
FG_RAW=$($BC fg 2>&1) || true
DCA_RAW=$($BC dca 2>&1) || true

# Parse everything with Python (avoids macOS grep -P issue)
PARSED=$($PYTHON - "$PORTFOLIO" "$FG_RAW" "$DCA_RAW" << 'PYEOF'
import sys, re

portfolio = sys.argv[1]
fg_raw    = sys.argv[2]
dca_raw   = sys.argv[3]

# Portfolio
totals = re.findall(r'\$([0-9,]+\.[0-9]+)', portfolio)
total  = totals[-1].replace(',','') if totals else '0'
health = re.search(r'Health:\s*(\d+)', portfolio)
grade  = re.search(r'Grade:\s*(\w+)', portfolio)

# F&G
fg_score = re.search(r'Score:\s*(\d+)', fg_raw)
fg_label = re.search(r'Status:\s*([^\n│]+)', fg_raw)

# DCA: extract per-coin RSI and multiplier
def get_rsi(coin):
    m = re.search(rf'{coin}.*?(\d+\.\d+)', dca_raw, re.IGNORECASE)
    return float(m.group(1)) if m else 50.0

def get_mult(coin):
    m = re.search(rf'{coin}.*?×(\d+\.\d+)', dca_raw, re.IGNORECASE)
    return float(m.group(1)) if m else 1.0

print(f"TOTAL={total}")
print(f"HEALTH={health.group(1) if health else '?'}")
print(f"GRADE={grade.group(1) if grade else '?'}")
print(f"FG_SCORE={fg_score.group(1) if fg_score else '50'}")
print(f"FG_LABEL={fg_label.group(1).strip() if fg_label else 'Unknown'}")
print(f"SHIB_RSI={get_rsi('SHIB')}")
print(f"SHIB_MULT={get_mult('SHIB')}")
print(f"ANKR_MULT={get_mult('ANKR')}")
print(f"DOGE_RSI={get_rsi('DOGE')}")
print(f"DOGE_MULT={get_mult('DOGE')}")
print(f"ADA_RSI={get_rsi('ADA')}")
print(f"ADA_MULT={get_mult('ADA')}")
print(f"BTC_MULT={get_mult('BTC')}")
PYEOF
) || true

# Load parsed vars
eval "$PARSED"

# --- Position advice ---
ADVICE=""

if (( $(echo "${SHIB_RSI:-50} > 68" | bc -l) )); then
    ADVICE+="⬇️ <b>SHIB</b> — RSI ${SHIB_RSI} (overbought). Trim or hold, don't add.\n"
fi

if (( $(echo "${ANKR_MULT:-1} > 1.1" | bc -l) )); then
    ADVICE+="⬆️ <b>ANKR</b> — ×${ANKR_MULT} multiplier. Best value in portfolio, accumulate.\n"
fi

if (( $(echo "${DOGE_RSI:-50} < 45" | bc -l) )); then
    ADVICE+="⬆️ <b>DOGE</b> — RSI ${DOGE_RSI} (low). Good speculative add.\n"
elif (( $(echo "${DOGE_RSI:-50} > 65" | bc -l) )); then
    ADVICE+="⬇️ <b>DOGE</b> — RSI ${DOGE_RSI}. Stretched, no new buys.\n"
fi

if (( $(echo "${ADA_RSI:-50} < 45" | bc -l) )); then
    ADVICE+="⬆️ <b>ADA</b> — RSI ${ADA_RSI}. DCA to lower avg entry (\$0.891).\n"
elif (( $(echo "${ADA_RSI:-50} > 62" | bc -l) )); then
    ADVICE+="⏸️ <b>ADA</b> — RSI ${ADA_RSI}. Already -69% underwater, wait for RSI &lt;50 to add.\n"
fi

FG_INT=${FG_SCORE:-50}
if (( $(echo "$FG_INT < 25" | bc -l) )); then
    if (( $(echo "${BTC_MULT:-1} > 0.7" | bc -l) )); then
        ADVICE+="⬆️ <b>BTC</b> — Extreme Fear zone (${FG_INT}). Good time for small buy.\n"
    fi
fi

if (( $(echo "$FG_INT > 75" | bc -l) )); then
    ADVICE+="⚠️ <b>Extreme Greed (${FG_INT})</b> — Scale DOWN memes. Take profits on SHIB/DOGE/FLOKI.\n"
fi

[ -z "$ADVICE" ] && ADVICE="✅ No position changes needed. Hold and monitor.\n"

MSG="${SESSION} <b>BinanceCoach Analysis</b>
📅 ${DATE}

💼 <b>Portfolio: \$${TOTAL:-0}</b>
🏥 Health: ${HEALTH:-?}/100 (${GRADE:-?})
😱 F&amp;G: ${FG_INT}/100 — ${FG_LABEL:-Unknown}

📐 <b>Position Advice:</b>
$(echo -e "$ADVICE")
<i>Snapshot saved to coach.db.</i>"

send_tg "$MSG"
echo "✅ Analysis sent: $SESSION $DATE"
