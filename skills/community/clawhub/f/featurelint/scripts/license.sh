#!/usr/bin/env bash
# ==============================================================================
# FeatureLint - Feature Flag Hygiene Analyzer
# License Validation Module
# ENV: FEATURELINT_LICENSE_KEY
# Product: featurelint
# ==============================================================================
set -euo pipefail

FEATURELINT_LICENSE_PRODUCT="featurelint"
FEATURELINT_LICENSE_API_URL="https://api.keygen.sh/v1/accounts"
FEATURELINT_LICENSE_CACHE_DIR="${HOME}/.cache/featurelint"
FEATURELINT_LICENSE_CACHE_FILE="${FEATURELINT_LICENSE_CACHE_DIR}/license.cache"
FEATURELINT_LICENSE_CACHE_TTL=86400  # 24 hours in seconds
FEATURELINT_LICENSE_VALIDATED=""
FEATURELINT_LICENSE_TIER_RESULT=""

# ==============================================================================
# License key format validation
# ==============================================================================
featurelint_license_format_valid() {
    local key="$1"

    # Expected format: FEATURELINT-XXXX-XXXX-XXXX-XXXX
    if echo "$key" | grep -qE '^FEATURELINT-[[:alnum:]]{4}-[[:alnum:]]{4}-[[:alnum:]]{4}-[[:alnum:]]{4}$'; then
        return 0
    fi

    # Also accept generic UUID format
    if echo "$key" | grep -qE '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'; then
        return 0
    fi

    return 1
}

# ==============================================================================
# License cache management
# ==============================================================================
featurelint_license_cache_init() {
    if [[ ! -d "${FEATURELINT_LICENSE_CACHE_DIR}" ]]; then
        mkdir -p "${FEATURELINT_LICENSE_CACHE_DIR}" 2>/dev/null || true
    fi
}

featurelint_license_cache_read() {
    local key="$1"

    if [[ ! -f "${FEATURELINT_LICENSE_CACHE_FILE}" ]]; then
        return 1
    fi

    # Check cache age
    local cache_mtime
    cache_mtime=$(stat -c %Y "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || \
                  stat -f %m "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || echo "0")
    local now
    now=$(date +%s)
    local age=$((now - cache_mtime))

    if [[ "$age" -gt "$FEATURELINT_LICENSE_CACHE_TTL" ]]; then
        featurelint_license_log "Cache expired (age: ${age}s, ttl: ${FEATURELINT_LICENSE_CACHE_TTL}s)"
        return 1
    fi

    # Read and verify cached key matches
    local cached_key cached_tier cached_expiry cached_status
    IFS='|' read -r cached_key cached_tier cached_expiry cached_status < "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || return 1

    if [[ "$cached_key" != "$key" ]]; then
        featurelint_license_log "Cache key mismatch"
        return 1
    fi

    if [[ "$cached_status" != "valid" ]]; then
        featurelint_license_log "Cached license status: ${cached_status}"
        return 1
    fi

    # Check expiry
    if [[ -n "$cached_expiry" && "$cached_expiry" != "none" ]]; then
        local expiry_epoch
        expiry_epoch=$(date -d "$cached_expiry" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$cached_expiry" +%s 2>/dev/null || echo "0")
        if [[ "$now" -gt "$expiry_epoch" && "$expiry_epoch" -gt 0 ]]; then
            featurelint_license_log "Cached license expired: ${cached_expiry}"
            return 1
        fi
    fi

    FEATURELINT_LICENSE_TIER_RESULT="$cached_tier"
    featurelint_license_log "Using cached license: tier=${cached_tier}"
    return 0
}

featurelint_license_cache_write() {
    local key="$1"
    local tier="$2"
    local expiry="${3:-none}"
    local status="${4:-valid}"

    featurelint_license_cache_init
    echo "${key}|${tier}|${expiry}|${status}" > "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || true
    chmod 600 "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || true
    featurelint_license_log "Cache written: tier=${tier}, status=${status}"
}

featurelint_license_cache_clear() {
    if [[ -f "${FEATURELINT_LICENSE_CACHE_FILE}" ]]; then
        rm -f "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || true
        featurelint_license_log "Cache cleared"
    fi
}

# ==============================================================================
# License logging helper
# ==============================================================================
featurelint_license_log() {
    local message="$1"
    if [[ "${FEATURELINT_VERBOSE:-0}" -ge 1 ]]; then
        echo -e "\033[0;90m[license] ${message}\033[0m" >&2
    fi
}

# ==============================================================================
# Offline license validation (hash-based)
# ==============================================================================
featurelint_license_validate_offline() {
    local key="$1"

    # Extract tier hint from key structure
    # FEATURELINT-PROX-...: Pro tier
    # FEATURELINT-TEAM-...: Team tier
    # UUID format: check hash prefix
    local tier="free"

    if echo "$key" | grep -qiE '^FEATURELINT-PRO'; then
        tier="pro"
    elif echo "$key" | grep -qiE '^FEATURELINT-TEAM'; then
        tier="team"
    elif echo "$key" | grep -qiE '^FEATURELINT-[[:alnum:]]{4}'; then
        # Hash-based validation for generic format
        local hash
        if command -v sha256sum >/dev/null 2>&1; then
            hash=$(echo -n "${FEATURELINT_LICENSE_PRODUCT}:${key}" | sha256sum | cut -d' ' -f1)
        elif command -v shasum >/dev/null 2>&1; then
            hash=$(echo -n "${FEATURELINT_LICENSE_PRODUCT}:${key}" | shasum -a 256 | cut -d' ' -f1)
        else
            featurelint_license_log "No hash utility found; defaulting to free tier"
            echo "free"
            return 0
        fi

        # Check hash prefix to determine tier
        local prefix="${hash:0:2}"
        case "$prefix" in
            [0-3]*)  tier="team" ;;
            [4-7]*)  tier="pro" ;;
            *)       tier="free" ;;
        esac
    fi

    featurelint_license_log "Offline validation: tier=${tier}"
    echo "$tier"
}

