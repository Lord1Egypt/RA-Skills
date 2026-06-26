#!/usr/bin/env bash
# antenna-pair.sh — Interactive pairing wizard for connecting to a remote peer.
# Can be launched standalone (antenna pair) or auto-offered at end of setup.
#
# Usage:
#   antenna-pair.sh                    Interactive wizard
#   antenna-pair.sh --peer-id <id>     Pre-fill peer ID (still interactive)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
BIN_DIR="$SKILL_DIR/bin"
ANTENNA="$BIN_DIR/antenna.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ── Helpers ──────────────────────────────────────────────────────────────────

info()   { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()     { echo -e "${GREEN}✓${NC}  $*"; }
warn()   { echo -e "${YELLOW}⚠${NC}  $*"; }
err()    { echo -e "${RED}✗${NC}  $*" >&2; }
header() { echo -e "\n${BOLD}═══ $* ═══${NC}\n"; }

# Wizard step prompt: [N]ext  [S]kip  [Q]uit
# Returns 0 for Next, 1 for Skip, exits for Quit
wizard_prompt() {
  local step_num="$1" total="$2" label="$3" can_skip="${4:-true}"
  echo ""
  echo -e "  ${DIM}Step ${step_num}/${total}${NC}  ${BOLD}${label}${NC}"
  echo ""
  if [[ "$can_skip" == "true" ]]; then
    local choice
    read -rp "$(echo -e "  ${CYAN}▸${NC} [${BOLD}N${NC}]ext  [${BOLD}S${NC}]kip  [${BOLD}Q${NC}]uit: ")" choice
    case "${choice,,}" in
      n|next|"") return 0 ;;
      s|skip)    return 1 ;;
      q|quit)
        echo ""
        info "No worries — pick up where you left off anytime:  ${BOLD}antenna pair${NC}"
        exit 0
        ;;
      *) return 0 ;;
    esac
  else
    local choice
    read -rp "$(echo -e "  ${CYAN}▸${NC} [${BOLD}N${NC}]ext  [${BOLD}Q${NC}]uit: ")" choice
    case "${choice,,}" in
      q|quit)
        echo ""
        info "No worries — pick up where you left off anytime:  ${BOLD}antenna pair${NC}"
        exit 0
        ;;
      *) return 0 ;;
    esac
  fi
}

prompt_value() {
  local var_name="$1" prompt_text="$2" default="${3:-}"
  local value
  if [[ -n "$default" ]]; then
    read -rp "$(echo -e "  ${CYAN}?${NC}  ${prompt_text} [${default}]: ")" value
    value="${value:-$default}"
  else
    read -rp "$(echo -e "  ${CYAN}?${NC}  ${prompt_text}: ")" value
  fi
  eval "$var_name=\$value"
}

wait_for_enter() {
  local msg="${1:-Press Enter when ready}"
  read -rp "$(echo -e "  ${CYAN}▸${NC} ${msg}... ")" _discard
}

# ── Parse args ───────────────────────────────────────────────────────────────

PEER_ID=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --peer-id) PEER_ID="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: antenna pair [--peer-id <id>]"
      echo "  Interactive wizard for pairing with a remote Antenna peer."
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

TOTAL_STEPS=8
USED_CLAWREEF=false

# ══════════════════════════════════════════════════════════════════════════════

header "🦞 Antenna Pairing Wizard"

echo -e "  Let's connect you to another host on the reef."
echo -e "  Each step has Next / Skip / Quit — go at your own pace."
echo -e "  You can bail out anytime and pick up where you left off:  ${BOLD}antenna pair${NC}"
echo ""
echo -e "  ${DIM}Two paths to connect:${NC}"
echo -e "    ${CYAN}•${NC} Direct exchange — share keys, build encrypted bundles (steps below)"
echo -e "    ${CYAN}•${NC} ClawReef invite — find a peer at ${BOLD}clawreef.io${NC} and send an invite"

# ── Step 1: Generate exchange keypair ────────────────────────────────────────

