#!/bin/bash
# Conclave environment setup: detect OS -> detect -> install -> config checklist.
# Run BEFORE preflight.sh on first activation, after any CLI failure, or on a new machine.
# Supported: macOS, Linux (apt/dnf/pacman), WSL, Windows via Git Bash/MSYS2.
#
# Usage: bash install.sh [--check-only]
#   --check-only   Only detect and print the config checklist; do not install anything.
#
# Exit codes: 0 = all four CLIs installed (config warnings may still exist)
#             1 = one or more CLIs missing after the install attempt
#
# Security: this script NEVER reads, prints, or writes API keys or passwords.
# It only checks whether credential files / env-var names exist, then tells the
# user where to configure each provider.

set -u

CHECK_ONLY=0
[ "${1:-}" = "--check-only" ] && CHECK_ONLY=1

MISSING_INSTALL=0
CONFIG_WARN=0

ok()     { echo "  [OK]     $1"; }
miss()   { echo "  [MISS]   $1"; }
action() { echo "  [ACTION] $1"; CONFIG_WARN=$((CONFIG_WARN+1)); }
info()   { echo "           $1"; }

have() { command -v "$1" >/dev/null 2>&1; }

ver() { # best-effort version probe
  CONDA_NO_PLUGINS=true no_proxy='*' "$1" --version 2>/dev/null | head -1
}

# ---------- OS detection ----------
detect_os() {
  case "$(uname -s 2>/dev/null)" in
    Darwin) echo macos ;;
    Linux)
      if grep -qi microsoft /proc/version 2>/dev/null; then echo wsl; else echo linux; fi ;;
    MINGW*|MSYS*|CYGWIN*) echo windows ;;
    *) echo unknown ;;
  esac
}
OS="$(detect_os)"
echo "Detected OS: $OS"

# Shell rc files to grep for persisted env vars (existence only, platform-aware)
RC_FILES=""
for f in "$HOME/.zshrc" "$HOME/.zshenv" "$HOME/.zprofile" \
         "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"; do
  [ -f "$f" ] && RC_FILES="$RC_FILES $f"
done

# Primary rc file the user should edit on this platform (for ACTION messages)
case "$OS" in
  macos)   PRIMARY_RC="~/.zshrc" ;;
  windows) PRIMARY_RC="~/.bashrc (Git Bash) — and/or Windows user env vars" ;;
  *)       PRIMARY_RC="~/.bashrc" ;;
esac

rc_grep() { # $1 = pattern; returns 0 if found in any existing rc file
  # Guard: with no rc files, bare grep would block reading stdin.
  [ -n "$RC_FILES" ] && grep -qsE "$1" $RC_FILES 2>/dev/null
}

echo "=========================================="
echo " Phase 0: Dependency check (Node.js / npm)"
echo "=========================================="
install_node() {
  case "$OS" in
    macos)
      if have brew; then
        info "installing node via Homebrew..."
        brew install node
      else
        action "Node.js missing and Homebrew not found. Install Node.js >= 18: https://nodejs.org/ (or nvm), then re-run this script."
        return 1
      fi ;;
    linux|wsl)
      if have apt-get; then
        info "installing node via apt-get (may prompt for sudo password)..."
        sudo apt-get update -qq && sudo apt-get install -y nodejs npm
      elif have dnf; then
        info "installing node via dnf (may prompt for sudo password)..."
        sudo dnf install -y nodejs npm
      elif have pacman; then
        info "installing node via pacman (may prompt for sudo password)..."
        sudo pacman -S --noconfirm nodejs npm
      else
        action "Node.js missing and no apt/dnf/pacman found. Install Node.js >= 18 via nvm: https://github.com/nvm-sh/nvm — then re-run this script."
        return 1
      fi ;;
    windows)
      action "Node.js missing. Install it with: winget install OpenJS.NodeJS  (or https://nodejs.org/), then reopen Git Bash and re-run this script."
      return 1 ;;
    *)
      action "Node.js missing. Install Node.js >= 18 from https://nodejs.org/, then re-run this script."
      return 1 ;;
  esac
}

if have node && have npm; then
  ok "node $(node --version 2>/dev/null) / npm $(npm --version 2>/dev/null)"
else
  miss "node/npm not found"
  if [ "$CHECK_ONLY" -eq 1 ]; then
    MISSING_INSTALL=1
  else
    install_node || MISSING_INSTALL=1
    if have node && have npm; then
      ok "node $(node --version) / npm $(npm --version)"
    else
      miss "node install incomplete"
      MISSING_INSTALL=1
    fi
  fi
fi

