#!/bin/bash
# Setup automated daily crypto report delivery
# Usage: ./setup-cron.sh [CHANNEL_ID] [--time HH:MM] [--timezone TZ]

set -e

CHANNEL_ID="${1:-}"
TIME="${2:-08:00}"
TIMEZONE="${3:-Asia/Shanghai}"

if [ -z "$CHANNEL_ID" ]; then
    echo "Usage: ./setup-cron.sh [CHANNEL_ID] [--time HH:MM] [--timezone TZ]"
    echo "Example: ./setup-cron.sh -1002009088194"
    echo "Example: ./setup-cron.sh -1002009088194 --time 09:00 --timezone Asia/Tokyo"
    exit 1
fi

# Convert time to cron expression (default 08:00 = 0 0 * * * in UTC)
HOUR=$(echo "$TIME" | cut -d: -f1)
MINUTE=$(echo "$TIME" | cut -d: -f2)

# For UTC+8 (Asia/Shanghai), 08:00 = 00:00 UTC
# This is handled by the timezone parameter in cron
CRON_EXPR="$MINUTE $HOUR * * *"

echo "Setting up daily crypto report..."
echo "Channel: $CHANNEL_ID"
echo "Time: $TIME"
echo "Timezone: $TIMEZONE"
echo "Cron: $CRON_EXPR"

# The actual cron setup would be done via the cron tool
# This script serves as documentation for the setup process
cat <<EOF

To complete setup, run:

cron add \\
  --name "crypto-daily-report" \\
  --schedule "$CRON_EXPR" \\
  --timezone "$TIMEZONE" \\
  --target "telegram:$CHANNEL_ID" \\
  --command "generate-crypto-daily-report"

Or use the OpenClaw agent with this skill to set it up automatically.
EOF
