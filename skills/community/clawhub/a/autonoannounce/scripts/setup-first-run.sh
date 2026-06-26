#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
exec python3 "$ROOT/skills/autonoannounce/scripts/setup_first_run.py" "$@"
