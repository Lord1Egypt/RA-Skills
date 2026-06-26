#!/usr/bin/env bash
# failure-memory: Initialize the failures log file
# Usage: bash init.sh [memory_dir]

set -euo pipefail

MEMORY_DIR="${1:-./memory}"

mkdir -p "$MEMORY_DIR"

FAILURES_FILE="$MEMORY_DIR/failures.md"

if [ -f "$FAILURES_FILE" ]; then
  echo "✅ $FAILURES_FILE already exists ($(grep -c '^## \[' "$FAILURES_FILE" 2>/dev/null || echo 0) entries)"
  exit 0
fi

cat > "$FAILURES_FILE" << 'EOF'
# Failure Memory

> Append-only log of failures, root causes, and resolutions.
> Search with `grep -i "<keyword>" memory/failures.md`

---

EOF

echo "✅ Created $FAILURES_FILE"
echo "Failures will be appended here automatically during agent work."