# ==============================================================================
# Online license validation
# ==============================================================================
featurelint_license_validate_online() {
    local key="$1"

    # Check if curl is available
    if ! command -v curl >/dev/null 2>&1; then
        featurelint_license_log "curl not available; falling back to offline validation"
        featurelint_license_validate_offline "$key"
        return
    fi

    # Check network connectivity with timeout
    local response
    response=$(curl -s --max-time 5 \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "{\"product\": \"${FEATURELINT_LICENSE_PRODUCT}\", \"key\": \"${key}\"}" \
        "https://featurelint.pages.dev/api/validate" 2>/dev/null) || {
        featurelint_license_log "Online validation failed; falling back to offline"
        featurelint_license_validate_offline "$key"
        return
    }

    # Parse response
    if [[ -z "$response" ]]; then
        featurelint_license_log "Empty response; falling back to offline validation"
        featurelint_license_validate_offline "$key"
        return
    fi

    # Extract tier from JSON response (basic parsing without jq dependency)
    local tier
    tier=$(echo "$response" | grep -o '"tier"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"tier"[[:space:]]*:[[:space:]]*"//;s/"//')

    if [[ -z "$tier" ]]; then
        featurelint_license_log "Could not parse tier from response; falling back to offline"
        featurelint_license_validate_offline "$key"
        return
    fi

    # Extract expiry if present
    local expiry
    expiry=$(echo "$response" | grep -o '"expires"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"expires"[[:space:]]*:[[:space:]]*"//;s/"//')

    # Extract status
    local status
    status=$(echo "$response" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"status"[[:space:]]*:[[:space:]]*"//;s/"//')

    if [[ "$status" == "expired" || "$status" == "revoked" || "$status" == "suspended" ]]; then
        featurelint_license_log "License status: ${status}"
        featurelint_license_cache_write "$key" "free" "${expiry:-none}" "$status"
        echo "free"
        return
    fi

    # Cache the validated result
    featurelint_license_cache_write "$key" "$tier" "${expiry:-none}" "valid"

    featurelint_license_log "Online validation: tier=${tier}"
    echo "$tier"
}

# ==============================================================================
# Main license validation entry point
# ==============================================================================
featurelint_validate_license() {
    local key="${1:-}"

    # No key provided
    if [[ -z "$key" ]]; then
        featurelint_license_log "No license key provided; using free tier"
        echo "free"
        return 0
    fi

    # Format validation
    if ! featurelint_license_format_valid "$key"; then
        featurelint_license_log "Invalid license key format"
        echo "free"
        return 0
    fi

    # Check cache first
    if featurelint_license_cache_read "$key"; then
        echo "${FEATURELINT_LICENSE_TIER_RESULT}"
        return 0
    fi

    # Try online validation first, fall back to offline
    local tier
    tier="$(featurelint_license_validate_online "$key")"

    # Validate tier value
    case "$tier" in
        free|pro|team)
            echo "$tier"
            ;;
        *)
            featurelint_license_log "Unknown tier value: ${tier}; defaulting to free"
            echo "free"
            ;;
    esac
}

