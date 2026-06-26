#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="${1:-.}"
COUNT="${2:-5}"

if [[ ! -d "$INPUT_DIR" ]]; then
  echo "error: directory not found: $INPUT_DIR" >&2
  exit 1
fi

echo "# Council v2 Monthly Retro"
echo "Source: $INPUT_DIR"
echo "Sample size: $COUNT"
echo

echo "## Sampled decisions"
find "$INPUT_DIR" -type f \( -name '*.json' -o -name '*.md' \) | sort | tail -n "$COUNT" | while read -r file; do
  echo "- $file"
done

echo
echo "## Review questions"
echo "- Was the decision correct in hindsight?"
echo "- Which reviewer surfaced signal vs. noise?"
echo "- Were critical findings real or false alarms?"
echo "- Should any role prompt be tightened or softened?"
echo "- Did synthesis preserve minority views accurately?"

echo
echo "## Output template"
cat <<'EOF'
- Decision:
- Original result:
- Hindsight verdict:
- Reviewer with best signal:
- Reviewer with most noise:
- Prompt changes to consider:
- Lessons:
EOF
