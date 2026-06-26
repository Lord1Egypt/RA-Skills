#!/bin/zsh
set -euo pipefail
cd /Users/vtammm/.openclaw/workspace
set -a
source ./.env.plan-a
set +a
/usr/bin/env node plan-a-demo.js prod-send
