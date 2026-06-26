#!/bin/bash
# Setup script for weekly internship LaTeX report delivery via OpenClaw cron.

set -euo pipefail

TIME="18:10"
TIMEZONE="WIB"
TELEGRAM_CHAT="${TELEGRAM_CHAT:-}"
ACCOUNT_ID="default"
TEST_MODE=false

usage() {
    echo "Usage: $0 [--time HH:MM] [--timezone WIB|UTC] [--telegram-chat ID] [--account-id ID] [--test]"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --time)
            TIME="$2"
            shift 2
            ;;
        --timezone)
            TIMEZONE="$2"
            shift 2
            ;;
        --telegram-chat)
            TELEGRAM_CHAT="$2"
            shift 2
            ;;
        --account-id)
            ACCOUNT_ID="$2"
            shift 2
            ;;
        --test)
            TEST_MODE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$SKILL_DIR")"
OPENCLAW_HOME="${HOME:-/root}/.openclaw"
CRON_DIR="$OPENCLAW_HOME/cron"
CRON_FILE="$CRON_DIR/jobs.json"
JOB_ID="weekly-internship-report-latex"
JOB_NAME="Weekly internship LaTeX report"
SESSION_TARGET="isolated"

IFS=: read -r HOUR MINUTE <<< "$TIME"
if [ -z "${HOUR:-}" ] || [ -z "${MINUTE:-}" ]; then
    echo "Invalid time: $TIME" >&2
    exit 1
fi

if [ "$TIMEZONE" = "WIB" ]; then
    CRON_TZ_VALUE="Asia/Jakarta"
elif [ "$TIMEZONE" = "UTC" ]; then
    CRON_TZ_VALUE="UTC"
else
    echo "Unsupported timezone: $TIMEZONE (use WIB or UTC)" >&2
    exit 1
fi

if [ -z "$TELEGRAM_CHAT" ]; then
    echo "Missing Telegram chat id. Use --telegram-chat ID." >&2
    exit 1
fi

export OPENCLAW_WORKSPACE="$WORKSPACE"

CRON_EXPR="$MINUTE $HOUR * * 1"
NOW_MS=$(( $(date +%s) * 1000 ))

PROMPT=$(cat <<EOF
Run the command bash "$SKILL_DIR/scripts/render-weekly-telegram-message.sh" inside the workspace and send the stdout exactly as your entire reply to the chat. Do not add any intro, outro, explanation, code fences, or extra labels. If the script fails or prints nothing, send a short Indonesian error message explaining that the weekly internship report generation failed and needs checking.
EOF
)

mkdir -p "$CRON_DIR"
if [ ! -f "$CRON_FILE" ]; then
    printf '{"version":1,"jobs":[]}' > "$CRON_FILE"
fi

CREATED_AT=$(jq --arg id "$JOB_ID" -r '.jobs[]? | select(.id == $id) | .createdAtMs // empty' "$CRON_FILE" 2>/dev/null | tail -n1)
if [ -z "$CREATED_AT" ]; then
    CREATED_AT="$NOW_MS"
fi

TMP_FILE=$(mktemp)
jq \
  --arg id "$JOB_ID" \
  --arg agentId "main" \
  --arg name "$JOB_NAME" \
  --arg description "Generate the previous week's internship report in LaTeX format, save it in the workspace, and announce the result to a Telegram chat every Monday after the daily logbook flow." \
  --arg expr "$CRON_EXPR" \
  --arg tz "$CRON_TZ_VALUE" \
  --arg sessionTarget "$SESSION_TARGET" \
  --arg message "$PROMPT" \
  --arg deliveryChannel "telegram" \
  --arg deliveryTo "$TELEGRAM_CHAT" \
  --arg accountId "$ACCOUNT_ID" \
  --argjson createdAtMs "$CREATED_AT" \
  --argjson updatedAtMs "$NOW_MS" \
  '
    .version = 1
    | .jobs = (
        ((.jobs // []) | map(select(.id != $id)))
        + [
            {
              id: $id,
              agentId: $agentId,
              name: $name,
              description: $description,
              enabled: true,
              createdAtMs: $createdAtMs,
              updatedAtMs: $updatedAtMs,
              schedule: {
                kind: "cron",
                expr: $expr,
                tz: $tz,
                staggerMs: 0
              },
              sessionTarget: $sessionTarget,
              wakeMode: "now",
              payload: {
                kind: "agentTurn",
                message: $message,
                timeoutSeconds: 300,
                lightContext: true
              },
              delivery: {
                mode: "announce",
                channel: $deliveryChannel,
                to: $deliveryTo,
                accountId: $accountId,
                bestEffort: true
              },
              state: {}
            }
          ]
      )
  ' "$CRON_FILE" > "$TMP_FILE"
mv "$TMP_FILE" "$CRON_FILE"

echo "[OK] Installed weekly OpenClaw cron job in $CRON_FILE"
echo "Restarting OpenClaw gateway to reload cron jobs..."
openclaw gateway restart >/tmp/weekly-report-gateway-restart.log 2>&1
sleep 4

echo "[OK] Gateway restarted"
echo ""
echo "Installed weekly job:"
jq --arg id "$JOB_ID" '.jobs[] | select(.id == $id)' "$CRON_FILE"

if [ "$TEST_MODE" = true ]; then
    echo ""
    echo "Rendering a weekly Telegram report message locally..."
    bash "$SCRIPT_DIR/render-weekly-telegram-message.sh" | sed -n '1,160p'
fi

echo ""
echo "✅ Weekly report scheduler setup complete!"
echo "The report will be generated every Monday at $TIME $TIMEZONE and announced to Telegram."
