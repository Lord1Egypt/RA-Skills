#!/usr/bin/env bash
# OpenClaw Boot Camp — Agent CLI Training (v1.2.1)
# Discovers CLI commands/flags and generates a reference doc for your agent.
# https://clawhub.ai/dank-varley/bootcamp

set -euo pipefail

# ── Colors & Formatting ──────────────────────────────────────────────
BOLD='\033[1m'
DIM='\033[2m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

# ── Defaults ─────────────────────────────────────────────────────────
OPENCLAW_HOME="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
COMPLETION_FILE="$OPENCLAW_HOME/completions/openclaw.bash"
WORKSPACE_NOTES="$OPENCLAW_HOME/workspace/notes"
OUTPUT_FILE="openclaw-cli-reference.md"
ENRICH_MODE=false
NON_INTERACTIVE=false
VERSION=""

# ── CLI argument parsing ─────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --enrich) ENRICH_MODE=true ;;
    --yes|-y) NON_INTERACTIVE=true ;;
    --output=*) WORKSPACE_NOTES="${arg#*=}" ;;
    --help|-h)
      echo "Usage: bash bootcamp.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --enrich    Run Phase 2: agent-assisted enrichment from docs"
      echo "  --yes, -y   Non-interactive mode (overwrite existing, skip prompts)"
      echo "  --output=   Custom output directory (default: ~/.openclaw/workspace/notes)"
      echo "  --help, -h  Show this help"
      exit 0
      ;;
  esac
done

# ── Helpers ──────────────────────────────────────────────────────────
banner() {
  echo ""
  echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════╗${RESET}"
  echo -e "${CYAN}${BOLD}║       🦞 OpenClaw Boot Camp — Agent CLI Training        ║${RESET}"
  echo -e "${CYAN}${BOLD}║       Generates a CLI reference for your agent           ║${RESET}"
  echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════╝${RESET}"
  echo ""
}

progress() {
  echo -e "  ${DIM}$1${RESET} $2"
}

success() {
  echo -e "  ${GREEN}✅${RESET} $1"
}

warn() {
  echo -e "  ${YELLOW}⚠${RESET}  $1"
}

fail() {
  echo -e "  ${RED}✗${RESET}  $1"
  exit 1
}

separator() {
  echo -e "${DIM}────────────────────────────────────────────────────────────${RESET}"
}

# ── Detect OpenClaw ──────────────────────────────────────────────────
detect_version() {
  if ! command -v openclaw &>/dev/null; then
    fail "OpenClaw not found in PATH. Install it first: https://docs.openclaw.ai"
  fi
  VERSION=$(openclaw --version 2>/dev/null | head -1 | grep -oP 'v?\K[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
  echo -e "  Detected OpenClaw version: ${BOLD}$VERSION${RESET}"
  echo -e "  Workspace: ${DIM}$OPENCLAW_HOME${RESET}"
}

# ── Check for existing doc ───────────────────────────────────────────
check_existing_doc() {
  local target="$WORKSPACE_NOTES/$OUTPUT_FILE"
  if [[ -f "$target" ]]; then
    # Extract version from existing doc
    local existing_ver
    existing_ver=$(grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' "$target" 2>/dev/null | head -1 || echo "unknown")
    echo ""
    warn "Existing reference found: $OUTPUT_FILE ($existing_ver)"
    echo -e "  You are running: ${BOLD}v$VERSION${RESET}"
    echo ""

    if [[ "$NON_INTERACTIVE" == true ]]; then
      echo "  Non-interactive mode: overwriting."
      return 0
    fi

    echo -e "  ${BOLD}[1]${RESET} Overwrite (replace with current version)"
    echo -e "  ${BOLD}[2]${RESET} Keep both (saves as openclaw-cli-reference-v${VERSION}.md)"
    echo -e "  ${BOLD}[q]${RESET} Cancel"
    echo ""
    read -rp "  Select [1/2/q]: " choice
    case "$choice" in
      1) return 0 ;;
      2) OUTPUT_FILE="openclaw-cli-reference-v${VERSION}.md"; return 0 ;;
      q|Q) echo "  Cancelled."; exit 0 ;;
      *) echo "  Invalid choice."; exit 1 ;;
    esac
  fi
}

