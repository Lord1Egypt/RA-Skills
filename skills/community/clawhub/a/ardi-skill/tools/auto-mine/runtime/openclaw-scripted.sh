#!/usr/bin/env bash
# runtime/openclaw-scripted.sh — invoke OpenClaw with --message in scripted mode.
#
# This is the "external timer" mode for OpenClaw users who want the same
# 60-90s cadence as Claude/Hermes (instead of OpenClaw's built-in 30-min
# heartbeat — for that, see ../openclaw-heartbeat-mode/).
#
# Requires:
#   - openclaw on PATH (install via OpenClaw docs)
#   - ardi skill installed in OpenClaw's skill registry
#   - --local: use embedded agent (no remote messaging round-trip)

set -euo pipefail

PROMPT_FILE="${1:?usage: openclaw-scripted.sh <prompt-file>}"
[[ -r "$PROMPT_FILE" ]] || { echo "prompt not readable: $PROMPT_FILE" >&2; exit 2; }

command -v openclaw >/dev/null || { echo "openclaw not on PATH" >&2; exit 3; }

PROMPT="$(cat "$PROMPT_FILE")"
exec openclaw agent \
  --local \
  --thinking medium \
  --message "$PROMPT"
