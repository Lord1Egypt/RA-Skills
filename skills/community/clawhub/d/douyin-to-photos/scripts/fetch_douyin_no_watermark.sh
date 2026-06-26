#!/usr/bin/env bash
set -euo pipefail

API_PRIMARY_DEFAULT="https://www.tikwm.com/api/"
TIMEOUT_DEFAULT=20

usage() {
  cat <<'USAGE'
Usage:
  fetch_douyin_no_watermark.sh --url <douyin_share_url> [--api-primary <url>] [--api-fallback <url>] [--timeout <sec>]

Output:
  JSON to stdout.
  Success example:
    {"ok":true,"provider":"tikwm","video_url":"https://...mp4"}
  Error example:
    {"ok":false,"error_code":"api_failed","message":"..."}
USAGE
}

emit_error() {
  local code="$1"
  local message="$2"
  jq -nc --arg code "$code" --arg message "$message" '{ok:false,error_code:$code,message:$message}'
}

emit_success() {
  local provider="$1"
  local video_url="$2"
  jq -nc --arg provider "$provider" --arg video_url "$video_url" '{ok:true,provider:$provider,video_url:$video_url}'
}

require_bin() {
  local bin="$1"
  if ! command -v "$bin" >/dev/null 2>&1; then
    emit_error "missing_dependency" "Missing required command: $bin"
    exit 2
  fi
}

is_valid_douyin_url() {
  local value="$1"
  [[ "$value" =~ https?://[^[:space:]]+ ]] && [[ "$value" =~ (douyin\.com|iesdouyin\.com) ]]
}

call_tikwm() {
  local api_url="$1"
  local share_url="$2"
  local timeout_sec="$3"

  curl -fsS --max-time "$timeout_sec" \
    -X POST "$api_url" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "url=$share_url" \
    --data "hd=1" \
    --data "count=12"
}

call_fallback() {
  local api_url="$1"
  local share_url="$2"
  local timeout_sec="$3"

  curl -fsS --max-time "$timeout_sec" \
    -X POST "$api_url" \
    -H 'Content-Type: application/json' \
    --data "{\"url\":\"$share_url\"}"
}

extract_primary_video_url() {
  jq -r '.data.hdplay // .data.play // empty' | head -n 1
}

extract_fallback_video_url() {
  jq -r '.video_url // .data.video_url // .data.hdplay // .data.play // empty' | head -n 1
}

main() {
  require_bin curl
  require_bin jq

  local share_url=""
  local api_primary="$API_PRIMARY_DEFAULT"
  local api_fallback=""
  local timeout_sec="$TIMEOUT_DEFAULT"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --url)
        share_url="${2:-}"
        shift 2
        ;;
      --api-primary)
        api_primary="${2:-}"
        shift 2
        ;;
      --api-fallback)
        api_fallback="${2:-}"
        shift 2
        ;;
      --timeout)
        timeout_sec="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        emit_error "invalid_argument" "Unknown argument: $1"
        exit 2
        ;;
    esac
  done

  if [[ -z "$share_url" ]]; then
    emit_error "invalid_input" "Missing --url"
    exit 2
  fi

  if ! [[ "$timeout_sec" =~ ^[0-9]+$ ]] || [[ "$timeout_sec" -lt 5 ]] || [[ "$timeout_sec" -gt 60 ]]; then
    emit_error "invalid_input" "timeout must be an integer in [5,60]"
    exit 2
  fi

  if ! is_valid_douyin_url "$share_url"; then
    emit_error "invalid_url" "Input is not a valid Douyin share URL"
    exit 2
  fi

  local primary_raw=""
  local primary_code=""
  local primary_video=""

  if primary_raw="$(call_tikwm "$api_primary" "$share_url" "$timeout_sec" 2>/dev/null)"; then
    primary_code="$(printf '%s' "$primary_raw" | jq -r '.code // empty')"
    if [[ "$primary_code" == "0" ]]; then
      primary_video="$(printf '%s' "$primary_raw" | extract_primary_video_url)"
      if [[ -n "$primary_video" ]]; then
        emit_success "tikwm" "$primary_video"
        exit 0
      fi
    fi
  fi

  if [[ -n "$api_fallback" ]]; then
    local fallback_raw=""
    local fallback_video=""
    if fallback_raw="$(call_fallback "$api_fallback" "$share_url" "$timeout_sec" 2>/dev/null)"; then
      fallback_video="$(printf '%s' "$fallback_raw" | extract_fallback_video_url)"
      if [[ -n "$fallback_video" ]]; then
        emit_success "fallback" "$fallback_video"
        exit 0
      fi
    fi
  fi

  emit_error "api_failed" "All providers failed or returned empty video URL"
  exit 3
}

main "$@"