# ── Wizard: mode selection ───────────────────────────────────────────
wizard_ui() {
  if [[ "$NON_INTERACTIVE" == true ]]; then
    return 0
  fi

  echo ""
  echo -e "  This script discovers your OpenClaw CLI commands, flags,"
  echo -e "  and syntax, then writes a reference doc your agent can"
  echo -e "  use to stop guessing and start working."
  echo -e "  ${GREEN}✅${RESET}  No APIs or tokens are used during this process."
  echo ""
  separator
  echo ""
  echo -e "  Choose your training mode:"
  echo ""
  echo -e "  ${BOLD}[1]${RESET} Local Only ${DIM}(Quickest)${RESET}"
  echo -e "      Discovers commands directly from your CLI."
  echo ""
  echo -e "  ${BOLD}[2]${RESET} Local + Enrich ${DIM}(Recommended)${RESET}"
  echo -e "      Runs local discovery first, then searches"
  echo -e "      docs.openclaw.ai for your version using the"
  echo -e "      built-in ${BOLD}openclaw docs${RESET} command."
  echo -e "      Adds doc links for key commands."
  echo ""
  echo -e "  ${BOLD}[q]${RESET} Quit"
  echo ""
  read -rp "  Select [1/2/q]: " mode
  case "$mode" in
    1) ENRICH_MODE=false ;;
    2) ENRICH_MODE=true ;;
    q|Q) echo "  Bye! 🦞"; exit 0 ;;
    *) echo "  Invalid choice."; exit 1 ;;
  esac
}

# ── Parse completion file ────────────────────────────────────────────
# Globals populated by parsing functions (NOT called in subshells)
declare -A CMD_SUBCOMMANDS
declare -A CMD_FLAGS
declare -A CMD_DESCRIPTIONS
GLOBAL_FLAGS=""
PARSE_COUNT=0
DESC_COUNT=0
JSON_COUNT=0

