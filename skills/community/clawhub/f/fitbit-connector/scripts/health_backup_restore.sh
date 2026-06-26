#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASSETS="$ROOT/assets"
BACKUP_ROOT="$ROOT/backups/manual"

usage() {
  cat <<EOF
Usage:
  $(basename "$0") backup
  $(basename "$0") restore <backup_dir> [--dry-run]

Creates/restores:
  - fitbit_metrics.sqlite3
  - health_unified.sqlite3
  - fitbit_tokens.json
EOF
}

backup() {
  ts="$(date -u +%Y%m%dT%H%M%SZ)"
  dir="$BACKUP_ROOT/$ts"
  mkdir -p "$dir"

  cp -a "$ASSETS/fitbit_metrics.sqlite3" "$dir/fitbit_metrics.sqlite3"
  cp -a "$ASSETS/health_unified.sqlite3" "$dir/health_unified.sqlite3"
  cp -a "$ASSETS/fitbit_tokens.json" "$dir/fitbit_tokens.json"

  (cd "$dir" && shasum -a 256 fitbit_metrics.sqlite3 health_unified.sqlite3 fitbit_tokens.json > SHA256SUMS)
  echo "$dir"
}

restore() {
  local dir="${1:-}"
  local dry="${2:-}"
  [[ -n "$dir" ]] || { usage; exit 1; }

  for f in fitbit_metrics.sqlite3 health_unified.sqlite3 fitbit_tokens.json SHA256SUMS; do
    [[ -f "$dir/$f" ]] || { echo "missing: $dir/$f" >&2; exit 1; }
  done

  (cd "$dir" && shasum -a 256 -c SHA256SUMS)

  if [[ "$dry" == "--dry-run" ]]; then
    echo "restore dry-run ok (checksums verified, no files copied)"
    return 0
  fi

  cp -a "$dir/fitbit_metrics.sqlite3" "$ASSETS/fitbit_metrics.sqlite3"
  cp -a "$dir/health_unified.sqlite3" "$ASSETS/health_unified.sqlite3"
  cp -a "$dir/fitbit_tokens.json" "$ASSETS/fitbit_tokens.json"
  echo "restore completed from $dir"
}

cmd="${1:-}"
case "$cmd" in
  backup)
    backup
    ;;
  restore)
    shift
    restore "$@"
    ;;
  *)
    usage
    exit 1
    ;;
esac
