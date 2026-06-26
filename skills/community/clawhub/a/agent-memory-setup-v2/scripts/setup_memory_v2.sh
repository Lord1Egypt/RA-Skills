#!/usr/bin/env bash
# setup_memory_v2.sh — Initialize the 3-tier memory structure for an OpenClaw agent
# Usage: bash setup_memory_v2.sh [workspace_dir]

set -euo pipefail

WORKSPACE="${1:-$(pwd)}"
TODAY=$(date +%Y-%m-%d)

echo "═══════════════════════════════════════"
echo "  Memory System v2 — Directory Setup"
echo "═══════════════════════════════════════"
echo ""
echo "Workspace: $WORKSPACE"

# ── Create directory structure ──
mkdir -p "$WORKSPACE/memory/hot"
mkdir -p "$WORKSPACE/memory/warm"
echo "  ✓ memory/, memory/hot/, memory/warm/"

# ── Initialize memory files (skip existing) ──

[ ! -f "$WORKSPACE/memory/hot/HOT_MEMORY.md" ] && \
  echo "# 🔥 HOT MEMORY — Active Session State" > "$WORKSPACE/memory/hot/HOT_MEMORY.md" && \
  echo "  ✓ memory/hot/HOT_MEMORY.md" || echo "  · HOT_MEMORY.md (exists)"

[ ! -f "$WORKSPACE/memory/warm/WARM_MEMORY.md" ] && \
  echo "# 🌡️ WARM MEMORY — Stable Config & Preferences" > "$WORKSPACE/memory/warm/WARM_MEMORY.md" && \
  echo "  ✓ memory/warm/WARM_MEMORY.md" || echo "  · WARM_MEMORY.md (exists)"

[ ! -f "$WORKSPACE/MEMORY.md" ] && \
  echo -e "# MEMORY.md — Long-Term Memory\n\n_Created: ${TODAY}_" > "$WORKSPACE/MEMORY.md" && \
  echo "  ✓ MEMORY.md" || echo "  · MEMORY.md (exists)"

[ ! -f "$WORKSPACE/memory/$TODAY.md" ] && \
  echo -e "# $TODAY\n\n- Workspace initialized. Memory system v2 set up." > "$WORKSPACE/memory/$TODAY.md" && \
  echo "  ✓ memory/$TODAY.md" || echo "  · $TODAY.md (exists)"

[ ! -f "$WORKSPACE/memory/heartbeat-state.json" ] && \
  echo '{"lastChecks":{"email":null,"calendar":null}}' > "$WORKSPACE/memory/heartbeat-state.json" && \
  echo "  ✓ memory/heartbeat-state.json" || echo "  · heartbeat-state.json (exists)"

echo ""
echo "  ✅ Done. See SKILL.md for configuration steps."
