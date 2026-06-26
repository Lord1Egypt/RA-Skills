#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT_DIR/dist}"
VERSION="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$ROOT_DIR/skill.json")"
PACKAGE_BASENAME="clawswap-v${VERSION}.skill"
PACKAGE_PATH="$OUT_DIR/$PACKAGE_BASENAME"
STAGE_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$STAGE_DIR"
}
trap cleanup EXIT

mkdir -p "$OUT_DIR"

# Run prepublish checks first
"$ROOT_DIR/tools/prepublish_check.sh"

# Whitelist copy: include only release-relevant files
mkdir -p "$STAGE_DIR/clawswap"
cp "$ROOT_DIR/SKILL.md" "$STAGE_DIR/clawswap/"
cp "$ROOT_DIR/skill.json" "$STAGE_DIR/clawswap/"
cp "$ROOT_DIR/runtime_client.py" "$STAGE_DIR/clawswap/"
cp "$ROOT_DIR/.env.example" "$STAGE_DIR/clawswap/"

cp -R "$ROOT_DIR/strategies" "$STAGE_DIR/clawswap/"
cp -R "$ROOT_DIR/tools" "$STAGE_DIR/clawswap/"
cp -R "$ROOT_DIR/examples" "$STAGE_DIR/clawswap/"

# Remove non-release files from staged tree
find "$STAGE_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$STAGE_DIR" -type f -name '*.pyc' -delete
find "$STAGE_DIR" -type f \( -name '.runtime_token' -o -name '.clawswap_api_key' -o -name '.env' \) -delete
rm -rf "$STAGE_DIR/clawswap/tests"

# Avoid nesting package scripts inside shipped tools
rm -f "$STAGE_DIR/clawswap/tools/package_skill.sh" "$STAGE_DIR/clawswap/tools/prepublish_check.sh"

(
  cd "$STAGE_DIR"
  zip -q -r "$PACKAGE_PATH" clawswap
)

echo "✅ Packaged: $PACKAGE_PATH"
echo "📦 Contents:"
unzip -l "$PACKAGE_PATH"
