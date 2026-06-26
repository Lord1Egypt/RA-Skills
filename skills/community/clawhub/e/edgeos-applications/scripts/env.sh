#!/usr/bin/env bash
# Single source of runtime values for edgeos-applications v1
# Source this file from other scripts: source "$(dirname "$0")/env.sh"

BASE_URL="https://api-citizen-portal.simplefi.tech"
STATE_DIR="${STATE_DIR:-$(dirname "$0")/.state}"
JWT_STATE_CURRENT_EMAIL_FILE="$STATE_DIR/current_email"

sanitize_email() {
  local email="${1:-}"
  echo "$email" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g'
}

email_hash8() {
  local email="${1:-}"
  # sha256 preferred; fallback to shasum on systems without sha256sum
  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$email" | sha256sum | awk '{print substr($1,1,8)}'
  else
    printf '%s' "$email" | shasum -a 256 | awk '{print substr($1,1,8)}'
  fi
}

jwt_state_file_for_email() {
  local email="${1:-}"
  local base hash key
  base="$(sanitize_email "$email")"
  hash="$(email_hash8 "$email")"
  key="${base}__${hash}"
  echo "$STATE_DIR/jwt_${key}.token"
}

load_jwt_from_state() {
  mkdir -p "$STATE_DIR"

  # Prefer explicit session email when provided by caller.
  local email="${SESSION_EMAIL:-}"
  if [[ -z "$email" && -f "$JWT_STATE_CURRENT_EMAIL_FILE" ]]; then
    email="$(cat "$JWT_STATE_CURRENT_EMAIL_FILE" 2>/dev/null || true)"
  fi

  if [[ -n "$email" ]]; then
    local file
    file="$(jwt_state_file_for_email "$email")"
    if [[ -f "$file" ]]; then
      JWT="$(cat "$file" 2>/dev/null || true)"
      return 0
    fi
  fi

  JWT="${JWT:-}"
}

save_jwt_to_state() {
  local token="${1:-}"
  local email="${2:-${SESSION_EMAIL:-}}"

  if [[ -z "$token" || -z "$email" ]]; then
    return 0
  fi

  mkdir -p "$STATE_DIR"
  local file
  file="$(jwt_state_file_for_email "$email")"
  printf '%s' "$token" > "$file"
  printf '%s' "$email" > "$JWT_STATE_CURRENT_EMAIL_FILE"
}
