#!/usr/bin/env bash
# canEYE guardrails for OpenClaw: ask canEYE before acting for the user.
#
# Talks only to the canEYE server: $CANEYE_URL, default https://mcp.caneye.ai.
# Reads one secret, $CANEYE_API_KEY (this AI's own canEYE key). It is passed to curl on stdin,
# never on the command line, and never printed.
#
#   caneye.sh check  <action> "<summary>" [amount] [target] [resource]
#   caneye.sh wait   <request_id> <action> [amount] [target] [resource]
#   caneye.sh status <request_id> <action> [amount] [target] [resource]
#   caneye.sh log    <action> "<summary>" [result] [request_id] [amount] [target] [resource]
#   caneye.sh rules
#
# Prints canEYE's JSON answer. Exit codes: 0 answered, 2 bad usage, 3 canEYE unreachable (treat as
# "ask the user"), 4 key missing or refused.

set -u

BASE="${CANEYE_URL:-https://mcp.caneye.ai}"
BASE="${BASE%/}"

die_usage() {
  sed -n '7,11p' "$0" | sed 's/^#   //' >&2
  exit 2
}

if [ -z "${CANEYE_API_KEY:-}" ]; then
  printf '%s\n' '{"error":"no_key","decision":"ask_first","reason":"CANEYE_API_KEY is not set. Ask the user before doing anything their canEYE rules cover."}'
  exit 4
fi

# A JSON string from any text: escape backslashes, quotes and control characters.
json_str() {
  local s=$1
  s=${s//\\/\\\\}
  s=${s//\"/\\\"}
  s=${s//$'\n'/\\n}
  s=${s//$'\r'/\\r}
  s=${s//$'\t'/\\t}
  s=$(printf '%s' "$s" | tr -d '\000-\010\013\014\016-\037')
  printf '"%s"' "$s"
}

is_amount() { [[ $1 =~ ^[0-9]+([.][0-9]+)?$ ]]; }

# Add "key": value to a JSON object being built in $BODY, skipping empty values.
add_str() { [ -n "$2" ] && BODY="$BODY,\"$1\":$(json_str "$2")"; return 0; }
add_amount() {
  [ -z "$2" ] && return 0
  if ! is_amount "$2"; then printf '%s\n' '{"error":"bad_amount","reason":"amount must be a plain number, like 49.99"}'; exit 2; fi
  BODY="$BODY,\"$1\":$2"
}

# call METHOD PATH [JSON body] [curl --data-urlencode args...]
call() {
  local method=$1 path=$2 body=${3:-}
  shift 3 2>/dev/null || shift $#
  local out status
  local args=(-sS -m 20 -X "$method" -H "content-type: application/json" -w '\n%{http_code}' -K -)
  if [ "$method" = "GET" ] && [ $# -gt 0 ]; then args=(-sS -m 20 -G -w '\n%{http_code}' -K - "$@"); fi
  [ -n "$body" ] && args+=(--data-binary "$body")
  if ! out=$(printf 'header = "authorization: Bearer %s"\n' "$CANEYE_API_KEY" | curl "${args[@]}" "$BASE$path" 2>/dev/null); then
    printf '%s\n' '{"error":"caneye_unreachable","decision":"ask_first","reason":"canEYE could not be reached. Ask the user directly before acting."}'
    exit 3
  fi
  status=${out##*$'\n'}
  out=${out%$'\n'*}
  printf '%s\n' "$out"
  case "$status" in
    2*) return 0 ;;
    401|403) exit 4 ;;
    5*|000) exit 3 ;;
    *) return 0 ;;
  esac
}

detail_args() { # request_id action amount target resource → --data-urlencode args in DQ
  DQ=()
  [ -n "${1:-}" ] && DQ+=(--data-urlencode "action=$1")
  if [ -n "${2:-}" ]; then is_amount "$2" || { printf '%s\n' '{"error":"bad_amount"}'; exit 2; }; DQ+=(--data-urlencode "amount=$2"); fi
  [ -n "${3:-}" ] && DQ+=(--data-urlencode "target=$3")
  [ -n "${4:-}" ] && DQ+=(--data-urlencode "resource=$4")
  return 0
}

valid_id() { [[ $1 =~ ^[A-Za-z0-9_-]{1,64}$ ]] || { printf '%s\n' '{"error":"bad_request_id"}'; exit 2; }; }

cmd=${1:-}
[ $# -gt 0 ] && shift
case "$cmd" in
  check)
    [ $# -ge 2 ] || die_usage
    BODY="{\"action\":$(json_str "$1"),\"summary\":$(json_str "$2")"
    add_amount amount "${3:-}"
    add_str target "${4:-}"
    add_str resource "${5:-}"
    call POST /v1/check "$BODY}"
    ;;
  status)
    [ $# -ge 2 ] || die_usage
    valid_id "$1"
    detail_args "$2" "${3:-}" "${4:-}" "${5:-}"
    call GET "/v1/approvals/$1" "" ${DQ[@]+"${DQ[@]}"}
    ;;
  wait)
    [ $# -ge 2 ] || die_usage
    valid_id "$1"
    detail_args "$2" "${3:-}" "${4:-}" "${5:-}"
    minutes=${CANEYE_WAIT_MINUTES:-30}
    [[ $minutes =~ ^[0-9]+$ ]] || minutes=30
    deadline=$(( $(date +%s) + minutes * 60 ))
    while :; do
      answer=$(call GET "/v1/approvals/$1" "" ${DQ[@]+"${DQ[@]}"})
      rc=$?
      if [ "$rc" -ne 0 ]; then printf '%s\n' "$answer"; exit "$rc"; fi
      case "$answer" in
        *'"status":"pending"'*) ;;
        *) printf '%s\n' "$answer"; exit 0 ;;
      esac
      if [ "$(date +%s)" -ge "$deadline" ]; then
        printf '%s\n' "$answer"
        exit 0
      fi
      sleep "${CANEYE_POLL_SECONDS:-15}"
    done
    ;;
  log)
    [ $# -ge 2 ] || die_usage
    BODY="{\"action\":$(json_str "$1"),\"summary\":$(json_str "$2")"
    case "${3:-completed}" in
      completed|failed|refused|not_attempted) BODY="$BODY,\"result\":\"${3:-completed}\"" ;;
      *) printf '%s\n' '{"error":"bad_result","reason":"result is completed, failed, refused or not_attempted"}'; exit 2 ;;
    esac
    add_str request_id "${4:-}"
    add_amount amount "${5:-}"
    add_str target "${6:-}"
    add_str resource "${7:-}"
    call POST /v1/log "$BODY}"
    ;;
  rules)
    call GET /v1/rules ""
    ;;
  *)
    die_usage
    ;;
esac
