#!/usr/bin/env bash
set -euo pipefail

# Ganglion Health Check
# Usage: bash healthcheck.sh [project_dir] [ganglion_url]
#
# Checks both local and remote mode depending on what's available.

PROJECT_DIR="${1:-${GANGLION_PROJECT:-}}"
GANGLION_URL="${2:-${GANGLION_URL:-}}"

PASS=0
FAIL=0

pass() { echo "  [PASS] $1"; ((PASS++)); }
fail() { echo "  [FAIL] $1"; ((FAIL++)); }

echo "=== Checking prerequisites ==="

# Python
if command -v python3 &>/dev/null; then
    PYVER=$(python3 --version 2>&1)
    pass "Python installed: $PYVER"
else
    fail "python3 not found"
fi

# Ganglion CLI
if command -v ganglion &>/dev/null; then
    pass "ganglion CLI installed"
else
    fail "ganglion CLI not found (pip install ganglion)"
fi

# OpenAI API key
if [ -n "${LLM_PROVIDER_API_KEY:-}" ]; then
    pass "LLM_PROVIDER_API_KEY is set"
else
    fail "LLM_PROVIDER_API_KEY is not set"
fi

echo ""
echo "=== Checking local mode ==="

if [ -n "$PROJECT_DIR" ]; then
    if [ -f "$PROJECT_DIR/config.py" ]; then
        pass "config.py found at $PROJECT_DIR/config.py"
    else
        fail "config.py not found at $PROJECT_DIR/config.py"
    fi

    if [ -d "$PROJECT_DIR/tools" ]; then
        TOOL_COUNT=$(find "$PROJECT_DIR/tools" -name "*.py" ! -name "_*" 2>/dev/null | wc -l)
        pass "tools/ directory exists ($TOOL_COUNT tool files)"
    else
        fail "tools/ directory not found"
    fi

    if [ -d "$PROJECT_DIR/agents" ]; then
        AGENT_COUNT=$(find "$PROJECT_DIR/agents" -name "*.py" ! -name "_*" 2>/dev/null | wc -l)
        pass "agents/ directory exists ($AGENT_COUNT agent files)"
    else
        fail "agents/ directory not found"
    fi

    # Try loading status
    if command -v ganglion &>/dev/null; then
        if ganglion status "$PROJECT_DIR" &>/dev/null; then
            pass "ganglion status loads successfully"
        else
            fail "ganglion status failed (check config.py for errors)"
        fi
    fi
else
    echo "  [SKIP] No project directory specified (set GANGLION_PROJECT or pass as argument)"
fi

echo ""
echo "=== Checking remote mode ==="

if [ -n "$GANGLION_URL" ]; then
    if command -v curl &>/dev/null; then
        pass "curl installed"
    else
        fail "curl not found (needed for remote mode)"
    fi

    # Check liveness
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$GANGLION_URL/healthz" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        pass "Liveness probe OK at $GANGLION_URL/healthz"
    elif [ "$HTTP_CODE" = "000" ]; then
        fail "Cannot connect to $GANGLION_URL (connection refused)"
    else
        fail "Liveness probe returned HTTP $HTTP_CODE"
    fi

    # Check readiness
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$GANGLION_URL/readyz" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        pass "Readiness probe OK at $GANGLION_URL/readyz"

        # Check if running
        RUNNING=$(curl -s "$GANGLION_URL/v1/status" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('data', {}).get('running', 'unknown'))" 2>/dev/null || echo "unknown")
        if [ "$RUNNING" = "False" ]; then
            pass "No pipeline currently running"
        elif [ "$RUNNING" = "True" ]; then
            pass "Pipeline currently running"
        else
            fail "Could not determine pipeline status"
        fi

        # Check tool count
        TOOL_COUNT=$(curl -s "$GANGLION_URL/v1/tools" 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data', [])))" 2>/dev/null || echo "?")
        pass "Tools registered: $TOOL_COUNT"

        # Check agent count
        AGENT_COUNT=$(curl -s "$GANGLION_URL/v1/agents" 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data', [])))" 2>/dev/null || echo "?")
        pass "Agents registered: $AGENT_COUNT"

    elif [ "$HTTP_CODE" = "503" ]; then
        fail "Readiness probe returned 503 — bridge not yet configured"
    else
        fail "Readiness probe returned HTTP $HTTP_CODE"
    fi
else
    echo "  [SKIP] No GANGLION_URL set (start server with: ganglion serve <project_dir>)"
fi

echo ""
echo "=== Results ==="
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "Some checks failed. See troubleshooting: skills/ganglion/references/troubleshooting.md"
    exit 1
else
    echo ""
    echo "All checks passed."
    exit 0
fi
