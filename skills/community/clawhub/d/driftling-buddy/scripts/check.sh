#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f SKILL.md ]]; then
  echo "missing SKILL.md"
  exit 1
fi

if ! grep -q '^name: buddy_mode$' SKILL.md; then
  echo "expected skill name buddy_mode"
  exit 1
fi

if ! grep -q '^metadata: {"openclaw":' SKILL.md; then
  echo "metadata.openclaw must be single-line JSON in frontmatter"
  exit 1
fi

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "python3 or python is required"
  exit 1
fi

"$PYTHON_BIN" scripts/buddy.py render \
  --phase implementation \
  --mood focused \
  --task "package buddy skill for release" \
  --next "run final smoke checks" \
  --risk "published docs drift from SKILL.md" \
  --theme general \
  --name "Mori" \
  --side-quest "It is rearranging three commas." >/dev/null

"$PYTHON_BIN" scripts/buddy.py hatch --theme academic --lang en >/dev/null
"$PYTHON_BIN" scripts/buddy.py sidequest --theme debug --lang zh >/dev/null
"$PYTHON_BIN" scripts/buddy.py /pool --theme coffee >/dev/null
"$PYTHON_BIN" scripts/buddy.py /buddy --theme general --lang en --name Mori >/dev/null
"$PYTHON_BIN" scripts/buddy.py /summon --theme coffee --lang zh --name Mori --main >/dev/null
"$PYTHON_BIN" scripts/buddy.py /unlock --theme tea --lang zh --name Nilo --reason "你刚设置了一个茶歇提醒" >/dev/null
"$PYTHON_BIN" scripts/buddy.py /collection --lang zh >/dev/null
"$PYTHON_BIN" scripts/buddy.py /buddy-help --lang zh >/dev/null

echo "buddy skill checks passed"
