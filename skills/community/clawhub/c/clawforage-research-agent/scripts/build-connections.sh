#!/bin/bash
# build-connections.sh — Find cross-article entity relationships
# Usage: build-connections.sh <knowledge_dir>
# Output: Entity co-occurrence map + article timeline to stdout
#
# For each entity appearing in 2+ articles, lists which articles mention it.
# This gives the agent a "connection map" to write about relationships.
set -euo pipefail

KNOWLEDGE_DIR="${1:?Usage: build-connections.sh <knowledge_dir>}"

if [ ! -d "$KNOWLEDGE_DIR" ]; then
  echo "ERROR: Not a directory: $KNOWLEDGE_DIR"
  exit 1
fi

# Known tech terms
TECH_TERMS="MCP|API|SDK|RAG|LLM|GPT"

# Build entity-to-file mapping
declare -A ENTITY_FILES 2>/dev/null || true
TMPDIR=$(mktemp -d)

# For each file, extract entities and record which file they came from
for FILE in "$KNOWLEDGE_DIR"/*.md; do
  [ -f "$FILE" ] || continue
  BASENAME=$(basename "$FILE" .md)
  BODY=$(sed -n '/^---$/,/^---$/!p' "$FILE" | tail -n +2)

  # Extract entities (same logic as extract-entities.sh, simplified)
  ENTITIES=$(echo "$BODY" | grep -oE '[A-Z][a-z]+([[:space:]][A-Z][a-z]*){0,2}' | sort -u || true)
  PROPER=$(echo "$BODY" | grep -oE '\b[A-Z][a-zA-Z]{3,}\b' | grep -vE '^(The|This|That|What|When|Where|Which|With|From|Into|About|After|Before|Under|Over|Between|Through|During|Against|Within|Without|Also|Here|There|However|Therefore|Furthermore|Moreover|Impact|Released|Raises|Supports|Updated|Announced|Closed|Enables|Includes|Maintains|Competing|Represents|Introduces|Noted|Said|Added|Brings|Planned|Directly|Native|Improved|Complex|Multi|Real|Critical|Fundamental|Most|Popular)$' | sort -u || true)
  TECH=$(echo "$BODY" | grep -oE "\b(${TECH_TERMS})\b" | sort -u || true)

  ALL=$(printf '%s\n%s\n%s' "$ENTITIES" "$PROPER" "$TECH" | grep -v '^$' | sort -u)

  # Write entity→file mappings to temp files
  echo "$ALL" | while IFS= read -r entity; do
    [ -z "$entity" ] && continue
    # Use entity as filename (sanitized)
    SAFE=$(echo "$entity" | sed 's/[^a-zA-Z0-9]/_/g')
    echo "$BASENAME" >> "$TMPDIR/$SAFE"
  done
done

# Find entities appearing in 2+ files
echo "=== CONNECTIONS (entities shared across articles) ==="
for ENTITY_FILE in "$TMPDIR"/*; do
  [ -f "$ENTITY_FILE" ] || continue
  COUNT=$(sort -u "$ENTITY_FILE" | wc -l | tr -d ' ')
  if [ "$COUNT" -ge 2 ]; then
    ENTITY_NAME=$(basename "$ENTITY_FILE" | sed 's/_/ /g')
    ARTICLES=$(sort -u "$ENTITY_FILE" | tr '\n' ', ' | sed 's/,$//')
    echo "  ${COUNT} articles → $ENTITY_NAME"
    echo "    Files: $ARTICLES"
  fi
done | sort -rn

# Build timeline
echo ""
echo "=== TIMELINE ==="
for FILE in "$KNOWLEDGE_DIR"/*.md; do
  [ -f "$FILE" ] || continue
  DATE=$(grep '^date:' "$FILE" | head -1 | sed 's/^date:[[:space:]]*//')
  TITLE=$(grep '^# ' "$FILE" | head -1 | sed 's/^# //')
  [ -n "$DATE" ] && [ -n "$TITLE" ] && echo "  $DATE  $TITLE"
done | sort

# Cleanup
rm -rf "$TMPDIR"
