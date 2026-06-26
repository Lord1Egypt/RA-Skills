#!/bin/bash
# extract-entities.sh — Extract named entities from knowledge Markdown files
# Usage: extract-entities.sh <knowledge_dir_or_file>
# Output: Sorted entity list with frequency counts to stdout
#
# Extracts entities by pattern matching:
#   - Capitalized multi-word names (2-4 words starting with capitals)
#   - Known technology terms (from inline dictionary)
#   - Entities from **Key facts:** sections
set -euo pipefail

INPUT="${1:?Usage: extract-entities.sh <knowledge_dir_or_file>}"

# Collect files
FILES=()
if [ -d "$INPUT" ]; then
  while IFS= read -r f; do FILES+=("$f"); done < <(find "$INPUT" -name "*.md" -type f | sort)
else
  FILES=("$INPUT")
fi

if [ ${#FILES[@]} -eq 0 ]; then
  echo "No .md files found in $INPUT"
  exit 1
fi

# Known tech terms to always extract
TECH_TERMS="MCP|API|SDK|RAG|LLM|GPT|JSONL|RSS|OAuth|WebSocket"

# Extract entities from all files
ALL_ENTITIES=""
for FILE in "${FILES[@]}"; do
  # Get body text (skip frontmatter)
  BODY=$(sed -n '/^---$/,/^---$/!p' "$FILE" | tail -n +2)

  # Extract capitalized multi-word names (2-4 words, each starting with uppercase)
  # This catches: "Sam Altman", "Harrison Chase", "OpenAI Agents SDK", "Sequoia Capital"
  NAMES=$(echo "$BODY" | grep -oE '[A-Z][a-z]+([[:space:]][A-Z][a-z]*){0,3}' | sort -u || true)

  # Extract single capitalized words that are likely proper nouns (>= 4 chars to avoid noise)
  PROPER=$(echo "$BODY" | grep -oE '\b[A-Z][a-zA-Z]{3,}\b' | grep -vE '^(The|This|That|What|When|Where|Which|With|From|Into|About|After|Before|Under|Over|Between|Through|During|Against|Within|Without|Along|Among|Around|Behind|Below|Beneath|Beside|Beyond|Despite|Down|Except|Inside|Onto|Outside|Since|Throughout|Toward|Upon|Every|Each|Some|Also|Here|There|However|Therefore|Furthermore|Moreover|Additionally|Meanwhile|Nevertheless|Nonetheless|Otherwise|Still|Thus|Instead|Indeed|Certainly|Perhaps|Probably|Possibly|Actually|Finally|Basically|Essentially|Generally|Obviously|Specifically|Particularly|Especially|Recently|Currently|Previously|Already|Impact|Released|Raises|Supports|Updated|Announced|Closed|Enables|Includes|Maintains|Competing|Represents|Introduces|Noted|Said|Added|Brings|Planned|Grew|Directly|Native|Improved|Complex|Multi|Real|Critical|Fundamental|Most|Popular)$' | sort -u || true)

  # Extract known tech acronyms
  TECH=$(echo "$BODY" | grep -oE "\b(${TECH_TERMS})\b" | sort -u || true)

  # Combine
  FILE_ENTITIES=$(printf '%s\n%s\n%s' "$NAMES" "$PROPER" "$TECH" | grep -v '^$' | sort -u)
  ALL_ENTITIES+="$FILE_ENTITIES"$'\n'
done

# Count frequencies and output
echo "=== ENTITIES ==="
echo "$ALL_ENTITIES" | grep -v '^$' | sort | uniq -c | sort -rn | while read -r count entity; do
  echo "  ${count}x  $entity"
done

# Extract entity co-occurrences (entities appearing in same file)
echo ""
echo "=== TOP ENTITIES BY FREQUENCY ==="
echo "$ALL_ENTITIES" | grep -v '^$' | sort | uniq -c | sort -rn | head -10 | while read -r count entity; do
  echo "  ${count}x  $entity"
done
