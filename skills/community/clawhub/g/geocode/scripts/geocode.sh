#!/usr/bin/env bash
set -euo pipefail

usage() {
  local exit_code="${1:-2}"
  cat >&2 <<'EOF'
Usage:
  geocode.sh hint
  geocode.sh reverse <latitude> <longitude> [--lang <code>] [--user-agent <ua>]

Examples:
  geocode.sh hint
  geocode.sh reverse 37.819929 -122.478255 --lang en

Environment:
  GEOCODE_BASE_URL     Override the geocode provider base URL.
  GEOCODE_USER_AGENT   Override the default User-Agent string.
EOF
  exit "$exit_code"
}

is_decimal() {
  [[ "${1:-}" =~ ^-?[0-9]+([.][0-9]+)?$ ]]
}

curl_json() {
  curl -fsSL "$@"
  printf '\n'
}

curl_hint() {
  local response
  response="$(
    curl -sSL \
      -A "$user_agent" \
      -w $'\n%{http_code}' \
      "${base_url%/}/"
  )"
  local http_code="${response##*$'\n'}"
  local body="${response%$'\n'*}"
  if [[ "$http_code" != "400" && "$http_code" != "200" ]]; then
    echo "Unexpected HTTP status from geocode provider root: $http_code" >&2
    if [[ "$body" != "" ]]; then
      printf '%s\n' "$body" >&2
    fi
    exit 1
  fi
  printf '%s\n' "$body"
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage 0
fi

command="${1:-}"
shift || true

base_url="${GEOCODE_BASE_URL:-https://geocode.com.cn}"
user_agent="${GEOCODE_USER_AGENT:-openclaw-geocode-skill/1.0 (interactive use)}"

case "$command" in
  hint)
    if [[ $# -gt 0 ]]; then
      echo "hint does not accept extra arguments" >&2
      usage
    fi
    curl_hint
    ;;
  search)
    echo "Unsupported command: search" >&2
    echo "geocode.com.cn currently supports reverse geocoding only (lat/lon query)." >&2
    exit 1
    ;;
  reverse)
    latitude="${1:-}"
    longitude="${2:-}"
    if [[ "$latitude" == "" || "$longitude" == "" ]]; then
      echo "Missing latitude/longitude" >&2
      usage
    fi
    shift 2 || true

    lang=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --lang)
          lang="${2:-}"
          shift 2
          ;;
        --user-agent)
          user_agent="${2:-}"
          shift 2
          ;;
        *)
          echo "Unknown arg: $1" >&2
          usage
          ;;
      esac
    done

    if ! is_decimal "$latitude"; then
      echo "Invalid latitude: $latitude" >&2
      exit 1
    fi
    if ! is_decimal "$longitude"; then
      echo "Invalid longitude: $longitude" >&2
      exit 1
    fi
    args=(
      --get
      "${base_url%/}/"
      -A "$user_agent"
      --data "lat=$latitude"
      --data "lon=$longitude"
    )

    if [[ "$lang" != "" ]]; then
      args+=(--data-urlencode "accept-language=$lang")
    fi
    curl_json "${args[@]}"
    ;;
  *)
    echo "Unknown command: $command" >&2
    usage
    ;;
esac
