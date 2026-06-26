#!/usr/bin/env bash
# Post current config to Telegram + ask for delta-only replies. Re-runnable anytime. No LLM.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/onboard.py" "$@"
