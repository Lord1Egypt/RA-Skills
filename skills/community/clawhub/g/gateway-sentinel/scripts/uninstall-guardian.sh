#!/usr/bin/env bash
# uninstall-guardian.sh — Remove OpenClaw Guardian service
#
# Stops the running service, removes the plist or systemd unit, and cleans
# the lockfile. Logs are intentionally preserved.
#
# Usage: ./uninstall-guardian.sh

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

info()  { echo "  ✅  $*"; }
warn()  { echo "  ⚠️   $*"; }

# ─────────────────────────────────────────────────────────────────────────────
# macOS — remove launchd plist
# ─────────────────────────────────────────────────────────────────────────────

uninstall_macos() {
  local plist_path="$HOME/Library/LaunchAgents/com.openclaw.guardian.plist"

  if [[ -f "$plist_path" ]]; then
    # Stop + disable — try modern bootout first, fall back to legacy unload
    local uid
    uid=$(id -u)
    if launchctl bootout "gui/${uid}/com.openclaw.guardian" 2>/dev/null; then
      info "Service removed (modern launchctl)"
    elif launchctl unload -w "$plist_path" 2>/dev/null; then
      info "Service unloaded"
    else
      warn "Service was not loaded (already stopped or never started)"
    fi
    rm -f "$plist_path"
    info "Plist removed: ${plist_path}"
  else
    warn "Plist not found — service may not have been installed: ${plist_path}"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Linux — remove systemd user unit
# ─────────────────────────────────────────────────────────────────────────────

uninstall_linux() {
  local unit_path="$HOME/.config/systemd/user/openclaw-guardian.service"

  # Stop and disable (ignore errors — service may not be running)
  if systemctl --user is-active --quiet openclaw-guardian.service 2>/dev/null; then
    systemctl --user stop openclaw-guardian.service
    info "Service stopped"
  else
    warn "Service was not running"
  fi

  if systemctl --user is-enabled --quiet openclaw-guardian.service 2>/dev/null; then
    systemctl --user disable openclaw-guardian.service
    info "Service disabled"
  fi

  if [[ -f "$unit_path" ]]; then
    rm -f "$unit_path"
    info "Unit file removed: ${unit_path}"
    systemctl --user daemon-reload
    info "systemd daemon reloaded"
  else
    warn "Unit file not found — service may not have been installed: ${unit_path}"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# COMMON CLEANUP
# ─────────────────────────────────────────────────────────────────────────────

remove_lockfile() {
  local lockfile="/tmp/openclaw-guardian.lock"
  if [[ -f "$lockfile" ]]; then
    rm -f "$lockfile"
    info "Lockfile removed: ${lockfile}"
  else
    warn "Lockfile not present (guardian was not running)"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "🛡️  Uninstalling OpenClaw Guardian..."
echo ""

os="$(uname -s)"
case "$os" in
  Darwin)
    uninstall_macos
    ;;
  Linux)
    uninstall_linux
    ;;
  *)
    warn "Unknown OS '${os}' — skipping service removal; only removing lockfile"
    ;;
esac

remove_lockfile

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  OpenClaw Guardian uninstalled"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ℹ️  Logs were intentionally preserved."
echo "  Log location:  \${GUARDIAN_LOG:-/tmp/openclaw-guardian.log}"
echo "  To remove logs manually:"
echo "    rm /tmp/openclaw-guardian.log /tmp/openclaw-guardian.log.1"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
