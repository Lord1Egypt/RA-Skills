#!/bin/bash
# Setup script for exact daily commit logbook delivery via OpenClaw cron.

set -euo pipefail

TIME="18:00"
TIMEZONE="WIB"
GITHUB_USER="${GITHUB_USER:-}"
TELEGRAM_CHAT="${TELEGRAM_CHAT:-}"
ACCOUNT_ID="default"
TEST_MODE=false

usage() {
    echo "Usage: $0 [--time HH:MM] [--timezone WIB|UTC] [--github-user NAME] [--telegram-chat ID] [--account-id ID] [--test]"
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
        --github-user)
            GITHUB_USER="$2"
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
JOB_ID="daily-commit-logbook-direct"
JOB_NAME="Daily MIS logbook synthesis + Telegram approval request"
SESSION_TARGET="isolated"
CONFIG_FILE="$SKILL_DIR/.env"

if [ -z "$GITHUB_USER" ] && [ -f "$CONFIG_FILE" ]; then
    # shellcheck disable=SC1090
    . "$CONFIG_FILE"
    GITHUB_USER="${GITHUB_USER:-}"
fi

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

if [ -z "$GITHUB_USER" ]; then
    echo "Missing GitHub username. Use --github-user NAME or set GITHUB_USER in $CONFIG_FILE." >&2
    exit 1
fi

if [ -z "$TELEGRAM_CHAT" ]; then
    echo "Missing Telegram chat id. Use --telegram-chat ID." >&2
    exit 1
fi

export OPENCLAW_WORKSPACE="$WORKSPACE"

CRON_EXPR="$MINUTE $HOUR * * 1-5"
NOW_MS=$(( $(date +%s) * 1000 ))

PROMPT=$(cat <<EOF
Run the command bash "$SKILL_DIR/scripts/render-telegram-approval-request.sh" inside the workspace and send the stdout exactly as your entire reply to the chat. Do not add any intro, outro, explanation, code fences, or extra labels. If the script fails or prints nothing, send a short Indonesian error message explaining that today's MIS logbook draft generation failed and needs checking.
EOF
)

mkdir -p "$WORKSPACE/reports" "$CRON_DIR"

cat > "$CONFIG_FILE" <<EOF
GITHUB_USER=$GITHUB_USER
EOF

echo "Setting up exact daily logbook delivery..."
echo "  Delivery time: $TIME $TIMEZONE"
echo "  Scheduler tz: $CRON_TZ_VALUE"
echo "  GitHub user: $GITHUB_USER"
echo "  Telegram target: $TELEGRAM_CHAT"
echo ""

EXISTING_CRONTAB=$(crontab -l 2>/dev/null || true)
FILTERED_CRONTAB=$(printf "%s\n" "$EXISTING_CRONTAB" | grep -vF "$SKILL_DIR/scripts/cron-generate.sh" | grep -vF "# Daily logbook report -" | grep -vE '^CRON_TZ=(Asia/Jakarta|UTC)$' || true)
printf "%s\n" "$FILTERED_CRONTAB" | crontab -

echo "[OK] Removed legacy crontab-based delivery path"

cat > "$WORKSPACE/HEARTBEAT.md" <<'EOF'
# Heartbeat Tasks

Daily logbook draft delivery is handled directly by OpenClaw cron in the Telegram session.

If nothing else needs attention, reply HEARTBEAT_OK.
EOF

echo "[OK] Updated HEARTBEAT.md to remove the old pending-file delivery path"

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
  --arg description "Generate a daily commit-based MIS activity summary and send a Telegram approval request before any MIS submission happens." \
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
                timeoutSeconds: 240,
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

echo "[OK] Installed OpenClaw cron job in $CRON_FILE"

echo "Restarting OpenClaw gateway to reload cron jobs..."
openclaw gateway restart >/tmp/daily-logbook-gateway-restart.log 2>&1
sleep 4

echo "[OK] Gateway restarted"
echo ""
echo "Installed job:"
jq --arg id "$JOB_ID" '.jobs[] | select(.id == $id)' "$CRON_FILE"

if [ "$TEST_MODE" = true ]; then
    echo ""
    echo "Rendering a Telegram approval request locally..."
    bash "$SCRIPT_DIR/render-telegram-approval-request.sh" | sed -n '1,120p'
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "From now on, a draft is generated and delivered in the Telegram chat at $TIME $TIMEZONE."
echo "MIS submission now waits for manual confirmation in Telegram."