if wizard_prompt 1 $TOTAL_STEPS "Generate your exchange keypair"; then
  # Check if keypair already exists
  EXCHANGE_KEY_DIR="$SKILL_DIR/secrets"
  if [[ -f "$EXCHANGE_KEY_DIR/exchange-key.txt" ]]; then
    warn "You've already got a keypair — no need to generate a new one unless you want a fresh start."
    if ! prompt_value _regen "  Regenerate? (y/N)" "n"; then true; fi
    if [[ "${_regen,,}" == "y" || "${_regen,,}" == "yes" ]]; then
      bash "$ANTENNA" peers exchange keygen --force
    else
      ok "Keeping existing keypair."
    fi
  else
    bash "$ANTENNA" peers exchange keygen
  fi
fi

# ── Step 2: Display your public key ─────────────────────────────────────────

if wizard_prompt 2 $TOTAL_STEPS "Share your public key" false; then
  echo ""
  echo -e "  Here's your public key — share it with your peer."
  echo -e "  It's safe to post openly; it's a lock, not a key."
  echo ""
  PUBKEY=$("$ANTENNA" peers exchange pubkey --bare 2>/dev/null || echo "")
  if [[ -n "$PUBKEY" ]]; then
    echo -e "  ${GREEN}${PUBKEY}${NC}"
    echo ""
    info "Your peer needs this to encrypt a bootstrap bundle that only you can open."
  else
    err "No public key found — run: antenna peers exchange keygen"
  fi
  echo ""
  wait_for_enter "Press Enter once your peer has your key"
fi

# ── Step 3: ClawReef invite (alternative path) ───────────────────────────────

if wizard_prompt 3 $TOTAL_STEPS "Send a ClawReef invite instead? 🪸"; then
  echo ""
  echo -e "  If your peer is on ${BOLD}clawreef.io${NC}, you can send them an invite"
  echo -e "  through the registry instead of exchanging bundles manually."
  echo ""
  echo -e "  ${BOLD}How it works:${NC}"
  echo -e "    1. Log in at ${CYAN}https://clawreef.io${NC}"
  echo -e "    2. Go to ${BOLD}Invites${NC} → search for your peer by name"
  echo -e "    3. Send the invite — ClawReef delivers it via Antenna"
  echo -e "    4. When they accept, you both finish pairing locally"
  echo ""
  echo -e "  ${DIM}If they're not on ClawReef (or you prefer direct exchange),${NC}"
  echo -e "  ${DIM}choose [S]kip and continue with the encrypted bundle steps below.${NC}"
  echo -e "  ${DIM}You can also skip and share bundles by email or another method.${NC}"
  echo ""
  USED_CLAWREEF=false
  if [[ -t 0 ]]; then
    prompt_value _cr_choice "Open clawreef.io/registry/dashboard/invites in your browser? (y/N)" "n"
    if [[ "${_cr_choice,,}" == "y" || "${_cr_choice,,}" == "yes" ]]; then
      USED_CLAWREEF=true
      # Try to open browser (works on most platforms)
      if command -v xdg-open &>/dev/null; then
        xdg-open "https://clawreef.io/registry/dashboard/invites" 2>/dev/null &
      elif command -v open &>/dev/null; then
        open "https://clawreef.io/registry/dashboard/invites" 2>/dev/null &
      else
        echo -e "  ${CYAN}→${NC} https://clawreef.io/registry/dashboard/invites"
      fi
      echo ""
      wait_for_enter "Press Enter once you've sent your invite (or to continue with direct exchange)"
    fi
  fi
fi

# ── Step 4: Get peer info and create bundle ──────────────────────────────────

