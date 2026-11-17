#!/usr/bin/env bash
# Read-only native health checks; never restores old relay policy.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
host="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
if [[ ${1:-} == --gateway && $# == 2 ]]; then host="$2"
elif [[ $# != 0 ]]; then echo 'Usage: antenna doctor [--gateway PATH]; legacy repairs are retired.' >&2; exit 64; fi
exec node "$SCRIPT_DIR/../plugin/doctor.mjs" doctor "$host" "$(dirname "$SCRIPT_DIR")"
