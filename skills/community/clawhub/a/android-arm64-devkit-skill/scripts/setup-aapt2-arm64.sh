#!/usr/bin/env bash
# Verify (and install, if needed) a native aarch64 Android resource toolchain.
#
# Usage:
#   ./setup-aapt2-arm64.sh                        # check + report only
#   ./setup-aapt2-arm64.sh --install              # apt-get install what's missing
#   ./setup-aapt2-arm64.sh --write-gradle-property PATH/TO/PROJECT
set -euo pipefail

DEBIAN_BIN_DIR=/usr/lib/android-sdk/build-tools/debian
AAPT2="$DEBIAN_BIN_DIR/aapt2"
PACKAGES=(android-sdk-build-tools android-sdk-platform-tools android-libaapt)

DO_INSTALL=0
PROJECT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --install) DO_INSTALL=1 ;;
    --write-gradle-property) PROJECT="${2:-}"; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

echo "== host =="
echo "  arch: $(uname -m)"
[ "$(uname -m)" = "aarch64" ] || echo "  note: not aarch64, this repo is aimed at ARM64 hosts"

echo
echo "== candidates on PATH / SDK =="
FOUND=0
SEARCH_DIRS=()
for d in "${ANDROID_HOME:-}" "${ANDROID_SDK_ROOT:-}" "$HOME/Android" "$HOME/Library/Android/sdk" /opt /usr/lib/android-sdk; do
  [ -n "$d" ] && [ -d "$d" ] && SEARCH_DIRS+=("$d")
done
while IFS= read -r bin; do
  [ -n "$bin" ] || continue
  FOUND=1
  arch=$(file -b "$bin" | cut -d, -f2 | xargs)
  printf '  %-60s %s\n' "$bin" "$arch"
  if [ "$arch" = "ARM aarch64" ]; then
    printf '    -> runs? '; "$bin" version 2>&1 | head -1 || true
  else
    printf '    -> NOT runnable here (expected on this host)\n'
  fi
done < <( { command -v aapt2 || true; [ ${#SEARCH_DIRS[@]} -gt 0 ] && timeout 20 find "${SEARCH_DIRS[@]}" -maxdepth 6 -name aapt2 -type f 2>/dev/null || true; } | sort -u )
[ "$FOUND" = 1 ] || echo "  (no aapt2 found)"

echo
echo "== Debian aarch64 build-tools =="
if [ -x "$AAPT2" ]; then
  echo "  found: $AAPT2"
  echo "  arch : $(file -b "$AAPT2" | cut -d, -f2 | xargs)"
  printf '  run  : '; "$AAPT2" version 2>&1 | head -1
else
  echo "  missing: $AAPT2"
  if [ "$DO_INSTALL" = 1 ]; then
    echo "  installing: ${PACKAGES[*]}"
    sudo apt-get update -qq && sudo apt-get install -y "${PACKAGES[@]}"
    printf '  run  : '; "$AAPT2" version 2>&1 | head -1
  else
    echo "  run this script with --install to get them"
  fi
fi

echo
echo "== other host-specific binaries =="
for b in aidl aidl-cpp zipalign split-select; do
  [ -e "$DEBIAN_BIN_DIR/$b" ] || continue
  printf '  %-14s %s\n' "$b" "$(file -b "$DEBIAN_BIN_DIR/$b" | cut -d, -f2 | xargs)"
done
echo "  (d8 / apksigner are JVM wrappers: architecture-independent)"

if [ -n "$PROJECT" ]; then
  GP="$PROJECT/gradle.properties"
  [ -f "$GP" ] || { echo "no gradle.properties at $GP" >&2; exit 1; }
  LINE="android.aapt2FromMavenOverride=$AAPT2"
  if grep -q '^android\.aapt2FromMavenOverride=' "$GP"; then
    echo "  gradle.properties already sets aapt2FromMavenOverride (left untouched)"
  else
    printf '\n%s\n' "$LINE" >> "$GP"
    echo "  appended to $GP:"
    echo "    $LINE"
  fi
fi

echo
echo "Next: ./gradlew clean assembleDebug  (clean matters, see docs/troubleshooting.md)"
