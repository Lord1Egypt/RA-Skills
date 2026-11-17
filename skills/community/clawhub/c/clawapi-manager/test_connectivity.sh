#!/bin/bash
#
# API Cockpit - Connectivity Test
# Tests API connectivity before making switches
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/config"

# Load config
if [ -f "${CONFIG_DIR}/.env" ]; then
    source "${CONFIG_DIR}/.env"
fi

# Test connectivity to a provider
test_connectivity() {
    local provider="$1"
    local url_var="${provider^^}_API_URL"
    local key_var="${provider^^}_API_KEY"
    
    local url="${!url_var}"
    local key="${!key_var}"
    
    if [ -z "${url}" ] || [ -z "${key}" ] || [ "${key}" == "your_${provider}_key_here" ]; then
        echo "${provider}: NOT CONFIGURED"
        return 1
    fi
    
    # Simple connectivity test - try to reach the endpoint
    if curl -sf --connect-timeout 5 --max-time 10 "${url}" > /dev/null 2>&1; then
        echo "${provider}: OK"
        return 0
    else
        echo "${provider}: FAILED"
        return 1
    fi
}

# Test all configured providers
test_all() {
    echo "Testing API connectivity..."
    echo ""
    
    local providers=("antigravity" "codex" "copilot" "windsurf")
    local failed=0
    
    for provider in "${providers[@]}"; do
        if ! test_connectivity "${provider}"; then
            ((failed++)) || true
        fi
    done
    
    echo ""
    if [ ${failed} -eq 0 ]; then
        echo "All providers OK"
        return 0
    else
        echo "${failed} provider(s) failed"
        return 1
    fi
}

# Main
case "${1:-all}" in
    all)
        test_all
        ;;
    *)
        test_connectivity "$1"
        ;;
esac
