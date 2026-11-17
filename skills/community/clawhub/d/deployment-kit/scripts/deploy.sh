#!/bin/bash
# 1-command deploy: build → restart → verify
# Usage: bash deploy.sh <service-name> [workdir]
#        bash deploy.sh --dry-run <service-name>   # preview only, no changes
# ⚠️ WARNING: restarts services (sudo systemctl / pkill / nohup) — can cause downtime.
#    Only run on services you own. Test on staging first. Have a rollback plan.
#    A confirmation prompt is shown before any destructive action.
SVC="${1:?Service-name missing}"
DRY=0
if [ "$1" = "--dry-run" ]; then
  DRY=1
  SVC="${2:?Service-name missing}"
  DIR="${3:-/home/openclaw/.openclaw/workspace/$SVC}"
else
  DIR="${2:-/home/openclaw/.openclaw/workspace/$SVC}"
fi

echo "1) Build/prepare"
cd "$DIR" || exit 1
# TODO: your build command (pip install, npm build, etc.)

echo "2) Restart service"
if systemctl list-units --type=service 2>/dev/null | grep -q "$SVC"; then
  echo "  target: systemd service '$SVC' via sudo systemctl restart"
  if [ "$DRY" = "1" ]; then echo "  [dry-run] no changes made"; exit 0; fi
  read -r -p "  Restart systemd service '$SVC'? [y/N] " ans
  [ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "  cancelled"; exit 1; }
  sudo systemctl restart "$SVC" && echo "  systemd: restarted"
else
  echo "  target: kill matching processes (pkill -f '$SVC') + relaunch via nohup"
  if [ "$DRY" = "1" ]; then echo "  [dry-run] no changes made"; exit 0; fi
  read -r -p "  Kill processes matching '$SVC' and relaunch? [y/N] " ans
  [ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "  cancelled"; exit 1; }
  pkill -f "$SVC" 2>/dev/null; sleep 2
  # Intentional daemonization: nohup keeps the process running after shell exit
  nohup python3 "$DIR/server.py" >/tmp/$SVC.log 2>&1 &
  echo "  nohup: restarted (pid $!)"
fi
sleep 3
echo "3) Verify"
curl -s --max-time 5 --cacert /etc/ssl/certs/ca-certificates.crt https://localhost:8791/health 2>/dev/null | head -c 150 || echo "  (no /health — check log)"
echo
echo "4) Log: tail /tmp/$SVC.log"
