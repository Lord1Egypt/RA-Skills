#!/usr/bin/env bash
# ClawAlarm REST API wrapper.
#
# This script wraps the ClawAlarm cloud-sync API. The API is bearer-token
# authenticated; tokens are minted on-device through the pairing handshake.
# One token = one Durable Object = one phone. Bring a separate token per
# device.
#
# Usage:
#   alarm-api.sh [-m METHOD] [-d JSON_BODY] <endpoint>
#   alarm-api.sh pair <PAIRING_CODE> [--location=local|global]
#   alarm-api.sh auth login --token=<TOKEN> [--location=local|global]
#   alarm-api.sh auth status
#   alarm-api.sh auth logout [--location=local|global]
#   alarm-api.sh refresh
#   alarm-api.sh --help
#   alarm-api.sh --help <route>
#
# Full API spec: https://api.claw-alarm.com/openapi.json
# Live reference UI: https://api.claw-alarm.com/reference

set -euo pipefail

BASE_URL="${CLAW_ALARM_API_BASE_URL:-https://api.claw-alarm.com}"
SPEC_URL="${CLAW_ALARM_API_SPEC_URL:-${BASE_URL}/openapi.json}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOCAL_ENV_FILE="${SKILL_ROOT}/.env"
GLOBAL_CONFIG_DIR="${HOME}/.claw-alarm-cli"
GLOBAL_ENV_FILE="${GLOBAL_CONFIG_DIR}/.env"
AUTH_VALIDATE_ENDPOINT="/v1/account/status"

usage() {
  cat <<'EOF'
Usage:
  alarm-api.sh <endpoint>                         GET request
  alarm-api.sh -m POST -d '{"k":"v"}' <ep>        POST/PATCH/PUT/DELETE with body
  alarm-api.sh pair <PAIRING_CODE>                Exchange pairing code → save token
  alarm-api.sh auth login --token=<TOKEN>         Save an already-minted bearer token
  alarm-api.sh auth status                        Show which credential is active
  alarm-api.sh auth logout                        Remove a saved token
  alarm-api.sh refresh                            Mint a new pairing code on this account
  alarm-api.sh --help                             This overview + all routes
  alarm-api.sh --help <route>                     Full spec for one route
EOF
}

