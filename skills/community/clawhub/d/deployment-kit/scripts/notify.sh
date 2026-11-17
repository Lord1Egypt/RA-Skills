#!/bin/bash
# Telegram alert: BOT_TOKEN + CHAT_ID in environment or file
# 🔒 Secrets: set permissions with: chmod 600 ~/.config/tg-alert.env
#    Never commit the token in git/logs/shell history.
TOKEN="${TG_BOT_TOKEN:-}"
CHAT="${TG_CHAT_ID:-}"
[ -z "$TOKEN" ] && [ -f ~/.config/tg-alert.env ] && source ~/.config/tg-alert.env
[ -z "$TOKEN" ] && { echo "Set TG_BOT_TOKEN"; exit 1; }
MSG="${1:-⚠️ Alert}"
curl -s --max-time 10 "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d "chat_id=$CHAT" -d "text=$MSG" > /dev/null
