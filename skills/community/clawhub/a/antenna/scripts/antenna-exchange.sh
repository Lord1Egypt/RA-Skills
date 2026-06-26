#!/usr/bin/env bash
# antenna-exchange.sh — Layer A encrypted bootstrap exchange for Antenna.
#
# Preferred encrypted flow:
#   antenna peers exchange keygen [--force]
#   antenna peers exchange pubkey [--bare] [--email <addr> [--account <name>] --send-email] [--email <addr> --send-email]
#   antenna peers exchange initiate <peer-id> [options]
#   antenna peers exchange import [file|-] [--yes] [--force-expired]
#   antenna peers exchange reply <peer-id> [options]
#
# Legacy/manual compatibility:
#   antenna peers exchange <peer-id> --export
#   antenna peers exchange <peer-id> --import <file>
#   antenna peers exchange <peer-id> --import-value <hex>
#   antenna peers exchange <peer-id>             # alias for initiate <peer-id>
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"
SECRETS_DIR="$SKILL_DIR/secrets"

# shellcheck source=../lib/peers.sh
source "$SKILL_DIR/lib/peers.sh"
# shellcheck source=../lib/config.sh
source "$SKILL_DIR/lib/config.sh"
# REF-2000: shape/freshness validators live in lib/bundles.sh so this script
# and antenna-bundle.sh stay in lockstep.
# shellcheck source=../lib/bundles.sh
source "$SKILL_DIR/lib/bundles.sh"
EXCHANGE_KEY_FILE="$SECRETS_DIR/antenna-exchange.agekey"
EXCHANGE_PUB_FILE="$SECRETS_DIR/antenna-exchange.agepub"
FALLBACK_LEGACY=false

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

