#!/bin/bash
# diagnose.sh — Full OpenClaw gateway health diagnosis
# Exit codes: 0 = healthy, 1 = issues found

set -uo pipefail
ISSUES=0
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
LABEL="ai.openclaw.gateway"
LOG="$HOME/.openclaw/logs/gateway.log"

echo "🔍 OpenClaw Gateway Health Diagnosis"
echo "====================================="
echo ""

# 1. Process state
echo "## 1. Process State"
if PRINT_OUT=$(launchctl print "gui/$(id -u)/$LABEL" 2>&1); then
    PID=$(echo "$PRINT_OUT" | grep '	pid' | awk '{print $3}')
    STATE=$(echo "$PRINT_OUT" | grep '	state =' | head -1 | awk '{print $3}')
    if [ -n "$PID" ] && [ "$PID" -gt 0 ] 2>/dev/null; then
        UPTIME=$(ps -o etime= -p "$PID" 2>/dev/null | xargs)
        echo "✅ Running (PID $PID, uptime: $UPTIME)"
    else
        echo "❌ NOT RUNNING (state: $STATE)"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "❌ Service not loaded in launchd"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# 2. launchd classification
echo "## 2. launchd Classification"
REASON=$(echo "$PRINT_OUT" | grep 'immediate reason' | awk '{print $4}' 2>/dev/null || echo "unknown")
EXIT_TIMEOUT=$(echo "$PRINT_OUT" | grep 'exit timeout' | awk '{print $4}' 2>/dev/null || echo "unknown")
JETSAM=$(echo "$PRINT_OUT" | grep 'jetsam priority' | awk '{print $4}' 2>/dev/null || echo "unknown")
RUNS=$(echo "$PRINT_OUT" | grep '	runs =' | awk '{print $3}' 2>/dev/null || echo "unknown")

if [ "$REASON" = "inefficient" ]; then
    echo "⚠️  Classified as INEFFICIENT — restarts will be delayed!"
    ISSUES=$((ISSUES + 1))
else
    echo "✅ Classification: $REASON"
fi

echo "   Exit timeout: $EXIT_TIMEOUT"
echo "   Jetsam priority: $JETSAM (40=Background, 100+=Interactive)"
echo "   Run count: $RUNS"

if [ "$JETSAM" -lt 80 ] 2>/dev/null; then
    echo "⚠️  Low jetsam priority ($JETSAM) — add ProcessType=Interactive to plist"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# 3. Plist config
echo "## 3. Plist Configuration"
if [ -f "$PLIST" ]; then
    for KEY in ExitTimeOut ProcessType LowPriorityBackgroundIO ThrottleInterval KeepAlive; do
        if plutil -p "$PLIST" 2>/dev/null | grep -q "\"$KEY\""; then
            VAL=$(plutil -p "$PLIST" | grep "\"$KEY\"" | head -1 | sed 's/.*=> //')
            echo "✅ $KEY = $VAL"
        else
            echo "❌ $KEY: MISSING"
            ISSUES=$((ISSUES + 1))
        fi
    done
else
    echo "❌ Plist not found at $PLIST"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# 4. Reload mode
echo "## 4. Config Reload Mode"
RELOAD_MODE=$(cat ~/.openclaw/openclaw.json 2>/dev/null | python3 -c "
import sys, json
try:
    c = json.load(sys.stdin)
    print(c.get('gateway', {}).get('reload', {}).get('mode', 'hybrid (default)'))
except:
    print('unknown')
" 2>/dev/null)
if [ "$RELOAD_MODE" = "hot" ]; then
    echo "✅ Reload mode: hot (plugin changes won't cause restarts)"
else
    echo "⚠️  Reload mode: $RELOAD_MODE — plugin re-resolve may cause restart loops"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# 5. Restart frequency
echo "## 5. Restart Frequency (last 24h)"
if [ -f "$LOG" ]; then
    TODAY=$(date +%Y-%m-%d)
    RESTARTS=$(grep "listening on ws:" "$LOG" 2>/dev/null | grep "$TODAY" | wc -l | xargs)
    SIGTERMS=$(grep "SIGTERM\|SIGUSR1" "$LOG" 2>/dev/null | grep "$TODAY" | wc -l | xargs)
    PLUGIN_RESTARTS=$(grep "restartReason.*plugins.installs" "$LOG" 2>/dev/null | grep "$TODAY" | wc -l | xargs)
    echo "   Boots today: $RESTARTS"
    echo "   Signals (SIGTERM/SIGUSR1): $SIGTERMS"
    echo "   Plugin-caused restarts: $PLUGIN_RESTARTS"
    if [ "$PLUGIN_RESTARTS" -gt 3 ] 2>/dev/null; then
        echo "⚠️  Plugin restart loop detected! Set gateway.reload.mode = \"hot\""
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "⚠️  Log file not found"
fi
echo ""

# 6. Power management
echo "## 6. Power Management"
POWERNAP=$(pmset -g 2>/dev/null | grep "powernap" | awk '{print $2}')
SLEEP=$(pmset -g 2>/dev/null | grep " sleep " | head -1 | awk '{print $2}')
echo "   Power Nap: $POWERNAP (0=disabled, 1=enabled)"
echo "   Sleep: $SLEEP (0=never)"
if [ "$POWERNAP" = "1" ]; then
    echo "⚠️  Power Nap enabled — may delay restarts. Fix: sudo pmset -a powernap 0"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Summary
echo "====================================="
if [ "$ISSUES" -eq 0 ]; then
    echo "✅ All checks passed — gateway is healthy"
    exit 0
else
    echo "⚠️  $ISSUES issue(s) found — see above for fixes"
    exit 1
fi
