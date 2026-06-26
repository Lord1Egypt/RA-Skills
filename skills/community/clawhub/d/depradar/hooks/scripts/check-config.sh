#!/usr/bin/env bash
# /depradar session-start hook — checks API key configuration
# Runs once per session, silent on pass, prints a tip if GITHUB_TOKEN is missing.
#
# Exit codes:
#   0 — all good (or missing keys are non-critical)
#   0 — always exits 0 so it never blocks the session

set -euo pipefail

# ── Locate config files ────────────────────────────────────────────────────────
PROJECT_ENV=".claude/depradar.env"
GLOBAL_ENV="$HOME/.config/depradar/.env"

# Load project-level env if present
if [[ -f "$PROJECT_ENV" ]]; then
  # shellcheck source=/dev/null
  set -a; source "$PROJECT_ENV"; set +a
fi

# Load global env if present
if [[ -f "$GLOBAL_ENV" ]]; then
  # shellcheck source=/dev/null
  set -a; source "$GLOBAL_ENV"; set +a
fi

# ── Check keys ────────────────────────────────────────────────────────────────
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
SCRAPECREATORS_API_KEY="${SCRAPECREATORS_API_KEY:-}"
XAI_API_KEY="${XAI_API_KEY:-}"
STACKOVERFLOW_API_KEY="${STACKOVERFLOW_API_KEY:-}"

# Build a list of what is missing
missing=()
[[ -z "$GITHUB_TOKEN" ]] && missing+=("GITHUB_TOKEN")
[[ -z "$SCRAPECREATORS_API_KEY" ]] && missing+=("SCRAPECREATORS_API_KEY")
[[ -z "$XAI_API_KEY" ]] && missing+=("XAI_API_KEY")

# Count configured keys
configured=0
[[ -n "$GITHUB_TOKEN" ]] && ((configured++)) || true
[[ -n "$SCRAPECREATORS_API_KEY" ]] && ((configured++)) || true
[[ -n "$XAI_API_KEY" ]] && ((configured++)) || true
[[ -n "$STACKOVERFLOW_API_KEY" ]] && ((configured++)) || true

# ── Output ────────────────────────────────────────────────────────────────────
# Only print if GITHUB_TOKEN is missing — it's the highest-value key
if [[ -z "$GITHUB_TOKEN" ]]; then
  # Use terminal colour codes if the terminal supports them
  if [[ -t 1 ]] && command -v tput &>/dev/null && tput colors &>/dev/null && [[ "$(tput colors)" -ge 8 ]]; then
    YELLOW="\033[0;33m"
    RESET="\033[0m"
    printf "${YELLOW}[/depradar]${RESET} Tip: Add GITHUB_TOKEN to ~/.config/depradar/.env for 5,000 GitHub API req/hr (currently 60). Run \`/depradar --diagnose\` for setup instructions.\n"
  else
    printf "[/depradar] Tip: Add GITHUB_TOKEN to ~/.config/depradar/.env for 5,000 GitHub API req/hr (currently 60). Run '/depradar --diagnose' for setup instructions.\n"
  fi
fi

# Always exit 0 — never block the session
exit 0
