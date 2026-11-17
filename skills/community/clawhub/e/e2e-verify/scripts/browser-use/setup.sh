#!/usr/bin/env bash
# browser-use setup script
# Creates a dedicated venv, installs browser-use + Playwright Chromium,
# and writes activation helper + config files.
#
# Usage:
#   bash skills/browser-use-web-test/scripts/setup.sh
#
# Works on: macOS, Linux, Windows (git-bash / MSYS2)
# After running, activate with:
#   source ~/.browser-use/activate.sh                  (macOS/Linux)
#   source ~/AppData/Local/browser-use/activate.sh     (Windows/git-bash)

set -euo pipefail

# --- Detect platform and set venv path ---
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    VENV_DIR="$HOME/AppData/Local/browser-use"
    IS_WINDOWS=1
    ;;
  Darwin)
    VENV_DIR="$HOME/.browser-use"
    IS_WINDOWS=0
    ;;
  Linux)
    VENV_DIR="$HOME/.browser-use"
    IS_WINDOWS=0
    ;;
  *)
    VENV_DIR="$HOME/.browser-use"
    IS_WINDOWS=0
    ;;
esac

echo "=== browser-use setup ==="
echo "Platform: $(uname -s)"
echo "Venv directory: $VENV_DIR"
echo ""

# --- Check prerequisites ---
if ! command -v uv &>/dev/null; then
    echo "❌ uv not found. Install with: pip install uv"
    exit 1
fi

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "❌ Python 3.11+ not found."
    exit 1
fi

# --- Create venv ---
if [ -d "$VENV_DIR" ]; then
    echo "ℹ️  $VENV_DIR already exists. Remove it first to recreate."
else
    echo "Creating Python venv..."
    uv venv "$VENV_DIR" --python 3.13 2>/dev/null || uv venv "$VENV_DIR" --python 3.12 2>/dev/null || uv venv "$VENV_DIR" --python 3.11
fi

# --- Activate and install ---
if [ "$IS_WINDOWS" = "1" ]; then
    ACTIVATE="$VENV_DIR/Scripts/activate"
else
    ACTIVATE="$VENV_DIR/bin/activate"
fi

echo "Installing browser-use + playwright..."
# shellcheck disable=SC1090
source "$ACTIVATE"
unset PYTHONPATH  # prevent venv leakage from apps that export a global PYTHONPATH (pyenv wrappers, etc.)

uv pip install "browser-use>=0.13,<0.14" "playwright>=1.60,<1.62" 2>/dev/null || pip install "browser-use>=0.13,<0.14" "playwright>=1.60,<1.62"

echo "Installing Chromium browser binary..."
python -m playwright install chromium

echo ""
echo "✅ Installation complete."

# --- Write activation helper ---
ACTIVATE_SH="$VENV_DIR/activate.sh"
cat > "$ACTIVATE_SH" << 'ACTIVATE_EOF'
#!/usr/bin/env bash
# browser-use activation helper — source to activate the venv with a clean PYTHONPATH.
# Usage:  source <path-to-activate.sh>
# Guard: fail clearly if executed instead of sourced
(return 0 2>/dev/null) || { echo "❌ Source this file: source $(basename "$0")"; exit 1; }

_VENV_DIR=""
if [ -d "$HOME/AppData/Local/browser-use" ]; then
    _VENV_DIR="$HOME/AppData/Local/browser-use"
elif [ -d "$HOME/.browser-use" ]; then
    _VENV_DIR="$HOME/.browser-use"
else
    echo "❌ browser-use venv not found. Run setup.sh first."
    return 1
fi

if [ -f "$_VENV_DIR/Scripts/activate" ]; then
    source "$_VENV_DIR/Scripts/activate"
elif [ -f "$_VENV_DIR/bin/activate" ]; then
    source "$_VENV_DIR/bin/activate"
else
    echo "❌ Could not find activate script in $_VENV_DIR"
    return 1
fi

# Critical: unset PYTHONPATH to prevent leakage from other venvs
unset PYTHONPATH

export BROWSER_USE_VENV="$_VENV_DIR"

# Load LLM API keys from .env files if available
for _envfile in "$HOME/.env" "$(pwd)/.env"; do
    if [ -f "$_envfile" ]; then
        set -a
        . "$_envfile"
        set +a
    fi
done

echo "✅ browser-use venv activated ($_VENV_DIR)"
echo "   Provider auto-detected from env vars (OPENAI_API_KEY, GEMINI_API_KEY, etc.)"
echo "   Override with: BROWSER_USE_LLM_KEY, BROWSER_USE_LLM_BASE_URL, BROWSER_USE_LLM_MODEL"
echo "   Run tests with: python your_test.py"
ACTIVATE_EOF

chmod +x "$ACTIVATE_SH"
echo "Wrote activation helper: $ACTIVATE_SH"

# --- Copy config.py into venv root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/config.py" ]; then
    cp "$SCRIPT_DIR/config.py" "$VENV_DIR/config.py"
    echo "Copied config.py to: $VENV_DIR/config.py"
fi

# --- Copy verify_template.py into venv root for convenience ---
if [ -f "$SCRIPT_DIR/verify_template.py" ]; then
    cp "$SCRIPT_DIR/verify_template.py" "$VENV_DIR/verify_template.py"
    echo "Copied verify_template.py to: $VENV_DIR/verify_template.py"
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "To activate:"
if [ "$IS_WINDOWS" = "1" ]; then
    echo "  source $ACTIVATE_SH"
else
    echo "  source $ACTIVATE_SH"
fi
echo ""
echo "Then run a test:"
echo "  python verify_template.py"
