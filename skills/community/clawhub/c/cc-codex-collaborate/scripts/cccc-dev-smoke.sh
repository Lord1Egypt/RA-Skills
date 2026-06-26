#!/usr/bin/env bash
# CCCC Dev-Smoke — developer self-test for skill installation.
# Runs validations without modifying user files (uses /tmp for any needed writes).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

ROOT="$(cccc_repo_root)"
cd "$ROOT"

SKILL_DIR="$(cccc_skill_dir)"
TEMPLATE_DIR="$SKILL_DIR/templates"
PASS=0
FAIL=0

check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "  PASS  $label"
    PASS=$((PASS + 1))
  else
    echo "  FAIL  $label"
    FAIL=$((FAIL + 1))
  fi
}

echo "CCCC Dev-Smoke"
echo ""

# ── JSON validation ──
echo "JSON validation:"
for f in "$TEMPLATE_DIR"/cccc/*.template.json; do
  [[ -f "$f" ]] || continue
  check "$(basename "$f")" python3 -c "import json; json.load(open('$f'))"
done
echo ""

# ── Shell syntax ──
echo "Shell syntax (bash -n):"
for f in "$SCRIPT_DIR"/*.sh "$SKILL_DIR"/hooks/*.sh; do
  [[ -f "$f" ]] || continue
  check "$(basename "$f")" bash -n "$f"
done
echo ""

# ── Python compile ──
echo "Python compile:"
for f in "$SCRIPT_DIR"/*.py; do
  [[ -f "$f" ]] || continue
  check "$(basename "$f")" python3 -m py_compile "$f"
done
echo ""

# ── Core files exist ──
echo "Core files:"
check "VERSION exists" test -f "$SKILL_DIR/VERSION"
check "SKILL.md exists" test -f "$SKILL_DIR/SKILL.md"
check "scripts/ exists" test -d "$SKILL_DIR/scripts"
check "templates/ exists" test -d "$SKILL_DIR/templates"
check "hooks/ exists" test -d "$SKILL_DIR/hooks"
echo ""

# ── Script executability ──
echo "Script executability:"
for f in "$SCRIPT_DIR"/*.sh "$SKILL_DIR"/hooks/*.sh; do
  [[ -f "$f" ]] || continue
  check "$(basename "$f") executable" test -x "$f"
done
echo ""

# ── Workspace files (if workspace exists) ──
if [[ -d "docs/cccc" ]]; then
  echo "Workspace files:"
  check "config.json valid" python3 -c "import json; json.load(open('docs/cccc/config.json'))"
  check "state.json valid" python3 -c "import json; json.load(open('docs/cccc/state.json'))"
  echo ""

  # ── Doctor runs ──
  echo "Doctor script:"
  check "doctor.py runs" python3 "$SCRIPT_DIR/cccc-doctor.py"
  echo ""

  # ── Gates runs ──
  echo "Gates script:"
  check "gates.py runs" python3 "$SCRIPT_DIR/cccc-gates.py"
  echo ""

  # ── Context rebuild (syntax-only to avoid modifying user files) ──
  echo "Context rebuild:"
  check "build-context.sh syntax" bash -n "$SCRIPT_DIR/cccc-build-context.sh"
  echo ""
fi

# ── Summary ──
echo "════════════════════════════════════════════════════════════"
echo "Summary: $PASS PASS, $FAIL FAIL"
echo "════════════════════════════════════════════════════════════"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
exit 0
