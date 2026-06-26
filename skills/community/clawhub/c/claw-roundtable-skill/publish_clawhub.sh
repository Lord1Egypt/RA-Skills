#!/bin/bash
# RoundTable Skill — ClawHub Publishing Script
# Backs up, publishes, then restores. Local files are NEVER modified permanently.
#
# NOTE: As of v3.0.3, source files are already ClawHub-compliant.
# This script only handles backup → publish → restore.

set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
MODEL_CONFIG_MD="$SKILL_DIR/MODEL_CONFIG.md"
README_MD="$SKILL_DIR/README.md"

# --- Pre-flight checks ---
if [[ ! -f "$SKILL_MD" ]]; then
  echo "❌ SKILL.md not found in $SKILL_DIR"; exit 1
fi
for bak in ".skill_backup" ".model_config_backup" ".readme_backup"; do
  if [[ -f "$SKILL_DIR/$bak" ]]; then
    echo "⚠️  Backup $bak already exists. Run restore_local.sh first."; exit 1
  fi
done

# =============================================
# Step 1: Backup
# =============================================
cp "$SKILL_MD" "$SKILL_DIR/.skill_backup"
cp "$MODEL_CONFIG_MD" "$SKILL_DIR/.model_config_backup"
cp "$README_MD" "$SKILL_DIR/.readme_backup"
echo "✅ Backups saved"

# =============================================
# Step 2: Publish
# =============================================
if command -v clawhub &>/dev/null; then
  VERSION=$(grep '"version"' "$SKILL_DIR/clawhub.json" | sed 's/.*"\([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\)".*/\1/')
  if [[ -z "$VERSION" ]]; then
    echo "⚠️  Could not parse version from clawhub.json"; exit 1
  fi
  echo "📦 Publishing version $VERSION..."
  clawhub publish "$SKILL_DIR" --slug claw-roundtable-skill --version "$VERSION"
  echo "✅ Published to ClawHub"
else
  echo "⚠️  clawhub CLI not found. Skipping publish."
  echo "   Install: npm install -g @anthropic/clawhub"
fi

# =============================================
# Step 3: Restore
# =============================================
bash "$SKILL_DIR/restore_local.sh"
echo "✅ All local files restored"
