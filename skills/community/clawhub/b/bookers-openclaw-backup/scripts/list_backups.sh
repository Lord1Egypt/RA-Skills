#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.env"
DEFAULT_OUT_DIR="$HOME/backups/openclaw-snapshots"
DEFAULT_PREFIX="occt7pkbak"

CONFIG_OUT_DIR=""
CONFIG_PREFIX=""
if [[ -f "$CONFIG_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      OPENCLAW_SNAPSHOT_DIR) CONFIG_OUT_DIR="${value//\$HOME/$HOME}" ;;
      OPENCLAW_SNAPSHOT_PREFIX) CONFIG_PREFIX="$value" ;;
    esac
  done < "$CONFIG_FILE"
fi

OUT_DIR="${CONFIG_OUT_DIR:-${OPENCLAW_SNAPSHOT_DIR:-$DEFAULT_OUT_DIR}}"
PREFIX="${CONFIG_PREFIX:-${OPENCLAW_SNAPSHOT_PREFIX:-$DEFAULT_PREFIX}}"

usage() {
  cat <<'EOF'
Usage: list_backups.sh [--out-dir DIR] [--prefix NAME]
EOF
}

require_value() {
  local option="$1"
  local value="${2-}"
  if [[ -z "$value" ]]; then
    echo "Missing value for $option" >&2
    usage >&2
    exit 1
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out-dir|--backup-dir)
      require_value "$1" "${2-}"
      OUT_DIR="$2"
      shift 2
      ;;
    --prefix)
      require_value "$1" "${2-}"
      PREFIX="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

mapfile -t bundles < <(find "$OUT_DIR" -maxdepth 1 -type f -name "${PREFIX}-*.tar.gz" | sort -r)
if (( ${#bundles[@]} == 0 )); then
  echo "No backup bundles found in: $OUT_DIR" >&2
  exit 1
fi

printf 'Backup bundles in %s\n\n' "$OUT_DIR"
for i in "${!bundles[@]}"; do
  file="${bundles[$i]}"
  mtime="$(date -d "@$(stat -c %Y "$file")" '+%Y-%m-%d %H:%M:%S')"
  size="$(du -h "$file" | cut -f1)"
  printf '%2d) %s  [%s, %s]\n' "$((i + 1))" "$(basename "$file")" "$mtime" "$size"
done
