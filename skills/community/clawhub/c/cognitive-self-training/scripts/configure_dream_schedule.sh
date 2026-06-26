#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
DREAM_TIME="${2:-}"
TIMEZONE="${3:-}"
STORE="$ROOT/.cognitive-training"
TODAY="$(date +%Y-%m-%d)"

if [ ! -d "$STORE" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  "$SCRIPT_DIR/init_cognitive_training.sh" "$ROOT"
fi

if [ -z "$DREAM_TIME" ]; then
  printf "What time should this bot run its daily dream review? (HH:MM, or blank for manual): "
  IFS= read -r DREAM_TIME || true
fi

if [ -z "$TIMEZONE" ]; then
  DETECTED_TZ="$(date +%Z 2>/dev/null || printf "local")"
  printf "Timezone? (default: %s): " "$DETECTED_TZ"
  IFS= read -r TIMEZONE || true
  TIMEZONE="${TIMEZONE:-$DETECTED_TZ}"
fi

if [ -z "$DREAM_TIME" ]; then
  STATUS="manual"
  DREAM_TIME="not-set"
else
  STATUS="active"
fi

cat > "$STORE/schedule.md" <<EOF
# Dream Schedule

Status: $STATUS
Time: $DREAM_TIME
Timezone: $TIMEZONE
Scope: project
Last configured: $TODAY

Prompt:
Run cognitive-self-training dream review. Read today's cognitive training files, randomly select an enabled dream style, write the result with exactly these top-level sections: Dream Review, Dream Recurrence Statement, Tian-Dao Deduction, Research Hypotheses, Tomorrow's Practice, Store Updates, Summary Narrative. Create due recall cards, update graph links, and propose tomorrow's strategy. Do not store secrets or raw private transcripts.
EOF

echo "Configured dream schedule at $STORE/schedule.md"
