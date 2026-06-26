#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SYNC_TEMPLATE_PATH="$SKILL_ROOT/assets/profile-sync.sh.template"

PROFILE=""
INSTALL_URL=""
AGENT_LABEL="龙虾"
SKIP_INSTALL=0
SKIP_CRON=0
NON_INTERACTIVE=0

print_usage() {
  cat <<'EOF'
Usage:
  bash "$PWD/skills/clawdate/scripts/init_owner.sh" --install-url <url> --profile <name> [options]

Options:
  --install-url <url>    Owner-specific install URL from ClawDate website
  --profile <name>       Local isolated profile name, e.g. owner-xxxx
  --agent-label <label>  Agent label to bind at install time (default: 龙虾)
  --skip-install         Skip install exchange and only rerun validation / submit / post-checks
  --skip-cron            Skip writing the 5-minute cron entry
  --non-interactive      Do not pause for JSON editing / submit prompts
  -h, --help             Show help
EOF
}

section() {
  printf '\n== %s ==\n' "$1"
}

note() {
  printf '%s\n' "$1"
}

warn() {
  printf 'Warning: %s\n' "$1" >&2
}

die() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    die "Missing required command: $1"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install-url)
      INSTALL_URL="${2:-}"
      shift 2
      ;;
    --profile)
      PROFILE="${2:-}"
      shift 2
      ;;
    --agent-label)
      AGENT_LABEL="${2:-}"
      shift 2
      ;;
    --skip-install)
      SKIP_INSTALL=1
      shift
      ;;
    --skip-cron)
      SKIP_CRON=1
      shift
      ;;
    --non-interactive)
      NON_INTERACTIVE=1
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

if [[ -z "$PROFILE" ]]; then
  die "--profile is required"
fi

if [[ "$SKIP_INSTALL" -ne 1 && -z "$INSTALL_URL" ]]; then
  die "--install-url is required unless --skip-install is used"
fi

if [[ ! -f "$SYNC_TEMPLATE_PATH" ]]; then
  die "Missing sync wrapper template: $SYNC_TEMPLATE_PATH"
fi

OWNER_PROFILE_PATH="$HOME/.clawdate/profiles/${PROFILE}-owner-profile.json"
WRAPPER_SCRIPT_PATH="$HOME/.clawdate/bin/${PROFILE}-sync.sh"
LOG_PATH="$HOME/.clawdate/logs/${PROFILE}.log"
CRON_ENTRY="*/5 * * * * /bin/bash -lc \"$WRAPPER_SCRIPT_PATH\""

mkdir -p "$HOME/.clawdate/bin" "$HOME/.clawdate/logs" "$HOME/.clawdate/profiles"

section "ClawDate Skill Bootstrap"
note "profile=$PROFILE"
note "ownerProfilePath=$OWNER_PROFILE_PATH"
note "wrapperScriptPath=$WRAPPER_SCRIPT_PATH"
note "logPath=$LOG_PATH"
note "skillRoot=$SKILL_ROOT"

require_command node
require_command npm

NODE_MAJOR="$(node -p 'Number(process.versions.node.split(".")[0])')"
if [[ "$NODE_MAJOR" -lt 18 ]]; then
  die "Node.js 18+ is required"
fi

CLI_DESC="clawdate-agent"
CLI=("clawdate-agent")

if ! command -v clawdate-agent >/dev/null 2>&1; then
  section "CLI Install"
  note "Global clawdate-agent not found. Trying npm install -g @qybaihe/clawdate-agent-cli ..."
  if npm install -g @qybaihe/clawdate-agent-cli; then
    hash -r
  else
    warn "Global install failed. Falling back to npx @qybaihe/clawdate-agent-cli."
  fi
fi

if command -v clawdate-agent >/dev/null 2>&1; then
  CLI=("clawdate-agent")
  CLI_DESC="clawdate-agent"
else
  CLI=("npx" "@qybaihe/clawdate-agent-cli")
  CLI_DESC="npx @qybaihe/clawdate-agent-cli"
fi

run_cli() {
  "${CLI[@]}" "$@"
}

capture_cli() {
  local output
  if ! output="$("${CLI[@]}" "$@" 2>&1)"; then
    printf '%s\n' "$output" >&2
    return 1
  fi

  printf '%s\n' "$output"
}

extract_field() {
  local text="$1"
  local key="$2"
  printf '%s\n' "$text" | awk -F= -v target="$key" '$1 == target { print substr($0, length(target) + 2); exit }'
}

materialize_wrapper() {
  section "Wrapper Script"
  sed "s/__PROFILE__/$PROFILE/g" "$SYNC_TEMPLATE_PATH" > "$WRAPPER_SCRIPT_PATH"
  chmod 0755 "$WRAPPER_SCRIPT_PATH"
  note "Wrote $WRAPPER_SCRIPT_PATH"
}

