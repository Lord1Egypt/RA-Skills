#!/usr/bin/env bash
# Validate that the Datadog MCP Server is reachable and credentials work.
# Usage: ./scripts/validate.sh
# Requires: DD_API_KEY, DD_APP_KEY environment variables
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check() { printf "  %-40s" "$1"; }
pass() { echo -e "${GREEN}✓${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; ERRORS=$((ERRORS + 1)); }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

ERRORS=0

echo "Datadog MCP Server — Validation"
echo "================================"
echo ""

# Check env vars
check "DD_API_KEY set"
if [ -n "${DD_API_KEY:-}" ]; then pass; else fail "missing"; fi

check "DD_APP_KEY set"
if [ -n "${DD_APP_KEY:-}" ]; then pass; else fail "missing"; fi

DD_SITE="${DD_SITE:-datadoghq.com}"
check "DD_SITE: $DD_SITE"
pass

if [ -z "${DD_API_KEY:-}" ] || [ -z "${DD_APP_KEY:-}" ]; then
  echo ""
  echo -e "${RED}Cannot continue without credentials.${NC}"
  exit 1
fi

# Validate API key
check "API key valid"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  "https://api.${DD_SITE}/api/v1/validate" \
  -H "DD-API-KEY: ${DD_API_KEY}")
if [ "$HTTP_CODE" = "200" ]; then pass; else fail "HTTP $HTTP_CODE"; fi

# Validate App key
check "Application key valid"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  "https://api.${DD_SITE}/api/v1/validate" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}")
if [ "$HTTP_CODE" = "200" ]; then pass; else fail "HTTP $HTTP_CODE"; fi

# Check MCP server endpoint
check "MCP server reachable"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  "https://mcp.${DD_SITE}/api/unstable/mcp-server/mcp" \
  -H "DD-API-KEY: ${DD_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"validate","version":"1.0.0"}},"id":1}' \
  --max-time 10 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
  pass
elif [ "$HTTP_CODE" = "000" ]; then
  warn "timeout (server may require SSE transport)"
else
  warn "HTTP $HTTP_CODE (may need Preview access)"
fi

# Check mcporter availability
check "mcporter installed"
if command -v mcporter &>/dev/null; then
  pass
else
  warn "not found (install: npm i -g mcporter)"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}All checks passed.${NC}"
else
  echo -e "${RED}$ERRORS check(s) failed.${NC}"
  exit 1
fi
