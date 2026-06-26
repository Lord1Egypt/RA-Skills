#!/usr/bin/env bash
# AuthAudit -- License Validation Module
# Offline JWT-based license validation (same pattern as APIShield, DocSync, etc.)
#
# Public API:
#   check_authaudit_license <required_tier>  -- Validate license and tier
#   get_authaudit_tier                        -- Return current tier string
#   show_authaudit_status                     -- Pretty-print license info
#
# Tier hierarchy: free=0, pro=1, team=2, enterprise=3

set -euo pipefail

# ─── Colors ──────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ─── Constants ───────────────────────────────────────────────────────────────

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
AUTHAUDIT_LICENSE_KEY="${AUTHAUDIT_LICENSE_KEY:-}"
PRODUCT_NAME="authaudit"
PRODUCT_DISPLAY="AuthAudit"
PRODUCT_URL="https://authaudit.dev"

# Tier hierarchy for access control
declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

# ─── Key Retrieval ───────────────────────────────────────────────────────────
# Check env var first, then openclaw.json config file, then CLI argument

get_authaudit_key() {
  # 1. Environment variable (highest priority)
  if [[ -n "$AUTHAUDIT_LICENSE_KEY" ]]; then
    echo "$AUTHAUDIT_LICENSE_KEY"
    return 0
  fi

  # 2. OpenClaw config file
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""

    # Try python3 first (most reliable JSON parsing)
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json, sys
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    val = cfg.get('skills', {}).get('entries', {}).get('$PRODUCT_NAME', {}).get('apiKey', '')
    print(val)
except Exception:
    pass
" 2>/dev/null) || true
    # Try node as fallback
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const fs = require('fs');
  const cfg = JSON.parse(fs.readFileSync('$OPENCLAW_CONFIG', 'utf8'));
  console.log(cfg?.skills?.entries?.['$PRODUCT_NAME']?.apiKey || '');
} catch(e) {}
" 2>/dev/null) || true
    # Try jq as last resort
    elif command -v jq &>/dev/null; then
      key=$(jq -r ".skills.entries.${PRODUCT_NAME}.apiKey // \"\"" "$OPENCLAW_CONFIG" 2>/dev/null) || true
    fi

    if [[ -n "${key:-}" && "$key" != "null" ]]; then
      echo "$key"
      return 0
    fi
  fi

  return 1
}

# ─── JWT Payload Decoding ────────────────────────────────────────────────────
# Base64url decode the middle section of a JWT (header.PAYLOAD.signature)
# Uses 3 fallback methods for cross-platform support (Linux, macOS, Git Bash)

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

# ─── JSON Field Extraction ───────────────────────────────────────────────────
# Extract a field from a JSON string using whatever tool is available

