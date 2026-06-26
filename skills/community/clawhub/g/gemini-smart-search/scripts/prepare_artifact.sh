#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="${1:-$SKILL_DIR/.artifact-out}"
STAGE_DIR="$OUT_DIR/gemini-smart-search"

INCLUDE_FILES=(
  "SKILL.md"
  "README.md"
  "scripts/gemini_smart_search.py"
  "scripts/gemini_smart_search.sh"
  "scripts/smoke_test.sh"
  "references/config.md"
  "references/release-checklist.md"
  "assets/example-output.json"
)

info() { printf 'INFO: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"

for rel in "${INCLUDE_FILES[@]}"; do
  src="$SKILL_DIR/$rel"
  dst="$STAGE_DIR/$rel"
  [ -f "$src" ] || fail "missing include file: $rel"
  mkdir -p "$(dirname -- "$dst")"
  cp "$src" "$dst"
done

# Validate excluded repo/dev files are not present in the staged artifact.
EXCLUDED_PATHS=(
  ".git"
  ".env.local"
  ".gitignore"
  "LICENSE"
  "references/development-goals-v0.1.1.md"
  "references/agent-qa-cases.md"
  "references/escalation-design.md"
  "references/model-id-recon.md"
  "references/qa-results-2026-03-12.md"
  "references/qa-test-plan.md"
  "references/release-notes-v0.1.0.md"
  "references/release-notes-v0.1.1.md"
  "references/vnext-review-2026-03-12.md"
)

for rel in "${EXCLUDED_PATHS[@]}"; do
  if [ -e "$STAGE_DIR/$rel" ]; then
    fail "excluded path leaked into artifact: $rel"
  fi
done

info "Prepared staged artifact at: $STAGE_DIR"
info "Included files:"
for rel in "${INCLUDE_FILES[@]}"; do
  printf ' - %s\n' "$rel"
done
