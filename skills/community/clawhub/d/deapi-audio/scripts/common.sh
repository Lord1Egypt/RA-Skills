#!/usr/bin/env bash
# deAPI shared utilities - sourced by skill scripts
# Usage: source "$(dirname "$0")/common.sh"

DEAPI_BASE_URL="https://api.deapi.ai/api/v1/client"
DEAPI_POLL_INTERVAL="${DEAPI_POLL_INTERVAL:-10}"
DEAPI_MAX_POLLS="${DEAPI_MAX_POLLS:-30}"

deapi_check_deps() {
  for cmd in curl jq; do
    if ! command -v "$cmd" &>/dev/null; then
      echo "Error: $cmd is required but not installed" >&2
      exit 1
    fi
  done
}

deapi_check_auth() {
  if [[ -z "${DEAPI_API_KEY:-}" ]]; then
    # Try config.json fallback (written by skill setup flow)
    local config_file="${SCRIPT_DIR}/../config.json"
    if [[ -f "$config_file" ]]; then
      DEAPI_API_KEY=$(jq -r '.api_key // empty' "$config_file" 2>/dev/null)
      export DEAPI_API_KEY
    fi
  fi
  if [[ -z "${DEAPI_API_KEY:-}" ]]; then
    echo "Error: DEAPI_API_KEY not set and no config.json found" >&2
    echo "Get your API key at https://deapi.ai (free \$5 credit)" >&2
    exit 1
  fi
}

deapi_submit_json() {
  local endpoint="$1"
  local json_body="$2"
  curl -s -X POST "${DEAPI_BASE_URL}/${endpoint}" \
    -H "Authorization: Bearer ${DEAPI_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$json_body"
}

deapi_submit_form() {
  local endpoint="$1"
  shift
  curl -s -X POST "${DEAPI_BASE_URL}/${endpoint}" \
    -H "Authorization: Bearer ${DEAPI_API_KEY}" \
    "$@"
}

deapi_poll_result() {
  local request_id="$1"
  local label="${2:-Processing}"

  for ((i = 1; i <= DEAPI_MAX_POLLS; i++)); do
    sleep "$DEAPI_POLL_INTERVAL"

    local status_response
    status_response=$(curl -s "${DEAPI_BASE_URL}/request-status/${request_id}" \
      -H "Authorization: Bearer ${DEAPI_API_KEY}")

    local status
    status=$(echo "$status_response" | jq -r '.data.status // empty')

    case "$status" in
      done)
        # Unwrap .data envelope if present so callers can use .result_url directly
        echo "$status_response" | jq 'if .data then .data else . end'
        return 0
        ;;
      failed)
        local error
        error=$(echo "$status_response" | jq -r '.data.error // "Unknown error"')
        echo "Error: Job failed - $error" >&2
        return 1
        ;;
      *)
        echo "${label}... ($i/$DEAPI_MAX_POLLS)" >&2
        ;;
    esac
  done

  echo "Error: Timed out after $((DEAPI_MAX_POLLS * DEAPI_POLL_INTERVAL))s" >&2
  return 1
}

deapi_ensure_local_file() {
  local input="$1"
  local tmp_prefix="${2:-deapi}"

  if [[ "$input" =~ ^https?:// ]]; then
    local tmp_file
    tmp_file=$(mktemp "/tmp/${tmp_prefix}_XXXXXX")
    curl -s -o "$tmp_file" "$input"
    if [[ ! -s "$tmp_file" ]]; then
      echo "Error: Failed to download file from $input" >&2
      rm -f "$tmp_file"
      return 1
    fi
    echo "$tmp_file"
  else
    if [[ ! -f "$input" ]]; then
      echo "Error: File not found: $input" >&2
      return 1
    fi
    echo "$input"
  fi
}

deapi_extract_request_id() {
  local response="$1"
  local request_id
  request_id=$(echo "$response" | jq -r '.data.request_id // empty')
  if [[ -z "$request_id" ]]; then
    echo "Error: Failed to submit job" >&2
    echo "$response" >&2
    return 1
  fi
  echo "$request_id"
}