if wizard_prompt 4 $TOTAL_STEPS "Build a bootstrap bundle for your peer"; then
  if [[ "$USED_CLAWREEF" == "true" ]]; then
    echo ""
    info "Already sent a ClawReef invite? You can ${BOLD}[S]kip${NC} steps 4–6."
    info "They're for direct encrypted exchange — not needed if you're using ClawReef."
    echo ""
  fi
  echo ""
  # Get peer ID
  if [[ -z "$PEER_ID" ]]; then
    prompt_value PEER_ID "Peer ID (a short name for the remote host, e.g. 'myserver')" ""
  else
    echo -e "  ${CYAN}ℹ${NC}  Peer ID: ${BOLD}${PEER_ID}${NC}"
  fi

  if [[ -z "$PEER_ID" ]]; then
    err "Need a peer ID to continue — what do you call the other host?"
  else
    prompt_value PEER_PUBKEY "Their age public key (starts with age1...)"
    if [[ -z "$PEER_PUBKEY" ]]; then
      err "Can't build a bundle without their public key — ask your peer for it."
    else
      echo ""
      info "Building your encrypted bootstrap bundle..."
      echo ""
      BUNDLE_OUTPUT=$(bash "$ANTENNA" peers exchange initiate "$PEER_ID" --pubkey "$PEER_PUBKEY" 2>&1) || true
      echo "$BUNDLE_OUTPUT"

      # Extract bundle file path from output
      BUNDLE_FILE=$(echo "$BUNDLE_OUTPUT" | grep -oP 'Bundle file: \K.*' || echo "")
      if [[ -n "$BUNDLE_FILE" ]]; then
        echo ""
        ok "Bundle created!"
        echo ""
        echo -e "  ${BOLD}Send this file to your peer:${NC}"
        echo -e "  ${CYAN}${BUNDLE_FILE}${NC}"
        echo ""
        echo -e "  ${DIM}Email attachment, scp, carrier pigeon — whatever works.${NC}"
        echo -e "  ${DIM}Just don't paste the contents inline; email clients love to mangle encoded text.${NC}"

        # Default state: no email attempted. We'll flip these when we try.
        BUNDLE_EMAIL_ATTEMPTED="n"
        BUNDLE_EMAIL_DELIVERED="n"

        if command -v gog >/dev/null 2>&1 || command -v himalaya >/dev/null 2>&1; then
          echo ""
          prompt_value SEND_BUNDLE_EMAIL "Email this bundle to your peer now? (y/N)" "n"
          if [[ "${SEND_BUNDLE_EMAIL,,}" == "y" || "${SEND_BUNDLE_EMAIL,,}" == "yes" ]]; then
            prompt_value BUNDLE_EMAIL "Recipient email address" ""
            if [[ -n "$BUNDLE_EMAIL" ]]; then
              BUNDLE_EMAIL_ACCOUNT=""
              if command -v himalaya >/dev/null 2>&1; then
                prompt_value BUNDLE_EMAIL_ACCOUNT "Himalaya account name (optional, press Enter to use default/Gmail)" ""
              fi
              echo ""
              info "Sending encrypted bundle email..."
              echo ""
              EMAIL_ARGS=(peers exchange initiate "$PEER_ID" --pubkey "$PEER_PUBKEY" --output "$BUNDLE_FILE" --email "$BUNDLE_EMAIL" --send-email)
              if [[ -n "$BUNDLE_EMAIL_ACCOUNT" ]]; then
                EMAIL_ARGS+=(--account "$BUNDLE_EMAIL_ACCOUNT")
              fi
              BUNDLE_EMAIL_ATTEMPTED="y"
              # REF-1206c: capture exit status of the send subcommand and
              # classify delivery honestly. Previously this was `|| true`
              # and the wizard then unconditionally printed
              # "Press Enter once you've sent it off...", which read as a
              # success confirmation even when both gog and himalaya had
              # failed. That is a soft-success in a security-critical step;
              # operators should only see "sent it off" language when the
              # send actually succeeded.
              set +e
              EMAIL_OUTPUT=$(bash "$ANTENNA" "${EMAIL_ARGS[@]}" 2>&1)
              EMAIL_EXIT=$?
              set -e
              echo "$EMAIL_OUTPUT"
              if [[ $EMAIL_EXIT -eq 0 ]]; then
                BUNDLE_EMAIL_DELIVERED="y"
              fi
            else
              warn "No email address entered — skipping email send."
            fi
          fi
        fi
      fi
    fi
  fi
  echo ""
  # REF-1206c: branch the post-email UX on real delivery status.
  if [[ "${BUNDLE_EMAIL_ATTEMPTED:-n}" == "y" && "${BUNDLE_EMAIL_DELIVERED:-n}" == "y" ]]; then
    ok "Bundle emailed. Waiting for your peer to import it and reply."
  elif [[ "${BUNDLE_EMAIL_ATTEMPTED:-n}" == "y" ]]; then
    err "Email delivery failed — bundle was NOT sent."
    if [[ -n "${BUNDLE_FILE:-}" ]]; then
      echo -e "  ${DIM}Transfer this file manually (scp, USB, encrypted drop):${NC}"
      echo -e "  ${CYAN}${BUNDLE_FILE}${NC}"
    fi
    echo ""
    prompt_value BUNDLE_DELIVERED_MANUALLY "Did you deliver it out of band? (y/N)" "n"
    if [[ "${BUNDLE_DELIVERED_MANUALLY,,}" != "y" && "${BUNDLE_DELIVERED_MANUALLY,,}" != "yes" ]]; then
      warn "Holding here. Re-run the wizard after you've delivered the bundle, or rerun with the bundle file path."
      exit 0
    fi
  else
    wait_for_enter "Press Enter once you've sent it off"
  fi
