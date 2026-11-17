#!/usr/bin/env bash
# audit_scan.sh — automated first-pass scan for a Flutter project.
# Usage: bash audit_scan.sh <path-to-flutter-project-root>
#
# Runs the mechanical checks (analyzer, formatter, outdated deps, grep-based
# anti-pattern scans) and prints a plain-text report. This is meant to be the
# FIRST pass of an audit — read references/audit-checklist.md and the other
# reference files for the human-judgment checks this script can't do.

set -uo pipefail

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR" || { echo "Cannot cd into $PROJECT_DIR"; exit 1; }

if [ ! -f "pubspec.yaml" ]; then
  echo "No pubspec.yaml found in $PROJECT_DIR — is this a Flutter project root?"
  exit 1
fi

hr() { printf '%s\n' "------------------------------------------------------------"; }

echo "FLUTTER AUDIT SCAN — $(date)"
echo "Project: $(pwd)"
hr

echo "## Flutter/Dart versions"
flutter --version 2>/dev/null || echo "flutter command not found on PATH"
hr

echo "## flutter analyze"
flutter analyze 2>&1 || true
hr

echo "## dart format check (files needing formatting)"
dart format --output=none --set-exit-if-changed . 2>&1 || true
hr

echo "## Outdated dependencies"
flutter pub outdated 2>&1 || true
hr

echo "## Anti-pattern scan (grep-based, may have false positives — verify each hit)"

echo ""
echo "--- print() statements (should be a real logger, or removed) ---"
grep -rn --include="*.dart" -E '\bprint\(' lib/ 2>/dev/null | grep -v '// ignore' || echo "(none found)"

echo ""
echo "--- Bare/empty catch blocks (silent failure risk) ---"
grep -rn --include="*.dart" -E 'catch\s*\([^)]*\)\s*\{\s*\}' lib/ 2>/dev/null || echo "(none found)"

echo ""
echo "--- Force-unwrap usage '!' worth double-checking (sample, high false-positive rate) ---"
grep -rcn --include="*.dart" -E '[a-zA-Z0-9_\]\)]\!(\.|;|,|\)|\s)' lib/ 2>/dev/null | awk -F: '$2>0' | sort -t: -k2 -n -r | head -20 || echo "(none found)"

echo ""
echo "--- Hardcoded http:// (non-HTTPS) endpoints ---"
grep -rn --include="*.dart" -E "http://" lib/ 2>/dev/null | grep -v "localhost\|127.0.0.1" || echo "(none found)"

echo ""
echo "--- Potential hardcoded secrets/keys ---"
grep -rniE --include="*.dart" '(api[_-]?key|secret|token|password)\s*=\s*['"'"'"][A-Za-z0-9_\-]{12,}['"'"'"]' lib/ 2>/dev/null || echo "(none found)"

echo ""
echo "--- TODO / FIXME density ---"
todo_count=$(grep -rn --include="*.dart" -E 'TODO|FIXME' lib/ 2>/dev/null | wc -l)
echo "$todo_count TODO/FIXME markers found in lib/"

echo ""
echo "--- Files over 400 lines (potential god-files) ---"
find lib -name "*.dart" -exec wc -l {} \; 2>/dev/null | awk '$1>400 {print}' | sort -rn || echo "(none found)"

echo ""
echo "--- ListView with eager children (check manually — may be a short/fixed list, which is fine) ---"
grep -rn --include="*.dart" -E 'ListView\(' lib/ 2>/dev/null | grep -v 'ListView.builder\|ListView.separated' || echo "(none found)"

echo ""
echo "--- StatefulWidget files: quick dispose() presence check ---"
for f in $(grep -rl --include="*.dart" 'extends State<' lib/ 2>/dev/null); do
  if grep -q 'Controller\|StreamSubscription\|AnimationController' "$f" && ! grep -q 'void dispose' "$f"; then
    echo "POSSIBLE MISSING dispose(): $f"
  fi
done

echo ""
echo "--- SharedPreferences usage (verify nothing sensitive is stored here — see references/security.md) ---"
grep -rln --include="*.dart" 'SharedPreferences' lib/ 2>/dev/null || echo "(none found)"

hr
echo "## Test coverage presence"
if [ -d "test" ]; then
  test_files=$(find test -name "*_test.dart" | wc -l)
  echo "$test_files test file(s) found in test/"
else
  echo "No test/ directory found."
fi
hr

echo "Scan complete. Cross-reference findings above against:"
echo "  references/audit-checklist.md   (full severity-tagged checklist)"
echo "  references/architecture.md, state-management.md, performance.md,"
echo "  security.md, code-style.md, testing.md, ux-quality.md, release-checklist.md"
echo "Remember: grep-based hits need human verification before being reported as findings — this script surfaces candidates, it doesn't conclude."
