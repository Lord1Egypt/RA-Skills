#!/usr/bin/env bash
# Opens the ClawBuddy LiteKit dashboard. Pass "setup" to jump to the wizard.
set -euo pipefail

BASE="https://agentcommander.lovable.app"
PATH_ARG="${1:-}"
URL="$BASE"
case "$PATH_ARG" in
  setup) URL="$BASE/setup" ;;
  "" ) ;;
  * ) URL="$BASE/$PATH_ARG" ;;
esac

echo "Opening ClawBuddy LiteKit → $URL"
if command -v open >/dev/null 2>&1; then open "$URL"
elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
else echo "Visit: $URL"
fi
