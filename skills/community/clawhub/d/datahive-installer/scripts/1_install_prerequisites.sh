#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM="${PLATFORM:-$($SCRIPT_DIR/0_detect_platform.sh)}"

PROFILE_DIR="$HOME/.chrome-datahive"
EXTENSION_ID="bonfdkhbkkdoipfojcnimjagphdnfedb"

install_websocat() {
  if command -v websocat >/dev/null 2>&1; then
    echo "==> websocat already installed"
    return
  fi

  if ! command -v brew >/dev/null 2>&1; then
    echo "Error: Homebrew is required to install websocat" >&2
    exit 1
  fi

  echo "==> Installing websocat..."
  brew install websocat
  echo "==> websocat installed successfully"
}

setup_profile() {
  echo "==> Creating 'datahive' Chrome profile..."
  mkdir -p "$PROFILE_DIR/datahive"
  cat > "$PROFILE_DIR/datahive/Preferences" << 'EOF'
{
  "profile": {
    "name": "datahive"
  }
}
EOF
}

install_ubuntu() {
  echo "==> [ubuntu] Installing Google Chrome + runtime deps..."
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends wget gnupg2 xvfb
  wget -qO- https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
  echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | \
    sudo tee /etc/apt/sources.list.d/google-chrome.list > /dev/null
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends google-chrome-stable
  sudo rm -rf /var/lib/apt/lists/*

  echo "==> [ubuntu] Force-installing DataHive extension via Chrome policy..."
  sudo mkdir -p /etc/opt/chrome/policies/managed
  sudo tee /etc/opt/chrome/policies/managed/extensions.json > /dev/null << EOF
{
  "ExtensionInstallForcelist": [
    "${EXTENSION_ID};https://clients2.google.com/service/update2/crx"
  ]
}
EOF

  echo "==> [ubuntu] Chrome installed/configured successfully"
}

install_macos() {
  echo "==> [macos] Installing Google Chrome (if missing)..."
  if [[ ! -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
    if ! command -v brew >/dev/null 2>&1; then
      echo "Error: Homebrew is required to install Google Chrome on macOS" >&2
      exit 1
    fi
    brew install --cask google-chrome
  else
    echo "==> [macos] Google Chrome already installed"
  fi

  echo "==> [macos] Removing quarantine attribute from Google Chrome (if present)..."
  xattr -dr com.apple.quarantine "/Applications/Google Chrome.app" 2>/dev/null || true

  echo "==> [macos] Applying managed extension policy (requires sudo)..."
  POLICY_DIR="/Library/Managed Preferences"
  POLICY_FILE="$POLICY_DIR/com.google.Chrome.plist"
  POLICY_VALUE="${EXTENSION_ID};https://clients2.google.com/service/update2/crx"

  sudo mkdir -p "$POLICY_DIR"
  sudo /usr/libexec/PlistBuddy -c "Delete :ExtensionInstallForcelist" "$POLICY_FILE" 2>/dev/null || true
  sudo /usr/libexec/PlistBuddy -c "Add :ExtensionInstallForcelist array" "$POLICY_FILE"
  sudo /usr/libexec/PlistBuddy -c "Add :ExtensionInstallForcelist:0 string $POLICY_VALUE" "$POLICY_FILE"
  sudo plutil -lint "$POLICY_FILE" >/dev/null

  echo "==> [macos] Chrome installed/configured successfully"
}

case "$PLATFORM" in
  ubuntu)
    install_ubuntu
    ;;
  macos)
    install_macos
    ;;
  *)
    echo "Unsupported platform: $PLATFORM. Supported platforms: ubuntu, macos" >&2
    exit 1
    ;;
esac

setup_profile
install_websocat
