#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${WORKSPACE:-${HOME}/.openclaw/workspace}"
PIPER_DIR="${WORKSPACE}/piper"
VENV_DIR="${SCRIPT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

PIPER_VERSION="v1.2.0"

declare -A VOICE_URLS=(
  ["pt_BR-jeff-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/jeff/medium/pt_BR-jeff-medium.onnx"
  ["pt_BR-jeff-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/jeff/medium/pt_BR-jeff-medium.onnx.json"
  ["pt_BR-cadu-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/cadu/medium/pt_BR-cadu-medium.onnx"
  ["pt_BR-cadu-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/cadu/medium/pt_BR-cadu-medium.onnx.json"
  ["pt_BR-faber-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx"
  ["pt_BR-faber-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"
  ["pt_BR-miro-high.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/miro/high/pt_BR-miro-high.onnx"
  ["pt_BR-miro-high.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/miro/high/pt_BR-miro-high.onnx.json"
)

info() { printf '%s\n' "$*"; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

download_to() {
  local url="$1"
  local dest="$2"
  if have_cmd curl; then
    curl -fsSL "$url" -o "$dest"
  elif have_cmd wget; then
    wget -q "$url" -O "$dest"
  else
    fail "Neither curl nor wget is installed. Install one of them and rerun."
  fi
}

detect_piper_archive() {
  local arch os file
  arch="$(uname -m)"
  os="$(uname -s)"

  case "$arch" in
    arm64|aarch64) file="piper_arm64.tar.gz" ;;
    x86_64|amd64) file="piper_x86_64.tar.gz" ;;
    *) fail "Unsupported architecture: ${arch}" ;;
  esac

  case "$os" in
    Linux|Darwin) ;;
    *) fail "Unsupported operating system: ${os}" ;;
  esac

  printf 'https://github.com/rhasspy/piper/releases/download/%s/%s\n' "$PIPER_VERSION" "$file"
}

check_os_dependencies() {
  have_cmd "$PYTHON_BIN" || fail "python3 is required but not found."
  have_cmd ffmpeg || fail "ffmpeg is required but not found."
  have_cmd tar || fail "tar is required but not found."
  if ! have_cmd curl && ! have_cmd wget; then
    fail "curl or wget is required but neither is installed."
  fi
}

create_venv() {
  info "[1/5] Creating local virtualenv"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
  "${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel
  "${VENV_DIR}/bin/pip" install -r "${SCRIPT_DIR}/requirements.txt"
  if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    info "ANTHROPIC_API_KEY detected; installing optional Anthropic dependency"
    "${VENV_DIR}/bin/pip" install -r "${SCRIPT_DIR}/requirements-optional.txt"
  fi
}

install_piper() {
  info "[2/5] Installing Piper into ${PIPER_DIR}"
  mkdir -p "$PIPER_DIR"
  if [[ -x "${PIPER_DIR}/piper/piper" ]]; then
    info "Piper already present"
    return 0
  fi

  local archive_url archive_path
  archive_url="$(detect_piper_archive)"
  archive_path="${PIPER_DIR}/piper.tar.gz"
  download_to "$archive_url" "$archive_path"
  tar -xzf "$archive_path" -C "$PIPER_DIR"
  rm -f "$archive_path"
  chmod +x "${PIPER_DIR}/piper/piper"
}

install_voices() {
  info "[3/5] Downloading PT-BR voice models"
  mkdir -p "$PIPER_DIR"
  local name url
  for name in "${!VOICE_URLS[@]}"; do
    url="${VOICE_URLS[$name]}"
    if [[ -f "${PIPER_DIR}/${name}" ]]; then
      info "  - ${name} already present"
    else
      info "  - downloading ${name}"
      download_to "$url" "${PIPER_DIR}/${name}"
    fi
  done
}

write_default_config() {
  info "[4/5] Writing default voice config"
  mkdir -p "$WORKSPACE"
  if [[ ! -f "${WORKSPACE}/.audio_pt_voice_config.json" ]]; then
    cat > "${WORKSPACE}/.audio_pt_voice_config.json" <<'JSON'
{"voice":"jeff"}
JSON
  fi
}

run_health_check() {
  info "[5/5] Running health check"
  "${VENV_DIR}/bin/python" "${SCRIPT_DIR}/health_check.py"
}

main() {
  check_os_dependencies
  create_venv
  install_piper
  install_voices
  write_default_config
  run_health_check
  info "Install complete."
  info "Restart OpenClaw after installation if needed."
}

main "$@"
