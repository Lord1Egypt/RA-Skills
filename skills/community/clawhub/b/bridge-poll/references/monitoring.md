# Monitoring & Health Checks

Copy-paste checks for your heartbeat or monitoring cron.

## All-in-One Health Check Script

Save as `bridge_healthcheck.sh` and run from heartbeat:

```bash
#!/bin/bash
# Bridge health check — run from heartbeat or monitoring cron.
# Exit 0 = healthy, exit 1 = problem (with diagnostic output).

BRIDGE_HOST="${BRIDGE_HOST:-localhost}"
BRIDGE_PORT="${BRIDGE_PORT:-18790}"
BRIDGE_TOKEN="${BRIDGE_TOKEN:-}"
TS_FILE="${BRIDGE_TS_FILE:-/tmp/acp_bridge_last_ts}"
MAX_STALE_SECONDS="${BRIDGE_MAX_STALE:-1800}"  # 30 min default

ISSUES=0

# --- Check 1: Bridge process alive ---
AUTH_HEADER=""
[ -n "$BRIDGE_TOKEN" ] && AUTH_HEADER="-H \"Authorization: Bearer $BRIDGE_TOKEN\""

HEALTH=$(eval curl -s -f --max-time 5 "http://$BRIDGE_HOST:$BRIDGE_PORT/api/health" $AUTH_HEADER 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ Bridge server unreachable at $BRIDGE_HOST:$BRIDGE_PORT"
    ISSUES=$((ISSUES + 1))
else
    echo "✅ Bridge server alive"
fi

# --- Check 2: Cursor timestamp not in future ---
if [ -f "$TS_FILE" ]; then
    LAST_TS=$(cat "$TS_FILE")
    NOW=$(python3 -c "import time; print(time.time())")
    IS_FUTURE=$(python3 -c "print('yes' if float('$LAST_TS') > float('$NOW') + 60 else 'no')")
    if [ "$IS_FUTURE" = "yes" ]; then
        echo "❌ Cursor is in the FUTURE ($LAST_TS > $NOW) — resetting"
        echo "$NOW" > "$TS_FILE"
        ISSUES=$((ISSUES + 1))
    else
        echo "✅ Cursor timestamp OK ($LAST_TS)"
    fi
else
    echo "⚠️ No cursor file at $TS_FILE — initializing"
    python3 -c "import time; print(time.time())" > "$TS_FILE"
fi

# --- Check 3: Last activity not too stale ---
if [ -f "$TS_FILE" ]; then
    LAST_TS=$(cat "$TS_FILE")
    AGE=$(python3 -c "import time; print(int(time.time() - float('$LAST_TS')))")
    if [ "$AGE" -gt "$MAX_STALE_SECONDS" ]; then
        echo "⚠️ Last poll was ${AGE}s ago (threshold: ${MAX_STALE_SECONDS}s)"
        ISSUES=$((ISSUES + 1))
    else
        echo "✅ Last poll ${AGE}s ago"
    fi
fi

# --- Check 4: JSONL file sizes ---
for f in inbox.jsonl outbox.jsonl; do
    FPATH="${ACP_BRIDGE_DIR:-/tmp/acp_bridge}/$f"
    if [ -f "$FPATH" ]; then
        SIZE=$(du -sh "$FPATH" | cut -f1)
        LINES=$(wc -l < "$FPATH")
        SIZE_BYTES=$(stat -c%s "$FPATH" 2>/dev/null || stat -f%z "$FPATH" 2>/dev/null)
        if [ "$SIZE_BYTES" -gt 52428800 ]; then  # 50MB
            echo "⚠️ $f is large: $SIZE ($LINES messages) — run bridge_prune.py"
            ISSUES=$((ISSUES + 1))
        else
            echo "✅ $f: $SIZE ($LINES messages)"
        fi
    fi
done

# --- Summary ---
if [ $ISSUES -eq 0 ]; then
    echo "Bridge health: ALL OK"
    exit 0
else
    echo "Bridge health: $ISSUES issue(s) found"
    exit 1
fi
```

## HEARTBEAT.md Snippet

Add to your agent's HEARTBEAT.md:

```markdown
## Bridge Health Check
Run: bash [WORKSPACE]/bridge_healthcheck.sh
- If bridge is dead → restart: `nohup python3 /path/to/acp_bridge.py &`
- If cursor is future → already auto-reset by script
- If stale > 30 min → check cron job logs for the bridge poll cron
- If JSONL > 50MB → run bridge_prune.py
```

## Minimal Inline Check (No Script)

If you don't want a separate script, paste this directly in the heartbeat cron prompt:

```
Bridge check:
1. curl -s localhost:18790/api/health — if fails, bridge is dead
2. cat /tmp/acp_bridge_last_ts — if value > current time, reset it
3. Check age — if > 30 min, cron poll may be broken
```