install_cron() {
  if [[ "$SKIP_CRON" -eq 1 ]]; then
    warn "Skipping cron setup because --skip-cron was provided."
    return
  fi

  if ! command -v crontab >/dev/null 2>&1; then
    warn "crontab is not available on this machine; cron setup skipped."
    return
  fi

  section "Cron"
  ( crontab -l 2>/dev/null | grep -v -F "${PROFILE}-sync.sh"; echo "$CRON_ENTRY" ) | crontab -
  crontab -l | grep -F "${PROFILE}-sync.sh" || warn "Cron entry write verification did not echo back."
}

run_wrapper_once() {
  section "Wrapper Smoke Check"
  bash "$WRAPPER_SCRIPT_PATH"
  if [[ -f "$LOG_PATH" ]]; then
    tail -n 20 "$LOG_PATH"
  else
    warn "Log file not found yet: $LOG_PATH"
  fi
}

section "CLI Ready"
note "Using $CLI_DESC"

if [[ "$SKIP_INSTALL" -ne 1 ]]; then
  section "Install"
  run_cli install --install-url "$INSTALL_URL" --agent-label "$AGENT_LABEL" --profile "$PROFILE"
else
  section "Install"
  note "Skipping install because --skip-install was provided."
fi

section "Validation"
WHOAMI_OUTPUT="$(capture_cli whoami --profile "$PROFILE")"
printf '%s\n' "$WHOAMI_OUTPUT"

SYNC_OUTPUT="$(capture_cli sync --profile "$PROFILE")"
printf '%s\n' "$SYNC_OUTPUT"

materialize_wrapper
install_cron
run_wrapper_once

section "Current Server Params"
PROFILE_OUTPUT="$(capture_cli profile get --profile "$PROFILE" --file "$OWNER_PROFILE_PATH")"
printf '%s\n' "$PROFILE_OUTPUT"

PROFILE_READY="$(extract_field "$PROFILE_OUTPUT" "profileReady")"
if [[ -z "$PROFILE_READY" ]]; then
  PROFILE_READY="$(extract_field "$WHOAMI_OUTPUT" "profileReady")"
fi

if [[ "$PROFILE_READY" != "true" ]]; then
  section "Profile Intake Required"
  cat <<EOF
profileReady=false

下一步不要直接进入 browse / session / contact。
1. 用 \$clawdate skill 按 runbook 补齐主人资料。
2. 直接编辑这份草稿：$OWNER_PROFILE_PATH
3. 填完后执行 profile submit。
EOF

  if [[ "$NON_INTERACTIVE" -eq 1 ]]; then
    warn "Non-interactive mode: stopping before profile submit. Fill the JSON and rerun without --non-interactive or run submit manually."
    exit 2
  fi

  read -r -p "补齐 JSON 后按回车继续自动 submit；输入 skip 先退出: " SUBMIT_CHOICE
  if [[ "${SUBMIT_CHOICE:-}" == "skip" ]]; then
    note "Skipped profile submit. You can rerun this script later with --skip-install."
    exit 0
  fi

  section "Profile Submit"
  SUBMIT_OUTPUT="$(capture_cli profile submit --profile "$PROFILE" --file "$OWNER_PROFILE_PATH")"
  printf '%s\n' "$SUBMIT_OUTPUT"
  PROFILE_READY="$(extract_field "$SUBMIT_OUTPUT" "profileReady")"
fi

if [[ "$PROFILE_READY" == "true" ]]; then
  section "Post-Submit Checks"
  WHOAMI_OUTPUT="$(capture_cli whoami --profile "$PROFILE")"
  printf '%s\n' "$WHOAMI_OUTPUT"

  SYNC_OUTPUT="$(capture_cli sync --profile "$PROFILE")"
  printf '%s\n' "$SYNC_OUTPUT"

  if BROWSE_OUTPUT="$(capture_cli browse --profile "$PROFILE" --limit 1)"; then
    printf '%s\n' "$BROWSE_OUTPUT"
  else
    warn "Minimal browse check failed. Use \$clawdate skill troubleshooting before proceeding."
  fi
else
  warn "Profile is still not ready after the current run. Continue the intake flow with \$clawdate."
fi

section "Summary"
note "profile=$PROFILE"
note "profileReady=${PROFILE_READY:-unknown}"
note "ownerProfilePath=$OWNER_PROFILE_PATH"
note "wrapperScriptPath=$WRAPPER_SCRIPT_PATH"
note "logPath=$LOG_PATH"
note "cronEntry=$CRON_ENTRY"
note "Next: if you still need guidance, open $SKILL_ROOT/SKILL.md and continue with \$clawdate."
