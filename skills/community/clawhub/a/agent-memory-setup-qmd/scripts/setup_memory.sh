#!/usr/bin/env bash
# setup_memory.sh — Initialize the full memory system for an OpenClaw agent
# Usage: bash setup_memory.sh [workspace_dir]
#
# Creates directory structure, initializes memory files, installs plugins,
# and configures openclaw.json for the 3-tier memory system.

set -euo pipefail

WORKSPACE="${1:-$(pwd)}"
TODAY=$(date +%Y-%m-%d)

echo "═══════════════════════════════════════"
echo "  OpenClaw Agent Memory System Setup"
echo "═══════════════════════════════════════"
echo ""
echo "Workspace: $WORKSPACE"
echo ""

# ── Step 1: Create directory structure ──
echo "→ Creating memory directories..."
mkdir -p "$WORKSPACE/memory/hot"
mkdir -p "$WORKSPACE/memory/warm"
echo "  ✓ memory/, memory/hot/, memory/warm/"

# ── Step 2: Initialize memory files ──
echo "→ Initializing memory files..."

if [ ! -f "$WORKSPACE/memory/hot/HOT_MEMORY.md" ]; then
  cat > "$WORKSPACE/memory/hot/HOT_MEMORY.md" << 'EOF'
# 🔥 HOT MEMORY — Active Session State

_Current task, pending actions, temporary context. Updated frequently, pruned aggressively._
EOF
  echo "  ✓ memory/hot/HOT_MEMORY.md"
else
  echo "  · memory/hot/HOT_MEMORY.md (already exists, skipped)"
fi

if [ ! -f "$WORKSPACE/memory/warm/WARM_MEMORY.md" ]; then
  cat > "$WORKSPACE/memory/warm/WARM_MEMORY.md" << 'EOF'
# 🌡️ WARM MEMORY — Stable Config & Preferences

_User preferences, team roster, API references, critical gotchas. Updated when things change._
EOF
  echo "  ✓ memory/warm/WARM_MEMORY.md"
else
  echo "  · memory/warm/WARM_MEMORY.md (already exists, skipped)"
fi

if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
  cat > "$WORKSPACE/MEMORY.md" << EOF
# MEMORY.md — Long-Term Memory

_Created: ${TODAY}_

## Notes
- Agent workspace initialized on ${TODAY}
EOF
  echo "  ✓ MEMORY.md"
else
  echo "  · MEMORY.md (already exists, skipped)"
fi

if [ ! -f "$WORKSPACE/memory/$TODAY.md" ]; then
  cat > "$WORKSPACE/memory/$TODAY.md" << EOF
# $TODAY

- Workspace initialized. Memory system set up.
EOF
  echo "  ✓ memory/$TODAY.md"
else
  echo "  · memory/$TODAY.md (already exists, skipped)"
fi

if [ ! -f "$WORKSPACE/memory/heartbeat-state.json" ]; then
  cat > "$WORKSPACE/memory/heartbeat-state.json" << 'EOF'
{
  "lastChecks": {
    "email": null,
    "calendar": null
  }
}
EOF
  echo "  ✓ memory/heartbeat-state.json"
else
  echo "  · memory/heartbeat-state.json (already exists, skipped)"
fi

# ── Step 3: Install QMD ──
echo ""
echo "→ Checking QMD (semantic memory search)..."
if command -v qmd &>/dev/null; then
  echo "  ✓ QMD already installed: $(qmd --version 2>/dev/null || echo 'unknown version')"
else
  echo "  ⚠ QMD not found. Install it with one of:"
  echo "    pip install qmd"
  echo "    pipx install qmd"
  echo "    brew install qmd"
fi

# ── Step 4: Install Lossless Claw plugin ──
echo ""
echo "→ Checking Lossless Claw plugin..."
if command -v openclaw &>/dev/null; then
  if openclaw plugins list 2>/dev/null | grep -q "lossless-claw"; then
    echo "  ✓ Lossless Claw already installed"
  else
    echo "  Installing @martian-engineering/lossless-claw..."
    openclaw plugins install @martian-engineering/lossless-claw && echo "  ✓ Installed" || echo "  ⚠ Install failed — run manually: openclaw plugins install @martian-engineering/lossless-claw"
  fi
else
  echo "  ⚠ openclaw CLI not found. Install Lossless Claw manually:"
  echo "    openclaw plugins install @martian-engineering/lossless-claw"
fi

# ── Step 5: Config reminder ──
echo ""
echo "═══════════════════════════════════════"
echo "  Manual config step required"
echo "═══════════════════════════════════════"
echo ""
echo "Add these to your openclaw.json under agents.defaults:"
echo ""
echo '  "memorySearch": { "provider": "local" },'
echo '  "compaction": { "mode": "safeguard" },'
echo '  "contextPruning": { "mode": "cache-ttl", "ttl": "1h" },'
echo '  "heartbeat": { "every": "1h" }'
echo ""
echo "And in your agent's plugins section, enable:"
echo ""
echo '  "session-memory": { "enabled": true },'
echo '  "bootstrap-extra-files": { "enabled": true },'
echo '  "lossless-claw": { "enabled": true }'
echo ""
echo "Then restart: openclaw gateway restart"
echo ""
echo "═══════════════════════════════════════"
echo "  ✅ Memory system setup complete!"
echo "═══════════════════════════════════════"
