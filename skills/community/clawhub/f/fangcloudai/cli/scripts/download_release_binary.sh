#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
ROOT_DIR="$(cd "$(dirname "${SCRIPT_PATH}")/.." && pwd)"
RELEASE_DIR="${ROOT_DIR}/release"
BIN_DIR="${ROOT_DIR}/bin"
BASE_URL="${BASE_URL:-https://app.fangcloud.com/sync/vv25/knowclaw/release}"

mkdir -p "${RELEASE_DIR}"
mkdir -p "${BIN_DIR}"

if [ "$#" -ge 1 ] && [ -n "$1" ]; then
  file="$1"
else
  os="$(uname -s)"
  arch="$(uname -m)"
  case "${os}" in
    Darwin)
      # On Apple Silicon running a Rosetta x86_64 shell, prefer arm64 binary.
      if [ "${arch}" = "arm64" ]; then
        file="fangcloud-macos-arm64"
      elif [ "${arch}" = "x86_64" ] && [ "$(sysctl -in hw.optional.arm64 2>/dev/null || echo 0)" = "1" ]; then
        file="fangcloud-macos-arm64"
      else
        file="fangcloud-macos-amd64"
      fi
      ;;
    Linux)
      if [ "${arch}" = "aarch64" ]; then
        file="fangcloud-linux-arm64"
      else
        file="fangcloud-linux-amd64"
      fi
      ;;
    *)
      echo "Unsupported OS for this script: ${os}" >&2
      echo "Use PowerShell script on Windows: cli/scripts/download_release_binary.ps1" >&2
      exit 1
      ;;
  esac
fi

target="${RELEASE_DIR}/${file}"
bin_target="${BIN_DIR}/${file}"
url="${BASE_URL}/${file}"

validate_binary() {
  local bin_path="$1"
  local os
  os="$(uname -s)"
  if [ "${os}" = "Darwin" ]; then
    # Avoid executing invalid Mach-O files that may be killed by the kernel.
    codesign --verify --verbose=2 "${bin_path}" >/dev/null 2>&1
  else
    "${bin_path}" --help >/dev/null 2>&1
  fi
}

extract_binary_from_zip() {
  local zip_path="$1"
  local expected_name="$2"
  local extract_dir="$3"
  unzip -q "${zip_path}" -d "${extract_dir}"
  find "${extract_dir}" -type f -name "${expected_name}" | head -n 1
}

case "$(uname -s)" in
  Darwin|Linux)
    zip_name="${file}.zip"
    zip_url="${BASE_URL}/${zip_name}"
    tmp_zip="${RELEASE_DIR}/${zip_name}.tmp.$$"
    tmp_extract_dir="$(mktemp -d "${TMPDIR:-/tmp}/fangcloud-extract.XXXXXX")"
    trap 'rm -f "${tmp_zip}"; rm -rf "${tmp_extract_dir}"' EXIT

    echo "Downloading ${zip_url}"
    curl -fL "${zip_url}" -o "${tmp_zip}"
    extracted_bin="$(extract_binary_from_zip "${tmp_zip}" "${file}" "${tmp_extract_dir}")"
    if [ -z "${extracted_bin}" ] || [ ! -f "${extracted_bin}" ]; then
      echo "Downloaded zip does not contain expected binary: ${file}" >&2
      exit 1
    fi
    chmod +x "${extracted_bin}"
    if ! validate_binary "${extracted_bin}"; then
      echo "Downloaded binary is invalid and cannot run: ${zip_url}" >&2
      echo "Please update the release artifact at the source URL." >&2
      exit 1
    fi
    mv -f "${tmp_zip}" "${RELEASE_DIR}/${zip_name}"
    cp "${extracted_bin}" "${bin_target}"
    chmod +x "${bin_target}"
    trap - EXIT
    rm -rf "${tmp_extract_dir}"
    echo "Saved zip to ${RELEASE_DIR}/${zip_name}"
    echo "Saved binary to ${bin_target}"
    ;;
  *)
    tmp_target="${target}.tmp.$$"
    trap 'rm -f "${tmp_target}"' EXIT
    echo "Downloading ${url}"
    curl -fL "${url}" -o "${tmp_target}"
    chmod +x "${tmp_target}"

    if ! validate_binary "${tmp_target}"; then
      echo "Downloaded binary is invalid and cannot run: ${url}" >&2
      echo "Please update the release artifact at the source URL." >&2
      exit 1
    fi

    mv -f "${tmp_target}" "${target}"
    trap - EXIT
    echo "Saved to ${target}"
    ;;
esac
