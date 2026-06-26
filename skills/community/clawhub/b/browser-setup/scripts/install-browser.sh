#!/usr/bin/env bash
# Install headless Chrome for OpenClaw in environments without root/sudo.
# Downloads Google Chrome .deb, extracts binary + shared libs + fonts to user dirs.
# Usage: bash install-browser.sh [--chrome-dir DIR] [--libs-dir DIR]
set -euo pipefail

CHROME_DIR="${HOME}/chrome-install"
LIBS_DIR="${HOME}/local-libs"
FONTS_DIR="${HOME}/.fonts"
FC_CONF="${HOME}/.config/fontconfig/fonts.conf"
WRAPPER="${LIBS_DIR}/chrome-wrapper.sh"
TMP_DIR="$(mktemp -d)"

trap 'rm -rf "$TMP_DIR"' EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --chrome-dir) CHROME_DIR="$2"; shift 2;;
    --libs-dir)   LIBS_DIR="$2";   shift 2;;
    *) echo "Unknown option: $1"; exit 1;;
  esac
done

echo "==> Downloading Google Chrome..."
wget -q -O "$TMP_DIR/chrome.deb" \
  https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
echo "==> Extracting Chrome binary..."
mkdir -p "$CHROME_DIR"
dpkg-deb -x "$TMP_DIR/chrome.deb" "$CHROME_DIR"

CHROME_BIN="$CHROME_DIR/opt/google/chrome/chrome"
if [[ ! -f "$CHROME_BIN" ]]; then
  echo "ERROR: Chrome binary not found at $CHROME_BIN"
  exit 1
fi

echo "==> Checking missing shared libraries..."
MISSING=$(LD_LIBRARY_PATH="${LIBS_DIR}/lib" ldd "$CHROME_BIN" 2>&1 | grep "not found" | awk '{print $1}' || true)
if [[ -z "$MISSING" ]]; then
  echo "    All libraries satisfied."
else
  echo "==> Downloading required library packages..."
  mkdir -p "$LIBS_DIR/lib"

  # Map .so names to package names (Ubuntu/Debian)
  PKGS=(
    libglib2.0-0t64 libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64
    libcups2t64 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3
    libxrandr2 libgbm1 libasound2t64 libatspi2.0-0t64 libdbus-1-3 libxcb1
    libx11-6 libxext6 libcairo2 libpango-1.0-0 libpangocairo-1.0-0
    libffi8 libpcre2-8-0 libxau6 libxdmcp6 libxi6 libxrender1
    libpng16-16t64 libfontconfig1 libfreetype6 libxcb-render0 libxcb-shm0
    libpixman-1-0 libfribidi0 libthai0 libharfbuzz0b libavahi-common3
    libavahi-client3 libdatrie1 libgraphite2-3
  )

  cd "$TMP_DIR"
  for pkg in "${PKGS[@]}"; do
    apt-get download "$pkg" 2>/dev/null || true
  done

  echo "==> Extracting shared libraries..."
  EXTRACT="$TMP_DIR/extract"
  mkdir -p "$EXTRACT"
  for deb in "$TMP_DIR"/*.deb; do
    [[ "$deb" == *chrome.deb ]] && continue
    dpkg-deb -x "$deb" "$EXTRACT" 2>/dev/null || true
  done
  find "$EXTRACT" -name "*.so*" -exec cp -a {} "$LIBS_DIR/lib/" \;

  # Verify
  STILL_MISSING=$(LD_LIBRARY_PATH="${LIBS_DIR}/lib" ldd "$CHROME_BIN" 2>&1 | grep "not found" || true)
  if [[ -n "$STILL_MISSING" ]]; then
    echo "WARNING: Some libraries still missing:"
    echo "$STILL_MISSING"
    echo "You may need to manually install these packages."
  else
    echo "    All libraries satisfied."
  fi
fi

echo "==> Installing fonts..."
mkdir -p "$FONTS_DIR"
cd "$TMP_DIR"
apt-get download fonts-liberation 2>/dev/null || true
FEXTRACT="$TMP_DIR/fonts_extract"
mkdir -p "$FEXTRACT"
for deb in "$TMP_DIR"/fonts-*.deb; do
  dpkg-deb -x "$deb" "$FEXTRACT" 2>/dev/null || true
done
find "$FEXTRACT" -name "*.ttf" -exec cp {} "$FONTS_DIR/" \;
FONT_COUNT=$(ls "$FONTS_DIR"/*.ttf 2>/dev/null | wc -l)
echo "    Installed $FONT_COUNT font files."

echo "==> Writing fontconfig..."
mkdir -p "$(dirname "$FC_CONF")"
cat > "$FC_CONF" << 'FCEOF'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>~/.fonts</dir>
  <cachedir>~/.cache/fontconfig</cachedir>
  <match target="pattern">
    <test qual="any" name="family"><string>sans-serif</string></test>
    <edit name="family" mode="assign" binding="same"><string>Liberation Sans</string></edit>
  </match>
  <match target="pattern">
    <test qual="any" name="family"><string>serif</string></test>
    <edit name="family" mode="assign" binding="same"><string>Liberation Serif</string></edit>
  </match>
  <match target="pattern">
    <test qual="any" name="family"><string>monospace</string></test>
    <edit name="family" mode="assign" binding="same"><string>Liberation Mono</string></edit>
  </match>
</fontconfig>
FCEOF

echo "==> Creating wrapper script..."
cat > "$WRAPPER" << WEOF
#!/bin/bash
export LD_LIBRARY_PATH=${LIBS_DIR}/lib\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}
export FONTCONFIG_FILE=${FC_CONF}
exec ${CHROME_BIN} "\$@"
WEOF
chmod +x "$WRAPPER"

echo "==> Verifying Chrome..."
VERSION=$("$WRAPPER" --version 2>/dev/null || echo "FAILED")
echo "    $VERSION"

echo ""
echo "=== Installation complete ==="
echo "Chrome binary:  $CHROME_BIN"
echo "Wrapper script: $WRAPPER"
echo "Libraries:      $LIBS_DIR/lib/"
echo "Fonts:          $FONTS_DIR/"
echo ""
echo "Next: configure OpenClaw (see SKILL.md)"
