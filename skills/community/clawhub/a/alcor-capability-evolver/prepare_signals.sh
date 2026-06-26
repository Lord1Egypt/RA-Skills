#!/bin/bash
# Prepare evolver signal sources before each run
# Merges memory files, cron run history, and health logs into MEMORY_DIR

set -e

MEMORY_DIR="${MEMORY_DIR:-/tmp/evolver_memory}"
mkdir -p "$MEMORY_DIR"

echo "[evolver-signal-prep] Merging signal sources into $MEMORY_DIR"

# 1. Memory files from all agent workspaces
echo "[evolver-signal-prep] Step 1: Memory files..."
total_mem=0
for d in /home/openclaw/.openclaw/workspace_roamer_*/memory; do
  if [ -d "$d" ]; then
    count=$(ls "$d"/*.md 2>/dev/null | wc -l)
    total_mem=$((total_mem + count))
    cp "$d"/*.md "$MEMORY_DIR/" 2>/dev/null || true
  fi
done
echo "[evolver-signal-prep]   Memory files merged: $total_mem"

# 2. Cron run history (error/failed/success signals)
echo "[evolver-signal-prep] Step 2: Cron run history..."
CRON_SIGNALS="$MEMORY_DIR/cron_signals.jsonl"
> "$CRON_SIGNALS"
for f in /home/openclaw/.openclaw/cron/runs/*.jsonl; do
  if [ -s "$f" ]; then
    cat "$f" >> "$CRON_SIGNALS"
  fi
done
cron_lines=$(wc -l < "$CRON_SIGNALS" 2>/dev/null || echo 0)
echo "[evolver-signal-prep]   Cron run entries: $cron_lines"

# 3. Health check log (config drift, security signals)
echo "[evolver-signal-prep] Step 3: Health logs..."
HEALTH_LOG="$MEMORY_DIR/health_log.json"
if [ -f /home/openclaw/.openclaw/logs/config-health.json ]; then
  cp /home/openclaw/.openclaw/logs/config-health.json "$HEALTH_LOG"
  echo "[evolver-signal-prep]   Health log copied"
else
  echo "[evolver-signal-prep]   No health log found"
fi

# 4. Config audit (security signals)
echo "[evolver-signal-prep] Step 4: Config audit..."
AUDIT_LOG="$MEMORY_DIR/config_audit.jsonl"
if [ -f /home/openclaw/.openclaw/logs/config-audit.jsonl ]; then
  cp /home/openclaw/.openclaw/logs/config-audit.jsonl "$AUDIT_LOG"
  audit_lines=$(wc -l < "$AUDIT_LOG" 2>/dev/null || echo 0)
  echo "[evolver-signal-prep]   Audit entries: $audit_lines"
else
  echo "[evolver-signal-prep]   No audit log found"
fi

# 5. OpenClaw commands log (error patterns)
echo "[evolver-signal-prep] Step 5: Commands log..."
CMD_LOG="$MEMORY_DIR/commands_log.log"
if [ -f /home/openclaw/.openclaw/logs/commands.log ]; then
  # Last 500 lines only to keep it manageable
  tail -500 /home/openclaw/.openclaw/logs/commands.log > "$CMD_LOG"
  echo "[evolver-signal-prep]   Commands log (last 500 lines) copied"
else
  echo "[evolver-signal-prep]   No commands log found"
fi

echo "[evolver-signal-prep] Signal preparation complete."
echo "[evolver-signal-prep] Total files in MEMORY_DIR: $(ls "$MEMORY_DIR" | wc -l)"