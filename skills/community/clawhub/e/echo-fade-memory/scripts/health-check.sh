#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BASE_URL="${EFM_BASE_URL:-$($SCRIPT_DIR/_resolve_base_url.py)}"

curl -fsS "${BASE_URL%/}/v1/healthz"
