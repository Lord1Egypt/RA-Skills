#!/usr/bin/env bash
set -euo pipefail

if ! command -v mcporter >/dev/null 2>&1; then
  echo "ERROR: mcporter is not installed or not on PATH."
  echo "Install/configure mcporter first, then ensure an 'obs' MCP server is available."
  exit 1
fi

if ! mcporter call 'obs.get_obs_status()' >/dev/null 2>&1; then
  echo "ERROR: OBS MCP server is not configured/reachable via mcporter."
  echo "Run these checks:"
  echo "  - mcporter list"
  echo "  - mcporter call 'obs.get_obs_status()'"
  echo "Then retry ClawCast scripts."
  exit 1
fi
