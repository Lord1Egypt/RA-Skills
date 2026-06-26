#!/usr/bin/env bash
# antenna-setup.sh — First-run setup wizard for Antenna.
# Creates config, peers file, identity secret, and prints gateway registration instructions.
# Runtime files are local installation state; tracked example files live alongside them.
#
# Usage:
#   antenna-setup.sh                           Interactive wizard
#   antenna-setup.sh --host-id <id>            Non-interactive (all flags)
#     --display-name <name>
#     --url <url>
#     --agent-id <agent-id>
#     --model <provider/model>
#     --token-file <path>
#     [--inbox true|false]                     Enable/disable inbox queue
#     [--inbox-auto-approve "peer1,peer2"]     Auto-approve peer list
#     [--force]                                Overwrite existing config
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"
SECRETS_DIR="$SKILL_DIR/secrets"

# REF-1313: shared URL validator lives in lib/peers.sh. Sourcing here is safe
# during first-run setup because lib/peers.sh only defines functions (no side
# effects) and has a double-source guard.
# shellcheck source=../lib/peers.sh
source "$SKILL_DIR/lib/peers.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── Helpers ──────────────────────────────────────────────────────────────────

info()  { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✓${NC}  $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
err()   { echo -e "${RED}✗${NC}  $*" >&2; }
header(){ echo -e "\n${BOLD}$*${NC}"; }

prompt() {
  local var_name="$1" prompt_text="$2" default="${3:-}"
  local value
  if [[ -n "$default" ]]; then
    read -rp "$(echo -e "${CYAN}?${NC}  ${prompt_text} [${default}]: ")" value
    value="${value:-$default}"
  else
    read -rp "$(echo -e "${CYAN}?${NC}  ${prompt_text}: ")" value
  fi
  eval "$var_name=\$value"
}

prompt_yn() {
  local prompt_text="$1" default="${2:-y}"
  local yn
  read -rp "$(echo -e "${CYAN}?${NC}  ${prompt_text} [${default}]: ")" yn
  yn="${yn:-$default}"
  [[ "${yn,,}" == "y" || "${yn,,}" == "yes" ]]
}

# ── Parse non-interactive flags ──────────────────────────────────────────────

NI_HOST_ID="" NI_DISPLAY="" NI_URL="" NI_AGENT="" NI_MODEL="" NI_TOKEN="" NI_FORCE=false
NI_INBOX="" NI_INBOX_AUTO="" NI_ALLOW_INSECURE=false
INTERACTIVE=true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host-id)       NI_HOST_ID="$2"; INTERACTIVE=false; shift 2 ;;
    --display-name)  NI_DISPLAY="$2"; shift 2 ;;
    --url)           NI_URL="$2"; shift 2 ;;
    --agent-id)      NI_AGENT="$2"; shift 2 ;;
    --model)         NI_MODEL="$2"; shift 2 ;;
    --token-file)    NI_TOKEN="$2"; shift 2 ;;
    --inbox)         NI_INBOX="$2"; shift 2 ;;
    --inbox-auto-approve) NI_INBOX_AUTO="$2"; shift 2 ;;
    --force)         NI_FORCE=true; shift ;;
    --allow-insecure) NI_ALLOW_INSECURE=true; shift ;;
    -h|--help)
      cat <<'EOF'
antenna setup — First-run setup wizard for Antenna

Interactive:
  antenna setup

Non-interactive:
  antenna setup --host-id myhost \
    --display-name "My Host (Server)" \
    --url "https://myhost.tailXXXXX.ts.net" \
    --agent-id main \
    --model "openai/gpt-4o-mini" \
    --token-file /path/to/hooks_token \
    [--force]

Creates:
  - antenna-config.json (local runtime settings; gitignored)
  - antenna-peers.json (local peer registry with self-peer entry; gitignored)
  - secrets/antenna-peer-<host-id>.secret (your identity secret)
  - Example/reference files remain available: antenna-config.example.json, antenna-peers.example.json
  - Prints gateway registration instructions
EOF
      exit 0
      ;;
    *) err "Unknown option: $1"; exit 1 ;;
  esac
done

# ── Pre-flight checks ───────────────────────────────────────────────────────

if ! command -v jq &>/dev/null; then
  err "jq not found — required for Antenna. Install with: apt install jq / brew install jq"
  exit 1
fi

if ! command -v curl &>/dev/null; then
  err "curl not found — required for Antenna."
  exit 1
fi

if ! command -v openssl &>/dev/null; then
  err "openssl not found — required for secret generation."
  exit 1
fi

if ! command -v age &>/dev/null; then
  warn "age not found — required for encrypted peer exchange (Layer A)."
  info "Install with: apt install age / brew install age / https://github.com/FiloSottile/age"
  info "Setup will continue, but you will need age for the peer exchange flow."
fi

# Check for existing config
if [[ -f "$CONFIG_FILE" && "$NI_FORCE" != "true" ]]; then
  if [[ "$INTERACTIVE" == "true" ]]; then
    warn "Antenna is already configured ($CONFIG_FILE exists)."
    if ! prompt_yn "Overwrite and start fresh?" "n"; then
      info "Setup cancelled. Use 'antenna status' to check your current config."
      exit 0
    fi
  else
    err "Config already exists. Use --force to overwrite."
    exit 1
  fi
fi

# ── Banner ───────────────────────────────────────────────────────────────────

if [[ "$INTERACTIVE" == "true" ]]; then
  echo ""
  echo -e "${BOLD}🦞 📡 Antenna Setup — Let's Get You on the Reef${NC}"
  echo ""
  echo "  This wizard configures Antenna on this host."
  echo "  Two minutes from now, you'll be ready to send your first"
  echo "  cross-host message. No PhD required. No shellfish expertise"
  echo "  necessary (though it helps)."
  echo ""
  echo "  You'll need:"
  echo "    1. A host ID (usually just your hostname)"
  echo "    2. Your reachable HTTPS hook URL"
  echo "    3. Your primary agent ID (e.g., 'main', 'betty', 'lobster')"
  echo "    4. A relay model (lightweight is best — the relay doesn't think, it dispatches)"
  echo "    5. Whether to enable inbox mode (optional, more secure)"
  echo "    6. Your OpenClaw hooks bearer token (setup can auto-detect or generate one)"
  echo ""
