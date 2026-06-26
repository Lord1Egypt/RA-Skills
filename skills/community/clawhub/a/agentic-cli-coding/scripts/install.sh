#!/usr/bin/env bash
# install.sh — Optional deployment helper.
#
# Creates an `oce` wrapper on PATH that invokes bash <skill>/scripts/oce.sh.
# This is purely a convenience — the skill works fine when invoked directly
# as `bash scripts/oce.sh <command>`.

set -euo pipefail

SCRIPT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd -P "$SCRIPT_DIR/.." && pwd)"

DEFAULT_BIN="$HOME/.local/bin"
INSTALL_BIN="${1:-$DEFAULT_BIN}"

mkdir -p "$INSTALL_BIN"

WRAPPER="$INSTALL_BIN/oce"
cat > "$WRAPPER" <<EOF
#!/usr/bin/env bash
exec bash "$SKILL_ROOT/scripts/oce.sh" "\$@"
EOF
chmod +x "$WRAPPER"

# Make sure node_modules are present (skill ships with them; this is a safety net)
if [ ! -d "$SKILL_ROOT/node_modules" ] && [ -f "$SKILL_ROOT/package.json" ]; then
  if command -v npm >/dev/null; then
    (cd "$SKILL_ROOT" && npm install --omit=dev --silent) || \
      echo "WARNING: npm install failed — AST features may not work"
  fi
fi

echo "✓ Wrapper installed at $WRAPPER"
echo "  → invokes bash $SKILL_ROOT/scripts/oce.sh"
echo
if echo ":$PATH:" | grep -q ":$INSTALL_BIN:"; then
  echo "✓ $INSTALL_BIN is on PATH — try: oce doctor"
else
  echo "  Add $INSTALL_BIN to PATH:"
  echo "    export PATH=\"$INSTALL_BIN:\$PATH\""
  echo "  Then: oce doctor"
fi