extract_json_field() {
  local json="$1"
  local field="$2"

  # Sanitize the JSON for safe embedding in single quotes
  # Replace single quotes with escaped form
  local safe_json
  safe_json=$(printf '%s' "$json" | sed "s/'/\\\\'/g")

  if command -v python3 &>/dev/null; then
    python3 -c "
import json, sys
try:
    data = json.loads('''$safe_json''')
    val = data.get('$field', '')
    if val is None:
        val = ''
    print(str(val))
except Exception:
    print('')
" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "
try {
  const d = JSON.parse(\`$safe_json\`);
  console.log(d['$field'] != null ? String(d['$field']) : '');
} catch(e) { console.log(''); }
" 2>/dev/null
  elif command -v jq &>/dev/null; then
    printf '%s' "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    # Grep-based fallback for simple string/numeric values
    printf '%s' "$json" | grep -oE "\"$field\"[[:space:]]*:[[:space:]]*\"?[^\",$\}]+" 2>/dev/null | \
      sed -E "s/\"$field\"[[:space:]]*:[[:space:]]*\"?//" | \
      sed 's/"$//' || echo ""
  fi
}

# ─── License Validation ─────────────────────────────────────────────────────
# Validates JWT: decodes payload, checks issuer, product, expiry, and tier

validate_license() {
  local key="$1"
  local required_tier="${2:-pro}"

  # Decode JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[${PRODUCT_DISPLAY}]${NC} Invalid license key format." >&2
    echo -e "  ${DIM}Expected a valid JWT token.${NC}" >&2
    return 1
  fi

  # Check issuer
  local iss
  iss=$(extract_json_field "$payload" "iss")
  if [[ "$iss" != "license-api" ]]; then
    echo -e "${RED}[${PRODUCT_DISPLAY}]${NC} Invalid license issuer." >&2
    return 1
  fi

  # Check product
  local product
  product=$(extract_json_field "$payload" "product")
  if [[ "$product" != "$PRODUCT_NAME" ]]; then
    echo -e "${RED}[${PRODUCT_DISPLAY}]${NC} License is for ${BOLD}$product${NC}, not ${PRODUCT_NAME}." >&2
    echo -e "  ${DIM}Get a ${PRODUCT_NAME} license at: ${CYAN}${PRODUCT_URL}/pricing${NC}" >&2
    return 1
  fi

  # Check expiry
  local expiry
  expiry=$(extract_json_field "$payload" "exp")
  if [[ -n "$expiry" && "$expiry" != "0" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[${PRODUCT_DISPLAY}]${NC} License expired." >&2
      echo -e "  Renew at: ${CYAN}${PRODUCT_URL}/renew${NC}" >&2
      return 1
    fi
  fi

  # Check tier level
  local tier
  tier=$(extract_json_field "$payload" "tier")
  tier="${tier:-free}"

  local required_level="${TIER_LEVELS[$required_tier]:-1}"
  local actual_level="${TIER_LEVELS[$tier]:-0}"

  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[${PRODUCT_DISPLAY}]${NC} This feature requires ${BOLD}${required_tier}${NC} tier. You have: ${BOLD}${tier}${NC}" >&2
    echo -e "  Upgrade at: ${CYAN}${PRODUCT_URL}/upgrade${NC}" >&2
    return 1
  fi

  return 0
}

# ─── Public API: check_authaudit_license ─────────────────────────────────────
# Called by dispatcher.sh to gate features by tier

check_authaudit_license() {
  local required_tier="${1:-pro}"

  local key
  if ! key=$(get_authaudit_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}--- ${PRODUCT_DISPLAY} License Required ---${NC}" >&2
    echo "" >&2
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license." >&2
    echo "" >&2
    echo -e "Get your license at: ${CYAN}${BOLD}${PRODUCT_URL}/pricing${NC}" >&2
    echo "" >&2
    echo "Then configure it:" >&2
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}" >&2
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"${PRODUCT_NAME}\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}" >&2
    echo "" >&2
    echo -e "  ${DIM}# Or set the environment variable:${NC}" >&2
    echo -e "  ${CYAN}export AUTHAUDIT_LICENSE_KEY=\"YOUR_KEY\"${NC}" >&2
    echo "" >&2
    return 1
  fi

  validate_license "$key" "$required_tier"
}

# ─── Public API: get_authaudit_tier ──────────────────────────────────────────
# Returns the tier string (free, pro, team, enterprise) from the license JWT.
# Returns "free" if no valid license is found.

get_authaudit_tier() {
  local key
  if ! key=$(get_authaudit_key) || [[ -z "$key" ]]; then
    echo "free"
    return 0
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo "free"
    return 0
  fi

  # Verify product matches
  local product
  product=$(extract_json_field "$payload" "product")
  if [[ "$product" != "$PRODUCT_NAME" ]]; then
    echo "free"
    return 0
  fi

  # Check expiry before returning tier
  local expiry
  expiry=$(extract_json_field "$payload" "exp")
  if [[ -n "$expiry" && "$expiry" != "0" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo "free"
      return 0
    fi
  fi

  local tier
  tier=$(extract_json_field "$payload" "tier")
  echo "${tier:-free}"
}

# ─── Public API: get_authaudit_tier_level ────────────────────────────────────
# Returns the numeric tier level (0-3) for pattern gating

get_authaudit_tier_level() {
  local tier
  tier=$(get_authaudit_tier)
  echo "${TIER_LEVELS[$tier]:-0}"
}

# ─── Public API: get_pattern_limit ───────────────────────────────────────────
# Returns how many patterns the current tier can access (per category)
#   free=5 (30 total), pro=10 (60 total), team/enterprise=15 (90 total)

get_pattern_limit() {
  local tier_level
  tier_level=$(get_authaudit_tier_level)

  if [[ "$tier_level" -ge 2 ]]; then
    echo 15    # team/enterprise: all 15 per category (90 total)
  elif [[ "$tier_level" -ge 1 ]]; then
    echo 10    # pro: 10 per category (60 total)
  else
    echo 5     # free: 5 per category (30 total)
  fi
}

# ─── Public API: show_authaudit_status ───────────────────────────────────────
# Pretty-print license information for status command

show_authaudit_status() {
  local key
  if ! key=$(get_authaudit_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Patterns: 30 of 90 (5 per category)"
    echo -e "  Available: scan (limited patterns)"
    echo -e "  Upgrade at: ${CYAN}${PRODUCT_URL}/pricing${NC}"
    return
  fi

  local payload tier expiry seats email
  payload=$(decode_jwt_payload "$key" 2>/dev/null) || {
    echo -e "License: ${RED}Invalid key${NC}"
    return
  }

  # Verify product
  local product
  product=$(extract_json_field "$payload" "product")
  if [[ "$product" != "$PRODUCT_NAME" ]]; then
    echo -e "License: ${RED}Wrong product (${product})${NC}"
    echo -e "  This key is for ${BOLD}$product${NC}, not ${PRODUCT_NAME}."
    return
  fi

  tier=$(extract_json_field "$payload" "tier")
  expiry=$(extract_json_field "$payload" "exp")
  seats=$(extract_json_field "$payload" "seats")
  email=$(extract_json_field "$payload" "sub")

  # Determine active/expired status
  local now status_color status_text
  now=$(date +%s)
  status_color="$GREEN"
  status_text="Active"
  if [[ -n "$expiry" && "$expiry" != "0" && "$now" -gt "$expiry" ]]; then
    status_color="$RED"
    status_text="Expired"
  fi

  # Format expiry date (cross-platform)
  local expiry_date="Never"
  if [[ -n "$expiry" && "$expiry" != "0" ]]; then
    expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || \
                  date -r "$expiry" +%Y-%m-%d 2>/dev/null || \
                  echo "unknown")
  fi

  # Determine pattern count
  local pattern_count=30
  local tier_level="${TIER_LEVELS[$tier]:-0}"
  if [[ "$tier_level" -ge 2 ]]; then pattern_count=90
  elif [[ "$tier_level" -ge 1 ]]; then pattern_count=60
  fi

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  [[ -n "$email" && "$email" != "" ]] && echo -e "  Email: $email"
  echo -e "  Seats: ${seats:-1}"
  echo -e "  Expires: $expiry_date"
  echo -e "  Patterns: ${pattern_count} of 90"

  # Show available features based on tier
  echo ""
  echo -e "  ${BOLD}Available features:${NC}"
  echo -e "    scan (${pattern_count} patterns)"
  if [[ "$tier_level" -ge 1 ]]; then
    echo -e "    hooks install/uninstall"
    echo -e "    report"
  fi
  if [[ "$tier_level" -ge 2 ]]; then
    echo -e "    scan --format html"
    echo -e "    all 90 patterns"
  fi
}
