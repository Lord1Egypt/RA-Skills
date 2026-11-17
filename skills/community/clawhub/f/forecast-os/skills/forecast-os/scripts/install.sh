#!/bin/sh
set -e

REPO="precog-markets/forecast-os"
BINARY="forecast"
INSTALL_DIR="${INSTALL_DIR-}"
# Pinned CLI release tag lives next to this script. FORECAST_VERSION wins.
SCRIPT_DIR="$(dirname "$0")"

is_windows() {
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) return 0 ;;
    *) return 1 ;;
  esac
}

get_asset_name() {
  os=$(uname -s)
  arch=$(uname -m)

  case "$os" in
    Darwin)
      case "$arch" in
        x86_64) echo "forecast-macos-x86_64" ;;
        arm64) echo "forecast-macos-arm64" ;;
        *) echo "Unsupported architecture: $arch" >&2; exit 1 ;;
      esac
      ;;
    Linux)
      case "$arch" in
        x86_64) echo "forecast-linux-x86_64" ;;
        aarch64) echo "forecast-linux-aarch64" ;;
        *) echo "Unsupported architecture: $arch" >&2; exit 1 ;;
      esac
      ;;
    MINGW*|MSYS*|CYGWIN*)
      case "$arch" in
        x86_64|amd64) echo "forecast-windows-x86_64.exe" ;;
        *) echo "Unsupported architecture: $arch" >&2; exit 1 ;;
      esac
      ;;
    *) echo "Unsupported OS: $os" >&2; exit 1 ;;
  esac
}

resolve_tag() {
  if [ -n "$FORECAST_VERSION" ]; then
    echo "$FORECAST_VERSION"
    return
  fi

  # Pinned tag from the skill metadata, when the script runs from the skill.
  metadata_file="$SCRIPT_DIR/../forecast-os-metadata.json"
  if [ -f "$metadata_file" ]; then
    # Read the "cli" field from forecast-os-metadata.json. The pin is the tested release.
    tag=$(python3 -c "import json; print(json.load(open('$metadata_file'))['cli'])" 2>/dev/null)
    if [ -n "$tag" ]; then
      echo "$tag"
      return
    fi
  fi

  # /releases/latest 404s when the newest tag is a prerelease. Fall back to the
  # newest published release, prereleases included.
  tag=$(curl -sS "https://api.github.com/repos/${REPO}/releases/latest" | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n 1)
  if [ -z "$tag" ]; then
    tag=$(curl -sS "https://api.github.com/repos/${REPO}/releases?per_page=5" | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -n 1)
  fi
  if [ -z "$tag" ]; then
    echo "Error: could not determine latest release" >&2
    echo "Set FORECAST_VERSION to install a specific tag (for example FORECAST_VERSION=2.0)." >&2
    exit 1
  fi
  echo "$tag"
}

file_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  elif command -v openssl >/dev/null 2>&1; then
    openssl dgst -sha256 "$1" | awk '{print $NF}'
  else
    echo "Error: need sha256sum, shasum, or openssl to verify download" >&2
    exit 1
  fi
}

main() {
  if is_windows; then
    BINARY="forecast.exe"
  fi
  if [ -z "$INSTALL_DIR" ]; then
    INSTALL_DIR=$(pwd)
  fi

  asset_name=$(get_asset_name)
  tag=$(resolve_tag)

  url="https://github.com/${REPO}/releases/download/${tag}/${asset_name}"
  checksums_url="https://github.com/${REPO}/releases/download/${tag}/checksums.txt"

  echo "Installing ${BINARY} ${tag} (${asset_name})..."

  tmpdir=$(mktemp -d)
  trap 'rm -rf "$tmpdir"' EXIT

  curl -sSfL "$url" -o "$tmpdir/$asset_name"
  if ! curl -sSfL "$checksums_url" -o "$tmpdir/checksums.txt"; then
    echo "Error: checksums.txt is required but was not found on release ${tag}" >&2
    exit 1
  fi

  expected_hash=$(grep "$asset_name" "$tmpdir/checksums.txt" | awk '{print $1}')
  if [ -z "$expected_hash" ]; then
    echo "Error: no checksum found for $asset_name" >&2
    exit 1
  fi

  actual_hash=$(file_sha256 "$tmpdir/$asset_name")
  actual_hash=$(echo "$actual_hash" | tr 'A-F' 'a-f')
  expected_hash=$(echo "$expected_hash" | tr 'A-F' 'a-f')

  if [ "$actual_hash" != "$expected_hash" ]; then
    echo "Error: checksum mismatch!" >&2
    echo "  Expected: $expected_hash" >&2
    echo "  Got:      $actual_hash" >&2
    echo "The downloaded file may have been tampered with. Aborting." >&2
    exit 1
  fi

  echo "Checksum verified."
  chmod +x "$tmpdir/$asset_name"

  if [ ! -d "$INSTALL_DIR" ]; then
    mkdir -p "$INSTALL_DIR"
  fi
  if [ -w "$INSTALL_DIR" ]; then
    mv "$tmpdir/$asset_name" "$INSTALL_DIR/$BINARY"
  elif is_windows; then
    echo "Error: cannot write to $INSTALL_DIR" >&2
    exit 1
  else
    sudo mv "$tmpdir/$asset_name" "$INSTALL_DIR/$BINARY"
  fi

  echo "Installed ${BINARY} to ${INSTALL_DIR}/${BINARY}"
  echo "Run 'forecast --help' to get started."
}

main
