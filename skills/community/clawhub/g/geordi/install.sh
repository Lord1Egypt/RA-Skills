#!/usr/bin/env bash
set -euo pipefail

REPO_TARBALL_URL="${GEORDI_TARBALL_URL:-https://codeload.github.com/h-mascot/Enterprise-Crew-skills/tar.gz/refs/tags/v1.1.0}"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${GEORDI_HOME:-$HOME/.geordi}"
BIN_DIR="${GEORDI_BIN_DIR:-$HOME/.local/bin}"
TEMP_DIR=""

cleanup() {
  if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

# When run as `bash <(curl ...)`, BASH_SOURCE points at /dev/fd instead of a
# checked-out bundle. Fetch the public repository tarball and install from it.
if [ ! -f "$SOURCE_DIR/SKILL.md" ] || [ ! -d "$SOURCE_DIR/scripts" ]; then
  command -v curl >/dev/null 2>&1 || { echo "ERROR: curl is required for remote install" >&2; exit 1; }
  command -v tar >/dev/null 2>&1 || { echo "ERROR: tar is required for remote install" >&2; exit 1; }
  TEMP_DIR="$(mktemp -d)"
  curl -fsSL "$REPO_TARBALL_URL" | tar -xz -C "$TEMP_DIR"
  SOURCE_DIR="$(find "$TEMP_DIR" -type d -path '*/geordi' | head -1)"
  [ -n "$SOURCE_DIR" ] && [ -f "$SOURCE_DIR/SKILL.md" ] || { echo "ERROR: could not locate geordi bundle in repository archive" >&2; exit 1; }
fi

mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# Copy bundle without VCS noise.
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude '.git' "$SOURCE_DIR/" "$INSTALL_DIR/"
else
  rm -rf "$INSTALL_DIR.tmp"
  mkdir -p "$INSTALL_DIR.tmp"
  cp -R "$SOURCE_DIR/." "$INSTALL_DIR.tmp/"
  rm -rf "$INSTALL_DIR"
  mv "$INSTALL_DIR.tmp" "$INSTALL_DIR"
fi

cat > "$BIN_DIR/geordi" <<WRAPPER
#!/usr/bin/env bash
set -euo pipefail
GEORDI_HOME="\${GEORDI_HOME:-$INSTALL_DIR}"
exec "\$GEORDI_HOME/scripts/geordi" "\$@"
WRAPPER
chmod +x "$BIN_DIR/geordi" "$INSTALL_DIR/scripts/geordi"

echo "Geordi installed to $INSTALL_DIR"
echo "Command: $BIN_DIR/geordi"
if ! command -v geordi >/dev/null 2>&1; then
  echo "Note: $BIN_DIR is not on PATH for this shell. Add: export PATH=\"$BIN_DIR:\$PATH\""
fi
echo "Verify: $BIN_DIR/geordi --version && $BIN_DIR/geordi doctor"
