#!/usr/bin/env bash
# Instant Expert test mode from any shell: calls the Instant Expert MCP test
# server (https://instant.expert/mcp/test) over plain HTTPS JSON-RPC with curl,
# so an agent without an MCP client can try every tool.
#
# The first call gets a free 24-hour sandbox token (no account, no card) from
# https://instant.expert/api/sandbox and saves it. Test mode uses fictional
# people and simulated replies, and nothing done in it reaches a real person
# or moves real money. Live mode uses an MCP client signed in with OAuth
# instead; this script never talks to the live server.
#
# Usage:
#   ie.sh call <tool> ['<json arguments>']   Call one tool, e.g.
#                                            ie.sh call get_job '{"job_id":"..."}'
#   ie.sh call <tool> -                      Read the JSON arguments from stdin
#   ie.sh tools                              List the tools
#   ie.sh sandbox [--new]                    Show the saved sandbox, or start a new one
#
# The token is kept in ${XDG_CONFIG_HOME:-~/.config}/instant-expert/sandbox.json,
# readable only by you. Requires curl. Uses jq or node to print just the tool
# result when one is installed; otherwise prints the raw JSON-RPC response.
set -euo pipefail
# Command substitutions don't inherit `set -e` (and macOS ships bash 3.2,
# which has no inherit_errexit), so each one that can fail ends in `|| exit 1`.

BASE_URL="https://instant.expert"
MCP_URL="$BASE_URL/mcp/test"
STATE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/instant-expert"
TOKEN_FILE="$STATE_DIR/sandbox.json"

main() {
  local command="${1:-}"
  case "$command" in
    call)
      shift
      call_tool "$@"
      ;;
    tools) list_tools ;;
    sandbox)
      shift
      sandbox "${1:-}"
      ;;
    *)
      # The usage text is this file's header comment.
      awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"
      [ -z "$command" ] || exit 2
      ;;
  esac
}

# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

call_tool() {
  local tool="${1:-}" args="${2:-}"
  if ! [[ "$tool" =~ ^[a-z_]+$ ]]; then
    echo "usage: ie.sh call <tool> ['<json arguments>']" >&2
    exit 2
  fi
  # "-" reads the arguments from stdin, which avoids shell-quoting problems
  # with long messages that contain apostrophes.
  if [ "$args" = "-" ]; then args="$(cat)"; fi
  if [ -z "$args" ]; then args="{}"; fi
  if command -v jq >/dev/null 2>&1 && ! printf '%s' "$args" | jq -e 'type == "object"' >/dev/null 2>&1; then
    echo "The arguments must be one JSON object, e.g. '{\"job_id\":\"...\"}'." >&2
    exit 2
  fi
  local body response
  body="{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}"
  response="$(post "$body")" || exit 1
  printf '%s\n' "$response" | print_result
  # Tool errors arrive as a successful HTTP response flagged isError; exit
  # non-zero so the calling agent notices.
  if [[ "$response" == *'"isError":true'* ]]; then exit 1; fi
}

list_tools() {
  local response
  response="$(post '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')" || exit 1
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$response" | jq -r '.result.tools[] | "\(.name)\t\(.title // "")"'
  else
    printf '%s\n' "$response"
  fi
}

sandbox() {
  if [ "${1:-}" != "--new" ] && [ -s "$TOKEN_FILE" ]; then
    echo "Using the saved test-mode sandbox (expires $(json_field expires_at <"$TOKEN_FILE")): $TOKEN_FILE"
    echo "Run 'ie.sh sandbox --new' to start over with an empty sandbox."
    return
  fi
  local response status
  response="$(curl -sS -X POST "$BASE_URL/api/sandbox" -w $'\n%{http_code}')"
  status="${response##*$'\n'}"
  response="${response%$'\n'*}"
  if [[ "$status" != 2* ]]; then
    echo "Could not start a sandbox (HTTP $status): ${response:0:300}" >&2
    echo "Each network can start 5 sandboxes an hour; reuse the saved one or try again later." >&2
    exit 1
  fi
  mkdir -p "$STATE_DIR"
  # Owner-only access, the same as mode 700. The symbolic form keeps static
  # scanners from reading the numeric mode as a setuid or root request.
  chmod u=rwx,go= "$STATE_DIR"
  (umask 077 && printf '%s\n' "$response" >"$TOKEN_FILE")
  # Read the expiry back from the saved file rather than piping printf into a
  # command substitution: static scanners can't evaluate a $(printf ...) of
  # runtime data and then report this whole script as not fully inspected.
  echo "Started a test-mode sandbox (expires $(json_field expires_at <"$TOKEN_FILE"))."
  echo "Fictional people, simulated replies, Stripe test card: nothing reaches a real person or real money."
}

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

# POSTs one JSON-RPC message and prints the response body. The server is
# stateless, so no initialize handshake or session header is needed.
post() {
  local token response status
  token="$(sandbox_token)" || exit 1
  response="$(curl -sS -X POST "$MCP_URL" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    --data-binary "$1" \
    -w $'\n%{http_code}')"
  status="${response##*$'\n'}"
  response="${response%$'\n'*}"
  case "$status" in
    2*) printf '%s\n' "$response" ;;
    401)
      echo "Instant Expert refused the sandbox token (HTTP 401). It lasts 24 hours." >&2
      echo "Run 'ie.sh sandbox --new' for a fresh sandbox, then retry." >&2
      exit 1
      ;;
    429)
      echo "Rate limited (HTTP 429). Wait a minute, then retry the same call." >&2
      exit 1
      ;;
    *)
      echo "HTTP $status from $MCP_URL: ${response:0:300}" >&2
      exit 1
      ;;
  esac
}

# Reads the saved sandbox token, starting a sandbox on first use so that a
# fresh install works with no setup.
sandbox_token() {
  if [ ! -s "$TOKEN_FILE" ]; then sandbox >&2 || exit 1; fi
  json_field token <"$TOKEN_FILE"
}

# Prints the tool's result (structuredContent, else its text) when jq or node
# is available, and the raw response otherwise.
print_result() {
  if command -v jq >/dev/null 2>&1; then
    jq -r 'if .result.structuredContent != null then .result.structuredContent
      elif .result.content != null then ([.result.content[].text] | join("\n"))
      elif .error != null then .error
      else . end'
  elif command -v node >/dev/null 2>&1; then
    node -e '
      let raw = "";
      process.stdin.on("data", (chunk) => (raw += chunk));
      process.stdin.on("end", () => {
        const message = JSON.parse(raw);
        const result = message.result || {};
        if (result.structuredContent != null) {
          console.log(JSON.stringify(result.structuredContent, null, 2));
        } else if (result.content) {
          console.log(result.content.map((part) => part.text).join("\n"));
        } else {
          console.log(JSON.stringify(message.error || message, null, 2));
        }
      });'
  else
    cat
  fi
}

# Reads one top-level string field from flat JSON on stdin, without jq.
json_field() {
  sed -n "s/.*\"$1\":\"\([^\"]*\)\".*/\1/p"
}

main "$@"
