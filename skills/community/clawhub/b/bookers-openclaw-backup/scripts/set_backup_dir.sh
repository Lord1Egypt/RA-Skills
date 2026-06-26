#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.env"
DEFAULT_PREFIX="occt7pkbak"
DEFAULT_KEEP="5"

usage() {
  cat <<'EOF'
Usage: set_backup_dir.sh /absolute/path
EOF
}

[[ $# -eq 1 ]] || { usage >&2; exit 1; }
NEW_DIR="$1"
[[ "$NEW_DIR" = /* ]] || { echo "Backup directory must be an absolute path" >&2; exit 1; }
mkdir -p "$NEW_DIR"
[[ -d "$NEW_DIR" ]] || { echo "Failed to create backup directory: $NEW_DIR" >&2; exit 1; }

prefix="$DEFAULT_PREFIX"
keep="$DEFAULT_KEEP"
if [[ -f "$CONFIG_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      OPENCLAW_SNAPSHOT_PREFIX) prefix="$value" ;;
      OPENCLAW_SNAPSHOT_KEEP) keep="$value" ;;
    esac
  done < "$CONFIG_FILE"
fi

cat > "$CONFIG_FILE" <<EOF
OPENCLAW_SNAPSHOT_DIR=$NEW_DIR
OPENCLAW_SNAPSHOT_PREFIX=$prefix
OPENCLAW_SNAPSHOT_KEEP=$keep
EOF

printf 'Backup directory updated to: %s\n' "$NEW_DIR"
