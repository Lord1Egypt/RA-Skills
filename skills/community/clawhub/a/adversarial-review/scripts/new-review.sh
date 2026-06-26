#!/bin/bash
# adversarial-review: Initialize a new review session directory
#
# Usage: new-review.sh <project-slug> <path-to-input-doc>
#
# Creates:
#   ~/.openclaw/workspace/reviews/{YYYY-MM-DD}-{slug}/
#     input/{filename}     ← copy of the document being reviewed
#     redlines/            ← populated by reviewers
#     output/              ← populated after v2 is written
#     positions.md         ← template for agree/disagree/modify log

set -e

REVIEWS_DIR=~/.openclaw/workspace/reviews

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: new-review.sh <project-slug> <path-to-input-doc>"
  echo "Example: new-review.sh bitwage-taxonomy ~/Desktop/strategy.md"
  exit 1
fi

SLUG="$1"
INPUT_DOC="$2"

if [ ! -f "$INPUT_DOC" ]; then
  echo "Error: File not found: $INPUT_DOC"
  exit 1
fi

DATE=$(date +%Y-%m-%d)
SESSION_NAME="${DATE}-${SLUG}"
SESSION_DIR="${REVIEWS_DIR}/${SESSION_NAME}"

if [ -d "$SESSION_DIR" ]; then
  echo "Warning: Session directory already exists: $SESSION_DIR"
  echo "Continue? (y/n)"
  read -r confirm
  if [ "$confirm" != "y" ]; then exit 1; fi
fi

mkdir -p "$SESSION_DIR/input"
mkdir -p "$SESSION_DIR/redlines"
mkdir -p "$SESSION_DIR/output"

# Copy input document
FILENAME=$(basename "$INPUT_DOC")
cp "$INPUT_DOC" "$SESSION_DIR/input/$FILENAME"

# Create positions.md template
cat > "$SESSION_DIR/positions.md" << EOF
# Positions — ${SESSION_NAME}

**Document:** ${FILENAME}
**Date:** ${DATE}
**Status:** In Progress

---

## Redline Positions

For each redline from combined.md, record your position here.

Format:
\`\`\`
## [REDLINE-{TYPE}-{NNN}] — {AGREE | DISAGREE | MODIFY}

**Redline summary:** {one sentence}
**Position:** AGREE | DISAGREE | MODIFY
**Rationale:** {required for DISAGREE and MODIFY}
**Change in v2:** {what changes, or "No change — rejected"}
\`\`\`

---

<!-- Positions go below this line -->


EOF

echo ""
echo "✓ Review session initialized: $SESSION_DIR"
echo ""
echo "  input/    → $FILENAME (ready)"
echo "  redlines/ → empty (populate after reviewer runs)"
echo "  output/   → empty (populate after v2 is written)"
echo "  positions.md → template ready"
echo ""
echo "Session name: $SESSION_NAME"
echo "Next: spawn reviewers from references/reviewer-personas.md"
echo "      write reviewer outputs to: $SESSION_DIR/redlines/reviewer-{role}.md"