print_pair_help() {
  cat <<EOF
Pairing:
  alarm-api.sh pair <PAIRING_CODE> [--location=local|global]
      Exchange a 6-letter ABC-DEF code (shown on the iOS device after the
      user opens "Connect Claude" in the ClawAlarm app) for a long-lived
      bearer token, validate it, and save it.

      Codes expire 10 minutes after issue and are single-use. After a
      successful exchange, the iOS app and this CLI hold the SAME token
      — both are first-class clients of the device's Durable Object.

      One token is scoped to ONE device. To configure alarms on a second
      phone, run \`alarm-api.sh pair\` again from a separate location.

Refresh:
  alarm-api.sh refresh
      Generate a new pairing code on the currently-authenticated account
      (e.g. to pair an additional non-iOS client). Invalidates any
      previously-outstanding code for the account.
EOF
}

print_auth_help() {
  cat <<EOF
Auth:
  alarm-api.sh auth login --token=<TOKEN> [--location=local|global]
      Save and validate a bearer token directly. Prefer \`pair\` for the
      first-time handshake; use \`auth login\` only when you already have
      a token (e.g. from a teammate's CLAUDE.md).

      Default location: local (${LOCAL_ENV_FILE})
      Global location:  ${GLOBAL_ENV_FILE}

  alarm-api.sh auth status
      Show which credential source is active.

  alarm-api.sh auth logout [--location=local|global]
      Remove the saved token from the selected location.

Credential precedence for API calls:
  1. CLAW_ALARM_API_TOKEN from the current shell environment
  2. Local saved token at ${LOCAL_ENV_FILE}
  3. Global saved token at ${GLOBAL_ENV_FILE}

Local API testing:
  CLAW_ALARM_API_BASE_URL=http://127.0.0.1:8787 alarm-api.sh pair ABC-DEF

The bearer token is a SECRET in the cryptographic sense, but anyone
holding it can only configure alarms on the one device it was minted
for. Storing it in a project-local CLAUDE.md (or .env) is fine for
solo / personal-project use.
EOF
}

require_python3() {
  if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required" >&2
    exit 1
  fi
}

load_env_file() {
  local env_file="$1"

  [[ -f "${env_file}" ]] || return 1

  local line
  while IFS= read -r line || [[ -n "${line}" ]]; do
    line="${line#"${line%%[![:space:]]*}"}"
    [[ -z "${line}" || "${line}" == \#* ]] && continue
    if [[ "${line}" =~ ^CLAW_ALARM_API_TOKEN=(.*)$ ]]; then
      CLAW_ALARM_API_TOKEN="${BASH_REMATCH[1]}"
      CLAW_ALARM_API_TOKEN="${CLAW_ALARM_API_TOKEN%\"}"
      CLAW_ALARM_API_TOKEN="${CLAW_ALARM_API_TOKEN#\"}"
      CLAW_ALARM_API_TOKEN="${CLAW_ALARM_API_TOKEN%\'}"
      CLAW_ALARM_API_TOKEN="${CLAW_ALARM_API_TOKEN#\'}"
      export CLAW_ALARM_API_TOKEN
      return 0
    fi
  done < "${env_file}"

  return 1
}

resolve_token() {
  TOKEN_SOURCE="none"

  if [[ -n "${CLAW_ALARM_API_TOKEN:-}" ]]; then
    TOKEN_SOURCE="env"
    return 0
  fi

  if load_env_file "${LOCAL_ENV_FILE}"; then
    TOKEN_SOURCE="local"
    return 0
  fi

  if load_env_file "${GLOBAL_ENV_FILE}"; then
    TOKEN_SOURCE="global"
    return 0
  fi

  return 1
}

mask_token() {
  local token="$1"
  local length="${#token}"

  if (( length <= 8 )); then
    printf '%s\n' '********'
    return
  fi

  printf '%s...%s\n' "${token:0:4}" "${token: -4}"
}

write_token_file() {
  local env_file="$1"
  local token="$2"

  mkdir -p "$(dirname "${env_file}")"
  umask 077
  printf 'CLAW_ALARM_API_TOKEN=%s\n' "${token}" > "${env_file}"
}

delete_token_file() {
  local env_file="$1"

  if [[ -f "${env_file}" ]]; then
    rm -f "${env_file}"
    echo "Removed saved token at ${env_file}"
  else
    echo "No saved token found at ${env_file}"
  fi
}

validate_bearer_token() {
  local token="$1"
  local status

  status="$(
    curl -sS -o /dev/null -w '%{http_code}' \
      -H "Authorization: Bearer ${token}" \
      -H "Content-Type: application/json" \
      "${BASE_URL}${AUTH_VALIDATE_ENDPOINT}"
  )"

  [[ "${status}" == 2* ]]
}

api_request() {
  local endpoint="$1"
  local method="${2:-GET}"
  local data="${3:-}"

  local curl_args=(
    -sS
    -X "${method}"
    "${BASE_URL}${endpoint}"
    -H "Authorization: Bearer ${CLAW_ALARM_API_TOKEN}"
    -H "Content-Type: application/json"
  )

  if [[ -n "${data}" ]]; then
    curl_args+=(-d "${data}")
  fi

  curl "${curl_args[@]}"
}

handle_pair() {
  require_python3

  # $1 is "pair" (the subcommand) — drop it.
  shift || true
  local code="${1:-}"
  # Drop the code, if present, before parsing flags.
  if [[ $# -gt 0 ]]; then shift; fi
  local location="local"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --location=*) location="${1#*=}" ;;
      --location)   shift; location="${1:-}" ;;
      *) echo "Error: unknown pair argument: $1" >&2; exit 1 ;;
    esac
    shift
  done

  if [[ -z "${code}" ]]; then
    echo "Error: missing pairing code" >&2
    echo "Usage: alarm-api.sh pair <PAIRING_CODE>" >&2
    exit 1
  fi

  # Normalize: uppercase, strip spaces, ensure ABC-DEF.
  code="$(printf '%s' "${code}" | tr '[:lower:]' '[:upper:]' | tr -d '[:space:]')"
  if [[ ! "${code}" =~ ^[A-Z]{3}-[A-Z]{3}$ ]]; then
    if [[ "${code}" =~ ^[A-Z]{6}$ ]]; then
      code="${code:0:3}-${code:3:3}"
    else
      echo "Error: pairing code must match ABC-DEF (six A-Z letters, dash-separated)" >&2
      exit 1
    fi
  fi

  local target_file
  case "${location}" in
    local)  target_file="${LOCAL_ENV_FILE}" ;;
    global) target_file="${GLOBAL_ENV_FILE}" ;;
    *) echo "Error: invalid location '${location}'. Use local or global." >&2; exit 1 ;;
  esac

  local body
  body="$(printf '{"code":"%s"}' "${code}")"

  local response_file http_status
  response_file="$(mktemp)"
  http_status="$(
    curl -sS -o "${response_file}" -w '%{http_code}' \
      -X POST \
      -H "Content-Type: application/json" \
      -d "${body}" \
      "${BASE_URL}/v1/pairing/exchange"
  )"

  if [[ "${http_status}" != 2* ]]; then
    echo "Error: pairing exchange failed (HTTP ${http_status})" >&2
    cat "${response_file}" >&2
    echo >&2
    rm -f "${response_file}"
    exit 1
  fi

  local token
  token="$(
    python3 - "${response_file}" <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    payload = json.load(f)
token = payload.get("token")
if not token:
    sys.exit(1)
print(token)
PY
  )" || {
    echo "Error: response from /v1/pairing/exchange did not include a token" >&2
    cat "${response_file}" >&2
    rm -f "${response_file}"
    exit 1
  }
  rm -f "${response_file}"

  if ! validate_bearer_token "${token}"; then
    echo "Error: token returned by exchange did not validate against ${AUTH_VALIDATE_ENDPOINT}" >&2
    exit 1
  fi

  write_token_file "${target_file}" "${token}"
  echo "Paired. Saved validated token to ${target_file}"
  echo "Active token: $(mask_token "${token}")"
}

handle_refresh() {
  require_python3

  if ! resolve_token; then
    echo "Error: not authenticated. Run \`alarm-api.sh pair <CODE>\` first." >&2
    exit 1
  fi

  local response
  response="$(api_request "/v1/pairing/refresh" "POST")"
  echo "${response}" | python3 -m json.tool 2>/dev/null || echo "${response}"
}

handle_auth_login() {
  local location="local"
  local token=""
  local target_file=""

  shift 2
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --token=*)    token="${1#*=}" ;;
      --token)      shift; token="${1:-}" ;;
      --location=*) location="${1#*=}" ;;
      --location)   shift; location="${1:-}" ;;
      *) echo "Error: unknown auth login argument: $1" >&2; exit 1 ;;
    esac
    shift
  done

  if [[ -z "${token}" ]]; then
    echo "Error: missing required --token for auth login" >&2
    echo "       Prefer: alarm-api.sh pair <PAIRING_CODE>" >&2
    exit 1
  fi

  case "${location}" in
    local)  target_file="${LOCAL_ENV_FILE}" ;;
    global) target_file="${GLOBAL_ENV_FILE}" ;;
    *) echo "Error: invalid location '${location}'. Use local or global." >&2; exit 1 ;;
  esac

  if ! validate_bearer_token "${token}"; then
    echo "Error: token validation failed. Nothing was saved." >&2
    exit 1
  fi

  write_token_file "${target_file}" "${token}"
  echo "Saved validated token to ${target_file}"
}

handle_auth_status() {
  resolve_token || true

  case "${TOKEN_SOURCE}" in
    env)    echo "Auth source: env ($(mask_token "${CLAW_ALARM_API_TOKEN}"))" ;;
    local)  echo "Auth source: local ${LOCAL_ENV_FILE} ($(mask_token "${CLAW_ALARM_API_TOKEN}"))" ;;
    global) echo "Auth source: global ${GLOBAL_ENV_FILE} ($(mask_token "${CLAW_ALARM_API_TOKEN}"))" ;;
    none)
      echo "Auth source: none"
      echo "Run: alarm-api.sh pair <PAIRING_CODE>"
      ;;
  esac
}

handle_auth_logout() {
  local location="local"

  shift 2
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --location=*) location="${1#*=}" ;;
      --location)   shift; location="${1:-}" ;;
      *) echo "Error: unknown auth logout argument: $1" >&2; exit 1 ;;
    esac
    shift
  done

  case "${location}" in
    local)  delete_token_file "${LOCAL_ENV_FILE}" ;;
    global) delete_token_file "${GLOBAL_ENV_FILE}" ;;
    *) echo "Error: invalid location '${location}'. Use local or global." >&2; exit 1 ;;
  esac
}

handle_help() {
  require_python3

  local spec spec_file
  spec="$(curl -sS "${SPEC_URL}")"
  spec_file="$(mktemp)"
  printf '%s' "${spec}" > "${spec_file}"

  if [[ -z "${2:-}" ]]; then
    cat <<'HEADER'
ClawAlarm API V1 — Live Route Reference
=======================================
HEADER
    echo
    usage
    echo
    print_pair_help
    echo
    print_auth_help
    echo
    echo "Routes:"

    python3 - "${spec_file}" <<'PY'
import json, sys

with open(sys.argv[1]) as f:
    spec = json.load(f)

methods = ("get", "post", "put", "patch", "delete")

for path, path_item in spec.get("paths", {}).items():
    for method, op in path_item.items():
        if method not in methods:
            continue

        method_upper = method.upper()
        query_required = []
        for param in op.get("parameters") or []:
            if param.get("in") == "query" and param.get("required") is True:
                query_required.append(f"{param.get('name')}=...")
        qs = f"?{'&'.join(query_required)}" if query_required else ""

        body = None
        schema = (((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema")
        if schema is not None:
            required = schema.get("required")
            required = required if isinstance(required, list) else []
            if required:
                body = "{" + ",".join(f"\"{f}\":\"...\"" for f in required) + "}"
            else:
                body = "{...}"

        if method == "get":
            usage = f"alarm-api.sh {path}{qs}"
        elif body is not None:
            usage = f"alarm-api.sh -m {method_upper} -d '{body}' {path}"
        else:
            usage = f"alarm-api.sh -m {method_upper} {path}"

        padding = " " * max(0, 7 - len(method_upper))
        summary = op.get("summary") or op.get("operationId") or ""
        print(f"{padding}{method_upper}  {path}\t{summary}")
        print(f"     ↳ {usage}")
        print()
PY

    cat <<FOOTER
Tip: Run alarm-api.sh --help <route> for full details on any route above.
     e.g. alarm-api.sh --help /v1/account/alarms

Spec:      ${SPEC_URL}
Reference: ${BASE_URL}/reference
FOOTER
  else
    local route="$2"
    python3 - "${spec_file}" "${route}" <<'PY'
import json, sys

with open(sys.argv[1]) as f:
    spec = json.load(f)

route = sys.argv[2]
path_item = spec.get("paths", {}).get(route)
methods = ("get", "post", "put", "patch", "delete")

if path_item is None:
    print(f"No route found: {route}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Available routes:", file=sys.stderr)
    for path in spec.get("paths", {}).keys():
        print(path, file=sys.stderr)
    sys.exit(1)

payload = {"route": route, "methods": []}
for method, operation in path_item.items():
    if method not in methods:
        continue
    payload["methods"].append({
        "method": method,
        "operationId": operation.get("operationId"),
        "summary": operation.get("summary"),
        "description": operation.get("description"),
        "parameters": operation.get("parameters"),
        "requestBody": operation.get("requestBody"),
        "responses": [
            {"status": s, "description": r.get("description")}
            for s, r in (operation.get("responses") or {}).items()
        ],
    })

print(json.dumps(payload, indent=2))
PY
  fi

  rm -f "${spec_file}"
}

if [[ "${1:-}" == "--help" ]]; then
  handle_help "$@"
  exit 0
fi

if [[ "${1:-}" == "pair" ]]; then
  handle_pair "$@"
  exit 0
fi

if [[ "${1:-}" == "refresh" ]]; then
  handle_refresh
  exit 0
fi

if [[ "${1:-}" == "auth" ]]; then
  case "${2:-}" in
    login)  handle_auth_login  "$@" ;;
    status) handle_auth_status ;;
    logout) handle_auth_logout "$@" ;;
    *)
      echo "Error: expected one of: login, status, logout" >&2
      usage >&2
      exit 1
      ;;
  esac
  exit 0
fi

if ! resolve_token; then
  echo "Error: CLAW_ALARM_API_TOKEN not set and no saved credentials found." >&2
  echo "Run: alarm-api.sh pair <PAIRING_CODE>" >&2
  exit 1
fi

METHOD="GET"
DATA=""

while getopts "m:d:" opt; do
  case $opt in
    m) METHOD="$OPTARG" ;;
    d) DATA="$OPTARG" ;;
    *) usage >&2; exit 1 ;;
  esac
done
shift $((OPTIND - 1))

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 1
fi

ENDPOINT="$1"

CURL_ARGS=(
  -sS
  -X "$METHOD"
  "${BASE_URL}${ENDPOINT}"
  -H "Authorization: Bearer ${CLAW_ALARM_API_TOKEN}"
  -H "Content-Type: application/json"
)

if [[ -n "$DATA" ]]; then
  CURL_ARGS+=(-d "$DATA")
fi

curl "${CURL_ARGS[@]}"