info()  { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✓${NC}  $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
err()   { echo -e "${RED}✗${NC}  $*" >&2; }
header(){ echo -e "\n${BOLD}$*${NC}"; }
die()   { err "$1"; exit "${2:-1}"; }

usage() {
  cat <<'EOF'
antenna peers exchange — Antenna Layer A bootstrap exchange

Encrypted flow (preferred):
  antenna peers exchange keygen [--force]
  antenna peers exchange pubkey [--bare] [--email <addr> [--account <name>] --send-email]
  antenna peers exchange initiate <peer-id> [options]
  antenna peers exchange import [file|-] [--yes] [--force-expired]
  antenna peers exchange reply <peer-id> [options]

Options for initiate / reply:
  --pubkey <age-recipient>      Recipient exchange public key
  --pubkey-file <path>          Read recipient exchange public key from file
  --email <addr>                Recipient email address (for optional direct send)
  --account <name>              Himalaya account to use with --send-email
  --output <path>               Output armored bundle path
  --print                       Print armored bundle after writing it
  --send-email                  Send bundle inline by email (requires himalaya)
  --notes <text>                Optional operator note stored in bundle metadata
  --yes                         Accept defaults / confirmations non-interactively
  --legacy                      Use the weaker raw-secret fallback instead

Options for import:
  --yes                         Skip confirmation prompts and accept allowlist updates
  --force-expired               Import an expired bundle anyway

Legacy/manual compatibility:
  antenna peers exchange <peer-id> --export
  antenna peers exchange <peer-id> --import <file>
  antenna peers exchange <peer-id> --import-value <hex>

Notes:
- Encrypted Layer A requires: age + age-keygen
- Direct email sending is optional and requires: himalaya
- The encrypted bundle includes the sender's exchange public key
- Import shows a preview and asks before applying allowlist changes
EOF
}

have_cmd() { command -v "$1" >/dev/null 2>&1; }
require_cmd() { have_cmd "$1" || die "$1 not found"; }
is_tty() { [[ -t 0 && -t 1 ]]; }

prompt() {
  local __var_name="$1" prompt_text="$2" default="${3:-}"
  local value
  if [[ -n "$default" ]]; then
    read -rp "$(echo -e "${CYAN}?${NC}  ${prompt_text} [${default}]: ")" value
    value="${value:-$default}"
  else
    read -rp "$(echo -e "${CYAN}?${NC}  ${prompt_text}: ")" value
  fi
  printf -v "$__var_name" '%s' "$value"
}

prompt_yn() {
  local prompt_text="$1" default="${2:-y}"
  local yn
  read -rp "$(echo -e "${CYAN}?${NC}  ${prompt_text} [${default}]: ")" yn
  yn="${yn:-$default}"
  [[ "${yn,,}" == "y" || "${yn,,}" == "yes" ]]
}

confirm_or_die() {
  local prompt_text="$1" assume_yes="${2:-false}"
  if [[ "$assume_yes" == "true" ]]; then
    return 0
  fi
  if is_tty; then
    prompt_yn "$prompt_text" "y"
    return $?
  fi
  die "Confirmation required in non-interactive mode. Re-run with --yes if you want to proceed."
}

resolve_path() {
  local p="$1"
  [[ "$p" == /* ]] && printf '%s\n' "$p" || printf '%s\n' "$SKILL_DIR/$p"
}

now_iso() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

expiry_iso() {
  if date -u -d '+7 days' +"%Y-%m-%dT%H:%M:%SZ" >/dev/null 2>&1; then
    date -u -d '+7 days' +"%Y-%m-%dT%H:%M:%SZ"
  else
    python3 - <<'PY'
from datetime import datetime, timedelta, timezone
print((datetime.now(timezone.utc) + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ'))
PY
  fi
}

random_id() {
  require_cmd openssl
  openssl rand -hex 12
}

ensure_core_files() {
  [[ -f "$PEERS_FILE" ]] || die "No peers file found. Run 'antenna setup' first."
  [[ -f "$CONFIG_FILE" ]] || die "No config file found. Run 'antenna setup' first."
  require_cmd jq
  mkdir -p "$SECRETS_DIR"
}

# self_id / peer_exists / peer_field are thin wrappers over lib/peers.sh
# (kept for call-site compatibility; the shared implementation lives in the
# library so adding new scripts reuses the same predicates).
self_id()     { peers_self_id; }
peer_exists() { peers_exists "$1"; }
peer_field()  { peers_get "$1" "$2"; }

self_field() {
  local field="$1" sid
  sid="$(self_id)"
  [[ -n "$sid" ]] || return 0
  peer_field "$sid" "$field"
}

log_path() {
  local p
  p=$(config_log_path)
  [[ "$p" == /* ]] && printf '%s\n' "$p" || printf '%s\n' "$SKILL_DIR/$p"
}

log_entry() {
  local enabled path
  enabled=$(config_log_enabled)
  [[ "$enabled" == "true" ]] || return 0
  path="$(log_path)"
  mkdir -p "$(dirname "$path")"
  echo "[$(now_iso)] EXCHANGE | $*" >> "$path"
}

age_available() {
  have_cmd age && have_cmd age-keygen
}

try_install_age() {
  # Attempt userland install of age via Homebrew if available
  local brew_bin=""
  for candidate in "brew" "/home/linuxbrew/.linuxbrew/bin/brew" "$HOME/.linuxbrew/bin/brew"; do
    if command -v "$candidate" &>/dev/null 2>&1 || [[ -x "$candidate" ]]; then
      brew_bin="$candidate"
      break
    fi
  done

  if [[ -n "$brew_bin" ]]; then
    info "Installing age via Homebrew ($brew_bin)..."
    if "$brew_bin" install age 2>&1; then
      # Ensure brew bin dir is on PATH for the rest of this session
      local brew_prefix
      brew_prefix=$("$brew_bin" --prefix 2>/dev/null || dirname "$(dirname "$brew_bin")")
      export PATH="${brew_prefix}/bin:$PATH"
      if age_available; then
        ok "age installed successfully"
        return 0
      fi
    fi
    warn "Homebrew install of age failed"
  fi
  return 1
}

require_age() {
  age_available && return 0

  # Interactive: offer to install or fall back to legacy
  if is_tty; then
    warn "age/age-keygen not found. Required for encrypted Layer A exchange."
    echo ""
    if prompt_yn "Install age now? (uses Homebrew if available)" "y"; then
      if try_install_age; then
        return 0
      fi
      warn "Could not install age automatically."
      info "Manual install: brew install age  OR  apt install age  OR  https://github.com/FiloSottile/age"
    fi
    echo ""
    if prompt_yn "Use the weaker legacy/manual raw-secret fallback instead?" "n"; then
      # Signal caller to switch to legacy mode
      FALLBACK_LEGACY=true
      return 0
    fi
    die "age is required for encrypted exchange. Install it and retry, or use --legacy."
  else
    die "age/age-keygen not found. Install age for encrypted Layer A exchange, or use --legacy for the manual fallback."
  fi
}

validate_runtime_secret() {
  local secret="$1"
  [[ "$secret" =~ ^[0-9a-f]{64}$ ]] || die "Invalid runtime identity secret format. Expected 64 lowercase hex characters."
}

validate_age_pubkey() {
  local key="$1"
  [[ "$key" =~ ^age1[0-9a-z]+$ ]] || die "Invalid age public key: $key"
}

self_identity_secret_ref() {
  local sid ref
  sid="$(self_id)"
  [[ -n "$sid" ]] || die "No self peer found in peers file. Run 'antenna setup' first."
  ref="$(peer_field "$sid" 'peer_secret_file')"
  [[ -n "$ref" ]] || ref="secrets/antenna-peer-${sid}.secret"
  printf '%s\n' "$ref"
}

ensure_self_identity_secret() {
  local sid ref abs tmp
  require_cmd openssl
  sid="$(self_id)"
  ref="$(self_identity_secret_ref)"
  abs="$(resolve_path "$ref")"
  mkdir -p "$(dirname "$abs")"
  if [[ ! -f "$abs" ]]; then
    openssl rand -hex 32 > "$abs"
    chmod 600 "$abs"
    ok "Generated local runtime identity secret: $abs"
  fi
  validate_runtime_secret "$(tr -d '[:space:]' < "$abs")"
  tmp=$(mktemp)
  jq --arg sid "$sid" --arg ref "$ref" '.[$sid].peer_secret_file = $ref' "$PEERS_FILE" > "$tmp" && mv "$tmp" "$PEERS_FILE"
  printf '%s\n' "$abs"
}

self_hooks_token_ref() {
  local sid ref
  sid="$(self_id)"
  [[ -n "$sid" ]] || die "No self peer found in peers file. Run 'antenna setup' first."
  ref="$(peer_field "$sid" 'token_file')"
  [[ -n "$ref" ]] || die "Self peer is missing token_file in antenna-peers.json"
  printf '%s\n' "$ref"
}

self_hooks_token_file() {
  resolve_path "$(self_hooks_token_ref)"
}

read_token_file() {
  local file="$1"
  [[ -f "$file" ]] || die "Token file not found: $file"
  tr -d '[:space:]' < "$file"
}

read_secret_file() {
  local file="$1"
  [[ -f "$file" ]] || die "Secret file not found: $file"
  tr -d '[:space:]' < "$file"
}

ensure_exchange_keypair() {
  local force="${1:-false}"
  require_age
  mkdir -p "$SECRETS_DIR"

  if [[ -f "$EXCHANGE_KEY_FILE" && "$force" != "true" ]]; then
    if [[ ! -f "$EXCHANGE_PUB_FILE" ]]; then
      age-keygen -y "$EXCHANGE_KEY_FILE" > "$EXCHANGE_PUB_FILE"
      chmod 644 "$EXCHANGE_PUB_FILE"
    fi
    sync_self_exchange_pubkey || true
    info "Exchange keypair already exists. Use --force to regenerate."
    info "Public key: $(current_exchange_pubkey)"
    return 0
  fi

  if [[ -f "$EXCHANGE_KEY_FILE" && "$force" == "true" ]]; then
    warn "Overwriting the existing exchange keypair. Older encrypted bundles will not decrypt with the replaced key."
  fi

  local tmp_dir tmp_key tmp_pub
  tmp_dir=$(mktemp -d)
  tmp_key="$tmp_dir/antenna-exchange.agekey"
  tmp_pub="$tmp_dir/antenna-exchange.agepub"
  age-keygen -o "$tmp_key" >/dev/null
  age-keygen -y "$tmp_key" > "$tmp_pub"
  mv "$tmp_key" "$EXCHANGE_KEY_FILE"
  mv "$tmp_pub" "$EXCHANGE_PUB_FILE"
  rmdir "$tmp_dir" 2>/dev/null || true
  chmod 600 "$EXCHANGE_KEY_FILE"
  chmod 644 "$EXCHANGE_PUB_FILE"
  sync_self_exchange_pubkey || true
  ok "Generated exchange keypair"
  info "Private key: $EXCHANGE_KEY_FILE"
  info "Public key:  $EXCHANGE_PUB_FILE"
}

current_exchange_pubkey() {
  [[ -f "$EXCHANGE_PUB_FILE" ]] || ensure_exchange_keypair false >/dev/null
  tr -d '[:space:]' < "$EXCHANGE_PUB_FILE"
}

sync_self_exchange_pubkey() {
  local sid pub tmp
  sid="$(self_id)"
  [[ -n "$sid" ]] || return 0
  [[ -f "$EXCHANGE_PUB_FILE" ]] || return 0
  pub="$(current_exchange_pubkey)"
  validate_age_pubkey "$pub"
  tmp=$(mktemp)
  jq --arg sid "$sid" --arg pub "$pub" '.[$sid].exchange_public_key = $pub' "$PEERS_FILE" > "$tmp" && mv "$tmp" "$PEERS_FILE"
}

read_pubkey_arg() {
  local pubkey_value="${1:-}" pubkey_file="${2:-}" result=""
  if [[ -n "$pubkey_value" ]]; then
    result="$pubkey_value"
  elif [[ -n "$pubkey_file" ]]; then
    [[ -f "$pubkey_file" ]] || die "Public key file not found: $pubkey_file"
    result=$(tr -d '[:space:]' < "$pubkey_file")
  fi
  if [[ -n "$result" ]]; then
    validate_age_pubkey "$result"
    printf '%s\n' "$result"
  fi
}

default_output_path() {
  local self_peer="$1" remote_peer="$2"
  printf './antenna-bootstrap-%s-to-%s-%s.age.txt\n' "$self_peer" "$remote_peer" "$(random_id)"
}

default_himalaya_account() {
  have_cmd himalaya || return 0
  himalaya account list -o json 2>/dev/null | jq -r 'map(select(.default == true)) | .[0].name // empty' 2>/dev/null || true
}

# REF-616: himalaya v1.2.0 does not expose per-account email addresses via its
# JSON CLI output (`himalaya account list -o json` returns only name/backend/default).
# The configured address lives in the TOML config. Read it directly, honoring
# $HIMALAYA_CONFIG first, then $XDG_CONFIG_HOME/himalaya/config.toml, then
# $HOME/.config/himalaya/config.toml. Returns empty if the account or its
# email key cannot be found.
himalaya_config_path() {
  if [[ -n "${HIMALAYA_CONFIG:-}" && -f "$HIMALAYA_CONFIG" ]]; then
    printf '%s\n' "$HIMALAYA_CONFIG"
    return 0
  fi
  local xdg="${XDG_CONFIG_HOME:-$HOME/.config}"
  if [[ -f "$xdg/himalaya/config.toml" ]]; then
    printf '%s\n' "$xdg/himalaya/config.toml"
    return 0
  fi
  if [[ -f "$HOME/.config/himalaya/config.toml" ]]; then
    printf '%s\n' "$HOME/.config/himalaya/config.toml"
    return 0
  fi
  return 0  # empty output, caller handles
}

himalaya_account_email() {
  local want_account="$1"
  [[ -n "$want_account" ]] || return 0
  local cfg_file
  cfg_file="$(himalaya_config_path)"
  [[ -n "$cfg_file" && -f "$cfg_file" ]] || return 0
  awk -v a="$want_account" '
    /^\[accounts\./ {
      in_sec = ($0 == "[accounts." a "]")
      next
    }
    /^\[/ { in_sec = 0; next }
    in_sec && /^[[:space:]]*email[[:space:]]*=/ {
      sub(/^[[:space:]]*email[[:space:]]*=[[:space:]]*"/, "")
      sub(/".*$/, "")
      print
      exit
    }
  ' "$cfg_file"
}

# Emits one TSV line per configured himalaya account: name<TAB>email<TAB>default
# where "default" is "true" or "false". Accounts without a resolvable email
# are skipped (they would hard-fail at send time anyway).
himalaya_accounts_list() {
  have_cmd himalaya || return 0
  local names_json names default_json default_name name email
  names_json="$(himalaya account list -o json 2>/dev/null || true)"
  [[ -n "$names_json" ]] || return 0
  default_name="$(printf '%s' "$names_json" | jq -r 'map(select(.default == true)) | .[0].name // empty' 2>/dev/null || true)"
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    email="$(himalaya_account_email "$name")"
    [[ -n "$email" ]] || continue
    if [[ "$name" == "$default_name" ]]; then
      printf '%s\t%s\ttrue\n' "$name" "$email"
    else
      printf '%s\t%s\tfalse\n' "$name" "$email"
    fi
  done < <(printf '%s' "$names_json" | jq -r '.[].name // empty' 2>/dev/null || true)
}

# REF-616: selection-only account picker. Takes the current account name as
# $1 and prints the chosen account name to stdout. UX is tightly constrained:
# the caller has already confirmed a default; this is only invoked when the
# operator wants to switch to a different configured account. No free text is
# accepted — only a numeric selection from the available accounts.
select_himalaya_account() {
  local current_account="$1"
  local -a names=() emails=() defaults=()
  local line name email is_default
  while IFS=$'\t' read -r name email is_default; do
    [[ -n "$name" ]] || continue
    names+=("$name")
    emails+=("$email")
    defaults+=("$is_default")
  done < <(himalaya_accounts_list)

  if (( ${#names[@]} == 0 )); then
    # Should not reach here (caller checks first), but bail safely.
    printf '%s\n' "$current_account" >&2
    printf '%s\n' "$current_account"
    return 0
  fi

  echo >&2
  echo -e "${BOLD}Available himalaya accounts:${NC}" >&2
  local i
  for (( i=0; i<${#names[@]}; i++ )); do
    local marker=""
    [[ "${defaults[i]}" == "true" ]] && marker="  (default)"
    [[ "${names[i]}" == "$current_account" ]] && marker="${marker}  ${DIM}← current${NC}"
    printf '  %d) %-20s %s%b\n' "$((i+1))" "${names[i]}" "${emails[i]}" "$marker" >&2
  done
  echo >&2

  # Default the picker to the current selection's index.
  local default_idx=1
  for (( i=0; i<${#names[@]}; i++ )); do
    if [[ "${names[i]}" == "$current_account" ]]; then
      default_idx=$((i+1))
      break
    fi
  done

  local choice
  prompt choice "Select account [1-${#names[@]}]" "$default_idx"
  # Strict numeric validation — no free text.
  if ! [[ "$choice" =~ ^[0-9]+$ ]] || (( choice < 1 )) || (( choice > ${#names[@]} )); then
    warn "Invalid selection '$choice'; keeping current account '$current_account'." >&2
    printf '%s\n' "$current_account"
    return 0
  fi
  printf '%s\n' "${names[$((choice-1))]}"
}

# REF-616: interactive From confirm loop. Takes an initial account name (must
# already have a resolvable email) and loops:
#   - display From / To / Subject
#   - [Y/n/change-account] when >1 configured account available
#   - [Y/n] when only 1 configured account
# Prints the confirmed account name to stdout on accept, or empty on abort.
confirm_from_account() {
  local account="$1" email_to="$2" subject="$3"
  local account_count
  account_count="$(himalaya_accounts_list | wc -l | awk '{print $1}')"
  local email

  while true; do
    email="$(himalaya_account_email "$account")"
    echo >&2
    echo -e "${BOLD}Send email${NC}" >&2
    printf '  %-9s %s  %s(himalaya account %s%s%s)%s\n' \
      "From:" "$email" "$DIM" "'" "$account" "'" "$NC" >&2
    printf '  %-9s %s\n' "To:" "$email_to" >&2
    printf '  %-9s %s\n' "Subject:" "$subject" >&2
    echo >&2

    local choices_label default_choice reply
    if (( account_count > 1 )); then
      choices_label="Send? [Y/n/change-account]"
      default_choice="y"
    else
      choices_label="Send? [Y/n]"
      default_choice="y"
    fi
    read -rp "$(echo -e "${CYAN}?${NC}  ${choices_label} [${default_choice}]: ")" reply
    reply="${reply:-$default_choice}"
    reply="${reply,,}"

    case "$reply" in
      y|yes) printf '%s\n' "$account"; return 0 ;;
      n|no)  printf '' ; return 1 ;;
      c|change|change-account|a|account)
        if (( account_count <= 1 )); then
          warn "Only one himalaya account is configured ('$account'); nothing to switch to." >&2
          continue
        fi
        account="$(select_himalaya_account "$account")"
        continue
        ;;
      *)
        warn "Please answer y (send), n (abort), or change-account (switch account)." >&2
        continue
        ;;
    esac
  done
}

send_bundle_email() {
  local email_to="$1" bundle_file="$2" peer_id="$3" account="${4:-}"
  [[ -f "$bundle_file" ]] || die "Bundle file not found: $bundle_file"

  local sid subject bundle_basename
  sid="$(self_id)"
  subject="Antenna bootstrap bundle from ${sid} for ${peer_id}"
  bundle_basename="$(basename "$bundle_file")"

  local body_text
  body_text="Encrypted Antenna Layer A bootstrap bundle from ${sid}.

To import it:
1. Save the attached .age.txt file
2. Run: antenna peers exchange import <saved-file>
3. If you do not have age installed yet: apt install age / brew install age

Important: Import the attached FILE directly — do not copy-paste the
bundle text, as email formatting may corrupt the base64 encoding."

  # Method 1: gog (Gmail API — handles attachments natively)
  if have_cmd gog; then
    local gog_account="${account:-}"
    # If account looks like a himalaya account name, try to find a gog account instead
    if [[ -n "$gog_account" ]] && ! [[ "$gog_account" == *@* ]]; then
      gog_account=""  # let gog use its default
    fi
    local gog_args=(gmail send --to "$email_to" --subject "$subject" --body "$body_text" --attach "$bundle_file" --force)
    [[ -n "$gog_account" ]] && gog_args=(gmail send --account "$gog_account" --to "$email_to" --subject "$subject" --body "$body_text" --attach "$bundle_file" --force)
    if gog "${gog_args[@]}" >/dev/null 2>&1; then
      ok "Sent encrypted bundle email to $email_to via gog (Gmail API)"
      return 0
    fi
    warn "gog send failed; trying himalaya fallback..."
  fi

  # Method 2: himalaya (IMAP/SMTP — raw MIME via stdin)
  if have_cmd himalaya; then
    if [[ -z "$account" ]]; then
      account="$(default_himalaya_account)"
    fi
    [[ -n "$account" ]] || die "No email account found. Install gog or himalaya, or use the bundle file manually."

    # REF-616: resolve the account's real email from himalaya config.toml.
    # Hard-fail if the account is not configured with an email — never fall
    # back to antenna@localhost (SMTP relays reject it or spam-filter it).
    local from_addr
    from_addr="$(himalaya_account_email "$account")"
    if [[ -z "$from_addr" ]]; then
      local cfg_hint
      cfg_hint="$(himalaya_config_path)"
      [[ -n "$cfg_hint" ]] || cfg_hint="${XDG_CONFIG_HOME:-$HOME/.config}/himalaya/config.toml"
      die "Could not resolve email address for himalaya account '$account'. Check [accounts.$account].email in $cfg_hint"
    fi

    local raw_file bundle_b64
    bundle_b64=$(base64 "$bundle_file")

    raw_file=$(mktemp)
    cat > "$raw_file" <<EOF
From: ${sid} <${from_addr}>
To: ${email_to}
Subject: ${subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="ANTENNABUNDLE"

--ANTENNABUNDLE
Content-Type: text/plain; charset=UTF-8

${body_text}

--ANTENNABUNDLE
Content-Type: application/octet-stream; name="${bundle_basename}"
Content-Disposition: attachment; filename="${bundle_basename}"
Content-Transfer-Encoding: base64

${bundle_b64}

--ANTENNABUNDLE--
EOF
    himalaya message send -a "$account" < "$raw_file" >/dev/null
    rm -f "$raw_file"
    ok "Sent encrypted bundle email to $email_to via himalaya ($from_addr)"
    return 0
  fi

  die "No email tool available (tried gog, himalaya). Use the bundle file or --print instead."
}

ensure_peer_entry_updated() {
  local peer_id="$1" url="$2" token_ref="$3" secret_ref="$4" agent_id="$5" display_name="$6" exchange_pubkey="$7"
  local tmp preserve_self
  # REF-600 defense-in-depth: if the existing entry is flagged as self, keep it that way.
  preserve_self=$(jq -r --arg p "$peer_id" '.[$p].self // false | tostring' "$PEERS_FILE" 2>/dev/null || echo "false")
  tmp=$(mktemp)
  jq \
    --arg peer "$peer_id" \
    --arg url "$url" \
    --arg token_ref "$token_ref" \
    --arg secret_ref "$secret_ref" \
    --arg agent_id "$agent_id" \
    --arg display_name "$display_name" \
    --arg exchange_pubkey "$exchange_pubkey" \
    --arg preserve_self "$preserve_self" \
    '
    # Merge the provided fields into the existing entry, keeping existing
    # values for any empty-string inputs. Use `*` to preserve unmentioned keys.
    .[$peer] = ((.[$peer] // {}) * {
      url: (if $url == "" then (.[$peer].url // "") else $url end),
      token_file: (if $token_ref == "" then (.[$peer].token_file // "") else $token_ref end),
      peer_secret_file: (if $secret_ref == "" then (.[$peer].peer_secret_file // "") else $secret_ref end),
      agentId: (if $agent_id == "" then (.[$peer].agentId // "antenna") else $agent_id end),
      display_name: (if $display_name == "" then (.[$peer].display_name // null) else $display_name end),
      exchange_public_key: (if $exchange_pubkey == "" then (.[$peer].exchange_public_key // null) else $exchange_pubkey end)
    })
    # REF-600 defense-in-depth: preserve the existing .self flag across updates.
    # Even if the merge object above did not list .self, this restores it when
    # the entry was previously the self-peer. The primary guard in import_bundle
    # should prevent ever reaching this path for the self-peer, but this keeps
    # the invariant local to the writer.
    | if ($preserve_self == "true") then .[$peer].self = true else . end
    ' \
    "$PEERS_FILE" > "$tmp" && mv "$tmp" "$PEERS_FILE"
}

update_allowlists() {
  local peer_id="$1" add_inbound="$2" add_outbound="$3"
  config_mutate '
    .allowed_inbound_peers = ((.allowed_inbound_peers // []) | if $add_in and (index($p) | not) then . + [$p] else . end) |
    .allowed_outbound_peers = ((.allowed_outbound_peers // []) | if $add_out and (index($p) | not) then . + [$p] else . end)
  ' --arg p "$peer_id" --argjson add_in "$add_inbound" --argjson add_out "$add_outbound"
}

legacy_export_runtime_secret() {
  local peer_id="$1"
  local abs secret
  abs="$(ensure_self_identity_secret)"
  secret="$(read_secret_file "$abs")"
  validate_runtime_secret "$secret"

  warn "This is the legacy/manual fallback. It is weaker than the encrypted Layer A bundle flow."
  info "Share it only over a trusted secure channel."
  info "Preferred: antenna peers exchange initiate $peer_id --pubkey <age1...>"
  info "Legacy peer import command: antenna peers exchange $peer_id --import-value <that-secret>"

  if ! is_tty; then
    die "Refusing to print the runtime identity secret to non-interactive stdout. Re-run in a terminal, or use the encrypted Layer A bundle flow instead."
  fi

  echo
  echo -e "${BOLD}Local runtime identity secret for $(self_id):${NC}"
  echo
  echo "$secret"
  echo
}

legacy_import_runtime_secret() {
  local peer_id="$1" secret="$2"
  local secret_ref secret_abs existing_url existing_token_ref existing_agent existing_name existing_pub
  validate_runtime_secret "$secret"

  secret_ref="$(peer_field "$peer_id" 'peer_secret_file')"
  [[ -n "$secret_ref" ]] || secret_ref="secrets/antenna-peer-${peer_id}.secret"
  secret_abs="$(resolve_path "$secret_ref")"
  mkdir -p "$(dirname "$secret_abs")"
  printf '%s' "$secret" > "$secret_abs"
  chmod 600 "$secret_abs"

  existing_url="$(peer_field "$peer_id" 'url')"
  existing_token_ref="$(peer_field "$peer_id" 'token_file')"
  existing_agent="$(peer_field "$peer_id" 'agentId')"
  existing_name="$(peer_field "$peer_id" 'display_name')"
  existing_pub="$(peer_field "$peer_id" 'exchange_public_key')"

  ensure_peer_entry_updated "$peer_id" "$existing_url" "$existing_token_ref" "$secret_ref" "$existing_agent" "$existing_name" "$existing_pub"
  update_allowlists "$peer_id" true true

  ok "Imported legacy raw runtime identity secret for $peer_id"
  warn "Legacy raw secret import bypasses encrypted Layer A bundles. Prefer the age-based flow when possible."
  log_entry "LEGACY-IMPORT | peer:${peer_id} | status:ok"
}

# REF-603: stream the plaintext bundle JSON to stdout instead of landing it on
# disk. Callers pipe this directly into `age` so the runtime identity secret,
# hooks token, and exchange key never touch the filesystem in cleartext. The
# old temp-file variant had no cleanup trap, so a mid-flow `die` (bad pubkey,
# disk full) or SIGINT would leave `/tmp/tmp.XXXXXXXX` behind with full secrets.
build_plaintext_bundle_stdout() {
  local target_peer_id="$1" notes="$2"
  local sid display_name endpoint agent_id token_file token secret_file secret exchange_pubkey
  sid="$(self_id)"
  [[ -n "$sid" ]] || die "No self peer found in peers file. Run 'antenna setup' first."

  display_name="$(self_field 'display_name')"
  endpoint="$(self_field 'url')"
  agent_id="$(self_field 'agentId')"
  [[ -n "$endpoint" ]] || die "Self peer is missing url in antenna-peers.json"
  # REF-1313: refuse to emit a bundle whose self endpoint is not a real URL.
  # Defense against a locally-corrupted self-peer propagating to every peer
  # that imports bundles from us (the "url: main" incident, 2026-04-21).
  if ! validate_peer_url "$endpoint" false 2>/tmp/antenna-urlcheck.$$; then
    local _reason
    _reason="$(cat /tmp/antenna-urlcheck.$$ 2>/dev/null || true)"
    rm -f /tmp/antenna-urlcheck.$$
    die "Self peer URL is not valid: ${_reason:-unknown}

Refusing to emit a bootstrap bundle with a malformed endpoint. Fix your self
peer in antenna-peers.json (or re-run 'antenna setup') so .url is a real
https:// URL that peers can reach, then try again."
  fi
  rm -f /tmp/antenna-urlcheck.$$
  [[ -n "$agent_id" ]] || agent_id="$(config_relay_agent_id)"

  token_file="$(self_hooks_token_file)"
  token="$(read_token_file "$token_file")"
  [[ -n "$token" ]] || die "Self token file is empty: $token_file"

  secret_file="$(ensure_self_identity_secret)"
  secret="$(read_secret_file "$secret_file")"
  validate_runtime_secret "$secret"

  ensure_exchange_keypair false >/dev/null
  exchange_pubkey="$(current_exchange_pubkey)"
  validate_age_pubkey "$exchange_pubkey"

  jq -n \
    --arg generated_at "$(now_iso)" \
    --arg expires_at "$(expiry_iso)" \
    --arg bundle_id "$(random_id)" \
    --arg from_peer_id "$sid" \
    --arg from_display_name "$display_name" \
    --arg from_endpoint_url "$endpoint" \
    --arg from_agent_id "$agent_id" \
    --arg from_hooks_token "$token" \
    --arg from_identity_secret "$secret" \
    --arg from_exchange_pubkey "$exchange_pubkey" \
    --arg expected_peer_id "$target_peer_id" \
    --arg notes "$notes" \
    '{
      schema_version: 1,
      bundle_type: "antenna-bootstrap",
      generated_at: $generated_at,
      expires_at: $expires_at,
      bundle_id: $bundle_id,
      from_peer_id: $from_peer_id,
      from_display_name: (if $from_display_name == "" then null else $from_display_name end),
      from_endpoint_url: $from_endpoint_url,
      from_agent_id: (if $from_agent_id == "" then "antenna" else $from_agent_id end),
      from_hooks_token: $from_hooks_token,
      from_identity_secret: $from_identity_secret,
      from_exchange_pubkey: $from_exchange_pubkey,
      expected_peer_id: (if $expected_peer_id == "" then null else $expected_peer_id end),
      notes: (if $notes == "" then null else $notes end)
    }'
}

# REF-603: encrypt straight from stdin so the plaintext bundle never exists as
# a file. `age` already supports stdin input when given `-` as its input arg.
encrypt_bundle_from_stdin() {
  local recipient_pubkey="$1" output_file="$2"
  mkdir -p "$(dirname "$output_file")"
  age -a -r "$recipient_pubkey" -o "$output_file" -
}

run_bundle_command() {
  local mode="$1" peer_id="$2" pubkey_arg="$3" pubkey_file_arg="$4" email="$5" account="$6" output_path="$7" print_bundle="$8" send_email="$9" notes="${10}" assume_yes="${11}" legacy_mode="${12}"
  local recipient_pubkey self_peer output_file existing_pubkey display_name

  self_peer="$(self_id)"
  [[ -n "$self_peer" ]] || die "No self peer found in peers file. Run 'antenna setup' first."

  if [[ "$legacy_mode" == "true" ]]; then
    legacy_export_runtime_secret "$peer_id"
    return 0
  fi

  FALLBACK_LEGACY=false
  require_age
  if [[ "$FALLBACK_LEGACY" == "true" ]]; then
    legacy_export_runtime_secret "$peer_id"
    return 0
  fi
  ensure_exchange_keypair false >/dev/null

  recipient_pubkey="$(read_pubkey_arg "$pubkey_arg" "$pubkey_file_arg")"
  if [[ -z "$recipient_pubkey" ]]; then
    existing_pubkey="$(peer_field "$peer_id" 'exchange_public_key')"
    recipient_pubkey="$existing_pubkey"
  fi
  if [[ -z "$recipient_pubkey" && is_tty && "$assume_yes" != "true" ]]; then
    prompt recipient_pubkey "Recipient age public key"
  fi
  [[ -n "$recipient_pubkey" ]] || die "No recipient exchange public key provided. Use --pubkey, --pubkey-file, or store exchange_public_key for that peer."
  validate_age_pubkey "$recipient_pubkey"

  output_file="${output_path:-$(default_output_path "$self_peer" "$peer_id")}"
  output_file="$(resolve_path "$output_file")"
  # REF-603: stream plaintext JSON directly from jq into age. The plaintext
  # (which carries from_identity_secret, from_hooks_token, from_exchange_pubkey)
  # exists only in the pipe between processes and is never written to disk.
  # If age fails, the pipe fails loudly via set -o pipefail and no output file
  # is created; there is nothing on disk to leak or clean up.
  build_plaintext_bundle_stdout "$peer_id" "$notes" | encrypt_bundle_from_stdin "$recipient_pubkey" "$output_file"

  display_name="$(peer_field "$peer_id" 'display_name')"
  ok "Created encrypted bootstrap bundle for $peer_id${display_name:+ ($display_name)}"
  info "Bundle file: $output_file"
  log_entry "OUTBOUND-BOOTSTRAP | mode:${mode} | to:${peer_id} | status:created | file:${output_file}"

  if [[ "$print_bundle" == "true" ]]; then
    echo
    header "Armored bundle"
    cat "$output_file"
    echo
  fi

  if [[ "$send_email" == "true" ]]; then
    [[ -n "$email" ]] || die "--send-email requires --email <addr>"
    send_bundle_email "$email" "$output_file" "$peer_id" "$account"
    log_entry "OUTBOUND-BOOTSTRAP | mode:${mode} | to:${peer_id} | status:emailed | email:${email}"
  elif [[ -n "$email" ]]; then
    info "Email not sent automatically. Re-run with --send-email, or send the bundle file manually to: $email"
  elif [[ "$send_email" != "true" && "$assume_yes" != "true" ]] && is_tty && (have_cmd gog || have_cmd himalaya); then
    # Interactive: offer to email the bundle
    echo
    if prompt_yn "Email this bundle to the peer?" "y"; then
      local interactive_email interactive_account=""
      prompt interactive_email "Recipient email address"
      if [[ -n "$interactive_email" ]]; then
        # REF-616: selection-only From confirmation. If himalaya is present
        # and at least one account resolves to a real email, show the
        # From/To/Subject preview and let the operator Y / n / change-account.
        # No free-text account name entry.
        if have_cmd himalaya; then
          local default_acct
          default_acct="$(default_himalaya_account)"
          if [[ -n "$default_acct" ]] && [[ -n "$(himalaya_account_email "$default_acct")" ]]; then
            local bundle_subject="Antenna bootstrap bundle from $(self_id) for ${peer_id}"
            interactive_account="$(confirm_from_account "$default_acct" "$interactive_email" "$bundle_subject" || true)"
            if [[ -z "$interactive_account" ]]; then
              info "Email aborted. Bundle file remains at: $output_file"
              return 0
            fi
          fi
        fi
        send_bundle_email "$interactive_email" "$output_file" "$peer_id" "$interactive_account"
        log_entry "OUTBOUND-BOOTSTRAP | mode:${mode} | to:${peer_id} | status:emailed | email:${interactive_email}"
      fi
    fi
  fi

  if [[ "$mode" == "reply" ]]; then
    ok "Reply bundle ready for ${peer_id}"
  else
    ok "Initiation bundle ready for ${peer_id}"
  fi
}

decrypt_bundle_to_json() {
  local input_path="$1" json_out
  require_age
  ensure_exchange_keypair false >/dev/null
  json_out=$(mktemp)
  if [[ "$input_path" == "-" ]]; then
    age -d -i "$EXCHANGE_KEY_FILE" -o "$json_out" -
  else
    [[ -f "$input_path" ]] || die "Bundle file not found: $input_path"
    age -d -i "$EXCHANGE_KEY_FILE" -o "$json_out" "$input_path"
  fi
  printf '%s\n' "$json_out"
}

validate_bundle_json() {
  local bundle_json="$1"
  # REF-2000: shape check is delegated to lib/bundles.sh so the import
  # path and `antenna bundle verify` agree on what "valid" means.
  local _shape_reason
  if ! _shape_reason="$(bundle_shape_reason "$bundle_json" 2>&1 >/dev/null)"; then
    die "Decrypted bundle JSON is missing required fields or is malformed: ${_shape_reason:-unknown reason}"
  fi

  # REF-1313: enforce URL shape on the incoming endpoint. Prior to this,
  # any non-empty string (e.g. "main") would pass and land verbatim in the
  # receiver's peer record, later causing mis-routed sends with a real
  # hook token attached. Independent of sender-side checks so a peer on
  # an older or broken toolchain cannot poison our state.
  local _url_reason
  if ! _url_reason="$(bundle_endpoint_url_reason "$bundle_json" 2>&1 >/dev/null)"; then
    die "Decrypted bundle has an invalid ${_url_reason:-from_endpoint_url}

Refusing to import. Ask the sender to fix their self peer's .url (it must be
a real https:// URL) and regenerate the bundle."
  fi
}

validate_bundle_freshness() {
  local bundle_json="$1" force_expired="${2:-false}"
  local now expires_at
  now="$(now_iso)"
  expires_at="$(jq -r '.expires_at' "$bundle_json")"

  if [[ "$force_expired" == "true" ]]; then
    return 0
  fi

  jq -e --arg now "$now" '.expires_at >= $now' "$bundle_json" >/dev/null || \
    die "Bundle expired at ${expires_at} (now: ${now}). Ask the sender to regenerate, or re-run with --force-expired if you really want to import it."
}

print_import_preview() {
  local bundle_json="$1" self_peer="$2"
  echo
  header "Import preview"
  echo "  Peer ID:        $(jq -r '.from_peer_id' "$bundle_json")"
  echo "  Display name:   $(jq -r '.from_display_name // "—"' "$bundle_json")"
  echo "  Endpoint URL:   $(jq -r '.from_endpoint_url' "$bundle_json")"
  echo "  Agent ID:       $(jq -r '.from_agent_id // "antenna"' "$bundle_json")"
  echo "  Generated at:   $(jq -r '.generated_at // "—"' "$bundle_json")"
  echo "  Expires at:     $(jq -r '.expires_at // "—"' "$bundle_json")"
  echo "  Bundle ID:      $(jq -r '.bundle_id // "—"' "$bundle_json")"
  echo "  Exchange pubkey:$(jq -r '.from_exchange_pubkey' "$bundle_json")"
  echo "  Notes:          $(jq -r '.notes // "—"' "$bundle_json")"
  local expected_peer
  expected_peer=$(jq -r '.expected_peer_id // empty' "$bundle_json")
  if [[ -n "$expected_peer" ]]; then
    echo "  Expected peer:  $expected_peer"
    if [[ "$expected_peer" != "$self_peer" ]]; then
      warn "Bundle says it was intended for '$expected_peer', but this host identifies as '$self_peer'."
    fi
  fi

  # REF-600: surface self-identity collision clearly at preview time.
  local bundle_peer
  bundle_peer=$(jq -r '.from_peer_id' "$bundle_json")
  if [[ -n "$bundle_peer" && "$bundle_peer" == "$self_peer" ]]; then
    warn "Bundle claims to be FROM peer '$bundle_peer' — the same ID this host uses for itself."
    warn "Import will be refused to protect the self-peer entry. Rename the remote peer and re-issue."
  fi
}

import_bundle() {
  local input_path="$1" assume_yes="$2" force_expired="${3:-false}"
  local bundle_json peer_id display_name endpoint agent_id exchange_pubkey expected_peer self_peer
  local existing_url existing_name existing_token_ref existing_secret_ref existing_agent
  local token_ref token_abs secret_ref secret_abs add_inbound add_outbound
  local hooks_token identity_secret

  bundle_json="$(decrypt_bundle_to_json "$input_path")"
  # REF-603: the decrypted bundle contains from_identity_secret + from_hooks_token
  # in cleartext on disk. Guarantee cleanup on EVERY exit path, including any
  # `die` from validate_bundle_json / validate_bundle_freshness / print_import_preview,
  # SIGINT during the confirm prompt, or a failure of the write steps below.
  # Previously only happy-path `rm -f` calls ran, so a failed validate could
  # leave the plaintext sitting in /tmp until the next reboot.
  #
  # The trap command uses double quotes so "$bundle_json" is expanded now, at
  # trap-install time. This matters because bundle_json is `local`: under
  # `set -u`, a trap that referenced it at fire time (after the local scope
  # collapses on RETURN) would blow up with "unbound variable". mktemp paths
  # are safe to embed verbatim — no shell metachars.
  # shellcheck disable=SC2064
  trap "rm -f '$bundle_json' 2>/dev/null || true" RETURN EXIT INT TERM
  validate_bundle_json "$bundle_json"
  validate_bundle_freshness "$bundle_json" "$force_expired"

  self_peer="$(self_id)"
  [[ -n "$self_peer" ]] || die "No self peer found in peers file. Run 'antenna setup' first."

  peer_id=$(jq -r '.from_peer_id' "$bundle_json")
  display_name=$(jq -r '.from_display_name // empty' "$bundle_json")
  endpoint=$(jq -r '.from_endpoint_url' "$bundle_json")
  agent_id=$(jq -r '.from_agent_id // "antenna"' "$bundle_json")
  exchange_pubkey=$(jq -r '.from_exchange_pubkey' "$bundle_json")
  expected_peer=$(jq -r '.expected_peer_id // empty' "$bundle_json")
  hooks_token=$(jq -r '.from_hooks_token' "$bundle_json")
  identity_secret=$(jq -r '.from_identity_secret' "$bundle_json")

  validate_age_pubkey "$exchange_pubkey"
  validate_runtime_secret "$identity_secret"

  # REF-600: primary guard against self-identity hijack.
  # A bundle must never be allowed to overwrite the local self-peer entry.
  # The self-peer is determined by '.self: true' in antenna-peers.json, not
  # by the from_peer_id in an (even validly encrypted) bundle. Refuse before
  # any writes occur; no --yes override is accepted for this condition.
  # REF-603: the RETURN/EXIT trap installed above handles bundle_json removal;
  # no explicit `rm -f` needed here.
  if [[ "$peer_id" == "$self_peer" ]]; then
    log_entry "INBOUND-BOOTSTRAP | from:${peer_id} | status:refused | reason:self_identity_collision"
    die "Refusing import: bundle claims peer_id='${peer_id}', which is this host's own self-peer.

This could indicate:
  - A bundle accidentally addressed to the wrong side of an exchange.
  - An attacker attempting to hijack the self-peer identity.

Self-peer identity is derived from antenna-peers.json (.self == true) and
cannot be rewritten by import. If the remote needs a different name, have
them re-run 'antenna setup' with a distinct peer_id and issue a new bundle."
  fi

  print_import_preview "$bundle_json" "$self_peer"

  if [[ -n "$expected_peer" && "$expected_peer" != "$self_peer" ]]; then
    confirm_or_die "Continue importing even though the bundle expects peer '$expected_peer' instead of '$self_peer'?" "$assume_yes" || die "Import cancelled."
  fi

  confirm_or_die "Import this bundle and write peer files?" "$assume_yes" || die "Import cancelled."

  if [[ "$assume_yes" == "true" ]]; then
    add_inbound=true
    add_outbound=true
  elif is_tty; then
    if prompt_yn "Add ${peer_id} to allowed_inbound_peers?" "y"; then add_inbound=true; else add_inbound=false; fi
    if prompt_yn "Add ${peer_id} to allowed_outbound_peers?" "y"; then add_outbound=true; else add_outbound=false; fi
  else
    die "Allowlist confirmation required in non-interactive mode. Re-run with --yes to accept the default allowlist updates."
  fi

  existing_url="$(peer_field "$peer_id" 'url')"
  existing_name="$(peer_field "$peer_id" 'display_name')"
  existing_agent="$(peer_field "$peer_id" 'agentId')"

  # Always use peer-specific paths for imported tokens and secrets.
  # This prevents stale references from a previous install from causing
  # the new token to be written to the wrong file (Issue #11).
  token_ref="secrets/hooks_token_${peer_id}"
  secret_ref="secrets/antenna-peer-${peer_id}.secret"

  token_abs="$(resolve_path "$token_ref")"
  secret_abs="$(resolve_path "$secret_ref")"
  mkdir -p "$(dirname "$token_abs")" "$(dirname "$secret_abs")"

  printf '%s' "$hooks_token" > "$token_abs"
  printf '%s' "$identity_secret" > "$secret_abs"
  chmod 600 "$token_abs" "$secret_abs"

  ensure_peer_entry_updated \
    "$peer_id" \
    "$endpoint" \
    "$token_ref" \
    "$secret_ref" \
    "${agent_id:-$existing_agent}" \
    "${display_name:-$existing_name}" \
    "$exchange_pubkey"

  update_allowlists "$peer_id" "$add_inbound" "$add_outbound"

  ok "Imported encrypted bootstrap bundle for $peer_id"
  info "Token file:  $token_abs"
  info "Secret file: $secret_abs"
  info "Allowlists: inbound=$add_inbound outbound=$add_outbound"
  log_entry "INBOUND-BOOTSTRAP | from:${peer_id} | status:imported | inbound:${add_inbound} | outbound:${add_outbound}"

  echo
  info "Next step: if you need to reciprocate, run: antenna peers exchange reply $peer_id"
  # REF-603: bundle_json removal is handled by the RETURN/EXIT trap installed at
  # the top of import_bundle. Nothing to do here.
}

cmd_keygen() {
  local force=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force) force=true; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown option for keygen: $1" ;;
    esac
  done
  ensure_exchange_keypair "$force"
}

send_pubkey_email() {
  local email_to="$1" account="${2:-}"
  local sid pubkey subject

  sid="$(self_id)"
  pubkey="$(current_exchange_pubkey)"
  subject="Antenna exchange public key from ${sid}"

  local body_text="Antenna exchange public key from ${sid}:

${pubkey}

To use this key when creating a bootstrap bundle for ${sid}:
  antenna peers exchange initiate ${sid} --pubkey ${pubkey}

Or save the attached .agepub file and use:
  antenna peers exchange initiate ${sid} --pubkey-file <saved-file>"

  local pubkey_file
  pubkey_file=$(mktemp --suffix="-${sid}.agepub")
  printf '%s\n' "$pubkey" > "$pubkey_file"

  # Method 1: gog
  if have_cmd gog; then
    local gog_account="${account:-}"
    [[ -n "$gog_account" ]] && ! [[ "$gog_account" == *@* ]] && gog_account=""
    local gog_args=(gmail send --to "$email_to" --subject "$subject" --body "$body_text" --attach "$pubkey_file" --force)
    [[ -n "$gog_account" ]] && gog_args=(gmail send --account "$gog_account" --to "$email_to" --subject "$subject" --body "$body_text" --attach "$pubkey_file" --force)
    if gog "${gog_args[@]}" >/dev/null 2>&1; then
      rm -f "$pubkey_file"
      ok "Sent exchange public key to $email_to via gog (Gmail API)"
      return 0
    fi
    warn "gog send failed; trying himalaya fallback..."
  fi

  # Method 2: himalaya
  if have_cmd himalaya; then
    if [[ -z "$account" ]]; then
      account="$(default_himalaya_account)"
    fi
    [[ -n "$account" ]] || { rm -f "$pubkey_file"; die "No email account found."; }

    # REF-616: resolve account email from himalaya config.toml — no antenna@localhost fallback.
    local from_addr raw_file
    from_addr="$(himalaya_account_email "$account")"
    if [[ -z "$from_addr" ]]; then
      rm -f "$pubkey_file"
      local cfg_hint
      cfg_hint="$(himalaya_config_path)"
      [[ -n "$cfg_hint" ]] || cfg_hint="${XDG_CONFIG_HOME:-$HOME/.config}/himalaya/config.toml"
      die "Could not resolve email address for himalaya account '$account'. Check [accounts.$account].email in $cfg_hint"
    fi

    raw_file=$(mktemp)
    cat > "$raw_file" <<EOF
From: ${sid} <${from_addr}>
To: ${email_to}
Subject: ${subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="ANTENNAPUBKEY"

--ANTENNAPUBKEY
Content-Type: text/plain; charset=UTF-8

${body_text}

--ANTENNAPUBKEY
Content-Type: text/plain; name="${sid}-exchange.agepub"
Content-Disposition: attachment; filename="${sid}-exchange.agepub"

${pubkey}

--ANTENNAPUBKEY--
EOF
    himalaya message send -a "$account" < "$raw_file" >/dev/null
    rm -f "$raw_file" "$pubkey_file"
    ok "Sent exchange public key to $email_to via himalaya ($from_addr)"
    return 0
  fi

  rm -f "$pubkey_file"
  die "No email tool available (tried gog, himalaya). Share the public key manually."
}

cmd_pubkey() {
  local bare=false email="" account="" send_email=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --bare) bare=true; shift ;;
      --email) email="$2"; shift 2 ;;
      --account) account="$2"; shift 2 ;;
      --send-email) send_email=true; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown option for pubkey: $1" ;;
    esac
  done
  ensure_exchange_keypair false >/dev/null
  if [[ "$bare" == "true" ]]; then
    current_exchange_pubkey
  else
    echo
    echo -e "${BOLD}Antenna exchange public key:${NC}"
    echo
    current_exchange_pubkey
    echo
    info "Share this public key with the peer that will encrypt your bootstrap bundle."

    # Send by email if requested
    if [[ "$send_email" == "true" ]]; then
      [[ -n "$email" ]] || die "--send-email requires --email <addr>"
      send_pubkey_email "$email" "$account"
    elif [[ "$send_email" != "true" ]] && is_tty && (have_cmd gog || have_cmd himalaya); then
      # Interactive: offer to email
      echo
      if prompt_yn "Email this public key to a peer?" "y"; then
        local interactive_email interactive_account=""
        prompt interactive_email "Recipient email address"
        if [[ -n "$interactive_email" ]]; then
          # REF-616: selection-only From confirmation (see send_bundle_email path).
          if have_cmd himalaya; then
            local default_acct
            default_acct="$(default_himalaya_account)"
            if [[ -n "$default_acct" ]] && [[ -n "$(himalaya_account_email "$default_acct")" ]]; then
              local pubkey_subject="Antenna exchange public key from $(self_id)"
              interactive_account="$(confirm_from_account "$default_acct" "$interactive_email" "$pubkey_subject" || true)"
              if [[ -z "$interactive_account" ]]; then
                info "Email aborted."
                return 0
              fi
            fi
          fi
          send_pubkey_email "$interactive_email" "$interactive_account"
        fi
      fi
    fi
  fi
}

cmd_initiate_or_reply() {
  local mode="$1"
  shift
  local peer_id="${1:-}"
  [[ -n "$peer_id" ]] || die "Usage: antenna peers exchange ${mode} <peer-id> [options]"
  shift || true

  local pubkey_arg="" pubkey_file_arg="" email="" account="" output_path=""
  local print_bundle=false send_email=false notes="" assume_yes=false legacy_mode=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --pubkey) pubkey_arg="$2"; shift 2 ;;
      --pubkey-file) pubkey_file_arg="$2"; shift 2 ;;
      --email) email="$2"; shift 2 ;;
      --account) account="$2"; shift 2 ;;
      --output) output_path="$2"; shift 2 ;;
      --print) print_bundle=true; shift ;;
      --send-email) send_email=true; shift ;;
      --notes) notes="$2"; shift 2 ;;
      --yes) assume_yes=true; shift ;;
      --legacy) legacy_mode=true; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown option for ${mode}: $1" ;;
    esac
  done

  run_bundle_command "$mode" "$peer_id" "$pubkey_arg" "$pubkey_file_arg" "$email" "$account" "$output_path" "$print_bundle" "$send_email" "$notes" "$assume_yes" "$legacy_mode"
}

cmd_import() {
  local input_path="${1:-}"
  shift || true
  [[ -n "$input_path" ]] || input_path="-"
  local assume_yes=false
  local force_expired=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --yes) assume_yes=true; shift ;;
      --force-expired) force_expired=true; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown option for import: $1" ;;
    esac
  done
  import_bundle "$input_path" "$assume_yes" "$force_expired"
}

cmd_legacy_peer_entry() {
  local peer_id="$1"
  shift || true
  local mode="initiate" import_path="" import_value="" legacy_mode=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --export) mode="export"; shift ;;
      --import) mode="import-file"; import_path="$2"; shift 2 ;;
      --import-value) mode="import-value"; import_value="$2"; shift 2 ;;
      --legacy) legacy_mode=true; shift ;;
      -h|--help) usage; exit 0 ;;
      *)
        if [[ "$mode" == "initiate" ]]; then
          # Pass through to the new initiate parser.
          cmd_initiate_or_reply initiate "$peer_id" "$@"
          return 0
        fi
        die "Unknown option: $1"
        ;;
    esac
  done

  case "$mode" in
    export)
      legacy_export_runtime_secret "$peer_id"
      ;;
    import-file)
      [[ -f "$import_path" ]] || die "File not found: $import_path"
      legacy_import_runtime_secret "$peer_id" "$(tr -d '[:space:]' < "$import_path")"
      ;;
    import-value)
      legacy_import_runtime_secret "$peer_id" "$(printf '%s' "$import_value" | tr -d '[:space:]')"
      ;;
    initiate)
      if [[ "$legacy_mode" == "true" ]]; then
        cmd_initiate_or_reply initiate "$peer_id" --legacy
      else
        cmd_initiate_or_reply initiate "$peer_id"
      fi
      ;;
  esac
}

main() {
  ensure_core_files
  local command="${1:-help}"
  shift || true

  case "$command" in
    help|-h|--help)
      usage
      ;;
    keygen)
      cmd_keygen "$@"
      ;;
    pubkey)
      cmd_pubkey "$@"
      ;;
    initiate)
      cmd_initiate_or_reply initiate "$@"
      ;;
    reply)
      cmd_initiate_or_reply reply "$@"
      ;;
    import)
      cmd_import "$@"
      ;;
    *)
      cmd_legacy_peer_entry "$command" "$@"
      ;;
  esac
}

main "$@"