parse_completion_file() {
  local comp_file="$1"

  # Ensure completion file exists; generate if needed
  if [[ ! -f "$comp_file" ]]; then
    warn "Completion file not found at $comp_file"
    progress "Generating..." "openclaw completion --shell bash"
    local generated
    generated=$(openclaw completion --shell bash 2>/dev/null || true)
    if [[ -z "$generated" ]]; then
      fail "Could not generate completion file. Is OpenClaw installed correctly?"
    fi
    mkdir -p "$(dirname "$comp_file")"
    echo "$generated" > "$comp_file"
    success "Generated completion file"
  fi

  local cmd="" opts=""
  PARSE_COUNT=0

  while IFS= read -r line; do
    # Match: command)
    if [[ "$line" =~ ^[[:space:]]+([a-z][-a-z0-9]*)\)$ ]]; then
      cmd="${BASH_REMATCH[1]}"
      continue
    fi
    # Match: opts="..."
    if [[ -n "$cmd" && "$line" =~ opts=\"([^\"]*)\" ]]; then
      opts="${BASH_REMATCH[1]}"

      local subcmds=""
      local flags=""

      for token in $opts; do
        # Strip trailing commas (artifact from short flags like -s,)
        token="${token%,}"
        [[ -z "$token" ]] && continue

        if [[ "$token" == --* || "$token" == -* ]]; then
          flags+="$token "
        else
          subcmds+="$token "
        fi
      done

      CMD_SUBCOMMANDS["$cmd"]="${subcmds% }"
      CMD_FLAGS["$cmd"]="${flags% }"
      PARSE_COUNT=$((PARSE_COUNT + 1))
      cmd=""
    fi
  done < "$comp_file"
}

parse_help_descriptions() {
  local help_output
  help_output=$(openclaw --help 2>&1 || true)

  # Extract command descriptions from the Commands section
  local in_commands=false
  DESC_COUNT=0
  while IFS= read -r line; do
    if [[ "$line" == *"Commands:"* ]]; then
      in_commands=true
      continue
    fi
    if [[ "$line" == *"Examples:"* || "$line" == *"Docs:"* ]]; then
      in_commands=false
      continue
    fi

    if [[ "$in_commands" == true ]]; then
      if [[ "$line" =~ ^[[:space:]]+([a-z][-a-z0-9]+)[[:space:]]+\*?[[:space:]]+(.+)$ ]]; then
        local cmd="${BASH_REMATCH[1]}"
        local desc="${BASH_REMATCH[2]}"
        CMD_DESCRIPTIONS["$cmd"]="$desc"
        DESC_COUNT=$((DESC_COUNT + 1))
      fi
    fi
  done <<< "$help_output"

  # Extract global flags from Options section
  GLOBAL_FLAGS=$(echo "$help_output" | grep -oP '\-\-[a-z][-a-z]+' | sort -u | tr '\n' ' ')
}

check_json_support() {
  JSON_COUNT=0
  for cmd in "${!CMD_FLAGS[@]}"; do
    if [[ "${CMD_FLAGS[$cmd]}" == *"--json"* ]]; then
      JSON_COUNT=$((JSON_COUNT + 1))
    fi
  done
}

# ── Generate markdown ────────────────────────────────────────────────
generate_markdown() {
  local output_path="$1"
  local json_count="$2"

  # Sort commands alphabetically
  local sorted_cmds
  sorted_cmds=$(for cmd in "${!CMD_FLAGS[@]}"; do echo "$cmd"; done | sort)

  # Count stats
  local total_cmds=0
  local total_flags=0
  local has_subcmds=0
  for cmd in $sorted_cmds; do
    total_cmds=$((total_cmds + 1))
    local flag_count
    flag_count=$(echo "${CMD_FLAGS[$cmd]}" | wc -w)
    total_flags=$((total_flags + flag_count))
    if [[ -n "${CMD_SUBCOMMANDS[$cmd]:-}" ]]; then
      has_subcmds=$((has_subcmds + 1))
    fi
  done

  cat > "$output_path" << HEADER
# OpenClaw CLI Reference (v${VERSION})

> Auto-generated by [OpenClaw Boot Camp](https://github.com/openclaw-bootcamp) on $(date -u '+%Y-%m-%d %H:%M UTC')
> Source: CLI completion data + help output | Commands: ${total_cmds} | Flags: ${total_flags} | JSON-capable: ${json_count}

---

## Global Flags

These work on any command:

\`\`\`
${GLOBAL_FLAGS}
\`\`\`

---

## Commands

HEADER

  for cmd in $sorted_cmds; do
    local desc="${CMD_DESCRIPTIONS[$cmd]:-}"
    local subcmds="${CMD_SUBCOMMANDS[$cmd]:-}"
    local flags="${CMD_FLAGS[$cmd]:-}"

    echo "### \`$cmd\`" >> "$output_path"
    if [[ -n "$desc" ]]; then
      echo "$desc" >> "$output_path"
    fi
    echo "" >> "$output_path"

    if [[ -n "$subcmds" ]]; then
      echo "**Subcommands:** \`$(echo "$subcmds" | sed 's/ /`, `/g')\`" >> "$output_path"
      echo "" >> "$output_path"
    fi

    if [[ -n "$flags" ]]; then
      echo "**Flags:** \`$(echo "$flags" | sed 's/ /`, `/g')\`" >> "$output_path"
      echo "" >> "$output_path"
    fi

    echo "---" >> "$output_path"
    echo "" >> "$output_path"
  done

  # Append tips section
  cat >> "$output_path" << 'TIPS'
## Tips & Gotchas

1. **`--help` is broken** on most subcommands — it just prints the parent help. Use this reference instead.
2. **`gateway` has subcommands** (`run`, `status`, `restart`, etc.) but top-level `openclaw status`, `openclaw health`, and `openclaw logs` are the preferred way to check gateway state.
3. **`--json`** works on many commands — use it for machine-readable output.
4. **Agent requires** at least one session selector: `--to`, `--session-id`, or `--agent`.
5. **Message send** needs `--channel`, `--target`, and `--message` for direct delivery.
6. **Config changes** need a `openclaw gateway restart` to take effect.
7. **Sessions list** via `openclaw sessions --json` shows all session keys and IDs.
8. **Logs** stream via `openclaw logs` (JSONL format). Use `--level error` to filter.

## Key Paths

| Path | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main configuration |
| `~/.openclaw/agents/main/sessions/` | Agent session data |
| `~/.openclaw/workspace/` | Agent workspace |
| `~/.openclaw/workspace/skills/` | Installed skills |
| `~/.openclaw/settings/tts.json` | TTS preferences |
| `~/.openclaw/completions/` | Shell completion scripts |
| `/tmp/openclaw/openclaw-*.log` | Gateway log files |

---
*Generated by OpenClaw Boot Camp 🦞🎓*
TIPS

}

# ── Extract flag details from a doc page ─────────────────────────────
fetch_doc_flags() {
  local url="$1"
  # --connect-timeout + --max-time prevent the wizard hanging on a flaky doc server
  curl -sL --connect-timeout 5 --max-time 15 "$url" 2>/dev/null | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
# Replace common HTML entities
text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
text = re.sub(r'<[^>]+>', '\n', text)
lines = [l.strip() for l in text.split('\n') if l.strip()]

# Reject mid-sentence captures (HTML often splits a sentence across tags,
# leaving fragments that begin with punctuation or lowercase continuations).
def looks_like_fragment(s):
    if not s:
        return True
    if s[0] in ',;:)':
        return True
    if not (s[0].isupper() or s[0] == '-' or s[0].isalnum()):
        return True
    return False

# A 'complete' line either ends in terminal punctuation OR contains a real flag token.
FLAG_TOKEN = re.compile(r'--?[a-z][-a-z0-9]+')
def looks_complete(s):
    if s.endswith(('.', '!', '?', ')', ']')):
        return True
    if FLAG_TOKEN.search(s):
        return True
    return False

useful = []
for line in lines:
    # Capture lines that describe flags (start with - or contain --)
    if re.match(r'^-{1,2}[a-z]', line):
        useful.append(line)
    # Capture 'key : description' patterns (flag docs format)
    elif ': ' in line and ('--' in line or line.startswith('-')):
        if not looks_like_fragment(line):
            useful.append(line)
    # Capture requirement/usage notes (full sentences only, not bare labels)
    elif any(w in line.lower() for w in ['must pass', 'at least one', 'required if', 'requires']):
        if 15 < len(line) < 200 and not looks_like_fragment(line) and looks_complete(line):
            useful.append(line)

seen = set()
for u in useful[:30]:
    clean = u[:200].strip()
    if clean and clean not in seen and len(clean) > 5:
        seen.add(clean)
        print(clean)
" 2>/dev/null || true
}

# ── Enrich from docs ────────────────────────────────────────────────
enrich_with_docs() {
  local doc_path="$1"
  echo ""
  separator
  echo ""
  echo -e "  ${BOLD}Phase 2: Enrich from OpenClaw Docs${RESET}"
  echo ""

  if [[ "$NON_INTERACTIVE" != true ]]; then
    read -rp "  Proceed? [Y/n]: " confirm
    if [[ "$confirm" =~ ^[nN] ]]; then
      echo "  Skipping enrichment."
      return 0
    fi
  fi

  # Build doc page list dynamically from every command that has flags
  declare -A DOC_PAGES
  for cmd in "${!CMD_FLAGS[@]}"; do
    if [[ -n "${CMD_FLAGS[$cmd]}" ]]; then
      DOC_PAGES["$cmd"]="https://docs.openclaw.ai/cli/$cmd"
    fi
  done

  local enriched=0
  local total=${#DOC_PAGES[@]}
  local current=0

  # Append enrichment section to the doc
  {
    echo ""
    echo "## Detailed Flag Reference (from docs.openclaw.ai)"
    echo ""
    echo "> Auto-fetched from official documentation. Includes flag descriptions and usage notes."
    echo ""
  } >> "$doc_path"

  # Sort keys for consistent ordering
  local sorted_keys
  sorted_keys=$(for k in "${!DOC_PAGES[@]}"; do echo "$k"; done | sort)

  for cmd in $sorted_keys; do
    local url="${DOC_PAGES[$cmd]}"
    current=$((current + 1))
    local pct=$((current * 100 / total))
    local filled=$((pct / 5))
    local empty=$((20 - filled))
    local bar=$(printf '%0.s█' $(seq 1 $filled 2>/dev/null) 2>/dev/null)$(printf '%0.s░' $(seq 1 $empty 2>/dev/null) 2>/dev/null)
    printf "\r  ${bar} %3d%%  ${DIM}%s${RESET}%-20s" "$pct" "$cmd" "" >&2

    local content
    content=$(fetch_doc_flags "$url")

    if [[ -n "$content" ]]; then
      {
        echo "### \`$cmd\`"
        echo ""
        echo "$content" | while IFS= read -r line; do
          echo "- \`$line\`"
        done
        echo ""
        echo "*Source: [docs.openclaw.ai/cli/$cmd]($url)*"
        echo ""
        echo "---"
        echo ""
      } >> "$doc_path"
      enriched=$((enriched + 1))
    fi
    sleep 1
  done
  printf "\r  ████████████████████ 100%%  ${GREEN}done${RESET}%-20s\n" "" >&2

  if [[ $enriched -gt 0 ]]; then
    success "Enriched $enriched commands with inline flag details"
  else
    warn "Could not fetch docs. The local reference is still comprehensive."
  fi
}

# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

banner
detect_version
check_existing_doc

if [[ "$NON_INTERACTIVE" != true ]]; then
  wizard_ui
fi

echo ""
separator
echo ""
echo -e "  ${BOLD}Phase 1: Local Discovery${RESET}"
echo ""

# Parse completion file (called directly, NOT in subshell — populates global arrays)
progress "Scanning completion file..." ""
parse_completion_file "$COMPLETION_FILE"
success "Parsed $PARSE_COUNT commands from completion data"

# Parse help descriptions (called directly — populates CMD_DESCRIPTIONS)
progress "Extracting command descriptions..." ""
parse_help_descriptions
success "Found descriptions for $DESC_COUNT commands"

# Check JSON support (called directly — sets JSON_COUNT)
progress "Checking JSON output support..." ""
check_json_support
success "$JSON_COUNT commands support --json"

# Generate markdown
progress "Generating reference document..." ""
mkdir -p "$WORKSPACE_NOTES"
output_path="$WORKSPACE_NOTES/$OUTPUT_FILE"
generate_markdown "$output_path" "$JSON_COUNT" > /dev/null

# Count stats for summary
total_cmds=${#CMD_FLAGS[@]}
total_flags=0
has_subcmds=0
for cmd in "${!CMD_FLAGS[@]}"; do
  flag_count=$(echo "${CMD_FLAGS[$cmd]}" | wc -w)
  total_flags=$((total_flags + flag_count)) || true
  if [[ -n "${CMD_SUBCOMMANDS[$cmd]:-}" ]]; then
    has_subcmds=$((has_subcmds + 1))
  fi
done

echo ""
success "Wrote: ${output_path}"
echo -e "     Version: ${BOLD}${VERSION}${RESET} | Commands: ${BOLD}${total_cmds}${RESET} | Flags: ${BOLD}${total_flags}${RESET} | With subcommands: ${BOLD}${has_subcmds}${RESET}"

# Phase 2: Enrich (if selected)
if [[ "$ENRICH_MODE" == true ]]; then
  enrich_with_docs "$output_path"
fi

echo ""
separator
echo ""
echo -e "  Your agent now has a CLI cheat sheet. 🦞🎓"
echo -e "  No more ${DIM}--help${RESET} roulette."
echo ""
echo -e "  ${BOLD}Next step:${RESET} Let your agent know where the reference lives."
echo -e "  Add this to your agent's ${BOLD}AGENTS.md${RESET}, ${BOLD}BOOT.md${RESET}, or workspace notes:"
echo ""
echo -e "  ${DIM}  CLI reference: ~/.openclaw/workspace/notes/${OUTPUT_FILE}${RESET}"
echo ""
