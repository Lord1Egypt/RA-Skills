#!/usr/bin/env bash
set -euo pipefail

# CLI version checker (stub).
#
# Intended usage:
# - Scheduled CI job (weekly)
# - Compare docs/cli-versions.yaml to upstream releases
# - Open an issue if a newer version is available
#
# NOTE: This script is a placeholder. Implement release checks per tool and
# wire it into CI once the process is finalized.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSIONS_FILE="${ROOT_DIR}/docs/cli-versions.yaml"

if [[ ! -f "$VERSIONS_FILE" ]]; then
  echo "Missing ${VERSIONS_FILE}" >&2
  exit 1
fi

echo "CLI version checker stub: ${VERSIONS_FILE}"
echo "TODO: implement release checks and issue creation."
