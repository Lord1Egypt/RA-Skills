#!/bin/sh
# camscanner-cli installer — downloads the platform-specific binary to a global PATH location.
# No Node.js or Go required. Only curl/wget needed.
#
# Usage:
#   bash scripts/setup.sh
#   curl -fsSL <CDN>/setup.sh | sh
#
# Environment variables (all optional):
#   CAMSCANNER_CLI_VERSION — version to install (default: read from SKILL.md or "latest")
#   CAMSCANNER_CLI_CDN     — CDN base URL override
#   CAMSCANNER_CLI_DIR     — install directory override (default: ~/.local/bin)

set -eu

CDN_BASE="${CAMSCANNER_CLI_CDN:-https://data.camscanner.com/camscanner-cli/releases}"
BIN_NAME="camscanner-cli"
INSTALL_DIR="${CAMSCANNER_CLI_DIR:-$HOME/.local/bin}"

# ── Helpers ──────────────────────────────────────────────────────────────────

say()  { printf '  %s\n' "$@"; }
err()  { printf '  \342\235\214 %s\n' "$@" >&2; exit 1; }

need_cmd() { command -v "$1" >/dev/null 2>&1; }

download() {
  url="$1"; dest="$2"
  if need_cmd curl; then
    curl -fsSL "$url" -o "$dest"
  elif need_cmd wget; then
    wget -qO "$dest" "$url"
  else
    err "Neither curl nor wget found. Please install one and retry."
  fi
}

detect_os() {
  case "$(uname -s)" in
    Linux*)  echo "linux"  ;;
    Darwin*) echo "darwin" ;;
    MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
    *) err "Unsupported OS: $(uname -s)" ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    x86_64|amd64)  echo "amd64" ;;
    arm64|aarch64) echo "arm64" ;;
    *) err "Unsupported architecture: $(uname -m)" ;;
  esac
}

resolve_version() {
  if [ -n "${CAMSCANNER_CLI_VERSION:-}" ]; then
    echo "$CAMSCANNER_CLI_VERSION"
    return
  fi
  script_dir="$(cd "$(dirname "$0")" 2>/dev/null && pwd || echo ".")"
  for candidate in "$script_dir/../SKILL.md" "$script_dir/../../SKILL.md" "./SKILL.md"; do
    if [ -f "$candidate" ]; then
      ver="$(sed -n 's/^version:[[:space:]]*//p' "$candidate" | head -1 | tr -d ' \r\n\"')"
      if [ -n "$ver" ]; then
        echo "$ver"
        return
      fi
    fi
  done
  err "Cannot determine version. Set CAMSCANNER_CLI_VERSION explicitly."
}

version_ge() {
  printf '%s\n%s\n' "$2" "$1" | sort -t. -k1,1n -k2,2n -k3,3n -C
}

check_existing() {
  if need_cmd "$BIN_NAME"; then
    existing_path="$(command -v "$BIN_NAME")"
    existing_ver="$("$BIN_NAME" --version 2>/dev/null | head -1 || echo "0.0.0")"
    if [ "$existing_ver" = "$1" ]; then
      say "${BIN_NAME} v${1} is already installed at ${existing_path}"
      exit 0
    fi
    if version_ge "$existing_ver" "$1"; then
      say "Installed ${BIN_NAME} v${existing_ver} >= target v${1}, skipping."
      exit 0
    fi
    say "Found existing ${BIN_NAME} v${existing_ver} at ${existing_path}"
    say "Will upgrade to v${1} in ${INSTALL_DIR}/"
  fi
}

# ── Main ─────────────────────────────────────────────────────────────────────

main() {
  os="$(detect_os)"
  arch="$(detect_arch)"
  version="$(resolve_version)"

  check_existing "$version"

  # 产物命名与 Makefile 一致: camscanner-cli-{os}-{arch}
  if [ "$os" = "windows" ]; then
    bin_suffix="${BIN_NAME}-${os}-${arch}.exe"
  else
    bin_suffix="${BIN_NAME}-${os}-${arch}"
  fi

  # CLI subpath — patched at build time for each target
  cli_subpath="clawhub/"

  download_url="${CDN_BASE}/v${version}/${cli_subpath}${bin_suffix}"

  say "Installing ${BIN_NAME} v${version} (${os}/${arch})..."
  say "Target: ${INSTALL_DIR}/${BIN_NAME}"

  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' EXIT INT TERM

  say "Downloading ${bin_suffix}..."
  download "$download_url" "$tmpdir/$bin_suffix"

  # Download and verify checksum
  checksums_url="${CDN_BASE}/v${version}/${cli_subpath}checksums.txt"
  checksums_file="$tmpdir/checksums.txt"
  if download "$checksums_url" "$checksums_file" 2>/dev/null; then
    expected_hash=$(grep "$bin_suffix" "$checksums_file" 2>/dev/null | awk '{print $1}')
    if [ -n "$expected_hash" ]; then
      if need_cmd shasum; then
        actual_hash=$(shasum -a 256 "$tmpdir/$bin_suffix" | awk '{print $1}')
      elif need_cmd sha256sum; then
        actual_hash=$(sha256sum "$tmpdir/$bin_suffix" | awk '{print $1}')
      else
        actual_hash=""
      fi
      if [ -n "$actual_hash" ]; then
        if [ "$actual_hash" != "$expected_hash" ]; then
          err "Checksum mismatch for ${bin_suffix}. Expected: ${expected_hash}, Got: ${actual_hash}"
        fi
        say "[OK] Checksum verified"
      else
        say "[WARN] No sha256sum/shasum available, skipping verification"
      fi
    else
      say "[WARN] No checksum entry found for this binary, skipping verification"
    fi
  else
    say "[WARN] Could not download checksums.txt, skipping verification"
  fi

  mkdir -p "$INSTALL_DIR"

  if [ "$os" = "windows" ]; then
    cp "$tmpdir/$bin_suffix" "$INSTALL_DIR/${BIN_NAME}.exe"
  else
    cp "$tmpdir/$bin_suffix" "$INSTALL_DIR/${BIN_NAME}"
    chmod +x "$INSTALL_DIR/${BIN_NAME}"
  fi

  say "Installed: ${INSTALL_DIR}/${BIN_NAME}"

  # Check if install_dir is in PATH
  case ":$PATH:" in
    *":${INSTALL_DIR}:"*) ;;
    *)
      say ""
      say "${INSTALL_DIR} is not in your PATH."
      say "  Add it with:"
      say "    export PATH=\"${INSTALL_DIR}:\$PATH\""
      ;;
  esac

  say ""
  say "${BIN_NAME} v${version} ready!"
  say "  Run: ${BIN_NAME} --version"
  say "  Login: ${BIN_NAME} auth login"
}

main
