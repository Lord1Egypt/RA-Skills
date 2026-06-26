#!/usr/bin/env bash
# Run after: clawhub install ap2-checkout
# Prefer one-shot: npx from AP2 repo (see SKILL.md "One-command install").
set -eu

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "AP2 Checkout skill installed at: $SKILL_DIR"
echo ""
echo "Recommended (skill + openclaw + auto-start mock backend):"
echo "  cd \"\$AP2_HOME\" && npx -y file:code/samples/python/scenarios/a2a/unified/clawhub/npm/ap2-agent-checkout install"
echo ""
echo "Manual steps if backend not started:"
echo "  1. export AP2_HOME=/path/to/AP2"
echo "  2. cd \"\$AP2_HOME/code/samples/python/scenarios/a2a/unified\" && ./openclaw/start_ap2_backend.sh"
echo "  3. export MCPORTER_CONFIG=\"$SKILL_DIR/mcporter.json\""
echo "  4. Enable mcporter + ap2-checkout in ~/.openclaw/openclaw.json, restart gateway"
echo ""
echo "Verify: AP2_HOME=\$AP2_HOME $SKILL_DIR/scripts/check-backend.sh"
