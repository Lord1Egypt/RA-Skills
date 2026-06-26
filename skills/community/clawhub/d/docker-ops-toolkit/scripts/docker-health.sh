#!/usr/bin/env bash
# docker-health.sh — Quick health check for running containers
# Usage: docker-health.sh [container-name-or-id]  (omit to check all)

set -euo pipefail

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: $0 [container-name-or-id]"
  echo "  (omit to check all running containers)"
  exit 0
fi

if [ $# -ge 1 ]; then
  TARGET="$1"
  echo "=== Health check: $TARGET ==="
  STATE=$(docker inspect --format='{{.State.Status}}' "$TARGET" 2>/dev/null || echo "NOT-FOUND")
  HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}N/A{{end}}' "$TARGET" 2>/dev/null)
  RESTARTS=$(docker inspect --format='{{.RestartCount}}' "$TARGET" 2>/dev/null)
  PORTS=$(docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}}{{ $p }} → {{range $conf}}{{.HostIp}}:{{.HostPort}} {{end}}{{end}}' "$TARGET" 2>/dev/null)

  echo "  Status:   $STATE"
  echo "  Health:   $HEALTH"
  echo "  Restarts: $RESTARTS"
  echo "  Ports:    ${PORTS:-none published}"
  echo ""
  echo "=== Recent logs (last 20 lines) ==="
  docker logs --tail 20 "$TARGET" 2>&1 || echo "  (no logs)"
else
  echo "=== All Running Containers ==="
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | head -1
  docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | tail -n +2 | \
    while IFS=$'\t' read -r name status ports; do
      health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}—{{end}}' "$name" 2>/dev/null)
      printf "  %-25s %-25s %-15s %s\n" "$name" "$status" "[health: $health]" "$ports"
    done
fi
