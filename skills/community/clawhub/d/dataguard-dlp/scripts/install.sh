#!/bin/bash
# DataGuard DLP — Installation Script
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Installing DataGuard..."
echo ""

# Create directory structure
mkdir -p "$SKILL_DIR"/{config,context,logs,hooks}

# Initialize config files
echo "📋 Initializing configuration..."

# Default config
cat > "$SKILL_DIR/config/config.json" <<'JSONEOF'
{
  "risk_thresholds": {
    "low": 2,
    "medium": 5,
    "high": 6
  },
  "auto_block_critical": true,
  "auto_block_high": true,
  "require_approval_medium": false,
  "log_all_attempts": false,
  "log_data_previews": false,
  "domain_policy": "allowlist",
  "context_tracking": {
    "enabled": true,
    "max_age_minutes": 30,
    "score_boost_recent_read": 3
  }
}
JSONEOF

# Initialize domain lists
touch "$SKILL_DIR/config/domain-allowlist.txt"
touch "$SKILL_DIR/config/domain-blocklist.txt"

# Initialize empty context
echo '{"reads": []}' > "$SKILL_DIR/context/sensitive-reads.json"

# Initialize empty logs
touch "$SKILL_DIR/logs/blocked-attempts.log"
touch "$SKILL_DIR/logs/warnings.log"
touch "$SKILL_DIR/logs/all-attempts.log"
touch "$SKILL_DIR/logs/approved.log"

# Make scripts executable
chmod +x "$SKILL_DIR/scripts"/*.sh
chmod +x "$SKILL_DIR/scripts/hooks"/*.sh 2>/dev/null || true

# Tighten permissions on sensitive directories
chmod 700 "$SKILL_DIR/context" "$SKILL_DIR/logs"
chmod 600 "$SKILL_DIR/context/sensitive-reads.json" 2>/dev/null || true
chmod 600 "$SKILL_DIR/logs"/*.log 2>/dev/null || true
chmod 600 "$SKILL_DIR/config/config.json" 2>/dev/null || true

# Initialize domain lists with defaults
bash "$SKILL_DIR/scripts/domain-allowlist.sh" --init

echo ""
echo "✅ DataGuard installed successfully!"
echo ""
echo "📁 Location: $SKILL_DIR"
echo ""
echo "Quick Start:"
echo "  echo 'test data' | bash $SKILL_DIR/scripts/dlp-scan.sh"
echo "  bash $SKILL_DIR/scripts/domain-allowlist.sh --list"
echo "  bash $SKILL_DIR/scripts/audit-log.sh --stats"
echo ""
echo "📖 Read SKILL.md for integration with OpenClaw hooks."