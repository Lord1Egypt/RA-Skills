#!/usr/bin/env bash
set -euo pipefail
#
# dreaming-optimizer — REM Cycle Pipeline
# Chains: score_entries → deduplicate → commit → summary
#
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="$SKILL_DIR/bin"
SCRIPTS_DIR="$SKILL_DIR/scripts"
STATE_DIR="$SKILL_DIR/.state"

THRESHOLD="${1:-70}"

echo "🌙 [dreaming-optimizer] Starting REM cycle optimization..."
echo "   Threshold: $THRESHOLD"
echo "   State dir: $STATE_DIR"
echo ""

# Clean old state (fresh cycle)
mkdir -p "$STATE_DIR"

# ── Step 1: Score entries ──────────────────────────────────────────────────
echo "📊 [Step 1/4] Scoring entries..."
if ! python3 "$BIN_DIR/score_entries.py" --threshold "$THRESHOLD"; then
    echo "❌ [Step 1] score_entries.py failed"
    exit 1
fi
echo ""

# ── Step 2: Deduplicate ────────────────────────────────────────────────────
echo "🔄 [Step 2/4] Deduplicating against B-layer..."
if ! python3 "$BIN_DIR/deduplicate.py" --threshold 0.85; then
    echo "❌ [Step 2] deduplicate.py failed"
    exit 1
fi
echo ""

# ── Step 3: Commit to B-layer ───────────────────────────────────────────────
echo "💾 [Step 3/4] Committing to B-layer..."
if ! python3 "$BIN_DIR/commit.py"; then
    echo "❌ [Step 3] commit.py failed"
    exit 1
fi
echo ""

# ── Step 4: Generate summary ───────────────────────────────────────────────
echo "📋 [Step 4/4] Generating REM cycle summary..."
if ! python3 "$SCRIPTS_DIR/dreaming_summary.py"; then
    echo "❌ [Step 4] dreaming_summary.py failed"
    exit 1
fi
echo ""

echo "🌙 [dreaming-optimizer] ✅ REM cycle complete."
echo ""
echo "   Summary saved to: ~/.openclaw/workspace/memory/dreaming-summaries/"
