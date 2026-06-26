#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(pwd)"
START_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-dir)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --project-dir requires a value" >&2
        exit 1
      fi
      PROJECT_DIR="$2"
      shift 2
      ;;
    *)
      START_ARGS+=("$1")
      shift
      ;;
  esac
done

"${SCRIPT_DIR}/install_project_tunnel.sh" "${PROJECT_DIR}"
cd "${PROJECT_DIR}"
exec sh ./project-tunnel.sh start "${START_ARGS[@]}"
