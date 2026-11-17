#!/bin/sh
# PreToolUse(Write) — before a new plan document is created, run the documentation governance checks first.
# Installed by the docs-gov skill's init, registered in the project's .claude/settings.json.
#
# Why this moment needs a device instead of a line saying "remember to run it first":
#   Neither CI nor pre-commit can catch "a compliant new plan written on top of an outdated spec" —
#   the new plan itself has nothing wrong with it, so gates just let it through. Only a reverse audit before starting can catch it.
#   And a reverse audit written in CLAUDE.md is only a sticky note: nobody flips back to it at the moment they start.
#
# Same lesson elsewhere: the comments of a credential-printing guard hook record it —
#   after the first credential leak, the fix was a rule hardcoded to "API responses"; the second leak came from reading a local file,
#   the rule never fired, and another rotation was forced. Only mechanical blocking by the shape of the action worked.
#   "A rule written down" versus "a device bound to the action" — that one incident is the whole difference.
#
# Only blocks creation (the file doesn't exist yet). Editing an existing plan is normal progress and isn't blocked.
# Escape hatch: comment this hook out of .claude/settings.json, or tell the session to skip it.

set -u

input=$(cat)
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[ -z "$path" ] && exit 0

case "$(basename "$path")" in PLAN-*.md|TASK-*.md) ;; *) exit 0 ;; esac
[ -e "$path" ] && exit 0          # already exists = editing, not starting

ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
[ -n "$ROOT" ] || exit 0
CFG="$ROOT/.doc-governance.json"
CHECKER="$ROOT/scripts/governance.py"
[ -f "$CFG" ] && [ -f "$CHECKER" ] || exit 0

PLAN_DIR=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['plan_dir'])" "$CFG" 2>/dev/null) || exit 0
case "$path" in *"/$PLAN_DIR/"*|"$PLAN_DIR/"*) ;; *) exit 0 ;; esac

if out=$(python3 "$CHECKER" check --root "$ROOT" 2>&1); then
  # Don't let green pass silently either: the machine can't judge the semantic part of CP-1, but it can make sure the three questions show up at the right moment.
  # Trigger line: a spec untouched for a long time isn't necessarily outdated, but it's the most likely setup for "a new plan written on an outdated spec".
  # Don't block, just put the fact in front of you — there's no evidence for adding a rule, and there is evidence this is when to take a second look.
  SPEC_DIR=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['docs_root'])" "$CFG" 2>/dev/null || echo docs)
  STALE=$(find "$ROOT/$SPEC_DIR" -name "SPEC*.md" -o -name "spec" -type d 2>/dev/null | head -1)
  if [ -n "$STALE" ]; then
    DAYS=$(python3 - "$ROOT" "$SPEC_DIR" <<'PYEOF' 2>/dev/null || echo ""
import subprocess, sys, datetime
root, docs = sys.argv[1], sys.argv[2]
out = subprocess.run(["git", "-C", root, "log", "-1", "--format=%cI", "--", f"{docs}/SPEC.md", f"{docs}/spec"],
                     capture_output=True, text=True)
line = out.stdout.strip()
if line:
    d = datetime.datetime.fromisoformat(line).date()
    print((datetime.date.today() - d).days)
PYEOF
)
    if [ -n "$DAYS" ] && [ "$DAYS" -gt 45 ] 2>/dev/null; then
      echo "⏳ Heads-up: the spec hasn't been touched in $DAYS days. If this plan depends on it, confirm it still holds first."
    fi
  fi
  echo "🔍 Documentation governance is green. Before writing this plan, the three CP-1 reverse-audit questions (a machine can't answer these; you have to):"
  echo "   1. Does the spec / PRD this plan relies on still hold? — go read it, don't go from memory"
  echo "   2. Has every §X.Y reference in the plan been verified, one by one?"
  echo "   3. Are the decisions (ADRs) it depends on still accepted, and has any been superseded?"
  exit 0
fi

{
  echo "⛔ Documentation governance checks are red — don't write the new plan yet."
  echo ""
  printf '%s\n' "$out" | grep -v "scanned [0-9]* files\{0,1\}$"
  echo ""
  echo "Why block at this moment: CI can't catch \"a compliant new plan written on top of an outdated spec\" —"
  echo "the new plan itself has nothing wrong with it; only a reverse audit before starting can catch it."
  echo "Fix the items above first; for anything that genuinely needs an exemption, state the reason in pending_exclude in .doc-governance.json."
} >&2
exit 2
