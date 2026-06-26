#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$(cd "$PROJECT_DIR/.." && pwd)/dist"
VERSION=""
DISPLAY_NAME=""

usage() {
  echo "Usage: $(basename "$0") --version <semver> [--name <display-name>]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      VERSION="${2:-}"
      shift 2
      ;;
    --name)
      DISPLAY_NAME="${2:-}"
      shift 2
      ;;
    *)
      usage
      ;;
  esac
done

[[ -n "$VERSION" ]] || usage

python3 - <<PY
import json
from pathlib import Path

project = Path(r"$PROJECT_DIR")
version = "$VERSION"

for filename in ("package.json", "_meta.json"):
    path = project / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

skill_path = project / "SKILL.md"
text = skill_path.read_text(encoding="utf-8")
if "version: " in text:
    import re
    text = re.sub(
        r'(^\s*version:\s*")[^"]+(")',
        lambda m: f'{m.group(1)}{version}{m.group(2)}',
        text,
        flags=re.M,
    )
skill_path.write_text(text, encoding="utf-8")
PY

mkdir -p "$DIST_DIR"
ZIP_PATH="$DIST_DIR/zhouyi-benjing-oracle-$VERSION.zip"
rm -f "$ZIP_PATH"

cd "$(dirname "$PROJECT_DIR")"
zip -rq "$ZIP_PATH" "$(basename "$PROJECT_DIR")" -x "*/__pycache__/*" "*/.DS_Store"

echo "Built $ZIP_PATH"
echo ""
echo "ClawHub CLI publish command:"
if [[ -n "$DISPLAY_NAME" ]]; then
  echo "clawhub publish \"$PROJECT_DIR\" --version \"$VERSION\" --name \"$DISPLAY_NAME\""
else
  echo "clawhub publish \"$PROJECT_DIR\" --version \"$VERSION\""
fi
