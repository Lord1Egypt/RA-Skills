#!/bin/bash
set -euo pipefail
exec /home/box/.local/bin/clawhub skill publish /workspace/delvorn-register \
  --categories finance,integrations \
  --topics marketplace,usdc-base,receipts \
  --version 1.0.1 \
  --changelog "Categorize under finance/integrations so browse finds the skill. No behavior change."
