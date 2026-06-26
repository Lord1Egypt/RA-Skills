#!/usr/bin/env bash
# Build the unified claw3d skill from modules.
# Run from claw3d-skill/ directory.
#
# Usage:
#   ./scripts/build-skill.sh [--modules ai-forger,directory,slicing,printing]
#   CLAW3D_MODULES=ai-forger,printing ./scripts/build-skill.sh
#
# Default: all modules if CLAW3D_MODULES not set and no --modules.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAW3D_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$CLAW3D_ROOT/src"
OUT_FILE="$CLAW3D_ROOT/SKILL.md"

# Parse --modules
MODULES_ARG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --modules)
      MODULES_ARG="${2:-}"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Module selection: env > arg > default all
MODULES_STR="${CLAW3D_MODULES:-${MODULES_ARG:-ai-forger,directory,slicing,printing}}"
IFS=',' read -ra MODULES_ARR <<< "$MODULES_STR"

# Validate modules against manifest
MANIFEST="$CLAW3D_ROOT/manifest.json"
if [[ ! -f "$MANIFEST" ]]; then
  echo "Error: manifest.json not found at $MANIFEST" >&2
  exit 1
fi

# Build requires JSON for OpenClaw metadata
# Collect env vars from selected modules
REQUIRES_ENV=()
for mod in "${MODULES_ARR[@]}"; do
  mod="${mod// /}"
  [[ -z "$mod" ]] && continue
  # Extract requires_env from manifest (simple jq or grep)
  if command -v jq &>/dev/null; then
    envs=$(jq -r --arg m "$mod" '.modules[$m].requires_env[]? // empty' "$MANIFEST" 2>/dev/null || true)
    for e in $envs; do
      [[ -n "$e" ]] && REQUIRES_ENV+=("$e")
    done
  fi
done

# Deduplicate and build requires JSON
# Format: { "anyBins": ["claw3d"], "env": ["FAL_API_KEY", ...] }
REQUIRES_JSON='{ "anyBins": ["claw3d"]'
if [[ ${#REQUIRES_ENV[@]} -gt 0 ]]; then
  ENV_JSON=$(printf '%s\n' "${REQUIRES_ENV[@]}" | sort -u | sed 's/.*/"&"/' | paste -sd, -)
  REQUIRES_JSON="$REQUIRES_JSON, \"env\": [$ENV_JSON]"
fi
REQUIRES_JSON="$REQUIRES_JSON }"

# Build frontmatter
FRONTMATTER="$SRC_DIR/00-frontmatter.md"
if [[ ! -f "$FRONTMATTER" ]]; then
  echo "Error: 00-frontmatter.md not found" >&2
  exit 1
fi

# Create temp file for assembled skill
TMP_OUT=$(mktemp)
trap 'rm -f "$TMP_OUT"' EXIT

# 1. Frontmatter with requires injected
sed "s|{{REQUIRES_JSON}}|$REQUIRES_JSON|g" "$FRONTMATTER" > "$TMP_OUT"

# 2. Core (always included)
echo "" >> "$TMP_OUT"
cat "$SRC_DIR/01-core.md" >> "$TMP_OUT"

# 3. Intent analysis (always included)
if [[ -f "$SRC_DIR/06-intent.md" ]]; then
  echo "" >> "$TMP_OUT"
  echo "---" >> "$TMP_OUT"
  echo "" >> "$TMP_OUT"
  cat "$SRC_DIR/06-intent.md" >> "$TMP_OUT"
fi

# 4. Selected modules in order
MODULE_ORDER=(ai-forger directory slicing printing)
for mod in "${MODULE_ORDER[@]}"; do
  for sel in "${MODULES_ARR[@]}"; do
    sel="${sel// /}"
    [[ -z "$sel" ]] && continue
    if [[ "$sel" == "$mod" ]]; then
      mod_rel=$(jq -r --arg m "$mod" '.modules[$m].file // empty' "$MANIFEST" 2>/dev/null)
      mod_file="$CLAW3D_ROOT/$mod_rel"
      if [[ -n "$mod_rel" && -f "$mod_file" ]]; then
        echo "" >> "$TMP_OUT"
        echo "---" >> "$TMP_OUT"
        echo "" >> "$TMP_OUT"
        cat "$mod_file" >> "$TMP_OUT"
      fi
      break
    fi
  done
done

# Write output
mv "$TMP_OUT" "$OUT_FILE"
trap - EXIT

echo "Built $OUT_FILE with modules: ${MODULES_ARR[*]}"
