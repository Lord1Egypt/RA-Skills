#!/bin/sh
# Thin wrapper over the public Agent-Readiness Audit MCP endpoint.
# Usage:
#   audit.sh scan <url-or-domain>
#   audit.sh rank <domain>
#   audit.sh list [category]
# Prints the raw JSON-RPC response. No credentials are used or needed.
set -eu
ENDPOINT="https://audit.gainsolutions.io/api/mcp"

json_escape() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
}

call() {
  curl -sS -m "$1" -X POST "$ENDPOINT" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -d "$2"
  echo
}

cmd="${1:-}"
arg="${2:-}"
case "$cmd" in
  scan)
    [ -n "$arg" ] || { echo "usage: audit.sh scan <url>" >&2; exit 2; }
    call 90 "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"scan_site\",\"arguments\":{\"url\":\"$(json_escape "$arg")\"}}}"
    ;;
  rank)
    [ -n "$arg" ] || { echo "usage: audit.sh rank <domain>" >&2; exit 2; }
    call 30 "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"get_index_rank\",\"arguments\":{\"domain\":\"$(json_escape "$arg")\"}}}"
    ;;
  list)
    if [ -n "$arg" ]; then
      call 30 "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"list_index\",\"arguments\":{\"category\":\"$(json_escape "$arg")\"}}}"
    else
      call 30 '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_index","arguments":{}}}'
    fi
    ;;
  *)
    echo "usage: audit.sh scan <url> | rank <domain> | list [category]" >&2
    exit 2
    ;;
esac