fi

# ── Gather info ──────────────────────────────────────────────────────────────

if [[ "$INTERACTIVE" == "true" ]]; then
  # Host ID
  local_hostname=$(hostname | tr '[:upper:]' '[:lower:]')
  header "Step 1/7 — Host Identity — Who Are You on the Reef?"
  prompt HOST_ID "Host ID (lowercase, no spaces — identifies you on the mesh)" "$local_hostname"
  HOST_ID=$(echo "$HOST_ID" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

  # Display name
  prompt DISPLAY_NAME "Display name (human-readable, shown in message headers)" "${HOST_ID^} ($(hostname))"

  # URL
  header "Step 2/7 — Reachable Endpoint — Where Do Peers Find You?"
  info "This is the URL other peers use to reach your /hooks/agent endpoint."
  info "Examples: https://myhost.tailXXXXX.ts.net  or  https://your-host.example.com"
  # REF-1313: loop until the operator gives us something that looks like a
  # reachable HTTPS URL. This prevents the 'url: "main"' class of typo from
  # silently landing in the self-peer record and then propagating to every
  # peer via bootstrap bundles.
  while :; do
    prompt HOST_URL "Your hook URL" ""
    HOST_URL="${HOST_URL%/}"
    if validate_peer_url "$HOST_URL" "${NI_ALLOW_INSECURE:-false}" 2>/tmp/antenna-urlcheck.$$; then
      rm -f /tmp/antenna-urlcheck.$$
      break
    fi
    err "$(cat /tmp/antenna-urlcheck.$$ 2>/dev/null || echo 'invalid URL')"
    rm -f /tmp/antenna-urlcheck.$$
    info "Please enter a real https:// URL peers can reach (examples above)."
  done

  # Agent ID — try to auto-detect from gateway config
  header "Step 3/7 — Agent Identity — Who's Running the Show?"
  info "This is your primary assistant agent's ID in your gateway config."
  info "Used to resolve 'main' → 'agent:<id>:main'."
  DETECTED_AGENT=""
  for candidate in "$HOME/.openclaw/openclaw.json" "/etc/openclaw/openclaw.json"; do
    if [[ -f "$candidate" ]]; then
      # Find the first non-antenna agent ID (supports both entries{} and list[] formats)
      DETECTED_AGENT=$(jq -r '
        (if .agents.entries then
          .agents.entries | to_entries[] | select(.key != "antenna") | .key
        elif .agents.list then
          .agents.list[] | select(.id != "antenna") | .id
        else empty end)' "$candidate" 2>/dev/null | head -1)
      [[ -n "$DETECTED_AGENT" ]] && break
    fi
  done
  if [[ -n "$DETECTED_AGENT" ]]; then
    info "Detected agent from gateway config: ${BOLD}$DETECTED_AGENT${NC}"
    prompt AGENT_ID "Primary agent ID" "$DETECTED_AGENT"
  else
    prompt AGENT_ID "Primary agent ID" ""
  fi

  # Relay model
  header "Step 4/7 — Relay Model — Choosing Your Dispatcher"
  info "The model used by Antenna's relay agent for tool dispatch."
  info "Use a full provider/model ID (not an alias) for portability."
  info "Pick something lightweight — the relay agent is a courier, not a philosopher."
  info "It dispatches messages, not opinions."

  # Try to load default model and aliases from gateway config
  _alias_names=()
  _alias_ids=()
  _default_model=""
  for _gw_cand in "$HOME/.openclaw/openclaw.json" "/home/$USER/.openclaw/openclaw.json"; do
    if [[ -f "$_gw_cand" ]]; then
      _default_model=$(jq -r '.agents.defaults.model.primary // empty' "$_gw_cand" 2>/dev/null || true)
      while IFS=$'\t' read -r _mid _aname; do
        [[ -z "$_mid" || -z "$_aname" ]] && continue
        _alias_ids+=("$_mid")
        _alias_names+=("$_aname")
      done < <(jq -r '
        (.agents.defaults.models // {}) | to_entries[] |
        select(.value.alias != null and .value.alias != "") |
        "\(.key)\t\(.value.alias)"
      ' "$_gw_cand" 2>/dev/null || true)
      break
    fi
  done

  # Use the host's default model as the suggested default (most likely to be working)
  _suggested_default="${_default_model:-openai/gpt-4o-mini}"

  RELAY_MODEL=""
  echo ""
  if [[ -n "$_default_model" ]]; then
    info "Your default model: ${BOLD}$_default_model${NC}"
  fi
  if [[ ${#_alias_names[@]} -gt 0 ]]; then
    info "Available model aliases from your gateway config:"
    _offset=1
    if [[ -n "$_default_model" ]]; then
      echo -e "    ${BOLD}D. (default) → $_default_model${NC}"
    fi
    for _i in "${!_alias_names[@]}"; do
      echo "    $((_i+1)). ${_alias_names[$_i]} → ${_alias_ids[$_i]}"
    done
    echo ""
    read -rp "$(echo -e "${CYAN}?${NC}  Enter D for default, number, full provider/model ID, or press Enter [$_suggested_default]: ")" _relay_input
    _relay_input="${_relay_input:-D}"
    if [[ "${_relay_input,,}" == "d" ]]; then
      RELAY_MODEL="$_suggested_default"
      info "Selected default model: $RELAY_MODEL"
    elif [[ "$_relay_input" =~ ^[0-9]+$ ]]; then
      _idx=$((_relay_input - 1))
      if [[ $_idx -ge 0 && $_idx -lt ${#_alias_ids[@]} ]]; then
        RELAY_MODEL="${_alias_ids[$_idx]}"
        info "Selected: ${_alias_names[$_idx]} → $RELAY_MODEL"
      else
        warn "Invalid selection, using as model ID: $_relay_input"
        RELAY_MODEL="$_relay_input"
      fi
    else
      # Check if input matches an alias name
      _found_alias=false
      for _i in "${!_alias_names[@]}"; do
        if [[ "${_alias_names[$_i]}" == "$_relay_input" ]]; then
          RELAY_MODEL="${_alias_ids[$_i]}"
          info "Resolved alias '$_relay_input' → $RELAY_MODEL"
          _found_alias=true
          break
        fi
      done
      if [[ "$_found_alias" == "false" ]]; then
        RELAY_MODEL="$_relay_input"
      fi
    fi
  else
    prompt RELAY_MODEL "Relay model" "$_suggested_default"
  fi

  # Token file — try autodiscovery first
  # Inbox mode
  header "Step 5/7 — Inbound Message Handling — Instant or Inspected?"
  echo ""
  echo "  When a message arrives, how should Antenna handle it?"
  echo ""
  echo -e "    ${BOLD}Instant relay${NC} (default)"
  echo "      Straight to your session, no delay. Like a walkie-talkie."
  echo "      Requires sandbox-off on the relay agent."
  echo ""
  echo -e "    ${BOLD}Inbox queue${NC} (more secure)"
  echo "      Messages wait in a queue for your review first."
  echo "      You approve or deny via 'antenna inbox' commands."
  echo "      Trusted peers can skip the line."
  echo ""

  INBOX_ENABLED=false
  INBOX_AUTO_APPROVE=""
  if prompt_yn "Enable inbox queue for inbound messages?" "n"; then
    INBOX_ENABLED=true
    ok "Inbox mode enabled"
    echo ""
    info "You can designate trusted peers whose messages skip the queue."
    info "Enter peer host IDs separated by commas, or leave empty for none."
    prompt INBOX_AUTO_APPROVE "Auto-approve peers (comma-separated, or empty)" ""
  else
    info "Inbox disabled — messages will relay instantly."
  fi

  header "Step 6/7 — Hooks Bearer Token — The Key to the Door"
  info "Path to the file containing your OpenClaw hooks bearer token."
  info "This authenticates HTTP requests to /hooks/agent."

  # Autodiscovery: try reading from gateway config
  TOKEN_FILE=""
  DISCOVERED_TOKEN=""
  for gw_candidate in "$HOME/.openclaw/openclaw.json" "/home/$USER/.openclaw/openclaw.json"; do
    if [[ -f "$gw_candidate" ]]; then
      DISCOVERED_TOKEN=$(jq -r '.hooks.token // empty' "$gw_candidate" 2>/dev/null || true)
      if [[ -n "$DISCOVERED_TOKEN" ]]; then
        info "Found hooks token in gateway config ($gw_candidate)"
        suggested_path="$SECRETS_DIR/hooks_token_${HOST_ID}"
        if prompt_yn "Create token file at $suggested_path from gateway config?" "y"; then
          mkdir -p "$SECRETS_DIR"
          printf '%s' "$DISCOVERED_TOKEN" > "$suggested_path"
          chmod 600 "$suggested_path"
          ok "Created token file: $suggested_path"
          TOKEN_FILE="$suggested_path"
        fi
        break
      fi
    fi
  done

  if [[ -z "$TOKEN_FILE" ]]; then
    if [[ -n "$DISCOVERED_TOKEN" ]]; then
      : # token found but user declined file creation; fall through to manual
    else
      warn "Could not auto-detect hooks token from gateway config."
      info "You can find it in ~/.openclaw/openclaw.json under hooks.token"
      echo ""
      if prompt_yn "Generate a new hooks bearer token now?" "y"; then
        gen_path="$SECRETS_DIR/hooks_token_${HOST_ID}"
        mkdir -p "$SECRETS_DIR"
        openssl rand -hex 24 > "$gen_path"
        chmod 600 "$gen_path"
        ok "Generated token file: $gen_path"
        info "You will need to add this token to your gateway hooks.token config."
        TOKEN_FILE="$gen_path"
      fi
    fi
    if [[ -z "$TOKEN_FILE" ]]; then
      prompt TOKEN_FILE "Token file path" ""
    fi
  fi

  if [[ -n "$TOKEN_FILE" && ! -f "$TOKEN_FILE" ]]; then
    warn "Token file not found at: $TOKEN_FILE"
    if prompt_yn "Continue anyway? (you can fix this later)" "y"; then
      true
    else
      err "Setup cancelled — create the token file first."
      exit 1
    fi
  fi

  header "Step 7/7 — Confirmation — Look Good?"
else
  # Non-interactive
  HOST_ID="$NI_HOST_ID"
  DISPLAY_NAME="${NI_DISPLAY:-${HOST_ID^}}"
  HOST_URL="${NI_URL:?--url is required}"
  HOST_URL="${HOST_URL%/}"
  # REF-1313: non-interactive setup must hard-fail on a malformed URL too.
  # Scripts that feed --url from gateway config or environment should not be
  # able to smuggle garbage past setup. Honor NI_ALLOW_INSECURE for parity
  # with the interactive path.
  if ! _reason="$(validate_peer_url "$HOST_URL" "${NI_ALLOW_INSECURE:-false}" 2>&1 >/dev/null)"; then
    err "--url is not valid: ${_reason:-invalid URL}"
    exit 1
  fi
  # Auto-detect primary agent from gateway config if --agent-id not given
  if [[ -z "$NI_AGENT" ]]; then
    for _cand in "$HOME/.openclaw/openclaw.json" "/etc/openclaw/openclaw.json"; do
      if [[ -f "$_cand" ]]; then
        NI_AGENT=$(jq -r '(
          if .agents.entries then
            .agents.entries | to_entries[] | select(.key != "antenna") | .key
          elif .agents.list then
            .agents.list[] | select(.id != "antenna") | .id
          else empty end)' "$_cand" 2>/dev/null | head -1)
        [[ -n "$NI_AGENT" ]] && break
      fi
    done
    if [[ -z "$NI_AGENT" ]]; then
      error "Could not detect primary agent. Pass --agent-id explicitly."
      exit 1
    fi
    info "Auto-detected primary agent: ${BOLD}${NI_AGENT}${NC}"
  else
    # Validate supplied --agent-id against registered agents
    _found=""
    for _cand in "$HOME/.openclaw/openclaw.json" "/etc/openclaw/openclaw.json"; do
      if [[ -f "$_cand" ]]; then
        _found=$(jq -r --arg id "$NI_AGENT" '(
          if .agents.entries then
            .agents.entries | to_entries[] | select(.key == $id) | .key
          elif .agents.list then
            .agents.list[] | select(.id == $id) | .id
          else empty end)' "$_cand" 2>/dev/null | head -1)
        [[ -n "$_found" ]] && break
      fi
    done
    if [[ -z "$_found" ]]; then
      warn "--agent-id '$NI_AGENT' is not a registered agent in the gateway config."
      # Try to suggest the right one
      _suggested=""
      for _cand in "$HOME/.openclaw/openclaw.json" "/etc/openclaw/openclaw.json"; do
        if [[ -f "$_cand" ]]; then
          _suggested=$(jq -r '(
            if .agents.entries then
              .agents.entries | to_entries[] | select(.key != "antenna") | .key
            elif .agents.list then
              .agents.list[] | select(.id != "antenna") | .id
            else empty end)' "$_cand" 2>/dev/null | head -1)
          [[ -n "$_suggested" ]] && break
        fi
      done
      if [[ -n "$_suggested" ]]; then
        warn "Did you mean '$_suggested'? Using '$_suggested' instead."
        NI_AGENT="$_suggested"
      else
        warn "Proceeding with '$NI_AGENT' — relay messages may not be visible in the UI."
      fi
    fi
  fi
  AGENT_ID="$NI_AGENT"
  RELAY_MODEL="${NI_MODEL:-openai/gpt-4o-mini}"

  # Resolve model alias if --model matched an alias name
  if [[ -n "$NI_MODEL" ]]; then
    for _gw_cand in "$HOME/.openclaw/openclaw.json" "/home/$USER/.openclaw/openclaw.json"; do
      if [[ -f "$_gw_cand" ]]; then
        _resolved=$(jq -r --arg alias "$NI_MODEL" '
          (.agents.defaults.models // {}) | to_entries[] |
          select(.value.alias == $alias) | .key
        ' "$_gw_cand" 2>/dev/null | head -1 || true)
        if [[ -n "$_resolved" ]]; then
          RELAY_MODEL="$_resolved"
          info "Resolved model alias '$NI_MODEL' → $RELAY_MODEL"
        fi
        break
      fi
    done
  fi

  # Inbox settings (non-interactive)
  if [[ "${NI_INBOX,,}" == "true" ]]; then
    INBOX_ENABLED=true
    INBOX_AUTO_APPROVE="${NI_INBOX_AUTO:-}"
  else
    INBOX_ENABLED=false
    INBOX_AUTO_APPROVE=""
  fi

  TOKEN_FILE="${NI_TOKEN:?--token-file is required}"

  # Non-interactive: try autodiscovery or auto-generate if token-file is "auto" or missing
  if [[ "$TOKEN_FILE" == "auto" || ! -f "$TOKEN_FILE" ]]; then
    # Try reading from gateway config first
    ni_discovered=""
    for gw_candidate in "$HOME/.openclaw/openclaw.json" "/home/$USER/.openclaw/openclaw.json"; do
      if [[ -f "$gw_candidate" ]]; then
        ni_discovered=$(jq -r '.hooks.token // empty' "$gw_candidate" 2>/dev/null || true)
        [[ -n "$ni_discovered" ]] && break
      fi
    done
    mkdir -p "$SKILL_DIR/secrets"
    ni_path="$SKILL_DIR/secrets/hooks_token_${HOST_ID}"
    if [[ -n "$ni_discovered" ]]; then
      printf '%s' "$ni_discovered" > "$ni_path"
      chmod 600 "$ni_path"
      info "Auto-discovered hooks token from gateway config"
      TOKEN_FILE="$ni_path"
    else
      openssl rand -hex 24 > "$ni_path"
      chmod 600 "$ni_path"
      info "Auto-generated hooks bearer token: $ni_path"
      TOKEN_FILE="$ni_path"
    fi
  fi
fi

# ── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo -e "  Host ID:      ${BOLD}$HOST_ID${NC}"
echo -e "  Display name: ${BOLD}$DISPLAY_NAME${NC}"
echo -e "  Hook URL:     ${BOLD}$HOST_URL${NC}"
echo -e "  Agent ID:     ${BOLD}$AGENT_ID${NC}"
echo -e "  Relay model:  ${BOLD}$RELAY_MODEL${NC}"
echo -e "  Token file:   ${BOLD}$TOKEN_FILE${NC}"
if [[ "$INBOX_ENABLED" == "true" ]]; then
  echo -e "  Inbox:        ${BOLD}enabled${NC}"
  if [[ -n "$INBOX_AUTO_APPROVE" ]]; then
    echo -e "  Auto-approve: ${BOLD}$INBOX_AUTO_APPROVE${NC}"
  else
    echo -e "  Auto-approve: ${BOLD}(none)${NC}"
  fi
else
  echo -e "  Inbox:        ${BOLD}disabled${NC} (instant relay)"
fi
echo -e "  Install path: ${BOLD}$SKILL_DIR${NC}"
echo -e "  Examples:     ${BOLD}$SKILL_DIR/antenna-config.example.json${NC}"
echo -e "                ${BOLD}$SKILL_DIR/antenna-peers.example.json${NC}"
echo ""

if [[ "$INTERACTIVE" == "true" ]]; then
  if ! prompt_yn "Create configuration with these settings?" "y"; then
    info "Setup cancelled."
    exit 0
  fi
fi

# ── Create config ────────────────────────────────────────────────────────────

# Build inbox auto-approve JSON array from comma-separated string
INBOX_AUTO_JSON="[]"
if [[ -n "$INBOX_AUTO_APPROVE" ]]; then
  INBOX_AUTO_JSON=$(echo "$INBOX_AUTO_APPROVE" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | jq -R . | jq -s .)
fi

jq -n \
  --arg model "$RELAY_MODEL" \
  --arg agent "$AGENT_ID" \
  --arg path "$SKILL_DIR" \
  --arg host "$HOST_ID" \
  --argjson inbox_enabled "$INBOX_ENABLED" \
  --argjson inbox_auto "$INBOX_AUTO_JSON" \
  '{
    max_message_length: 10000,
    default_target_session: ("agent:" + $agent + ":main"),
    relay_agent_id: "antenna",
    relay_agent_model: $model,
    local_agent_id: $agent,
    install_path: $path,
    log_enabled: true,
    log_path: "antenna.log",
    log_max_size_bytes: 10485760,
    log_verbose: false,
    rate_limit: {
      per_peer_per_minute: 10,
      global_per_minute: 30
    },
    mcs_enabled: false,
    mcs_model: "sonnet",
    inbox_enabled: $inbox_enabled,
    inbox_auto_approve_peers: $inbox_auto,
    inbox_queue_path: "antenna-inbox.json",
    allowed_inbound_sessions: [("agent:" + $agent + ":main"), ("agent:" + $agent + ":antenna"), "agent:antenna:modeltest"],
    allowed_inbound_peers: [$host],
    allowed_outbound_peers: [$host]
  }' > "$CONFIG_FILE"
chmod 644 "$CONFIG_FILE"
ok "Created $CONFIG_FILE"

# ── Normalize self token to canonical path ────────────────────────────────────

CANONICAL_TOKEN_REF="secrets/hooks_token_${HOST_ID}"
CANONICAL_TOKEN_ABS="$SKILL_DIR/$CANONICAL_TOKEN_REF"
mkdir -p "$SECRETS_DIR"

if [[ -n "$TOKEN_FILE" && -f "$TOKEN_FILE" && "$TOKEN_FILE" != "$CANONICAL_TOKEN_ABS" ]]; then
  # Copy token contents to canonical location so the self peer always uses
  # a predictable relative path. This prevents stale absolute paths from
  # being baked into exchange bundles (Issue #12).
  cp "$TOKEN_FILE" "$CANONICAL_TOKEN_ABS"
  chmod 600 "$CANONICAL_TOKEN_ABS"
  info "Copied token to canonical path: $CANONICAL_TOKEN_REF"
elif [[ -n "$TOKEN_FILE" && -f "$TOKEN_FILE" ]]; then
  : # already at canonical path
elif [[ -n "$TOKEN_FILE" && ! -f "$TOKEN_FILE" ]]; then
  warn "Token file not found at $TOKEN_FILE — self peer token_file may need manual update later."
fi

# ── Create peers file with self-peer ─────────────────────────────────────────

jq -n \
  --arg id "$HOST_ID" \
  --arg url "$HOST_URL" \
  --arg tf "$CANONICAL_TOKEN_REF" \
  --arg dn "$DISPLAY_NAME" \
  --arg psf "secrets/antenna-peer-${HOST_ID}.secret" \
  '{
    ($id): {
      url: $url,
      token_file: $tf,
      peer_secret_file: $psf,
      agentId: "antenna",
      display_name: $dn,
      self: true
    }
  }' > "$PEERS_FILE"
chmod 644 "$PEERS_FILE"
ok "Created $PEERS_FILE (self-peer: $HOST_ID)"

# ── Generate identity secret ────────────────────────────────────────────────

mkdir -p "$SECRETS_DIR"
SECRET_PATH="$SECRETS_DIR/antenna-peer-${HOST_ID}.secret"
SECRET=$(openssl rand -hex 32)
echo -n "$SECRET" > "$SECRET_PATH"
chmod 600 "$SECRET_PATH"
ok "Generated identity secret: $SECRET_PATH"

# ── Create .gitignore if missing ─────────────────────────────────────────────

GITIGNORE="$SKILL_DIR/.gitignore"
if [[ ! -f "$GITIGNORE" ]]; then
  cat > "$GITIGNORE" <<'GITIGNORE'
# Runtime files — don't version
antenna.log
antenna.log.*
test-results/
antenna-config.json
antenna-peers.json

# Secrets — never commit
**/secrets/
*.token

# OS junk
.DS_Store
Thumbs.db
antenna-ratelimit.json
GITIGNORE
  ok "Created .gitignore"
fi

# ── Print gateway registration instructions ──────────────────────────────────

echo ""
# ── Back up gateway config before user edits it ─────────────────────────────

header "═══ Backing Up Your Gateway Config (Just in Case) ═══"
echo ""
GATEWAY_CFG=""
for candidate in "$HOME/.openclaw/openclaw.json" "/home/$USER/.openclaw/openclaw.json"; do
  if [[ -f "$candidate" ]]; then
    GATEWAY_CFG="$candidate"
    break
  fi
done

if [[ -n "$GATEWAY_CFG" ]]; then
  BACKUP_PATH="${GATEWAY_CFG}.antenna-backup"
  cp "$GATEWAY_CFG" "$BACKUP_PATH"
  chmod 600 "$BACKUP_PATH"
  ok "Gateway config backed up: $BACKUP_PATH"
  echo ""
  echo -e "  ${YELLOW}If anything goes wrong after editing, restore with:${NC}"
  echo -e "  ${CYAN}cp $BACKUP_PATH $GATEWAY_CFG${NC}"
  echo -e "  ${CYAN}openclaw gateway restart${NC}"
else
  warn "Could not find gateway config to back up (checked ~/.openclaw/openclaw.json)"
  info "If your config is elsewhere, back it up manually before proceeding."
fi
echo ""

header "═══ Registering Antenna with Your Gateway ═══"
echo ""

# ── Attempt automatic gateway registration ──────────────────────────────────
AUTO_REGISTERED=false
if [[ -n "$GATEWAY_CFG" ]]; then
  # Detect whether the gateway build supports systemPrompt in agent entries
  # by checking existing agents or trying a conservative approach (omit it)
  AGENT_ENTRY_FIELDS='{
    id: "antenna",
    name: "Antenna Relay",
    model: $model,
    agentDir: $agentdir
  }'

  # Check if openclaw CLI is available for agent/hooks management
  OPENCLAW_BIN=""
  for oc_candidate in "openclaw" "$HOME/.local/bin/openclaw" "/usr/local/bin/openclaw"; do
    if command -v "$oc_candidate" &>/dev/null 2>&1 || [[ -x "$oc_candidate" ]]; then
      OPENCLAW_BIN="$oc_candidate"
      break
    fi
  done

  do_auto_register=false
  if [[ "$INTERACTIVE" == "true" ]]; then
    if prompt_yn "Automatically register Antenna agent and enable hooks in gateway config?" "y"; then
      do_auto_register=true
    fi
  else
    # Non-interactive: always auto-register when gateway config is found
    do_auto_register=true
    info "Auto-registering Antenna agent and hooks in gateway config..."
  fi

  if [[ "$do_auto_register" == "true" ]]; then
      # Back up again right before editing
      cp "$GATEWAY_CFG" "${GATEWAY_CFG}.antenna-pre-register-$(date +%Y%m%d-%H%M%S)"

      # 1) Enable/merge hooks config
      tmp_gw=$(mktemp)
      # Read the hooks token from the token file to register it in gateway config
      file_token=""
      existing_hooks_token=""
      hooks_token_action="preserved"
      if [[ -n "$TOKEN_FILE" && -f "$TOKEN_FILE" ]]; then
        file_token="$(tr -d '[:space:]' < "$TOKEN_FILE")"
      fi
      existing_hooks_token="$(jq -r '.hooks.token // empty' "$GATEWAY_CFG" 2>/dev/null || true)"

      if [[ -n "$file_token" ]]; then
        if [[ -z "$existing_hooks_token" ]]; then
          hooks_token_action="registered"
        elif [[ "$existing_hooks_token" == "$file_token" ]]; then
          hooks_token_action="unchanged"
        else
          hooks_token_action="preserved"
          warn "Gateway already has hooks.token set to a different value. Preserving the existing gateway token and leaving Antenna's token only in $TOKEN_FILE"
        fi
      fi

      jq --arg aid "antenna" --arg prefix "hook:" --arg agent_prefix "agent:${AGENT_ID}:" --arg file_token "$file_token" '
        .hooks.enabled = true |
        .hooks.allowRequestSessionKey = true |
        .hooks.allowedAgentIds = ((.hooks.allowedAgentIds // []) | if (index($aid) | not) then . + [$aid] else . end) |
        .hooks.allowedSessionKeyPrefixes = (
          (.hooks.allowedSessionKeyPrefixes // [])
          | if (index($prefix) | not) then . + [$prefix] else . end
          | if (index($agent_prefix) | not) then . + [$agent_prefix] else . end
        ) |
        (if $file_token != "" and ((.hooks.token // "") == "" or (.hooks.token == $file_token)) then .hooks.token = $file_token else . end)
      ' "$GATEWAY_CFG" > "$tmp_gw" && mv "$tmp_gw" "$GATEWAY_CFG"
      ok "Hooks enabled and allowlists updated"
      case "$hooks_token_action" in
        registered) ok "Hooks token registered in gateway config" ;;
        unchanged) info "Gateway hooks.token already matched Antenna token" ;;
        preserved)
          if [[ -n "$file_token" && -n "$existing_hooks_token" && "$existing_hooks_token" != "$file_token" ]]; then
            info "Kept existing gateway hooks.token to avoid breaking other hook consumers"
          fi
          ;;
      esac

      # 2) Ensure a default agent exists before adding antenna
      #    If agents.list is empty/absent, the default main agent is implicit.
      #    Adding antenna alone would make it the only visible agent in the UI.
      has_any_agent=""
      has_any_agent=$(jq '[.agents.list // [] | .[]] | length' "$GATEWAY_CFG" 2>/dev/null || echo "0")
      if [[ "$has_any_agent" -eq 0 ]]; then
        _def_workspace=$(jq -r '.agents.defaults.workspace // "~/clawd"' "$GATEWAY_CFG" 2>/dev/null || echo "~/clawd")
        _def_model=$(jq -r '.agents.defaults.model.primary // "openai/gpt-4o-mini"' "$GATEWAY_CFG" 2>/dev/null || echo "openai/gpt-4o-mini")
        tmp_gw=$(mktemp)
        jq --arg aid "$AGENT_ID" --arg ws "$_def_workspace" --arg model "$_def_model" '
          .agents.list = [{
            id: $aid,
            name: "Main Agent",
            model: $model,
            agentDir: $ws,
            workspace: $ws
          }]
        ' "$GATEWAY_CFG" > "$tmp_gw" && mv "$tmp_gw" "$GATEWAY_CFG"
        info "Created default main agent entry '$AGENT_ID' (agents.list was empty)"
      fi

      # 3) Register antenna agent if not already present
      #    The relay agent gets:
      #    - sandbox off: prevents per-command-hash approval prompts
      #    - restrictive tools.deny: least-privilege (only exec needed)
      #    NOTE: Do NOT set tools.exec (security/ask) on the antenna agent.
      #    Explicit exec overrides cause silent relay failures where the hook session
      #    acknowledges but delivery never completes, making messages invisible.
      has_antenna=""
      has_antenna=$(jq '[.agents.list // [] | .[] | select(.id == "antenna")] | length' "$GATEWAY_CFG" 2>/dev/null || echo "0")
      if [[ "$has_antenna" -eq 0 ]]; then
        tmp_gw=$(mktemp)
        jq --arg model "$RELAY_MODEL" --arg agentdir "$SKILL_DIR/agent" '
          .agents.list = ((.agents.list // []) + [{
            id: "antenna",
            name: "Antenna Relay",
            model: $model,
            agentDir: $agentdir,
            workspace: $agentdir,
            sandbox: { mode: "off" },
            tools: {
              deny: [
                "group:web", "browser", "image", "image_generate",
                "cron", "memory_search", "memory_get",
                "web_search", "web_fetch"
              ]
            }
          }])
        ' "$GATEWAY_CFG" > "$tmp_gw" && mv "$tmp_gw" "$GATEWAY_CFG"
        ok "Registered Antenna agent in gateway config (sandbox off, least-privilege tools)"
      else
        info "Antenna agent already registered in gateway config"
        # Ensure sandbox.mode=off on existing antenna entry without stripping any
        # operator-managed tools.exec or tools.deny customization.
        _needs_antenna_repair=$(jq '[.agents.list // [] | .[] | select(.id == "antenna" and ((.sandbox.mode // "") != "off" or (.tools | type) != "object"))] | length' "$GATEWAY_CFG" 2>/dev/null || echo "0")
        if [[ "$_needs_antenna_repair" -gt 0 ]]; then
          tmp_gw=$(mktemp)
          jq '
            .agents.list = [.agents.list[] |
              if .id == "antenna" then
                .sandbox = { mode: "off" } |
                .tools = (if (.tools | type) == "object" then .tools else {} end) |
                .tools.deny = (.tools.deny // [
                  "group:web", "browser", "image", "image_generate",
                  "cron", "memory_search", "memory_get",
                  "web_search", "web_fetch"
                ])
              else . end
            ]
          ' "$GATEWAY_CFG" > "$tmp_gw" && mv "$tmp_gw" "$GATEWAY_CFG"
          ok "Updated existing Antenna agent: sandbox off without removing operator tool overrides"
        fi
      fi

      # 4) Enable cross-agent session visibility
      #    The deliver script's gateway RPC needs to deliver into other agents' sessions.
      #    Without this, OpenClaw blocks cross-agent session access.
      _current_vis=$(jq -r '.tools.sessions.visibility // empty' "$GATEWAY_CFG" 2>/dev/null || true)
      if [[ "$_current_vis" != "all" ]]; then
        tmp_gw=$(mktemp)
        jq '.tools.sessions.visibility = "all"' "$GATEWAY_CFG" > "$tmp_gw" && mv "$tmp_gw" "$GATEWAY_CFG"
        ok "Set tools.sessions.visibility = \"all\" (required for cross-agent relay)"
      else
        info "tools.sessions.visibility already set to \"all\""
      fi

      _current_a2a=$(jq -r '.tools.agentToAgent.enabled // empty' "$GATEWAY_CFG" 2>/dev/null || true)
      if [[ "$_current_a2a" != "true" ]]; then
        tmp_gw=$(mktemp)
        jq '.tools.agentToAgent.enabled = true' "$GATEWAY_CFG" > "$tmp_gw" && mv "$tmp_gw" "$GATEWAY_CFG"
        ok "Set tools.agentToAgent.enabled = true"
      else
        info "tools.agentToAgent.enabled already true"
      fi

      # 6) Register exec allowlist for the antenna agent
      #    The relay agent needs to run shell commands (bash, echo, jq, cat)
      #    without requiring manual approval on each inbound message.
      if command -v openclaw &>/dev/null; then
        _allowlist_cmds=("/usr/bin/bash" "/usr/bin/echo" "/usr/bin/jq" "/usr/bin/cat")
        for _cmd in "${_allowlist_cmds[@]}"; do
          # Resolve actual path in case of different distro layouts
          _real_cmd="$_cmd"
          if [[ ! -f "$_cmd" ]] && command -v "$(basename "$_cmd")" &>/dev/null; then
            _real_cmd="$(command -v "$(basename "$_cmd")")"
          fi
          openclaw approvals allowlist add --agent antenna "$_real_cmd" >/dev/null 2>&1 || true
        done
        ok "Exec allowlist configured for antenna agent (bash, echo, jq, cat)"
      else
        warn "Could not configure exec allowlist (openclaw CLI not found)"
        info "You may need to approve exec commands manually or run:"
        info "  openclaw approvals allowlist add --agent antenna /usr/bin/bash"
        info "  openclaw approvals allowlist add --agent antenna /usr/bin/echo"
        info "  openclaw approvals allowlist add --agent antenna /usr/bin/jq"
        info "  openclaw approvals allowlist add --agent antenna /usr/bin/cat"
      fi

      # 7) Validate
      if jq empty "$GATEWAY_CFG" 2>/dev/null; then
        ok "Gateway config is valid JSON — nothing broken, nothing weird."
        AUTO_REGISTERED=true
      else
        err "Gateway config is not valid JSON after changes!"
        warn "Restoring from backup..."
        cp "${GATEWAY_CFG}.antenna-backup" "$GATEWAY_CFG" 2>/dev/null || true
      fi
  fi
fi

# ── PATH symlink ─────────────────────────────────────────────────────────────
# Ensure `antenna` CLI is on PATH so agents (and humans) can just type "antenna".
header "═══ Putting Antenna on Your PATH ═══"

ANTENNA_BIN="$SKILL_DIR/bin/antenna.sh"
SYMLINK_TARGET=""

# Prefer /usr/local/bin; fall back to ~/.local/bin
for candidate in /usr/local/bin "$HOME/.local/bin"; do
  if [[ -d "$candidate" ]] && echo "$PATH" | tr ':' '\n' | grep -qx "$candidate"; then
    SYMLINK_TARGET="$candidate/antenna"
    break
  fi
done

# If ~/.local/bin doesn't exist yet but /usr/local/bin isn't writable, create it
if [[ -z "$SYMLINK_TARGET" ]]; then
  if [[ -w /usr/local/bin ]]; then
    SYMLINK_TARGET="/usr/local/bin/antenna"
  else
    mkdir -p "$HOME/.local/bin"
    SYMLINK_TARGET="$HOME/.local/bin/antenna"
    # Ensure it's on PATH for current and future shells
    if ! echo "$PATH" | tr ':' '\n' | grep -qx "$HOME/.local/bin"; then
      export PATH="$HOME/.local/bin:$PATH"
      # Append to profile if not already there
      for profile in "$HOME/.bashrc" "$HOME/.profile"; do
        if [[ -f "$profile" ]] && ! grep -q '\.local/bin' "$profile"; then
          echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$profile"
          info "Added ~/.local/bin to PATH in $(basename "$profile")"
          break
        fi
      done
    fi
  fi
fi

if [[ -n "$SYMLINK_TARGET" ]]; then
  if [[ -L "$SYMLINK_TARGET" ]] && [[ "$(readlink -f "$SYMLINK_TARGET")" == "$(readlink -f "$ANTENNA_BIN")" ]]; then
    ok "antenna CLI already on PATH: $SYMLINK_TARGET"
  else
    # Remove stale symlink or file if it exists
    rm -f "$SYMLINK_TARGET" 2>/dev/null || true
    if ln -s "$ANTENNA_BIN" "$SYMLINK_TARGET" 2>/dev/null; then
      ok "Symlinked antenna CLI → $SYMLINK_TARGET"
    elif sudo ln -s "$ANTENNA_BIN" "$SYMLINK_TARGET" 2>/dev/null; then
      ok "Symlinked antenna CLI → $SYMLINK_TARGET (with sudo)"
    else
      warn "Could not create symlink at $SYMLINK_TARGET"
      echo "  Manual fix: ln -s $ANTENNA_BIN /usr/local/bin/antenna"
    fi
  fi
else
  warn "Could not determine a suitable PATH directory for the antenna CLI."
  echo "  Manual fix: ln -s $ANTENNA_BIN /usr/local/bin/antenna"
fi

if [[ "$AUTO_REGISTERED" == "false" ]]; then
  echo "  Add the following to your OpenClaw gateway config (openclaw.yaml or equivalent):"
  echo ""
  echo -e "  ${BOLD}1. Enable hooks:${NC}"
  echo "     hooks:"
  echo "       enabled: true"
  echo "       allowRequestSessionKey: true"
  echo "       token: <contents of your hooks token file>"
  echo "       allowedAgentIds: [\"antenna\"]"
  echo "       allowedSessionKeyPrefixes: [\"hook:\", \"agent:${AGENT_ID}:\"]"
  echo ""
  echo -e "  ${BOLD}2. Register the Antenna agent (sandbox off + least-privilege):${NC}"
  echo "     agents:"
  echo "       - id: antenna"
  echo "         name: Antenna Relay"
  echo "         model: $RELAY_MODEL"
  echo "         agentDir: $SKILL_DIR/agent"
  echo "         workspace: $SKILL_DIR/agent"
  echo "         sandbox:"
  echo "           mode: off"
  echo "         tools:"
  echo "           deny: [group:web, browser, image, image_generate,"
  echo "                  cron, memory_search, memory_get, web_search, web_fetch]"
  echo ""
  echo -e "  ${BOLD}3. Enable cross-agent session access:${NC}"
  echo "     tools:"
  echo "       sessions:"
  echo "         visibility: all"
  echo "       agentToAgent:"
  echo "         enabled: true"
  echo ""
  echo -e "  ${BOLD}4. Allow exec for the relay agent (no manual approval needed):${NC}"
  echo "     openclaw approvals allowlist add --agent antenna /usr/bin/bash"
  echo "     openclaw approvals allowlist add --agent antenna /usr/bin/echo"
  echo "     openclaw approvals allowlist add --agent antenna /usr/bin/jq"
  echo "     openclaw approvals allowlist add --agent antenna /usr/bin/cat"
  echo ""
  echo -e "  ${BOLD}5. Restart your gateway:${NC}"
  echo "     openclaw gateway restart"
fi
echo ""

header "═══ Almost There! ═══"
echo ""
if [[ "$AUTO_REGISTERED" == "true" ]]; then
  echo "  1. Restart the gateway to bring Antenna online:"
  echo "     openclaw gateway restart"
  echo ""
  echo -e "  2. Run the doctor to make sure everything checks out:"
  echo "     antenna doctor"
else
  echo "  1. Register the agent in your gateway config (see above)"
  echo -e "  2. ${BOLD}Verify your edits before restarting:${NC}"
  echo "     antenna doctor"
  echo "  3. Restart the gateway: openclaw gateway restart"
fi
echo ""
echo -e "  ${BOLD}═══ Ready to Connect? ═══${NC}"
echo ""
echo "  The fun part! The pairing wizard walks you through connecting"
echo "  to another host — keypair exchange, encrypted bundles, and your"
echo "  first message."
echo ""
echo -e "  Run it now or save it for later:  ${BOLD}antenna pair${NC}"
echo ""
echo "  Manual/legacy alternative (if age is unavailable):"
echo "     antenna peers add <peer-id> --url <url> --token-file <path>"
echo "     antenna peers exchange <peer-id> --legacy"
echo ""
echo "  Notes:"
echo "    - antenna-config.json and antenna-peers.json are local runtime files"
echo "    - tracked reference examples live at:"
echo "      antenna-config.example.json"
echo "      antenna-peers.example.json"
echo ""
if [[ "$INBOX_ENABLED" == "true" ]]; then
  echo -e "  ${BOLD}═══ Inbox Mode ═══${NC}"
  echo ""
  echo "  Inbox is enabled. Non-auto-approved peers' messages will be queued."
  echo "  Check the queue:    antenna inbox"
  echo "  Approve messages:   antenna inbox approve all"
  echo "  Deny messages:      antenna inbox deny 1,3"
  echo "  Deliver approved:   antenna inbox drain"
  echo ""
  echo "  Tip: Add this to your HEARTBEAT.md for automatic checking:"
  echo "    ## Antenna inbox check"
  echo "    - Run: antenna inbox count"
  echo "    - If > 0: run antenna inbox list and mention it"
  echo ""
  if [[ -n "$INBOX_AUTO_APPROVE" ]]; then
    echo "  Auto-approved peers: $INBOX_AUTO_APPROVE"
  else
    echo "  No auto-approved peers. All inbound messages will be queued."
    echo "  Add trusted peers later: antenna config set inbox_auto_approve_peers \"peer1,peer2\""
  fi
  echo ""
else
  echo -e "  ${YELLOW}ℹ${NC}  Inbox is disabled — messages relay instantly (requires sandbox-off)."
  echo "    To enable later: antenna config set inbox_enabled true"
  echo ""
fi
echo -e "  ${BOLD}═══ 🪸 ClawReef — Peer Discovery ═══${NC}"
echo ""
echo -e "  ${CYAN}clawreef.io${NC} is the community registry for Antenna hosts."
echo "  Register your host, find peers, and send connection invites —"
echo "  ClawReef delivers them via Antenna to the recipient's session."
echo ""
echo "  Get started:"
echo "    1. Create an account at https://clawreef.io"
echo "    2. Register this host (peer name, endpoint, exchange key)"
echo "    3. Complete bootstrap pairing with ClawReef"
echo "    4. Browse the reef and send invites!"
echo ""
echo -e "  ClawReef is optional — direct pairing via ${BOLD}antenna pair${NC} always works."
echo -e "  ClawReef stores public info only; trust stays local to Antenna."
echo ""
ok "Setup complete! Welcome to the reef, ${BOLD}$HOST_ID${NC}. 🦞"
echo ""

# Auto-offer pairing wizard (interactive mode only)
if [[ -t 0 && "$INTERACTIVE" == "true" ]]; then
  if prompt_yn "Ready to pair with your first peer? (The wizard handles everything.)"; then
    echo ""
    bash "$SCRIPT_DIR/antenna-pair.sh"
  fi
fi
