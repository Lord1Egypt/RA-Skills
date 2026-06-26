#!/usr/bin/env bash
# CloudGuard -- License Validation Module
# JWT-based offline validation with tier hierarchy support.
# Same architecture as other ClawHub skills (SecretScan, ConfigSafe, DepGuard, etc.)
#
# Tier hierarchy:
#   free=0, pro=1, team=2, enterprise=3
#
# License key format: JWT with payload containing:
#   product: "cloudguard"
#   tier: "free"|"pro"|"team"|"enterprise"
#   exp: Unix timestamp (expiry)
#   seats: number (optional)
#
# Validation is 100% offline -- no network calls.

set -euo pipefail

# --- Colors ------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# --- Configuration -----------------------------------------------------------

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
CLOUDGUARD_LICENSE_KEY="${CLOUDGUARD_LICENSE_KEY:-}"

# --- Tier Hierarchy ----------------------------------------------------------

declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

declare -A TIER_LABELS=(
  [free]="Free"
  [pro]="Pro"
  [team]="Team"
  [enterprise]="Enterprise"
)

declare -A TIER_PATTERN_LIMITS=(
  [free]=30
  [pro]=60
  [team]=90
  [enterprise]=90
)

# --- Key Retrieval -----------------------------------------------------------

# Retrieve the CloudGuard license key from environment or openclaw.json config.
# Priority: CLOUDGUARD_LICENSE_KEY env var > openclaw.json config
get_cloudguard_key() {
  # 1. Check environment variable
  if [[ -n "$CLOUDGUARD_LICENSE_KEY" ]]; then
    echo "$CLOUDGUARD_LICENSE_KEY"
    return 0
  fi

  # 2. Check openclaw.json configuration file
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""

    # Try python3 first (most common)
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('cloudguard', {}).get('apiKey', ''))
except: pass
" 2>/dev/null)

    # Fallback to node
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  console.log(cfg?.skills?.entries?.cloudguard?.apiKey || '');
} catch(e) {}
" 2>/dev/null)

    # Fallback to jq
    elif command -v jq &>/dev/null; then
      key=$(jq -r '.skills.entries.cloudguard.apiKey // ""' "$OPENCLAW_CONFIG" 2>/dev/null)
    fi

    if [[ -n "${key:-}" ]]; then
      echo "$key"
      return 0
    fi
  fi

  return 1
}

# --- JWT Decoding ------------------------------------------------------------

