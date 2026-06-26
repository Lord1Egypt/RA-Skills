#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:-$HOME/.openclaw/workspace/AutoResearchClaw}"
EXAMPLE_NAME="${2:-finance_event_study}"

case "$EXAMPLE_NAME" in
  finance_event_study)
    CONFIG_PATH="examples/finance_event_study.config.yaml"
    ;;
  accounting_forecast_error)
    CONFIG_PATH="examples/accounting_forecast_error.config.yaml"
    ;;
  *)
    echo "Unknown example: $EXAMPLE_NAME" >&2
    exit 1
    ;;
esac

cd "$REPO_DIR"
python3 -m venv .venv >/dev/null 2>&1 || true
source .venv/bin/activate
python -m pip install -e .
researchclaw run --config "$CONFIG_PATH" --auto-approve
