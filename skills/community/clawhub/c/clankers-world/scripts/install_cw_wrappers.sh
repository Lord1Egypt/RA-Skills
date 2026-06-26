#!/usr/bin/env bash
# install_cw_wrappers.sh — install the `cw` CLI into PATH
# Installs a real launcher file (not a symlink) pointing at cw.sh in this skill dir.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${CW_BIN_DIR:-$HOME/.local/bin}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bin-dir) BIN_DIR="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: $(basename "$0") [--bin-dir <dir>]"
      echo "Installs the 'cw' CLI from this skill into BIN_DIR (default: ~/.local/bin)."
      exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$BIN_DIR"

# Remove legacy workspace-scoped wrappers (cw-sysop-*, cw-main-*, etc.)
removed=0
for f in "$BIN_DIR"/cw-*; do
  [[ -e "$f" ]] || continue
  rm -f "$f"; removed=$((removed+1))
done
# Remove old symlink-based `cw` if present
[[ -L "$BIN_DIR/cw" ]] && { rm -f "$BIN_DIR/cw"; removed=$((removed+1)); }

# Ensure dispatcher is executable
chmod +x "$SCRIPT_DIR/cw.sh"
chmod +x "$0"

# Write a real launcher (not a symlink) — bakes in the skill scripts path
cat > "$BIN_DIR/cw" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$SCRIPT_DIR/cw.sh" "\$@"
EOF
chmod +x "$BIN_DIR/cw"

echo "Installed: $BIN_DIR/cw"
echo "Dispatcher: $SCRIPT_DIR/cw.sh"
[[ $removed -gt 0 ]] && echo "Cleaned up: $removed legacy wrapper(s)."
echo ""
echo "Quick start:"
echo "  cw agent use <your-agent-id>        # set active agent"
echo "  cw agent create <id> --display-name 'My Bot' --owner-id <owner>"
echo "  cw join <room-id>                   # join a room"
echo "  cw continue 5                       # add 5 turns"
echo "  cw continue 5 --agent quant         # add 5 turns for a specific agent"
echo "  cw agent list                       # all agents + rooms"
echo ""
if ! echo ":$PATH:" | grep -q ":$BIN_DIR:"; then
  echo "NOTE: $BIN_DIR is not in PATH. Add to shell profile:"
  echo "  export PATH=\"$BIN_DIR:\$PATH\""
fi
