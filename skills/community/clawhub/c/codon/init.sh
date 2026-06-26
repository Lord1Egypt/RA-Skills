#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
# Walk up to workspace root: skills/codon/ -> skills/ -> workspace/
WORKSPACE_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
MEMORY_ROOT="$WORKSPACE_ROOT/MEMORY"

# Permission check
if [ ! -w "$WORKSPACE_ROOT" ]; then
  echo "ERROR: Cannot write to workspace at $WORKSPACE_ROOT" >&2
  exit 1
fi

# Category definitions: dirname -> ID prefix
declare -A PREFIXES=(
  ["10-19-People"]="10"
  ["20-29-Projects"]="20"
  ["30-39-Resources"]="30"
  ["40-49-Work"]="40"
)

declare -A DESCRIPTIONS=(
  ["10-19-People"]="Contacts, clients, team members"
  ["20-29-Projects"]="Active and past projects"
  ["30-39-Resources"]="Tools, docs, links, references"
  ["40-49-Work"]="Tasks, decisions, meeting notes"
)

mkdir -p "$MEMORY_ROOT"

# Process in order
for dir in "10-19-People" "20-29-Projects" "30-39-Resources" "40-49-Work"; do
  mkdir -p "$MEMORY_ROOT/$dir"

  PREFIX="${PREFIXES[$dir]}"
  INDEX_FILE="$MEMORY_ROOT/$dir/${PREFIX}.00-index.md"

  if [ ! -f "$INDEX_FILE" ]; then
    cat > "$INDEX_FILE" <<EOF
# ${dir} — Index
${DESCRIPTIONS[$dir]}

## IDs assigned

(none yet — entries appear here as XX.YY Description)

## How to add an entry

1. Pick the next available ID (e.g. ${PREFIX}.01, ${PREFIX}.02...)
2. Create \`MEMORY/${dir}/${PREFIX}.YY-short-description.md\`
3. Add the ID + one-line description to this index
EOF
    echo "  created  $dir/${PREFIX}.00-index.md"
  else
    echo "  exists   $dir/${PREFIX}.00-index.md (skipped)"
  fi
done

echo ""
echo "Codon initialized at $MEMORY_ROOT"
echo "Taxonomy: 10-19 People · 20-29 Projects · 30-39 Resources · 40-49 Work"
