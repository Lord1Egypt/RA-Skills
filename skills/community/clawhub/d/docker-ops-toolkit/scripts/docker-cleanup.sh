#!/usr/bin/env bash
# docker-cleanup.sh — Clean up unused Docker resources
# Usage: docker-cleanup.sh [--aggressive] [--dry-run]

set -euo pipefail

DRY_RUN=false
AGGRESSIVE=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --aggressive) AGGRESSIVE=true ;;
    --help)
      echo "Usage: $0 [--aggressive] [--dry-run]"
      echo "  --aggressive  Also remove unused volumes and build cache"
      echo "  --dry-run     Show what would be removed (docker system df)"
      exit 0
      ;;
  esac
done

echo "=== Docker Cleanup ==="
echo "Mode: $($AGGRESSIVE && echo 'aggressive' || echo 'standard')"
echo ""

do_cmd() {
  local desc="$1"; shift
  echo "→ $desc"
  if $DRY_RUN; then
    echo "  (dry run) $*"
  else
    eval "$@" || echo "  ⚠️  command returned non-zero (ignored)"
  fi
}

do_cmd "Removing stopped containers..." "docker container prune -f"
do_cmd "Removing dangling images..." "docker image prune -f"
do_cmd "Removing unused networks..." "docker network prune -f"

if $AGGRESSIVE; then
  do_cmd "Removing unused volumes (⚠️ risk of data loss)..." "docker volume prune -f"
  do_cmd "Clearing build cache..." "docker builder prune --all -f"
fi

echo ""
echo "=== Disk Usage ==="
docker system df
