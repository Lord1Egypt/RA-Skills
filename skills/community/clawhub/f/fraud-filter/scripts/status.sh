#!/usr/bin/env bash
# status.sh — Show trust database status, coverage, and sync info.
#
# Usage:
#   status.sh          — Show trust DB status
#   status.sh --full   — Include pending reports and config

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

FULL=false
[ "${1:-}" = "--full" ] && FULL=true

node --input-type=module -e "
  import { getDbStatus, loadConfig } from '${SERVER_DIR}/trust-db.js';
  import { getPendingStatus } from '${SERVER_DIR}/reporter.js';

  const full = process.argv[1] === 'true';
  const status = getDbStatus();
  const result = { db: status };

  if (full) {
    result.reports = getPendingStatus();
    const config = loadConfig();
    const { install_id, ...safeConfig } = config;
    result.config = safeConfig;
  }

  console.log(JSON.stringify(result, null, 2));
" "$FULL"
