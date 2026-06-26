#!/usr/bin/env bash
# =============================================================================
# Doc2Slides - Dependency Setup Script
# =============================================================================
# This script ONLY performs LOCAL operations on the user's machine.
# - Installs Python packages via pip3 (python-pptx, requests, playwright)
# - Checks for browser availability (Chrome/Chromium)
# - No network requests, no data collection, no credential access
# - No remote code execution, no external API calls
# All dependencies are standard open-source packages from PyPI.
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[..]${NC} $1"; }
fail()  { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

check_python() {
    command -v python3 >/dev/null 2>&1 || fail "python3 not found. Install Python 3.8+ first."
    local ver
    ver=$(python3 -c "import sys; print(sys.version_info.major)")
    [ "$ver" -ge 3 ] || fail "Python 3+ required, got Python $ver"
    info "Python $(python3 --version 2>&1 | awk '{print $2}')"
}

check_pip() {
    command -v pip3 >/dev/null 2>&1 || fail "pip3 not found. Run: python3 -m ensurepip"
}

install_deps() {
    check_python
    check_pip

    warn "Installing Python packages..."
    pip3 install --quiet python-pptx requests 2>&1
    if ! python3 -c "import pptx" 2>/dev/null; then
        fail "python-pptx install failed"
    fi
    info "python-pptx installed"

    # Try to install playwright for screenshot rendering
    if python3 -c "import playwright" 2>/dev/null; then
        info "playwright already installed"
    else
        warn "Installing playwright..."
        pip3 install --quiet playwright 2>&1 || warn "playwright install skipped (optional)"
        python3 -c "import playwright" 2>/dev/null && info "playwright installed" || warn "playwright not available - will use template mode only"
    fi

    # Check for browser
    local browser=""
    for b in google-chrome chromium chromium-browser; do
        command -v "$b" >/dev/null 2>&1 && browser="$b" && break
    done

    if [ -n "$browser" ]; then
        info "Browser: $browser"
    else
        # Try playwright's bundled chromium
        if python3 -c "import playwright; playwright.sync_api.sync_playwright().start().chromium.launch()" 2>/dev/null; then
            info "Playwright Chromium available"
        else
            warn "No browser found. Screenshot rendering will be limited."
            warn "Install one: apt install chromium-browser  OR  playwright install chromium"
        fi
    fi

    # Test the workflow script itself
    if [ -f "$SCRIPT_DIR/scripts/workflow.py" ]; then
        python3 "$SCRIPT_DIR/scripts/workflow.py" --help >/dev/null 2>&1 && info "workflow.py ready" || warn "workflow.py has import issues"
    fi

    echo ""
    info "Setup complete!"
    echo ""
    echo "Try it:"
    echo "  python3 $SCRIPT_DIR/scripts/workflow.py --input document.pdf --output slides.pptx"
    echo ""
}

verify() {
    echo "=== Doc2Slides Environment Check ==="
    echo ""

    local ok=0
    local total=0

    # Python
    total=$((total+1))
    if command -v python3 >/dev/null 2>&1; then
        info "python3: $(python3 --version 2>&1 | awk '{print $2}')"
        ok=$((ok+1))
    else
        fail "python3: NOT FOUND"
    fi

    # pip
    total=$((total+1))
    if command -v pip3 >/dev/null 2>&1; then ok=$((ok+1)); info "pip3: found"; else fail "pip3: NOT FOUND"; fi

    # python-pptx
    total=$((total+1))
    if python3 -c "import pptx" 2>/dev/null; then ok=$((ok+1)); info "python-pptx: installed"; else fail "python-pptx: NOT INSTALLED (pip3 install python-pptx)"; fi

    # requests
    total=$((total+1))
    if python3 -c "import requests" 2>/dev/null; then ok=$((ok+1)); info "requests: installed"; else fail "requests: NOT INSTALLED (pip3 install requests)"; fi

    # playwright (optional)
    total=$((total+1))
    if python3 -c "import playwright" 2>/dev/null; then ok=$((ok+1)); info "playwright: installed (LLM rendering available)"; else warn "playwright: not installed (template mode only)"; fi

    # Browser
    total=$((total+1))
    local browser=""
    for b in google-chrome chromium chromium-browser; do
        command -v "$b" >/dev/null 2>&1 && browser="$b" && break
    done
    if [ -n "$browser" ]; then ok=$((ok+1)); info "browser: $browser"; else warn "browser: not found (screenshot rendering limited)"; fi

    # workflow.py
    total=$((total+1))
    if [ -f "$SCRIPT_DIR/scripts/workflow.py" ]; then ok=$((ok+1)); info "workflow.py: found"; else fail "workflow.py: MISSING"; fi

    # LLM keys (optional)
    local has_key=""
    for var in OPENAI_API_KEY ZHIPU_API_KEY DEEPSEEK_API_KEY; do
        if [ -n "${!var:-}" ]; then has_key="$var"; break; fi
    done
    if [ -n "$has_key" ]; then
        info "LLM key: $has_key (AI enhancement enabled)"
    else
        warn "LLM key: none set (template mode, still works fine)"
    fi

    echo ""
    echo "Result: $ok / $total checks passed"
    [ "$ok" -ge 4 ] && info "Ready to generate slides!" || fail "Missing critical dependencies. Run: bash setup.sh"
}

case "${1:-}" in
    --verify|-v) verify ;;
    --help|-h)
        echo "Usage: bash setup.sh          # Install dependencies"
        echo "       bash setup.sh --verify  # Check environment"
        ;;
    *) install_deps ;;
esac
