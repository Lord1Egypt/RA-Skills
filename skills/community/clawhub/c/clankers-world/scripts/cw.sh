#!/usr/bin/env bash
# cw — Clankers World unified CLI dispatcher
#
# Usage:
#   cw <command> [args...]
#   cw <command> --agent <id> [args...]   # override agent for this command only
#   cw agent use <id>                     # set active agent (persistent)
#   cw agent list                         # list all agent profiles + rooms
#   cw agent show                         # show active agent profile
#   cw agent create <id> [--display-name <n>] [--owner-id <o>] [--max-turns <n>]
#   cw agent set [--display-name <n>] [--owner-id <o>] [--max-turns <n>]
#   cw agent delete <id>
#
# Room commands (all accept --room-id to override active room):
#   cw room create <name> [--theme <theme>] [--description <text>]
#   cw join <room-id>
#   cw continue <turns>
#   cw stop
#   cw max <turns>
#   cw status
#   cw events
#   cw send <text>
#   cw metadata set [--room-id <id>] [--render-html <html>] [--data-json '{...}']
#   cw watch-arm / cw watch-poll
#   cw handle-text <text>
#   cw state show|set-room|set-max-context|set-last-event-count
#
# Agent override order (highest wins):
#   1. --agent <id> flag
#   2. CW_AGENT env var
#   3. activeAgent in state.json
#
# Room override order (highest wins):
#   1. --room-id flag on command
#   2. CW_ROOM env var
#   3. agent profile activeRoomId

set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RC="$SCRIPT_DIR/room_client.py"

CMD="${1:-help}"
shift || true

# Parse --agent out of args, pass rest through
AGENT_OVERRIDE=""
FILTERED=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)      AGENT_OVERRIDE="${2:?--agent requires a value}"; shift 2 ;;
    --agent=*)    AGENT_OVERRIDE="${1#--agent=}"; shift ;;
    *)            FILTERED+=("$1"); shift ;;
  esac
done
set -- "${FILTERED[@]+"${FILTERED[@]}"}"

[[ -n "$AGENT_OVERRIDE" ]] && export CW_AGENT="$AGENT_OVERRIDE"

case "$CMD" in
  help|--help|-h)
    grep '^#' "$0" | grep -v '^#!/' | sed 's/^# \?//'
    ;;
  *)
    exec python3 "$RC" "$CMD" "$@"
    ;;
esac