fi

# ── Step 5: Wait for their bundle ───────────────────────────────────────────

if wizard_prompt 5 $TOTAL_STEPS "Wait for their reply"; then
  echo ""
  echo -e "  Ball's in their court. They need to:"
  echo -e "    1. Import your bundle:  ${DIM}antenna peers exchange import <your-bundle>${NC}"
  echo -e "    2. Create a reply:      ${DIM}antenna peers exchange reply ${PEER_ID:-<your-host-id>}${NC}"
  echo -e "    3. Send you the reply file"
  echo ""
  echo -e "  This is a good time to grab coffee. ☕"
  echo ""
  wait_for_enter "Press Enter once you have their reply bundle"
fi

# ── Step 6: Import their bundle ─────────────────────────────────────────────

if wizard_prompt 6 $TOTAL_STEPS "Import their bundle"; then
  echo ""
  prompt_value IMPORT_FILE "Path to the reply bundle you received" ""
  # Expand leading ~ to $HOME (read doesn't do shell expansion)
  IMPORT_FILE="${IMPORT_FILE/#\~/$HOME}"
  if [[ -z "$IMPORT_FILE" ]]; then
    err "No file path provided."
  elif [[ ! -f "$IMPORT_FILE" ]]; then
    err "Can't find that file: $IMPORT_FILE — double-check the path?"
  else
    echo ""
    bash "$ANTENNA" peers exchange import "$IMPORT_FILE" || true
    echo ""
  fi
fi

# ── Step 7: Test connectivity ────────────────────────────────────────────────

if wizard_prompt 7 $TOTAL_STEPS "Test the connection"; then
  echo ""
  # Use PEER_ID if we have it, otherwise ask
  if [[ -z "$PEER_ID" ]]; then
    prompt_value PEER_ID "Peer ID to test"
  fi
  if [[ -n "$PEER_ID" ]]; then
    info "Pinging ${BOLD}${PEER_ID}${NC} — let's see if anyone's home..."
    echo ""
    bash "$ANTENNA" peers test "$PEER_ID" || true
    echo ""
  else
    err "No peer ID provided."
  fi
fi

# ── Step 8: Send first message ──────────────────────────────────────────────

if wizard_prompt 8 $TOTAL_STEPS "Send your first message! 🦞"; then
  echo ""
  if [[ -z "$PEER_ID" ]]; then
    prompt_value PEER_ID "Peer ID to message"
  fi
  if [[ -n "$PEER_ID" ]]; then
    prompt_value FIRST_MSG "Message to send" "Hello from the other side of the reef! 🦞"
    echo ""
    info "Releasing the lobster to ${BOLD}${PEER_ID}${NC}... 🦞"
    echo ""
    bash "$ANTENNA" msg "$PEER_ID" "$FIRST_MSG" || true
    echo ""
  else
    err "No peer ID provided."
  fi
fi

# ── Done ─────────────────────────────────────────────────────────────────────

header "🦞 You're Claw-nected!"

echo -e "  Welcome to the reef. Here's your cheat sheet:"
echo ""
echo -e "  ${BOLD}Send a message:${NC}     antenna msg ${PEER_ID:-<peer>} \"Your message\""
echo -e "  ${BOLD}Target a session:${NC}   antenna msg ${PEER_ID:-<peer>} --session agent:main:test \"Hi\""
echo -e "  ${BOLD}Check status:${NC}       antenna peers test ${PEER_ID:-<peer>}"
echo -e "  ${BOLD}List peers:${NC}         antenna peers list"
echo -e "  ${BOLD}Run diagnostics:${NC}    antenna doctor"
echo ""
ok "Happy messaging! The ocean just got smaller. 🦞 📡"
echo ""
