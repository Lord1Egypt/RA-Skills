#!/bin/bash
# FlowForge — Account rotation for Claude Code
# Switches to the next available Claude Max account on rate limit.
#
# SETUP: Add your Claude accounts to ~/.flowforge/accounts.txt
# (one email per line). Example:
#
#   you@gmail.com
#   you-alt@gmail.com
#   you-work@company.com
#
# Save credentials for each account first:
#   claude auth login   # log in as account 1
#   mkdir -p ~/.claude/accounts
#   cp ~/.claude/.credentials.json ~/.claude/accounts/you@gmail.com.json
#   # repeat for each account

ACCOUNTS_FILE="$HOME/.flowforge/accounts.txt"

if [[ ! -f "$ACCOUNTS_FILE" ]]; then
  echo "⚠️  No accounts configured. Create ~/.flowforge/accounts.txt with one email per line."
  echo "    See: https://github.com/windseeker1111/flowforge#multi-account-setup"
  exit 1
fi

mapfile -t ACCOUNTS < "$ACCOUNTS_FILE"

if [[ ${#ACCOUNTS[@]} -eq 0 ]]; then
  echo "⚠️  accounts.txt is empty. Add at least one email."
  exit 1
fi

CURRENT=$(claude auth status 2>/dev/null | grep email | awk '{print $2}')
echo "Current account: ${CURRENT:-none}"

# Find next account in rotation
NEXT=""
for i in "${!ACCOUNTS[@]}"; do
  if [[ "${ACCOUNTS[$i]}" == "$CURRENT" ]]; then
    NEXT="${ACCOUNTS[$(( (i + 1) % ${#ACCOUNTS[@]} ))]}"
    break
  fi
done

# Default to first account if current not found
if [[ -z "$NEXT" ]]; then
  NEXT="${ACCOUNTS[0]}"
fi

echo "Switching to: $NEXT"

CREDS_DIR="$HOME/.claude/accounts"
if [[ -f "$CREDS_DIR/$NEXT.json" ]]; then
  cp "$CREDS_DIR/$NEXT.json" "$HOME/.claude/.credentials.json"
  echo "✅ Switched to $NEXT"
else
  echo "⚠️  No saved credentials for $NEXT"
  echo "    Run: claude auth login (as $NEXT)"
  echo "    Then: cp ~/.claude/.credentials.json ~/.claude/accounts/$NEXT.json"
  exit 1
fi
