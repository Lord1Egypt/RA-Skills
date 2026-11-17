#!/bin/bash
#
# API Cockpit - OpenClaw Config Reader
# Reads API config from openclaw.json (READ-ONLY, no modifications)
#

set -euo pipefail

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
OUTPUT_FILE="${1:-config/auto_providers.env}"

if [ ! -f "${OPENCLAW_CONFIG}" ]; then
    echo "Error: openclaw.json not found at ${OPENCLAW_CONFIG}"
    exit 1
fi

echo "Reading API providers from openclaw.json (READ-ONLY)..."

# Extract providers and generate env file
jq -r '.models.providers | to_entries[] | 
"export \(.key | ascii_upcase)_API_KEY=\"\(.value.apiKey // "")\""
' "${OPENCLAW_CONFIG}" > "${OUTPUT_FILE}"

echo "Generated ${OUTPUT_FILE}"
echo ""
echo "Providers found:"
jq -r '.models.providers | keys[]' "${OPENCLAW_CONFIG}"
