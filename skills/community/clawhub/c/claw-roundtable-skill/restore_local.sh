#!/bin/bash
# RoundTable Skill — Restore Local SKILL.md from Backup
# Restores the original SKILL.md after ClawHub publishing.

set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
BACKUP="$SKILL_DIR/.skill_backup"
MODEL_CONFIG_MD="$SKILL_DIR/MODEL_CONFIG.md"
README_MD="$SKILL_DIR/README.md"

if [[ -f "$BACKUP" ]]; then
  mv "$BACKUP" "$SKILL_MD"
  echo "✅ SKILL.md restored from backup"
else
  echo "⚠️  No backup found — SKILL.md unchanged"
fi

# Restore MODEL_CONFIG.md
MODEL_BACKUP="$SKILL_DIR/.model_config_backup"
if [[ -f "$MODEL_BACKUP" ]]; then
  mv "$MODEL_BACKUP" "$MODEL_CONFIG_MD"
  echo "✅ MODEL_CONFIG.md restored from backup"
fi

# Restore README.md
README_BACKUP="$SKILL_DIR/.readme_backup"
if [[ -f "$README_BACKUP" ]]; then
  mv "$README_BACKUP" "$README_MD"
  echo "✅ README.md restored from backup"
fi
