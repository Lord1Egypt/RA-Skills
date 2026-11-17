#!/bin/sh
# PostToolUse(Write|Edit) — right after a decision record is edited, check its cascade memo and schema on the spot.
# Installed by the docs-gov skill's init, registered in the project's .claude/settings.json.
#
# Why Post and not Pre: the file is already written, so blocking is pointless; what matters is "knowing right away".
#
# The failure it guards against: a large project learned the same lesson three times —
#   every time, it took the user asking "did this land in the plan?" to discover the memo routes were never written into the target files.
#   Another repo caught it again while adding cascade discipline: ADR-0006's body said "folded into PLAN-05 Wave 3",
#   and PLAN-05 never mentioned it — a one-way declaration.
# Every one of these is visible the moment you run the check; nobody ever ran it at that moment.

set -u

input=$(cat)
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -z "$path" ] && exit 0
case "$path" in *.md) ;; *) exit 0 ;; esac

ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
[ -n "$ROOT" ] || exit 0
CFG="$ROOT/.doc-governance.json"
CHECKER="$ROOT/scripts/governance.py"
[ -f "$CFG" ] && [ -f "$CHECKER" ] || exit 0

ADR_DIR=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['adr_dir'])" "$CFG" 2>/dev/null) || exit 0
case "$path" in *"/$ADR_DIR/"*|"$ADR_DIR/"*) ;; *) exit 0 ;; esac

out=$(python3 "$CHECKER" check --root "$ROOT" cascade refs 2>&1) && exit 0

{
  echo "⚠️ The decision record you just edited has problems — a cascade memo item hasn't landed, or the frontmatter schema fails:"
  echo ""
  printf '%s\n' "$out" | grep -v "scanned [0-9]* files\{0,1\}$"
  echo ""
  echo "Every ✅ item in a cascade memo requires ADR-NNNN to actually appear in the target file."
  echo "The same lesson was really learned three times, and each time it took someone asking to find the routes never landed."
} >&2
exit 2
