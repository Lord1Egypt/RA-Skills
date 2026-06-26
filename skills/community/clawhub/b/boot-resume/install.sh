#!/usr/bin/env bash
# boot-resume installer
# Deploys the detection script and systemd drop-in.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Auto-detect OpenClaw workspace
if [[ -n "${OPENCLAW_STATE_DIR:-}" ]]; then
  OPENCLAW_HOME="$OPENCLAW_STATE_DIR"
elif [[ -d "$HOME/.openclaw" ]]; then
  OPENCLAW_HOME="$HOME/.openclaw"
elif [[ -d "$HOME/.openclaw-dev" ]]; then
  OPENCLAW_HOME="$HOME/.openclaw-dev"
else
  echo "✗ Could not find OpenClaw state directory."
  echo "  Set OPENCLAW_STATE_DIR or ensure ~/.openclaw exists."
  exit 1
fi

WORKSPACE="$OPENCLAW_HOME/workspace"
SCRIPTS_DIR="$WORKSPACE/scripts"
SCRIPT_TARGET="$SCRIPTS_DIR/boot-resume-check.sh"

echo "⚡ boot-resume installer"
echo "  workspace: $WORKSPACE"
echo ""

if [[ ! -d "$WORKSPACE" ]]; then
  echo "✗ Workspace not found at $WORKSPACE"
  exit 1
fi

# 1. Deploy detection script
mkdir -p "$SCRIPTS_DIR"
if [[ -f "$SCRIPT_TARGET" ]]; then
  echo "  boot-resume-check.sh already exists."
  read -rp "  Overwrite? [y/N] " answer
  if [[ "${answer,,}" != "y" ]]; then
    echo "  Skipped script deployment."
  else
    cp "$SKILL_DIR/scripts/boot-resume-check.sh" "$SCRIPT_TARGET"
    chmod +x "$SCRIPT_TARGET"
    echo "✓ Updated boot-resume-check.sh"
  fi
else
  cp "$SKILL_DIR/scripts/boot-resume-check.sh" "$SCRIPT_TARGET"
  chmod +x "$SCRIPT_TARGET"
  echo "✓ Deployed boot-resume-check.sh → $SCRIPTS_DIR/"
fi

# 2. Deploy systemd drop-in (Linux only)
if [[ "$(uname)" == "Linux" ]]; then
  SYSTEMD_DROPIN_DIR="$HOME/.config/systemd/user/openclaw-gateway.service.d"
  DROPIN_TARGET="$SYSTEMD_DROPIN_DIR/boot-resume.conf"
  mkdir -p "$SYSTEMD_DROPIN_DIR"

  if [[ -f "$DROPIN_TARGET" ]]; then
    echo "  boot-resume.conf already exists."
    read -rp "  Overwrite? [y/N] " answer
    if [[ "${answer,,}" != "y" ]]; then
      echo "  Skipped drop-in deployment."
    else
      cp "$SKILL_DIR/templates/boot-resume.conf" "$DROPIN_TARGET"
      echo "✓ Updated systemd drop-in"
    fi
  else
    cp "$SKILL_DIR/templates/boot-resume.conf" "$DROPIN_TARGET"
    echo "✓ Deployed systemd drop-in → $SYSTEMD_DROPIN_DIR/"
  fi

  # 2b. Deploy sleep/wake service (triggers on system resume from suspend/hibernate)
  WAKE_SERVICE_DIR="$HOME/.config/systemd/user"
  WAKE_SERVICE_TARGET="$WAKE_SERVICE_DIR/boot-resume-wake.service"

  if [[ -f "$WAKE_SERVICE_TARGET" ]]; then
    echo "  boot-resume-wake.service already exists."
    read -rp "  Overwrite? [y/N] " answer
    if [[ "${answer,,}" != "y" ]]; then
      echo "  Skipped wake service deployment."
    else
      cp "$SKILL_DIR/templates/boot-resume-wake.service" "$WAKE_SERVICE_TARGET"
      echo "✓ Updated wake service"
    fi
  else
    cp "$SKILL_DIR/templates/boot-resume-wake.service" "$WAKE_SERVICE_TARGET"
    echo "✓ Deployed wake service → $WAKE_SERVICE_DIR/"
  fi

  # Reload systemd and enable wake service
  systemctl --user daemon-reload 2>/dev/null && echo "✓ Reloaded systemd" || echo "⚠ systemctl daemon-reload failed"
  systemctl --user enable boot-resume-wake.service 2>/dev/null && echo "✓ Enabled wake service" || echo "⚠ Could not enable wake service"

elif [[ "$(uname)" == "Darwin" ]]; then
  echo ""
  echo "⚠ macOS detected. Systemd is not available."
  echo "  To run the script on gateway start, add this to your launchd plist"
  echo "  or use a wrapper script that calls:"
  echo ""
  echo "    $SCRIPT_TARGET >> /tmp/openclaw/boot-resume.log 2>&1 &"
  echo ""
fi

# 3. Ensure log directory
mkdir -p /tmp/openclaw

echo ""
echo "✅ Done."
echo ""
echo "Verify:"
echo "  systemctl --user restart openclaw-gateway"
echo "  sleep 20 && cat /tmp/openclaw/boot-resume.log"
echo ""
echo "Test:"
echo "  1. Send your agent a task that takes time"
echo "  2. Wait for it to start processing"
echo "  3. systemctl --user restart openclaw-gateway"
echo "  4. tail -f /tmp/openclaw/boot-resume.log"
