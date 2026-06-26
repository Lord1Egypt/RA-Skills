#!/bin/bash
# Post-install bootstrap for AiriLab skill runtime.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -z "${AIRILAB_HOME:-}" ]; then
  export AIRILAB_HOME="$HOME/.openclaw/skills/airilab"
fi

PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python)"
  else
    echo "ERROR: python3/python not found in PATH"
    exit 1
  fi
fi

INSTALL_DEPS=1
CONFIGURE_AUTOSTART=1

for arg in "$@"; do
  case "$arg" in
    --no-deps)
      INSTALL_DEPS=0
      ;;
    --no-autostart)
      CONFIGURE_AUTOSTART=0
      ;;
    *)
      echo "WARN: unknown option: $arg"
      ;;
  esac
done

mkdir -p "$AIRILAB_HOME/config" "$AIRILAB_HOME/scheduler"

echo "AiriLab post-install"
echo "skill_dir: $SKILL_DIR"
echo "airilab_home: $AIRILAB_HOME"
echo "python: $PYTHON_BIN"
echo

if [ "$INSTALL_DEPS" -eq 1 ]; then
  if [ -f "$SKILL_DIR/requirements.txt" ]; then
    echo "[1/4] Installing dependencies..."
    "$PYTHON_BIN" -m pip install -r "$SKILL_DIR/requirements.txt"
  else
    echo "[1/4] Skip dependency install: requirements.txt not found"
  fi
else
  echo "[1/4] Skip dependency install (--no-deps)"
fi

echo "[2/4] Runtime health check..."
"$PYTHON_BIN" "$SKILL_DIR/core/config.py" health || true

setup_systemd_user() {
  local service_dir service_file
  service_dir="$HOME/.config/systemd/user"
  service_file="$service_dir/airilab-worker.service"

  mkdir -p "$service_dir"
  cat > "$service_file" <<EOF
[Unit]
Description=AiriLab Worker
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=AIRILAB_HOME=$AIRILAB_HOME
WorkingDirectory=$SKILL_DIR
ExecStart=$PYTHON_BIN $SKILL_DIR/scheduler/worker.py
Restart=always
RestartSec=5
StandardOutput=append:$AIRILAB_HOME/scheduler/worker.log
StandardError=append:$AIRILAB_HOME/scheduler/worker.log

[Install]
WantedBy=default.target
EOF

  systemctl --user daemon-reload
  systemctl --user enable --now airilab-worker.service
}

setup_cron_reboot() {
  local cron_line existing
  cron_line="@reboot AIRILAB_HOME=\"$AIRILAB_HOME\" \"$SKILL_DIR/scripts/start-worker.sh\" >> \"$AIRILAB_HOME/scheduler/autostart.log\" 2>&1"
  existing="$(crontab -l 2>/dev/null | grep -F "$SKILL_DIR/scripts/start-worker.sh" || true)"
  if [ -z "$existing" ]; then
    (crontab -l 2>/dev/null; echo "$cron_line") | crontab -
  fi
}

if [ "$CONFIGURE_AUTOSTART" -eq 1 ]; then
  echo "[3/4] Configuring autostart..."
  if command -v systemctl >/dev/null 2>&1 && systemctl --user --version >/dev/null 2>&1; then
    if setup_systemd_user; then
      echo "Autostart: systemd user service enabled (airilab-worker.service)"
      START_MODE="systemd"
    else
      echo "WARN: systemd user setup failed, fallback to cron/start-worker."
      START_MODE="fallback"
    fi
  elif command -v crontab >/dev/null 2>&1; then
    if setup_cron_reboot; then
      echo "Autostart: cron @reboot configured"
    else
      echo "WARN: cron autostart setup failed"
    fi
    START_MODE="cron"
  else
    echo "WARN: no systemd/crontab found, autostart not configured"
    START_MODE="none"
  fi
else
  echo "[3/4] Skip autostart setup (--no-autostart)"
  START_MODE="none"
fi

echo "[4/4] Ensuring worker process is running..."
if [ "${START_MODE:-none}" = "systemd" ]; then
  systemctl --user status airilab-worker.service --no-pager || true
else
  "$SKILL_DIR/scripts/start-worker.sh"
fi

echo
echo "Post-install complete."
echo "Next checks:"
echo "  $PYTHON_BIN $SKILL_DIR/core/config.py status"
echo "  $PYTHON_BIN $SKILL_DIR/core/config.py health"
echo "  $SKILL_DIR/scripts/health.sh"

