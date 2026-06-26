#!/usr/bin/env bash
set -euo pipefail

# Install cli-ai-proxy from the public npm registry.
# This script performs exactly one privileged action: `npm install -g cli-ai-proxy`.
# It does NOT clone code from GitHub, does NOT run a build step, and the package
# itself declares no postinstall/preinstall scripts. Optional flag:
#   --configure-openclaw   Also run `cli-ai-proxy configure-openclaw` afterwards.

PACKAGE_NAME="cli-ai-proxy"

echo "=== cli-ai-proxy installer ==="

# ─── Prerequisites ───

command -v node >/dev/null 2>&1 || { echo "ERROR: node not found. Install Node.js first."; exit 1; }
command -v npm  >/dev/null 2>&1 || { echo "ERROR: npm not found. Install Node.js first."; exit 1; }

HAS_GEMINI=false
HAS_CLAUDE=false
command -v gemini >/dev/null 2>&1 && HAS_GEMINI=true
command -v claude >/dev/null 2>&1 && HAS_CLAUDE=true

if [[ "$HAS_GEMINI" == false && "$HAS_CLAUDE" == false ]]; then
  echo "WARNING: Neither gemini nor claude CLI found in PATH."
  echo "  Install at least one before running the proxy:"
  echo "    Gemini CLI:  npm install -g @google/gemini-cli"
  echo "    Claude Code: npm install -g @anthropic-ai/claude-code"
  echo ""
fi

# ─── Install ───

echo "Installing $PACKAGE_NAME from npm..."
if npm install -g "$PACKAGE_NAME"; then
  :
else
  echo ""
  echo "Global install failed. If this is a permissions issue, try one of:"
  echo "  • Use a Node version manager (nvm, fnm, volta) so global installs go to \$HOME"
  echo "  • Re-run with sudo: sudo npm install -g $PACKAGE_NAME"
  exit 1
fi

# ─── Verify ───

if ! command -v cli-ai-proxy >/dev/null 2>&1; then
  echo "ERROR: cli-ai-proxy installed but not on PATH."
  echo "  Check: npm bin -g"
  exit 1
fi

echo ""
echo "=== Installation complete ==="
echo "  Package:   $PACKAGE_NAME"
echo "  Binary:    $(command -v cli-ai-proxy)"
echo "  CLI tools:"
$HAS_GEMINI && echo "    ✓ gemini ($(gemini --version 2>/dev/null | head -1))"
$HAS_CLAUDE && echo "    ✓ claude ($(claude --version 2>/dev/null | head -1))"
$HAS_GEMINI || echo "    ✗ gemini (not installed)"
$HAS_CLAUDE || echo "    ✗ claude (not installed)"
echo ""
echo "Next steps:"
echo "  Start:  cli-ai-proxy start"
echo "  Status: cli-ai-proxy status"

# ─── Optional: Configure OpenClaw ───

if [[ "${1:-}" == "--configure-openclaw" ]]; then
  echo ""
  echo "Configuring OpenClaw..."
  cli-ai-proxy configure-openclaw
fi
