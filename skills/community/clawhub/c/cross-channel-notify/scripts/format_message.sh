#!/usr/bin/env bash
# format_message.sh — Apply shared template, output email + imessage bodies
# Usage: format_message.sh "Your message body"
# Output: EMAIL_BODY<TAB>IMESSAGE_BODY
set -euo pipefail

BODY="${1:?Usage: format_message.sh <message body>}"
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")

# Email body: full markdown with template
EMAIL_BODY="## Notification

${BODY}

---
_Sent at ${TIMESTAMP}_"

# iMessage body: strip markdown syntax, truncate to 2000 chars
IMESSAGE_BODY=$(echo "$EMAIL_BODY" | \
  sed 's/^## //; s/^\*\*//; s/\*\*$//; s/^[-*] /• /; s/^#* //' | \
  head -c 2000)

printf '%s\t%s' "$EMAIL_BODY" "$IMESSAGE_BODY"
