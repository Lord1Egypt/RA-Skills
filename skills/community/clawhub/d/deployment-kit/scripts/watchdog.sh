#!/bin/bash
# Heartbeat-watchdog: hvis HB-fil > 90s gammel → genstart + alert
# Cron: */2 * * * * bash /opt/watchdog.sh myapp
SVC="${1:?Navn mangler}"
HB="/tmp/${SVC}_HB.txt"
[ ! -f "$HB" ] && { echo "HB mangler — genstarter $SVC"; bash "$(dirname "$0")/deploy.sh" "$SVC"; bash "$(dirname "$0")/notify.sh" "⚠️ $SVC: HB manglede — genstartet"; exit; }
AGE=$(( $(date +%s) - $(stat -c %Y "$HB") ))
if [ "$AGE" -gt 90 ]; then
  echo "HB forældet ($AGE s) — genstarter $SVC"
  bash "$(dirname "$0")/deploy.sh" "$SVC"
  bash "$(dirname "$0")/notify.sh" "⚠️ $SVC: HB $AGE s gammel — genstartet"
else
  echo "OK — $SVC HB $AGE s"
fi
