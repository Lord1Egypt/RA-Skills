#!/usr/bin/env bash
# Native companion entry points. Invoke scripts with their interpreter so a
# text-only ClawHub installation does not require broad executable-bit repair.
set -euo pipefail
REAL_PATH="$(readlink -f "$0")"
SKILL_DIR="$(dirname "$(dirname "$REAL_PATH")")"
command="${1:-help}"; shift || true
host="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
SCRIPTS_DIR="$SKILL_DIR/scripts"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"
remote_peer_ids() { jq -r 'to_entries[] | select((.value | type)=="object" and (.value.url? | type)=="string" and .value.self != true) | .key' "$PEERS_FILE"; }
cmd_msg() {
  # Quick send: native transport by default; prompts if no message
  local peer="${1:-}"
  shift || true

  if [[ -z "$peer" ]]; then
    # If only one remote peer, use it; otherwise list and ask
    local remote_peers
    remote_peers=$(remote_peer_ids)
    local peer_count
    peer_count=$(echo "$remote_peers" | grep -c '.' || echo "0")

    if [[ "$peer_count" -eq 1 ]]; then
      peer="$remote_peers"
      echo "→ Sending to: $peer"
    else
      echo "Available peers:"
      echo "$remote_peers" | while read -r p; do
        local dn
        dn=$(jq -r --arg p "$p" '.[$p].display_name // "—"' "$PEERS_FILE" 2>/dev/null)
        echo "  $p ($dn)"
      done
      echo ""
      read -rp "Peer: " peer
    fi
  fi

  # Parse msg options; stay plain/original unless --user is explicitly supplied.
  local explicit_user=""
  local msg_session=""
  local msg_subject=""
  local msg_reply_to=""
  local msg_dry_run=false
  local positional=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --user) explicit_user="$2"; shift 2 ;;
      --session) msg_session="$2"; shift 2 ;;
      --subject) msg_subject="$2"; shift 2 ;;
      --reply-to) msg_reply_to="$2"; shift 2 ;;
      --dry-run) msg_dry_run=true; shift ;;
      -h|--help) bash "$SKILL_DIR/bin/antenna.sh" help; return ;;
      *) positional+=("$1"); shift ;;
    esac
  done

  # Get message from remaining args or prompt
  local message=""
  if [[ ${#positional[@]} -gt 0 ]]; then
    message="${positional[*]}"
  else
    echo "Type your message (Ctrl-D or empty line to send):"
    local line
    while IFS= read -r line; do
      [[ -z "$line" && -n "$message" ]] && break
      if [[ -n "$message" ]]; then
        message="${message}
${line}"
      else
        message="$line"
      fi
    done
  fi

  if [[ -z "$message" ]]; then
    echo "No message entered. Cancelled." >&2
    exit 1
  fi

  echo ""
  local send_args=("$peer")
  [[ -n "$msg_session" ]] && send_args+=(--session "$msg_session")
  [[ -n "$msg_subject" ]] && send_args+=(--subject "$msg_subject")
  [[ -n "$msg_reply_to" ]] && send_args+=(--reply-to "$msg_reply_to")
  [[ "$msg_dry_run" == true ]] && send_args+=(--dry-run)

  if [[ -n "$explicit_user" ]]; then
    echo "Sending as $explicit_user to $peer..."
    send_args+=(--user "$explicit_user")
  else
    echo "Sending from $(hostname) to $peer..."
  fi

  send_args+=("$message")
  bash "$SCRIPTS_DIR/antenna-send.sh" "${send_args[@]}"
}

case "$command" in
  help|-h|--help)
    cat <<'HELP'
Antenna for OpenClaw — native companion
  antenna msg|send PEER [--session DESTINATION] MESSAGE
  antenna send @LIST MESSAGE
  antenna peers list
  antenna health PEER                    Read-only remote health endpoint
  antenna contacts export HOST OUTPUT
  antenna contacts import CONTACT EXPECTED_PEER DEFAULT_TARGET
  antenna groups list|install|refresh|remove|send ...
  antenna clawreef --help
  antenna doctor [--gateway HOST]
  antenna readiness [--json] [--gateway HOST]
  antenna backup --help
  antenna status
  antenna plugin HOST status|init|mode|check|select|rules|inbox ...
  antenna mcs ...       Acquisition guidance for optional diagnostics

Select the host with OPENCLAW_CONFIG_PATH or the explicit plugin HOST argument.
Fresh setup: references/USER-GUIDE.md. Migration: plugin/OPTIONAL-KITS.md.
Legacy setup/model/relay commands are not included. No automatic kit downloads.
HELP
    ;;
  msg) cmd_msg "$@" ;;
  send)
    if [[ ${1:-} == @* ]]; then exec bash "$SKILL_DIR/scripts/antenna-list-send.sh" "$@"; fi
    exec bash "$SKILL_DIR/scripts/antenna-send.sh" "$@" ;;
  peers)
    [[ $# == 1 && $1 == list ]] || { echo 'Use contacts import/export for native pairing; see the User Guide.' >&2; exit 64; }
    jq 'to_entries | map({peer:.key,self:(.value.self // false),url:.value.url,transport_profile:.value.transport_profile,default_target:.value.default_target})' "$SKILL_DIR/antenna-peers.json" ;;
  health) exec bash "$SKILL_DIR/scripts/antenna-health.sh" "$@" ;;
  contacts)
    action="${1:?Use contacts export or import}"; shift
    exec node "$SKILL_DIR/plugin/pairing.mjs" "$action" "$SKILL_DIR" "$@" ;;
  plugin) exec node "$SKILL_DIR/plugin/cli.mjs" "$@" ;;
  status) exec node "$SKILL_DIR/plugin/cli.mjs" "$host" status "$@" ;;
  mcs|migrate) exec node "$SKILL_DIR/plugin/cli.mjs" "$host" "$command" "$@" ;;
  groups) exec bash "$SKILL_DIR/scripts/antenna-public-group.sh" "$@" ;;
  clawreef) exec python3 -B "$SKILL_DIR/scripts/antenna-clawreef.py" "$@" ;;
  backup)
    export ANTENNA_INVOKED_CLI="$0"
    exec python3 -B "$SKILL_DIR/scripts/antenna-backup.py" "$@" ;;
  readiness) exec python3 -B "$SKILL_DIR/scripts/antenna-readiness.py" "$@" ;;
  doctor) exec bash "$SKILL_DIR/scripts/antenna-doctor.sh" "$@" ;;
  setup|pair|upgrade|uninstall|model|test|test-suite|inbox|sessions|config|log)
    echo 'Legacy command retired. Use native plugin operators and references/USER-GUIDE.md; migration is separate (plugin/OPTIONAL-KITS.md). Nothing changed.' >&2; exit 64 ;;
  *) echo 'Unknown command; run antenna help.' >&2; exit 64 ;;
esac
