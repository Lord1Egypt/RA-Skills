# BOOT.md

Gateway startup checklist fragment for cancelling a pending rollback only after Gateway becomes healthy.

```bash
STATE="$HOME/.openclaw/state/rollback-pending.json"
LOG="$HOME/.openclaw/logs/rollback.log"
GATEWAY_PORT="18789"

if [ -f "$STATE" ]; then
  LABEL=$(jq -r '.launchd_label // empty' "$STATE")
  PLIST="$HOME/.openclaw/${LABEL}.plist"

  echo "[$(date -Iseconds)] BOOT: detected rollback state file: $STATE" >> "$LOG"
  echo "[$(date -Iseconds)] BOOT: waiting for Gateway health check" >> "$LOG"

  HEALTHY=false
  for i in {1..30}; do
    if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$GATEWAY_PORT/health" 2>/dev/null | grep -q "200"; then
      HEALTHY=true
      echo "[$(date -Iseconds)] BOOT: Gateway health check passed on attempt $i" >> "$LOG"
      break
    fi
    sleep 1
  done

  if [ "$HEALTHY" = true ]; then
    if [ -n "$LABEL" ] && [ -f "$PLIST" ]; then
      launchctl unload "$PLIST" 2>/dev/null || true
      rm -f "$PLIST"
      rm -f "$HOME/.openclaw/.rollback_execute.sh"
      echo "[$(date -Iseconds)] BOOT: rollback cancelled (label=$LABEL)" >> "$LOG"
    else
      echo "[$(date -Iseconds)] BOOT: rollback state present but plist missing (label=$LABEL)" >> "$LOG"
    fi

    rm -f "$STATE"
    echo "[$(date -Iseconds)] BOOT: rollback state removed" >> "$LOG"
  else
    echo "[$(date -Iseconds)] BOOT: Gateway still unhealthy after 30s, keeping rollback pending" >> "$LOG"
  fi
fi
```
