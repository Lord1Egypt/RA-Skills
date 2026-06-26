#!/usr/bin/env bash
# =============================================================================
# setup.sh — Setup for astrill-watchdog
# Version: 2.0.0
#
# Installs the Astrill StealthVPN watchdog as a systemd user service.
# No sudo required.
#
# Usage: bash setup.sh
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCHDOG_SCRIPT="$SCRIPT_DIR/astrill-watchdog.sh"
INSTALL_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/astrill-watchdog"
INSTALL_BIN="$INSTALL_DIR/astrill-watchdog.sh"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/astrill-watchdog"
SYSTEMD_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
UNIT_FILE="$SYSTEMD_DIR/astrill-watchdog.service"
ASTRILL_BIN="/usr/local/Astrill/astrill"

GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RED="\033[0;31m"; RESET="\033[0m"
ok()   { echo -e "${GREEN}✓${RESET}  $*"; }
warn() { echo -e "${YELLOW}⚠${RESET}  $*"; }
fail() { echo -e "${RED}✗${RESET}  $*"; exit 1; }

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  astrill-watchdog 2.0.0 — Setup                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Preflight checks ──────────────────────────────────────────────────────────

echo "── Checking prerequisites…"

[[ -f "$WATCHDOG_SCRIPT" ]] \
    || fail "astrill-watchdog.sh not found in ${SCRIPT_DIR}."
ok "astrill-watchdog.sh found."

[[ -x "$ASTRILL_BIN" ]] \
    || fail "Astrill binary not found: ${ASTRILL_BIN}. Is Astrill installed?"
ok "Astrill binary found."

for tool in ping ip pgrep pkill setsid; do
    command -v "$tool" &>/dev/null || fail "Required tool missing: ${tool}"
done
ok "Required tools present (ping, ip, pgrep, pkill, setsid)."

command -v systemctl &>/dev/null \
    || fail "systemctl not found. Systemd required."

systemctl --user status &>/dev/null 2>&1 \
    || warn "systemd user session may not be fully initialised. Continuing anyway."

# ── Install watchdog script ───────────────────────────────────────────────────

echo ""
echo "── Installing watchdog script…"

mkdir -p "$INSTALL_DIR"
chmod 700 "$INSTALL_DIR"
cp "$WATCHDOG_SCRIPT" "$INSTALL_BIN"
chmod 700 "$INSTALL_BIN"
ok "Installed: ${INSTALL_BIN}"

# ── Log directory ─────────────────────────────────────────────────────────────

mkdir -p "$LOG_DIR"
chmod 700 "$LOG_DIR"
ok "Log directory: ${LOG_DIR}"

# ── Systemd user unit ─────────────────────────────────────────────────────────

echo ""
echo "── Writing systemd user unit…"

mkdir -p "$SYSTEMD_DIR"

cat > "$UNIT_FILE" << EOF
[Unit]
Description=Astrill VPN Watchdog
After=graphical-session.target network-online.target
Wants=graphical-session.target network-online.target

[Service]
Type=simple
ExecStart=${INSTALL_BIN} _loop
ExecStop=${INSTALL_BIN} stop
Restart=on-failure
RestartSec=15
StandardOutput=append:${LOG_DIR}/watchdog.log
StandardError=append:${LOG_DIR}/watchdog.log

[Install]
WantedBy=graphical-session.target
EOF

ok "Unit written: ${UNIT_FILE}"

systemctl --user daemon-reload
ok "systemd daemon reloaded."

systemctl --user enable astrill-watchdog.service
ok "Service enabled (starts on login)."

# ── Start watchdog ────────────────────────────────────────────────────────────

echo ""
echo "── Starting watchdog…"

systemctl --user restart astrill-watchdog.service
sleep 2

if systemctl --user is-active --quiet astrill-watchdog.service; then
    ok "Watchdog running."
else
    warn "Service may not have started cleanly. Check:"
    warn "  journalctl --user -u astrill-watchdog.service -n 20"
fi

# ── Summary ───────────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  Setup complete                                   ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Status:  ${INSTALL_BIN} status"
echo "  Log:     ${LOG_DIR}/watchdog.log"
echo ""
