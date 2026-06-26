#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${PRISMFY_BASE_URL:-https://api.prismfy.io}"
SEARCH_ENDPOINT="$BASE_URL/v1/search"
ME_ENDPOINT="$BASE_URL/v1/user/me"

die() { echo "ERROR: $*" >&2; exit 1; }

need() {
  command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"
}

need curl
need jq

usage() {
  cat <<'EOF'
Claim Verifier helper

Usage:
  claim-verify.sh --quota
  claim-verify.sh --claim "text to verify" [--engine google] [--lang en] [--time week]
  claim-verify.sh --raw --claim "text to verify"

Notes:
  - This helper runs Prismfy query calls for a single claim.
  - For full multi-claim verification, orchestrate multiple calls from the skill workflow.
EOF
}

show_quota() {
  curl -sS "$ME_ENDPOINT" \
    -H "Authorization: Bearer $PRISMFY_API_KEY" \
    | jq .
}

run_claim() {
  local claim="$1"
  local engines_json="$2"
  local lang="$3"
  local time_range="$4"
  local raw="$5"

  local body
  body=$(jq -n \
    --arg q "$claim" \
    --argjson engines "$engines_json" \
    --arg lang "$lang" \
    '{query: $q, engines: $engines, language: $lang, page: 1}')

  if [[ -n "$time_range" ]]; then
    body=$(echo "$body" | jq --arg t "$time_range" '. + {timeRange: $t}')
  fi

  local resp
  resp=$(curl -sS -X POST "$SEARCH_ENDPOINT" \
    -H "Authorization: Bearer $PRISMFY_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$body")

  if [[ "$raw" == "true" ]]; then
    echo "$resp" | jq .
    return
  fi

  echo "$resp" | jq -r '
    . as $root
    | "claim: " + ($root.query // "n/a"),
      "results: " + (($root.results|length|tostring) // "0"),
      "cached: " + (($root.cached|tostring) // "false"),
      "",
      ($root.results[]? | "- [" + (.engine // "n/a") + "] " + (.title // "untitled") + "\n  " + (.url // ""))
  '
}

quota_mode=false
raw=false
claim=""
lang="en"
time_range=""
engines='["google"]'

while [[ $# -gt 0 ]]; do
  case "$1" in
    --quota) quota_mode=true ;;
    --raw) raw=true ;;
    --claim) shift; claim="${1:-}" ;;
    --engine) shift; engines="[\"${1:-google}\"]" ;;
    --engines) shift; engines=$(echo "${1:-google}" | jq -Rc 'split(",")') ;;
    --lang) shift; lang="${1:-en}" ;;
    --time) shift; time_range="${1:-}" ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown arg: $1" ;;
  esac
  shift
done

if [[ "$quota_mode" == "true" ]]; then
  [[ -n "${PRISMFY_API_KEY:-}" ]] || die "PRISMFY_API_KEY is not set"
  show_quota
  exit 0
fi

[[ -n "$claim" ]] || { usage; die "--claim is required (unless --quota)"; }
[[ -n "${PRISMFY_API_KEY:-}" ]] || die "PRISMFY_API_KEY is not set"
run_claim "$claim" "$engines" "$lang" "$time_range" "$raw"
