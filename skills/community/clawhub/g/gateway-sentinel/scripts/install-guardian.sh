#!/usr/bin/env bash
# install-guardian.sh — Install OpenClaw Guardian as a system service
#
# macOS  → launchd plist at ~/Library/LaunchAgents/com.openclaw.guardian.plist
# Linux  → systemd user unit at ~/.config/systemd/user/openclaw-guardian.service
#
# Usage:
#   ./install-guardian.sh
#   GUARDIAN_LOG=/var/log/openclaw-guardian.log ./install-guardian.sh

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

GUARDIAN_LOG="${GUARDIAN_LOG:-/tmp/openclaw-guardian.log}"
GUARDIAN_WORKSPACE="${GUARDIAN_WORKSPACE:-$HOME/.openclaw/workspace}"

# Resolve the directory this script lives in so we can find guardian.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARDIAN_SCRIPT="${SCRIPT_DIR}/guardian.sh"

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

info()  { echo "  ✅  $*"; }
warn()  { echo "  ⚠️   $*"; }
error() { echo "  ❌  $*" >&2; exit 1; }

# validate_prereqs — check guardian.sh exists and is executable
validate_prereqs() {
  if [[ ! -f "$GUARDIAN_SCRIPT" ]]; then
    error "guardian.sh not found at: ${GUARDIAN_SCRIPT}"
  fi
  if [[ ! -x "$GUARDIAN_SCRIPT" ]]; then
    warn "guardian.sh is not executable — fixing now"
    chmod +x "$GUARDIAN_SCRIPT"
  fi
  if ! command -v openclaw &>/dev/null; then
    warn "openclaw CLI not found in PATH — guardian will fail unless PATH is set in the service config"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# macOS — launchd plist
# ─────────────────────────────────────────────────────────────────────────────

install_macos() {
  local plist_dir="$HOME/Library/LaunchAgents"
  local plist_path="${plist_dir}/com.openclaw.guardian.plist"

  mkdir -p "$plist_dir"

  # Resolve the current user's PATH so launchd finds openclaw
  local user_path
  user_path=$(command -v openclaw 2>/dev/null | xargs dirname || echo "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin")

  # Load optional alert env vars from guardian.env for plist injection
  local env_file="$HOME/.openclaw/guardian.env"
  local _tg_token="" _tg_chat="" _discord_url="" _enable_rollback="" _check_interval="" _max_repair="" _cooldown="" _oc_port=""
  if [[ -f "$env_file" ]]; then
    _tg_token=$(grep -E '^GUARDIAN_TELEGRAM_BOT_TOKEN=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _tg_chat=$(grep -E '^GUARDIAN_TELEGRAM_CHAT_ID=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _discord_url=$(grep -E '^GUARDIAN_DISCORD_WEBHOOK_URL=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _enable_rollback=$(grep -E '^GUARDIAN_ENABLE_ROLLBACK=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _check_interval=$(grep -E '^GUARDIAN_CHECK_INTERVAL=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _max_repair=$(grep -E '^GUARDIAN_MAX_REPAIR=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _cooldown=$(grep -E '^GUARDIAN_COOLDOWN=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
    _oc_port=$(grep -E '^OPENCLAW_PORT=' "$env_file" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)
  fi

  # Build optional env var XML entries for plist
  local extra_env_xml=""
  [[ -n "$_tg_token" ]]        && extra_env_xml+="    <key>GUARDIAN_TELEGRAM_BOT_TOKEN</key><string>${_tg_token}</string>"$'\n'
  [[ -n "$_tg_chat" ]]         && extra_env_xml+="    <key>GUARDIAN_TELEGRAM_CHAT_ID</key><string>${_tg_chat}</string>"$'\n'
  [[ -n "$_discord_url" ]]     && extra_env_xml+="    <key>GUARDIAN_DISCORD_WEBHOOK_URL</key><string>${_discord_url}</string>"$'\n'
  [[ -n "$_enable_rollback" ]] && extra_env_xml+="    <key>GUARDIAN_ENABLE_ROLLBACK</key><string>${_enable_rollback}</string>"$'\n'
  [[ -n "$_check_interval" ]]  && extra_env_xml+="    <key>GUARDIAN_CHECK_INTERVAL</key><string>${_check_interval}</string>"$'\n'
  [[ -n "$_max_repair" ]]      && extra_env_xml+="    <key>GUARDIAN_MAX_REPAIR</key><string>${_max_repair}</string>"$'\n'
  [[ -n "$_cooldown" ]]        && extra_env_xml+="    <key>GUARDIAN_COOLDOWN</key><string>${_cooldown}</string>"$'\n'
  [[ -n "$_oc_port" ]]         && extra_env_xml+="    <key>OPENCLAW_PORT</key><string>${_oc_port}</string>"$'\n'

  cat > "$plist_path" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.openclaw.guardian</string>

  <key>ProgramArguments</key>
  <array>
    <string>${GUARDIAN_SCRIPT}</string>
  </array>

  <!-- Ensure openclaw and common brew paths are available to launchd -->
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>${user_path}:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    <key>HOME</key>
    <string>${HOME}</string>
    <key>GUARDIAN_LOG</key>
    <string>${GUARDIAN_LOG}</string>
    <key>GUARDIAN_WORKSPACE</key>
    <string>${GUARDIAN_WORKSPACE}</string>
${extra_env_xml}  </dict>

  <!-- Start on login and keep running -->
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>

  <!-- Wait 10s before restarting after a crash -->
  <key>ThrottleInterval</key>
  <integer>10</integer>

  <key>StandardOutPath</key>
  <string>${GUARDIAN_LOG}</string>
  <key>StandardErrorPath</key>
  <string>${GUARDIAN_LOG}</string>
</dict>
</plist>
PLIST

  info "Plist written to: ${plist_path}"

  # Use modern bootstrap/bootout on macOS 13+, fall back to load/unload
  local uid
  uid=$(id -u)
  if launchctl bootout "gui/${uid}/com.openclaw.guardian" 2>/dev/null; then
    info "Previous instance removed"
  fi
  if launchctl bootstrap "gui/${uid}" "$plist_path" 2>/dev/null; then
    info "Service bootstrapped (modern launchctl)"
  else
    # Fallback for older macOS
    launchctl load -w "$plist_path" 2>/dev/null || true
    info "Service loaded (legacy launchctl)"
  fi

  info "Service loaded and enabled"
  info "To configure alerts, create ~/.openclaw/guardian.env with your GUARDIAN_TELEGRAM_* or GUARDIAN_DISCORD_* vars."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  OpenClaw Guardian installed (macOS launchd)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Check status:  launchctl list | grep openclaw"
  echo "  View logs:     tail -f ${GUARDIAN_LOG}"
  echo "  Stop:          launchctl unload ${plist_path}"
  echo "  Uninstall:     ./uninstall-guardian.sh"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ─────────────────────────────────────────────────────────────────────────────
# Linux — systemd user unit
# ─────────────────────────────────────────────────────────────────────────────

install_linux() {
  local unit_dir="$HOME/.config/systemd/user"
  local unit_path="${unit_dir}/openclaw-guardian.service"

  mkdir -p "$unit_dir"

  cat > "$unit_path" <<UNIT
[Unit]
Description=OpenClaw Gateway Guardian Watchdog
After=network.target

[Service]
Type=simple
ExecStart=${GUARDIAN_SCRIPT}
Environment="HOME=${HOME}"
Environment="GUARDIAN_LOG=${GUARDIAN_LOG}"
Environment="GUARDIAN_WORKSPACE=${GUARDIAN_WORKSPACE}"
EnvironmentFile=-${HOME}/.openclaw/guardian.env
Restart=always
RestartSec=10
StandardOutput=append:${GUARDIAN_LOG}
StandardError=append:${GUARDIAN_LOG}

[Install]
WantedBy=default.target
UNIT

  info "Unit file written to: ${unit_path}"

  systemctl --user daemon-reload
  systemctl --user enable --now openclaw-guardian.service

  info "Service enabled and started"
  info "To configure alerts, create ~/.openclaw/guardian.env with your GUARDIAN_TELEGRAM_* or GUARDIAN_DISCORD_* vars."
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  OpenClaw Guardian installed (Linux systemd user)"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Check status:  systemctl --user status openclaw-guardian"
  echo "  View logs:     tail -f ${GUARDIAN_LOG}"
  echo "  Stop:          systemctl --user stop openclaw-guardian"
  echo "  Uninstall:     ./uninstall-guardian.sh"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "🛡️  Installing OpenClaw Guardian..."
echo ""

validate_prereqs

os="$(uname -s)"
case "$os" in
  Darwin)
    install_macos
    ;;
  Linux)
    install_linux
    ;;
  *)
    error "Unsupported OS: ${os}. Only macOS (Darwin) and Linux are supported."
    ;;
esac