# Decode the payload portion of a JWT token using 3 fallback methods:
#   1. base64 -d (Linux/GNU coreutils)
#   2. base64 -D (macOS/BSD)
#   3. openssl base64 -d (universal fallback)
#
# Handles URL-safe base64 encoding (replaces -_ with +/) and padding.
decode_jwt_payload() {
  local token="$1"

  # --- JWT Structure Validation ---
  # A valid JWT must have exactly 3 dot-separated parts: header.payload.signature
  local dot_count
  dot_count=$(echo "$token" | tr -cd '.' | wc -c)
  if [[ "$dot_count" -ne 2 ]]; then
    echo "[JWT] Malformed token: expected 3 parts (header.payload.signature), got $((dot_count + 1))" >&2
    return 1
  fi

  local header payload signature
  header=$(echo "$token" | cut -d. -f1)
  payload=$(echo "$token" | cut -d. -f2)
  signature=$(echo "$token" | cut -d. -f3)

  # Signature must be non-empty
  if [[ -z "$signature" ]]; then
    echo "[JWT] Rejected: signature segment is empty (unsigned token)" >&2
    return 1
  fi

  # --- Signature Verification (HMAC-SHA256 via openssl, if available) ---
  # NOTE: Full cryptographic verification requires the shared secret. When
  # CLAWHUB_JWT_SECRET is set, we verify the HMAC-SHA256 signature. Without
  # the secret, we still enforce structural integrity (3-part, non-empty sig)
  # which blocks trivially forged tokens (e.g., alg:none attacks).
  if [[ -n "${CLAWHUB_JWT_SECRET:-}" ]] && command -v openssl &>/dev/null; then
    local signing_input="${header}.${payload}"
    local expected_sig
    expected_sig=$(printf '%s' "$signing_input" \
      | openssl dgst -sha256 -hmac "$CLAWHUB_JWT_SECRET" -binary 2>/dev/null \
      | openssl base64 -e 2>/dev/null \
      | tr '/+' '_-' | tr -d '=')
    if [[ "$expected_sig" != "$signature" ]]; then
      echo "[JWT] Signature verification failed" >&2
      return 1
    fi
  fi

  # --- Decode Payload ---
  local padded="$payload"
  local mod=$((${#payload} % 4))
  if [[ $mod -eq 2 ]]; then padded="${payload}=="; fi
  if [[ $mod -eq 3 ]]; then padded="${payload}="; fi

  local decoded
  decoded=$(echo "$padded" | tr '_-' '/+' | base64 -d 2>/dev/null || \
            echo "$padded" | tr '_-' '/+' | base64 -D 2>/dev/null || \
            echo "$padded" | tr '_-' '/+' | openssl base64 -d 2>/dev/null) || {
    echo "[JWT] Failed to decode payload" >&2
    return 1
  }

  # --- Expiry Check ---
  # Check exp claim inline to catch expired tokens at decode time
  local exp_val=""
  if command -v python3 &>/dev/null; then
    exp_val=$(python3 -c "import json; print(json.loads('$decoded').get('exp', ''))" 2>/dev/null || true)
  elif command -v node &>/dev/null; then
    exp_val=$(node -e "console.log(JSON.parse('$decoded').exp || '')" 2>/dev/null || true)
  elif command -v jq &>/dev/null; then
    exp_val=$(echo "$decoded" | jq -r '.exp // ""' 2>/dev/null || true)
  fi

  if [[ -n "$exp_val" && "$exp_val" != "null" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$exp_val" ]]; then
      echo "[JWT] Token expired (exp=$exp_val, now=$now)" >&2
      return 1
    fi
  fi

  echo "$decoded"
}

# --- JSON Field Extraction ---------------------------------------------------

# Extract a field value from a JSON string.
# Uses python3 > node > jq > grep fallback chain.
extract_field() {
  local json="$1" field="$2"

  if command -v python3 &>/dev/null; then
    python3 -c "import json; print(json.loads('$json').get('$field', ''))" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "console.log(JSON.parse('$json')['$field'] || '')" 2>/dev/null
  elif command -v jq &>/dev/null; then
    echo "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    # Last resort: basic grep extraction
    echo "$json" | grep -oE "\"$field\"[[:space:]]*:[[:space:]]*\"?[^\",$}]+\"?" 2>/dev/null | \
      sed 's/.*:[[:space:]]*//' | tr -d '"' || echo ""
  fi
}

# --- License Validation ------------------------------------------------------

# Validate a license key by decoding its JWT payload and checking the product field.
# Returns the decoded payload JSON on success, non-zero exit on failure.
validate_license() {
  local key="$1"

  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    return 1
  fi

  local product
  product=$(extract_field "$payload" "product")

  # Validate product matches cloudguard
  if [[ -n "$product" && "$product" != "cloudguard" ]]; then
    return 1
  fi

  echo "$payload"
  return 0
}

# --- Primary License Check ---------------------------------------------------

# Check if the user has a valid CloudGuard license at the required tier.
# Usage: check_cloudguard_license "pro"
#
# Exit behavior:
#   - Returns 0 if license is valid and tier is sufficient
#   - Returns 1 with user-facing error message if not
check_cloudguard_license() {
  local required_tier="${1:-pro}"
  local required_level="${TIER_LEVELS[$required_tier]:-1}"

  # Retrieve the key
  local key
  if ! key=$(get_cloudguard_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}--- CloudGuard License Required ---${NC}"
    echo ""
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license."
    echo ""
    echo -e "Get your license at: ${CYAN}${BOLD}https://cloudguard.pages.dev/pricing${NC}"
    echo ""
    echo "Then configure it:"
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}"
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"cloudguard\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}"
    echo ""
    echo -e "  ${DIM}# Or set the environment variable:${NC}"
    echo -e "  ${CYAN}export CLOUDGUARD_LICENSE_KEY=\"YOUR_KEY\"${NC}"
    return 1
  fi

  # Decode the JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[CloudGuard]${NC} Invalid license key."
    echo -e "Get a valid license at: ${CYAN}https://cloudguard.pages.dev/pricing${NC}"
    return 1
  fi

  # Extract claims
  local product tier expiry
  product=$(extract_field "$payload" "product")
  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")

  # Validate product
  if [[ -n "$product" && "$product" != "cloudguard" ]]; then
    echo -e "${RED}[CloudGuard]${NC} License is for product '${BOLD}$product${NC}', not cloudguard."
    echo -e "Get a CloudGuard license at: ${CYAN}https://cloudguard.pages.dev/pricing${NC}"
    return 1
  fi

  # Validate tier level
  local actual_level="${TIER_LEVELS[$tier]:-0}"
  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[CloudGuard]${NC} This feature requires ${BOLD}${required_tier}${NC} tier. You have: ${BOLD}${tier}${NC}"
    echo -e "Upgrade at: ${CYAN}https://cloudguard.pages.dev/upgrade${NC}"
    return 1
  fi

  # Validate expiry
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[CloudGuard]${NC} License expired."
      echo -e "Renew at: ${CYAN}https://cloudguard.pages.dev/renew${NC}"
      return 1
    fi
  fi

  return 0
}

# --- Tier Retrieval ----------------------------------------------------------

# Get the current user's tier level from their license key.
# Returns "free" if no valid key is found.
get_cloudguard_tier() {
  local key
  if ! key=$(get_cloudguard_key) || [[ -z "$key" ]]; then
    echo "free"
    return 0
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key" 2>/dev/null); then
    echo "free"
    return 0
  fi

  local tier
  tier=$(extract_field "$payload" "tier")
  echo "${tier:-free}"
}

# --- Pattern Limit -----------------------------------------------------------

# Get the number of patterns available for the current tier.
get_cloudguard_pattern_limit() {
  local tier
  tier=$(get_cloudguard_tier)
  echo "${TIER_PATTERN_LIMITS[$tier]:-30}"
}

# --- Status Display ----------------------------------------------------------

# Show license and configuration status to the user.
show_cloudguard_status() {
  local key
  if ! key=$(get_cloudguard_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Patterns: 30 of 90"
    echo -e "  Available: scan (30 patterns)"
    echo -e "  Upgrade at: ${CYAN}https://cloudguard.pages.dev/pricing${NC}"
    return
  fi

  local payload tier expiry seats product
  payload=$(decode_jwt_payload "$key" 2>/dev/null) || {
    echo -e "License: ${RED}Invalid key${NC}"
    return
  }

  product=$(extract_field "$payload" "product")
  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")
  seats=$(extract_field "$payload" "seats")

  # Validate product
  if [[ -n "$product" && "$product" != "cloudguard" ]]; then
    echo -e "License: ${RED}Wrong product ($product)${NC}"
    echo -e "  This key is for $product, not CloudGuard."
    echo -e "  Get a CloudGuard license at: ${CYAN}https://cloudguard.pages.dev/pricing${NC}"
    return
  fi

  local now status_color status_text
  now=$(date +%s)
  status_color="$GREEN"; status_text="Active"
  if [[ -n "$expiry" && "$now" -gt "$expiry" ]]; then
    status_color="$RED"; status_text="Expired"
  fi

  local expiry_date="Never"
  if [[ -n "$expiry" ]]; then
    expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || \
                  date -r "$expiry" +%Y-%m-%d 2>/dev/null || \
                  echo "unknown")
  fi

  local pattern_limit="${TIER_PATTERN_LIMITS[$tier]:-30}"

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  echo -e "  Product: cloudguard"
  echo -e "  Patterns: $pattern_limit of 90"
  echo -e "  Seats: ${seats:-unlimited}"
  echo -e "  Expires: $expiry_date"
  echo ""

  case "$tier" in
    pro)
      echo -e "  Available: scan (60 patterns), hooks, report, audit"
      echo -e "  Upgrade to Team for: JSON/HTML output, category filtering, CI/CD integration"
      ;;
    team)
      echo -e "  Available: scan (90 patterns), hooks, report, audit, JSON/HTML, categories, CI/CD"
      ;;
    enterprise)
      echo -e "  Available: All features + priority support"
      ;;
  esac
}
