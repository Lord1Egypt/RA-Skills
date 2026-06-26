#!/usr/bin/env bash
# Filed.dev API client — search and retrieve US business entity data
# Usage: filed.sh <command> [options]
# Commands: search, entity
# Requires: FILED_API_KEY env var or --api-key flag
# Get a free key at https://filed.dev/register

set -euo pipefail

BASE_URL="https://filed.dev/api/v1"
API_KEY="${FILED_API_KEY:-}"

usage() {
  cat <<'EOF'
Usage: filed.sh <command> [options]

Commands:
  search    Search business entities
  entity    Get full entity details

Search options:
  --name <name>           Business name (required unless --agent or --filing-number used)
  --state <ST>            Two-letter state code (required)
  --agent <name>          Search by registered agent name
  --officer <name>        Search by officer/director name
  --filing-number <num>   Look up by state filing number
  --status <status>       Filter: active, inactive, all (default: all)
  --type <type>           Filter: llc, corporation, lp
  --formed-after <date>   Only entities formed after YYYY-MM-DD
  --formed-before <date>  Only entities formed before YYYY-MM-DD
  --exact                 Exact name match
  --limit <n>             Results per page, max 50 (default: 10)
  --offset <n>            Pagination offset (default: 0)

Entity options:
  <id>                    Entity ID from search results

Global options:
  --api-key <key>         API key (or set FILED_API_KEY env var)
  --raw                   Output raw JSON (default: formatted)

Examples:
  filed.sh search --name "Acme" --state FL
  filed.sh search --agent "CSC Global" --state NY --status active
  filed.sh search --officer "John Smith" --state PA
  filed.sh entity ent_mNqR7xKp
EOF
  exit 1
}

die() { echo "Error: $1" >&2; exit 1; }

# Parse global options first
RAW=false
COMMAND=""
ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --api-key) API_KEY="$2"; shift 2 ;;
    --raw) RAW=true; shift ;;
    search|entity) COMMAND="$1"; shift; ARGS=("$@"); break ;;
    -h|--help) usage ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

[[ -z "$API_KEY" ]] && die "No API key. Set FILED_API_KEY or use --api-key. Get one free at https://filed.dev/register"
[[ -z "$COMMAND" ]] && usage

format_json() {
  if command -v jq &>/dev/null; then
    jq .
  else
    cat
  fi
}

format_search() {
  if [[ "$RAW" == "true" ]] || ! command -v jq &>/dev/null; then
    cat
    return
  fi
  jq -r '
    "Found \(.meta.total) result(s) in \(.meta.state // "all states") [\(.meta.source // "")]",
    "",
    (.data[] |
      "  \(.name)",
      "    ID: \(.id)  |  Type: \(.type)  |  Status: \(.status)",
      "    Formed: \(.formedDate // "N/A")  |  Officers: \(.officerCount // 0)",
      (if .registeredAgent then "    Agent: \(.registeredAgent.name)" else empty end),
      (if .principalAddress then "    Address: \(.principalAddress)" else empty end),
      ""
    )
  '
}

format_entity() {
  if [[ "$RAW" == "true" ]] || ! command -v jq &>/dev/null; then
    cat
    return
  fi
  jq -r '
    .data |
    "\(.name)",
    "  State: \(.state)  |  Type: \(.type)  |  Status: \(.status)",
    "  Filing #: \(.stateEntityId // "N/A")  |  Formed: \(.formedDate // "N/A")",
    (if .registeredAgent then "  Registered Agent: \(.registeredAgent.name)\n    \(.registeredAgent.address // "")" else empty end),
    (if .principalAddress then "  Principal Address: \(.principalAddress)" else empty end),
    "",
    (if (.officers // [] | length) > 0 then
      "  Officers:",
      (.officers[] | "    \(.title // "Officer"): \(.name)")
    else empty end),
    "",
    (if (.filings // [] | length) > 0 then
      "  Filing History:",
      (.filings[] | "    \(.date)  \(.type)")
    else empty end)
  '
}

cmd_search() {
  local name="" state="" agent="" officer="" filing_number=""
  local status="" type="" formed_after="" formed_before=""
  local exact="" limit="" offset=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) name="$2"; shift 2 ;;
      --state) state="$2"; shift 2 ;;
      --agent) agent="$2"; shift 2 ;;
      --officer) officer="$2"; shift 2 ;;
      --filing-number) filing_number="$2"; shift 2 ;;
      --status) status="$2"; shift 2 ;;
      --type) type="$2"; shift 2 ;;
      --formed-after) formed_after="$2"; shift 2 ;;
      --formed-before) formed_before="$2"; shift 2 ;;
      --exact) exact="true"; shift ;;
      --limit) limit="$2"; shift 2 ;;
      --offset) offset="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$state" ]] && die "--state is required"

  local url="${BASE_URL}/search?state=${state}"
  [[ -n "$name" ]] && url+="&name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$name'))" 2>/dev/null || echo "$name")"
  [[ -n "$agent" ]] && url+="&agent=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$agent'))" 2>/dev/null || echo "$agent")"
  [[ -n "$officer" ]] && url+="&officer=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$officer'))" 2>/dev/null || echo "$officer")"
  [[ -n "$filing_number" ]] && url+="&filing_number=${filing_number}"
  [[ -n "$status" ]] && url+="&status=${status}"
  [[ -n "$type" ]] && url+="&type=${type}"
  [[ -n "$formed_after" ]] && url+="&formed_after=${formed_after}"
  [[ -n "$formed_before" ]] && url+="&formed_before=${formed_before}"
  [[ -n "$exact" ]] && url+="&exact=true"
  [[ -n "$limit" ]] && url+="&limit=${limit}"
  [[ -n "$offset" ]] && url+="&offset=${offset}"

  curl -sS "$url" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" | format_search
}

cmd_entity() {
  local id="${1:-}"
  [[ -z "$id" ]] && die "Entity ID required. Get IDs from search results."

  curl -sS "${BASE_URL}/entity/${id}" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Content-Type: application/json" | format_entity
}

case "$COMMAND" in
  search) cmd_search "${ARGS[@]}" ;;
  entity) cmd_entity "${ARGS[@]}" ;;
  *) usage ;;
esac