# ==============================================================================
# License information display
# ==============================================================================
featurelint_license_info() {
    local key="${FEATURELINT_LICENSE_KEY:-}"
    local tier

    echo ""
    echo -e "\033[1m  FeatureLint License Information\033[0m"
    echo -e "  \033[0;90m-------------------------------------------\033[0m"
    echo "  Product:     ${FEATURELINT_LICENSE_PRODUCT}"

    if [[ -z "$key" ]]; then
        echo "  License key: (not set)"
        echo "  Tier:        free"
        echo "  Patterns:    30"
        echo ""
        echo "  Set FEATURELINT_LICENSE_KEY to activate Pro or Team features."
        echo "  Visit https://featurelint.pages.dev for plans."
    else
        # Mask the license key
        local masked
        masked="${key:0:12}...${key: -4}"
        echo "  License key: ${masked}"

        tier="$(featurelint_validate_license "$key")"
        echo "  Tier:        ${tier}"

        local pattern_count
        case "$tier" in
            free) pattern_count=30 ;;
            pro)  pattern_count=60 ;;
            team) pattern_count=90 ;;
        esac
        echo "  Patterns:    ${pattern_count}"

        # Cache status
        if [[ -f "${FEATURELINT_LICENSE_CACHE_FILE}" ]]; then
            local cache_mtime
            cache_mtime=$(stat -c %Y "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || \
                          stat -f %m "${FEATURELINT_LICENSE_CACHE_FILE}" 2>/dev/null || echo "0")
            local now
            now=$(date +%s)
            local age=$((now - cache_mtime))
            local remaining=$((FEATURELINT_LICENSE_CACHE_TTL - age))
            if [[ "$remaining" -gt 0 ]]; then
                echo "  Cache:       valid (expires in ${remaining}s)"
            else
                echo "  Cache:       expired"
            fi
        else
            echo "  Cache:       empty"
        fi
    fi

    echo -e "  \033[0;90m-------------------------------------------\033[0m"
    echo ""
}

# ==============================================================================
# Tier feature availability checks
# ==============================================================================
featurelint_tier_has_feature() {
    local tier="$1"
    local feature="$2"

    case "$feature" in
        stale_flags|flag_complexity)
            # Available in all tiers
            return 0
            ;;
        flag_safety|sdk_misuse)
            # Pro and Team only
            [[ "$tier" == "pro" || "$tier" == "team" ]]
            ;;
        flag_lifecycle|flag_architecture)
            # Team only
            [[ "$tier" == "team" ]]
            ;;
        parallel_scan|json_output|csv_output)
            # Available in all tiers
            return 0
            ;;
        markdown_report|baseline)
            # Pro and Team only
            [[ "$tier" == "pro" || "$tier" == "team" ]]
            ;;
        custom_patterns|api_integration)
            # Team only
            [[ "$tier" == "team" ]]
            ;;
        *)
            return 1
            ;;
    esac
}

featurelint_tier_gate_message() {
    local feature="$1"
    local required_tier="$2"

    echo ""
    echo -e "  \033[0;35mThis feature requires the ${required_tier} tier.\033[0m"
    echo -e "  \033[0;90mFeature: ${feature}\033[0m"
    echo -e "  \033[0;90mCurrent: ${FEATURELINT_TIER}\033[0m"
    echo ""
    echo "  Upgrade at https://featurelint.pages.dev"
    echo ""
}

# ==============================================================================
# License key generation hint (for development)
# ==============================================================================
featurelint_license_generate_hint() {
    echo ""
    echo "  License key format: FEATURELINT-XXXX-XXXX-XXXX-XXXX"
    echo ""
    echo "  Tier prefixes:"
    echo "    FEATURELINT-PRO*  -> Pro tier  (60 patterns)"
    echo "    FEATURELINT-TEAM* -> Team tier (90 patterns)"
    echo ""
    echo "  Set via environment variable:"
    echo "    export FEATURELINT_LICENSE_KEY=\"FEATURELINT-XXXX-XXXX-XXXX-XXXX\""
    echo ""
}
