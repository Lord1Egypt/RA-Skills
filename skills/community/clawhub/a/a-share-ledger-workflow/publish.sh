#!/usr/bin/env bash
# Build the public bundle from committed files and publish next patch version.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI is required (npm i -g clawhub)" >&2
  exit 1
fi
if [ -n "$(git status --porcelain)" ]; then
  echo "Commit all intended changes before publishing; working tree is not clean." >&2
  exit 1
fi

slug=a-share-ledger-workflow
latest=$(clawhub inspect "$slug" --json | python3 -c \
  'import json,sys; d=json.load(sys.stdin); v=d.get("latestVersion") or {}; print(v.get("version", "0.0.0") if isinstance(v, dict) else v)')
version=$(python3 - "$latest" <<'PY'
import sys
major, minor, patch = map(int, sys.argv[1].split("."))
print(f"{major}.{minor}.{patch + 1}")
PY
)
sha=$(git rev-parse HEAD)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

git archive HEAD | tar -x -C "$tmp"
cp SKILL.md "$tmp/SKILL.md"
python3 - "$tmp/SKILL.md" "$version" <<'PY'
import pathlib, re, sys
p = pathlib.Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
s, n = re.subn(r"(?m)^version: [^\n]+$", f"version: {sys.argv[2]}", s, count=1)
if n != 1:
    raise SystemExit("SKILL.md must define exactly one frontmatter version")
p.write_text(s, encoding="utf-8")
PY

echo "Publishing $slug v$version from $sha"
clawhub skill publish "$tmp" \
  --slug "$slug" \
  --name "A股台账工作流 · 选股跟踪·持仓管理·财报核验·复盘（8步投研流程）" \
  --version "$version" \
  --categories finance \
  --topics "a股,股票,选股,持仓,台账" \
  --source-repo yangclaw2026-png/a-share-ledger-workflow \
  --source-commit "$sha" \
  --changelog "See GitHub commit $sha"