npm_install() { # $1=npm package, $2=display name
  if [ "$CHECK_ONLY" -eq 1 ]; then
    miss "$2 (skipped, --check-only)"
    MISSING_INSTALL=1
    return
  fi
  info "installing $2 via: npm install -g $1"
  if CONDA_NO_PLUGINS=true no_proxy='*' npm install -g "$1" >/dev/null 2>&1 && have "$2"; then
    ok "$2 installed — $(ver "$2")"
  else
    miss "$2 install failed — run manually: npm install -g $1"
    MISSING_INSTALL=1
  fi
}

echo ""
echo "=========================================="
echo " Phase 1: Panelist CLI detection + install"
echo "=========================================="

echo "-- 1/4 Claude Code --"
if have claude; then
  ok "claude — $(ver claude)"
else
  npm_install "@anthropic-ai/claude-code" "claude"
fi

echo "-- 2/4 Codex --"
if have codex; then
  ok "codex — $(ver codex)"
else
  npm_install "@openai/codex" "codex"
fi

echo "-- 3/4 Gemini CLI --"
if have gemini; then
  ok "gemini — $(ver gemini)"
else
  npm_install "@google/gemini-cli" "gemini"
fi

echo "-- 4/4 Qwen --"
if have qwen; then
  ok "qwen — $(ver qwen)"
else
  npm_install "@qwen-code/qwen-code" "qwen"
fi

echo ""
echo "=========================================="
echo " Phase 2: API / auth configuration check"
echo " (existence checks only — no secrets read)"
echo "=========================================="

echo "-- Claude Code --"
CLAUDE_CRED=0
[ -f "$HOME/.claude/.credentials.json" ] && CLAUDE_CRED=1
if [ "$OS" = "macos" ] && security find-generic-password -s "Claude Code-credentials" >/dev/null 2>&1; then
  CLAUDE_CRED=1
fi
if [ "$CLAUDE_CRED" -eq 1 ]; then
  ok "claude credentials found"
else
  action "Claude not authenticated. Run 'claude' once interactively and complete the OAuth login."
fi
if [ "$OS" = "macos" ]; then
  info "macOS background sessions also need an unlocked login keychain — user must run, in an interactive terminal:"
  info "  security unlock-keychain ~/Library/Keychains/login.keychain-db"
fi

echo "-- Codex --"
if [ -f "$HOME/.codex/auth.json" ]; then
  ok "~/.codex/auth.json present"
  if [ -f "$HOME/.codex/config.toml" ]; then
    ok "~/.codex/config.toml present"
  else
    action "~/.codex/config.toml missing — create it with requires_openai_auth / wire_api / base_url per references/panelists.md."
  fi
else
  action "Codex auth missing — place the API key in ~/.codex/auth.json and set base_url in ~/.codex/config.toml (see references/panelists.md)."
fi

echo "-- Gemini CLI --"
if [ -n "${GEMINI_API_KEY:-}" ] || rc_grep "GEMINI_API_KEY"; then
  ok "GEMINI_API_KEY found (env or shell rc)"
else
  action "Gemini key missing — add 'export GEMINI_API_KEY=...' (and GOOGLE_GEMINI_BASE_URL if using a relay) to $PRIMARY_RC. Key format decides the provider (AQ.Ab8... = Google official, sk-... = relay); do not mix."
fi

echo "-- Qwen --"
if [ -f "$HOME/.qwen/settings.json" ] || [ -f "$HOME/.qwen/oauth_creds.json" ] \
   || [ -n "${OPENAI_API_KEY:-}" ] || rc_grep "OPENAI_API_KEY|DASHSCOPE_API_KEY"; then
  ok "qwen auth material found (~/.qwen/ or env)"
else
  action "Qwen not authenticated — either run 'qwen' once interactively to log in, or export OPENAI_API_KEY / OPENAI_BASE_URL in $PRIMARY_RC (see references/panelists.md)."
fi

echo "-- Manus (external advisor) --"
info "Manus runs through the Hermes MCP channel, not a local CLI."
info "The chair verifies it in-session via mcp__manus_mcp__create_task (see references/panelists.md)."

echo ""
echo "=========================================="
echo " Summary"
echo "=========================================="
if [ "$MISSING_INSTALL" -eq 0 ]; then
  echo " CLIs: all four installed."
else
  echo " CLIs: some installs missing/failed — fix the [MISS] items above and re-run."
fi
if [ "$CONFIG_WARN" -eq 0 ]; then
  echo " Config: all credential material detected."
  echo " Next: bash ~/.hermes/skills/conclave/scripts/preflight.sh <arena-path>"
else
  echo " Config: $CONFIG_WARN provider(s) need action — complete every [ACTION] line above,"
  echo "         then run preflight.sh to verify end-to-end."
fi

[ "$MISSING_INSTALL" -eq 0 ]
