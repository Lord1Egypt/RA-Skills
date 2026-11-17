#!/usr/bin/env bash
# Content Ingestion Demo - turn a single file into a skill package.
#
# Usage:
#   content-ingest.sh <input-file> <output-skill-dir> [skill-name]
#
# Example:
#   content-ingest.sh ./article.md ./skills/article-note article-note

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 <input-file> <output-skill-dir> [skill-name]" >&2
  exit 2
fi

INPUT="$1"
OUT="$2"
GIVEN_NAME="${3:-}"

if [ ! -f "$INPUT" ]; then
  echo "input not found: $INPUT" >&2
  exit 1
fi

FILENAME="$(basename "$INPUT")"
STEM="${FILENAME%.*}"
SIZE_BYTES="$(stat -c '%s' "$INPUT")"
SHA="$(sha256sum "$INPUT" | awk '{print $1}')"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
NAME="${GIVEN_NAME:-${STEM// /-}}"
NAME="${NAME,,}"
NAME="${NAME//[^a-z0-9-]/}"

mkdir -p "$OUT/references" "$OUT/assets"
cp "$INPUT" "$OUT/references/$FILENAME"

cat > "$OUT/SKILL.md" <<EOF
---
name: ${NAME}
description: Ingested content from ${FILENAME}. SHA256 ${SHA:0:16}. Size ${SIZE_BYTES} bytes.
---

# ${NAME}

Ingested on ${NOW} from ${INPUT}.

- source file: \`${FILENAME}\`
- size: ${SIZE_BYTES} bytes
- sha256: ${SHA}

## Use it

Read [references/${FILENAME}](references/${FILENAME}).
EOF

cat > "$OUT/assets/metadata.json" <<EOF
{
  "name": "${NAME}",
  "source_path": "${INPUT}",
  "filename": "${FILENAME}",
  "size_bytes": ${SIZE_BYTES},
  "sha256": "${SHA}",
  "created_at": "${NOW}"
}
EOF

echo "${OUT}"
