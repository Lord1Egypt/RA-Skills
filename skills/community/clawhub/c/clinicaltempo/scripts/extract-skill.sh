#!/bin/bash
# Scaffold a new Agent Skill folder from this package's template (Clinical Tempo convention).
# Usage: ./extract-skill.sh <skill-slug> [--dry-run]
# Output: ../../<skill-slug>/  (relative to scripts/ → .cursor/skills/<skill-slug>/)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SKILL_ROOT/assets/SKILL-TEMPLATE.md"
# Parent of `clawhub/` is `.cursor/skills/`
OUT_BASE="$(cd "$SKILL_ROOT/.." && pwd)"

usage() {
  echo "Usage: $(basename "$0") <skill-slug> [--dry-run]"
  echo "Creates: .cursor/skills/<skill-slug>/SKILL.md (from template header) + README stub."
}

SKILL_NAME=""
DRY_RUN=false
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) SKILL_NAME="$1"; shift ;;
  esac
done

if [[ -z "$SKILL_NAME" ]] || [[ "$SKILL_NAME" == *" "* ]]; then
  echo -e "${RED}ERROR:${NC} provide a lowercase-hyphenated skill slug" >&2
  usage
  exit 1
fi

DEST="$OUT_BASE/$SKILL_NAME"
if [[ -e "$DEST" ]]; then
  echo -e "${RED}ERROR:${NC} already exists: $DEST" >&2
  exit 1
fi

if $DRY_RUN; then
  echo -e "${GREEN}[dry-run]${NC} would create $DEST"
  exit 0
fi

mkdir -p "$DEST/references" "$DEST/assets" "$DEST/scripts"
cat > "$DEST/SKILL.md" << EOF
---
name: $SKILL_NAME
description: >-
  TODO: one paragraph — triggers, key files, when to load this skill.
metadata: {}
---

# ${SKILL_NAME//-/ }

Brief description. Replace this file with content modeled on \`.cursor/skills/clawhub/SKILL.md\`.

## Quick reference

| Situation | Action |
| --- | --- |
| … | … |

## See also

- Parent patterns: **Clinical Tempo** \`.cursor/skills/clawhub/\`
EOF

cp "$TEMPLATE" "$DEST/assets/SKILL-TEMPLATE.md" 2>/dev/null || true

cat > "$DEST/README.md" << EOF
# \`$SKILL_NAME\`

Scaffolded by \`clawhub/scripts/extract-skill.sh\`. Fill \`SKILL.md\`, add \`references/\`, then zip for [ClawHub](https://clawhub.ai/).
EOF

echo -e "${GREEN}OK:${NC} $DEST"
