#!/bin/bash
#
# API Cockpit - Key Rotation Manager
# Manages key pool with automatic rotation on failure/quota exhaustion
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/config"
DATA_DIR="${SCRIPT_DIR}/data"
LOCK_DIR="${SCRIPT_DIR}/locks"

mkdir -p "${DATA_DIR}" "${LOCK_DIR}"

KEY_POOL_FILE="${DATA_DIR}/key_pool.json"
LOCK_FILE="${LOCK_DIR}/key_rotation.lock"

# File lock
exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
    echo "Another rotation in progress"
    exit 1
fi

# Load key pool
load_pool() {
    if [ -f "${KEY_POOL_FILE}" ]; then
        cat "${KEY_POOL_FILE}"
    else
        echo '{"providers": {}}'
    fi
}

# Save key pool (atomic)
save_pool() {
    local content="$1"
    local tmp="${KEY_POOL_FILE}.$$"
    echo "${content}" > "${tmp}"
    mv "${tmp}" "${KEY_POOL_FILE}"
}

# Get current active key for a provider
get_active_key() {
    local provider="$1"
    local pool
    pool=$(load_pool)
    
    echo "${pool}" | jq -r ".providers.${provider}.active // empty"
}

# Rotate key for a provider
rotate_key() {
    local provider="$1"
    local pool
    pool=$(load_pool)
    
    local keys
    keys=$(echo "${pool}" | jq -r ".providers.${provider}.keys[]")
    
    if [ -z "${keys}" ]; then
        echo "No keys in pool for ${provider}"
        return 1
    fi
    
    local current
    current=$(echo "${pool}" | jq -r ".providers.${provider}.active // empty")
    
    # Find next key
    local found=0
    local next=""
    for key in ${keys}; do
        if [ "${found}" == "1" ]; then
            next="${key}"
            break
        fi
        if [ "${key}" == "${current}" ]; then
            found=1
        fi
    done
    
    # If current is last, wrap to first
    if [ -z "${next}" ]; then
        next=$(echo "${keys}" | head -1)
    fi
    
    # Backup current key before switching
    if [ -n "${current}" ]; then
        local backup
        backup=$(echo "${pool}" | jq ".providers.${provider}.backup = \"${current}\"")
        pool="${backup}"
    fi
    
    # Switch to next key
    pool=$(echo "${pool}" | jq ".providers.${provider}.active = \"${next}\"")
    
    save_pool "${pool}"
    
    echo "Rotated ${provider}: ${current} -> ${next}"
}

# Add key to pool
add_key() {
    local provider="$1"
    local key="$2"
    
    local pool
    pool=$(load_pool)
    
    pool=$(echo "${pool}" | jq ".providers.${provider}.keys += [\"${key}\"]")
    
    # If no active key, set this one
    local active
    active=$(echo "${pool}" | jq -r ".providers.${provider}.active // empty")
    if [ -z "${active}" ]; then
        pool=$(echo "${pool}" | jq ".providers.${provider}.active = \"${key}\"")
    fi
    
    save_pool "${pool}"
    echo "Added key to ${provider} pool"
}

# List keys
list_keys() {
    local pool
    pool=$(load_pool)
    
    echo "${pool}" | jq .
}

# Validate key works before switching
validate_key() {
    local provider="$1"
    local key="$2"
    
    # TODO: Implement actual validation
    # This should test the API key before marking it as active
    echo "Validating ${provider} key..."
    return 0
}

# Main
case "${1:-}" in
    rotate)
        rotate_key "${2:-}"
        ;;
    add)
        add_key "${2:-}" "${3:-}"
        ;;
    list)
        list_keys
        ;;
    active)
        get_active_key "${2:-}"
        ;;
    *)
        echo "Usage: $0 {rotate|add|list|active} [provider] [key]"
        ;;
esac
