#!/usr/bin/env bash
# APIShield -- License Validation Module
# Offline JWT-based license validation (same pattern as DocSync, DepGuard, etc.)

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
APISHIELD_LICENSE_KEY="${APISHIELD_LICENSE_KEY:-}"

# Tier hierarchy for access control
declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

# ─── Key retrieval ───────────────────────────────────────────────────────────
# Check env var first, then openclaw.json config file

get_apishield_key() {
  # 1. Environment variable (highest priority)
  if [[ -n "$APISHIELD_LICENSE_KEY" ]]; then
    echo "$APISHIELD_LICENSE_KEY"
    return 0
  fi

  # 2. OpenClaw config file
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('apishield', {}).get('apiKey', ''))
except: pass
" 2>/dev/null)
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  console.log(cfg?.skills?.entries?.apishield?.apiKey || '');
} catch(e) {}
" 2>/dev/null)
    elif command -v jq &>/dev/null; then
      key=$(jq -r '.skills.entries.apishield.apiKey // ""' "$OPENCLAW_CONFIG" 2>/dev/null)
    fi

    if [[ -n "${key:-}" ]]; then
      echo "$key"
      return 0
    fi
  fi

  return 1
}

# ─── JWT payload decoding ────────────────────────────────────────────────────
# Base64url decode the middle section of a JWT (header.PAYLOAD.signature)

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

# ─── JSON field extraction ───────────────────────────────────────────────────
# Extract a field from a JSON string using whatever tool is available

extract_field() {
  local json="$1" field="$2"
  if command -v python3 &>/dev/null; then
    python3 -c "import json; print(json.loads('$json').get('$field', ''))" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "console.log(JSON.parse('$json')['$field'] || '')" 2>/dev/null
  elif command -v jq &>/dev/null; then
    echo "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    # Fallback: grep-based extraction (handles simple values)
    echo "$json" | grep -oP "\"$field\"\s*:\s*\"?\K[^\",$}]+" 2>/dev/null || echo ""
  fi
}

# ─── License validation ─────────────────────────────────────────────────────
# Validates JWT: decodes payload, checks iss, product, expiry, and tier level

validate_license() {
  local key="$1"
  local required_tier="${2:-pro}"

  # Decode JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[APIShield]${NC} Invalid license key format."
    return 1
  fi

  # Check issuer
  local iss
  iss=$(extract_field "$payload" "iss")
  if [[ "$iss" != "license-api" ]]; then
    echo -e "${RED}[APIShield]${NC} Invalid license issuer."
    return 1
  fi

  # Check product
  local product
  product=$(extract_field "$payload" "product")
  if [[ "$product" != "apishield" ]]; then
    echo -e "${RED}[APIShield]${NC} License is for ${BOLD}$product${NC}, not apishield."
    return 1
  fi

  # Check expiry
  local expiry
  expiry=$(extract_field "$payload" "exp")
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[APIShield]${NC} License expired."
      echo -e "Renew at: ${CYAN}https://apishield.pages.dev/renew${NC}"
      return 1
    fi
  fi

  # Check tier level
  local tier
  tier=$(extract_field "$payload" "tier")
  local required_level="${TIER_LEVELS[$required_tier]:-1}"
  local actual_level="${TIER_LEVELS[$tier]:-0}"

  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[APIShield]${NC} This feature requires ${BOLD}$required_tier${NC} tier. You have: ${BOLD}$tier${NC}"
    echo -e "Upgrade at: ${CYAN}https://apishield.pages.dev/upgrade${NC}"
    return 1
  fi

  return 0
}

# ─── Public API: check license ───────────────────────────────────────────────
# Called by apishield.sh require_license()

check_apishield_license() {
  local required_tier="${1:-pro}"

  local key
  if ! key=$(get_apishield_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}--- APIShield License Required ---${NC}"
    echo ""
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license."
    echo ""
    echo -e "Get your license at: ${CYAN}${BOLD}https://apishield.pages.dev/pricing${NC}"
    echo ""
    echo "Then configure it:"
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}"
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"apishield\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}"
    echo ""
    echo -e "  ${DIM}# Or set the environment variable:${NC}"
    echo -e "  ${CYAN}export APISHIELD_LICENSE_KEY=\"YOUR_KEY\"${NC}"
    return 1
  fi

  validate_license "$key" "$required_tier"
}

# ─── Public API: get current tier ────────────────────────────────────────────
# Returns the tier string (free, pro, team, enterprise) from the license JWT

get_apishield_tier() {
  local key
  if ! key=$(get_apishield_key) || [[ -z "$key" ]]; then
    echo "free"
    return 0
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo "free"
    return 0
  fi

  # Verify it is an apishield license
  local product
  product=$(extract_field "$payload" "product")
  if [[ "$product" != "apishield" ]]; then
    echo "free"
    return 0
  fi

  # Check expiry before returning tier
  local expiry
  expiry=$(extract_field "$payload" "exp")
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo "free"
      return 0
    fi
  fi

  local tier
  tier=$(extract_field "$payload" "tier")
  echo "${tier:-free}"
}

# ─── Public API: show license status ─────────────────────────────────────────
# Pretty-print license information for apishield status command

show_apishield_status() {
  local key
  if ! key=$(get_apishield_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Available: scan (up to 5 route files)"
    echo -e "  Upgrade at: ${CYAN}https://apishield.pages.dev/pricing${NC}"
    return
  fi

  local payload tier expiry seats email
  payload=$(decode_jwt_payload "$key" 2>/dev/null) || { echo -e "License: ${RED}Invalid key${NC}"; return; }

  # Verify product
  local product
  product=$(extract_field "$payload" "product")
  if [[ "$product" != "apishield" ]]; then
    echo -e "License: ${RED}Wrong product (${product})${NC}"
    echo -e "  This key is for ${BOLD}$product${NC}, not apishield."
    return
  fi

  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")
  seats=$(extract_field "$payload" "seats")
  email=$(extract_field "$payload" "sub")

  # Determine active/expired status
  local now status_color status_text
  now=$(date +%s)
  status_color="$GREEN"; status_text="Active"
  if [[ -n "$expiry" && "$now" -gt "$expiry" ]]; then
    status_color="$RED"; status_text="Expired"
  fi

  # Format expiry date (cross-platform)
  local expiry_date="Never"
  if [[ -n "$expiry" ]]; then
    expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || \
                  date -r "$expiry" +%Y-%m-%d 2>/dev/null || \
                  echo "unknown")
  fi

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  [[ -n "$email" ]] && echo -e "  Email: $email"
  echo -e "  Seats: ${seats:-1}"
  echo -e "  Expires: $expiry_date"

  # Show available features based on tier
  echo ""
  echo -e "  ${BOLD}Available features:${NC}"
  echo -e "    scan (unlimited route files)"
  if [[ "${TIER_LEVELS[$tier]:-0}" -ge 1 ]]; then
    echo -e "    hooks install/uninstall"
    echo -e "    report"
  fi
  if [[ "${TIER_LEVELS[$tier]:-0}" -ge 2 ]]; then
    echo -e "    inventory"
    echo -e "    compliance"
  fi
}
