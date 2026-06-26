#!/usr/bin/env bash
# 8k4.sh — Thin wrapper for 8K4 Protocol API calls
# Handles: auth header, default chain, dry-run enforcement
set -euo pipefail

BASE_URL="https://api.8k4protocol.com"
API_KEY="${EIGHTK4_API_KEY:-}"
DEFAULT_CHAIN="${EIGHTK4_DEFAULT_CHAIN:-eth}"

usage() {
  cat <<EOF
Usage: 8k4.sh <command> [options]

Commands:
  health                                  Health check
  stats                                   Protocol stats (public)
  top [--limit N] [--chain C]             Top agents
  score <id> [--chain C]                  Trust score
  explain <id> [--chain C]                Trust score with explanation
  validations <id> [--chain C] [--limit N]
                                          Validation history (paid/x402)
  search <query> [--chain C] [--contactable] [--min-score N] [--limit N]
  card <id> [--chain C] [--query Q]
  wallet-agents <addr> [--chain C]        Wallet lookup (paid/x402)
  wallet-score <addr> [--chain C]         Wallet-level score (paid/x402)
  identity <global_id>                    Identity lookup (paid/x402)
  contact <id> --task "..." [--chain C] [--dry-run]
  dispatch --task "..." [--max N] [--chain C] [--dry-run]
  metadata <id> [--chain C]               Read metadata envelope
  key-info                                Current key info

Options:
  --chain C       Chain: eth, base, bsc (default: $DEFAULT_CHAIN)
  --dry-run       Preview only (contact/dispatch; default: live send)

Environment:
  EIGHTK4_API_KEY        API key
  EIGHTK4_DEFAULT_CHAIN  Default chain (default: eth)
EOF
  exit 1
}

# Build auth header
auth_header() {
  if [[ -n "$API_KEY" ]]; then
    echo "-H" "X-API-Key: $API_KEY"
  fi
}

# GET request
api_get() {
  local path="$1"
  curl -s $(auth_header) "${BASE_URL}${path}"
}

# POST request (JSON body)
api_post() {
  local path="$1"
  local body="${2:-{}}"
  curl -s -X POST $(auth_header) \
    -H "Content-Type: application/json" \
    -d "$body" \
    "${BASE_URL}${path}"
}

# Parse common flags
CHAIN="$DEFAULT_CHAIN"
DRY_RUN=false
LIMIT=""
MIN_SCORE=""
CONTACTABLE=""
TASK=""
QUERY=""
MAX=""

parse_flags() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --chain) CHAIN="$2"; shift 2 ;;
      --dry-run) DRY_RUN=true; shift ;;
      --limit) LIMIT="$2"; shift 2 ;;
      --min-score) MIN_SCORE="$2"; shift 2 ;;
      --contactable) CONTACTABLE=true; shift ;;
      --task) TASK="$2"; shift 2 ;;
      --query) QUERY="$2"; shift 2 ;;
      --max) MAX="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
}

[[ $# -lt 1 ]] && usage

CMD="$1"; shift

case "$CMD" in
  health)
    api_get "/health"
    ;;

  stats)
    api_get "/stats/public"
    ;;

  top)
    parse_flags "$@"
    params="chain=${CHAIN}"
    [[ -n "$LIMIT" ]] && params="${params}&limit=${LIMIT}"
    api_get "/agents/top?${params}"
    ;;

  score)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh score <agent_id> [--chain C]"; exit 1; }
    ID="$1"; shift
    parse_flags "$@"
    api_get "/agents/${ID}/score?chain=${CHAIN}"
    ;;

  explain)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh explain <agent_id> [--chain C]"; exit 1; }
    ID="$1"; shift
    parse_flags "$@"
    api_get "/agents/${ID}/score/explain?chain=${CHAIN}"
    ;;

  validations)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh validations <agent_id> [--chain C] [--limit N]"; exit 1; }
    ID="$1"; shift
    parse_flags "$@"
    params="chain=${CHAIN}"
    [[ -n "$LIMIT" ]] && params="${params}&limit=${LIMIT}"
    api_get "/agents/${ID}/validations?${params}"
    ;;

  search)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh search <query> [flags]"; exit 1; }
    Q="$1"; shift
    parse_flags "$@"
    params="q=$(echo "$Q" | sed 's/ /+/g')&chain=${CHAIN}"
    [[ -n "$LIMIT" ]] && params="${params}&limit=${LIMIT}"
    [[ -n "$MIN_SCORE" ]] && params="${params}&min_score=${MIN_SCORE}"
    [[ "$CONTACTABLE" == "true" ]] && params="${params}&contactable=true"
    api_get "/agents/search?${params}"
    ;;

  card)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh card <agent_id> [--chain C] [--query Q]"; exit 1; }
    ID="$1"; shift
    parse_flags "$@"
    params="chain=${CHAIN}"
    [[ -n "$QUERY" ]] && params="${params}&q=$(echo "$QUERY" | sed 's/ /+/g')"
    api_get "/agents/${ID}/card?${params}"
    ;;

  wallet-agents)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh wallet-agents <address> [--chain C]"; exit 1; }
    ADDR="$1"; shift
    parse_flags "$@"
    api_get "/wallet/${ADDR}/agents?chain=${CHAIN}"
    ;;

  wallet-score)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh wallet-score <address> [--chain C]"; exit 1; }
    ADDR="$1"; shift
    parse_flags "$@"
    api_get "/wallet/${ADDR}/score?chain=${CHAIN}"
    ;;

  identity)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh identity <global_id>"; exit 1; }
    api_get "/identity/$1"
    ;;

  contact)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh contact <agent_id> --task '...' [--chain C] [--dry-run]"; exit 1; }
    ID="$1"; shift
    parse_flags "$@"
    [[ -z "$TASK" ]] && { echo "Error: --task is required"; exit 1; }
    SEND=$( [[ "$DRY_RUN" == "true" ]] && echo "false" || echo "true" )
    BODY=$(cat <<JSON
{"task": "$TASK", "chain": "$CHAIN", "dry_run": $DRY_RUN, "send": $SEND}
JSON
    )
    api_post "/agents/${ID}/contact" "$BODY"
    ;;

  dispatch)
    parse_flags "$@"
    [[ -z "$TASK" ]] && { echo "Error: --task is required"; exit 1; }
    SEND=$( [[ "$DRY_RUN" == "true" ]] && echo "false" || echo "true" )
    BODY=$(cat <<JSON
{"task": "$TASK", "max": ${MAX:-3}, "chain": ${CHAIN:+\"$CHAIN\"}, "dry_run": $DRY_RUN, "send": $SEND}
JSON
    )
    BODY=$(echo "$BODY" | sed 's/"chain": ,/"chain": null,/')
    api_post "/agents/dispatch" "$BODY"
    ;;

  metadata)
    [[ $# -lt 1 ]] && { echo "Usage: 8k4.sh metadata <agent_id> [--chain C]"; exit 1; }
    ID="$1"; shift
    parse_flags "$@"
    api_get "/agents/${ID}/metadata.json?chain=${CHAIN}"
    ;;

  key-info)
    api_get "/keys/info"
    ;;

  *)
    echo "Unknown command: $CMD"
    usage
    ;;
esac
