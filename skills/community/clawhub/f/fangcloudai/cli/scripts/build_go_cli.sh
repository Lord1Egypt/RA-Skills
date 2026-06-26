#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RELEASE_DIR="${ROOT_DIR}/release"
BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/fangcloud-build.XXXXXX")"
MACOS_SIGN="${MACOS_SIGN:-0}"
MACOS_NOTARIZE="${MACOS_NOTARIZE:-0}"
MACOS_SIGN_IDENTITY="${MACOS_SIGN_IDENTITY:-}"
MACOS_NOTARY_PROFILE="${MACOS_NOTARY_PROFILE:-}"

cleanup() {
  rm -rf "${BUILD_DIR}"
}

trap cleanup EXIT

require_command() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Missing required command: ${cmd}" >&2
    exit 1
  fi
}

require_env() {
  local name="$1"
  local value="$2"
  if [ -z "${value}" ]; then
    echo "Missing required environment variable: ${name}" >&2
    exit 1
  fi
}

mkdir -p "${BUILD_DIR}/darwin" "${BUILD_DIR}/linux" "${BUILD_DIR}/windows"
rm -rf "${RELEASE_DIR}"
mkdir -p "${RELEASE_DIR}"

build_one() {
  local goos="$1"
  local goarch="$2"
  local output_name="$3"

  GOOS="${goos}" GOARCH="${goarch}" CGO_ENABLED=0 \
    go build -o "${BUILD_DIR}/${goos}/${output_name}" ./cmd/fangcloud
}

sign_macos_binary() {
  local binary_path="$1"
  require_command codesign
  require_env "MACOS_SIGN_IDENTITY" "${MACOS_SIGN_IDENTITY}"
  codesign --force --options runtime --timestamp \
    --sign "${MACOS_SIGN_IDENTITY}" \
    "${binary_path}"
}

verify_macos_signature() {
  local binary_path="$1"
  require_command codesign
  codesign --verify --verbose=2 "${binary_path}"
}

verify_macos_gatekeeper() {
  local binary_path="$1"
  require_command spctl
  spctl -a -vv --type exec "${binary_path}"
}

notarize_macos_binary() {
  local binary_path="$1"
  local archive_path="${binary_path}.zip"
  require_command ditto
  require_command xcrun
  require_env "MACOS_NOTARY_PROFILE" "${MACOS_NOTARY_PROFILE}"
  rm -f "${archive_path}"
  ditto -c -k --keepParent "${binary_path}" "${archive_path}"
  xcrun notarytool submit "${archive_path}" \
    --keychain-profile "${MACOS_NOTARY_PROFILE}" \
    --wait
  echo "${archive_path}"
}

process_macos_binary() {
  local binary_path="$1"
  if [ "${MACOS_SIGN}" = "1" ]; then
    sign_macos_binary "${binary_path}"
    verify_macos_signature "${binary_path}"
  fi
  if [ "${MACOS_NOTARIZE}" = "1" ]; then
    if [ "${MACOS_SIGN}" != "1" ]; then
      echo "MACOS_NOTARIZE=1 requires MACOS_SIGN=1" >&2
      exit 1
    fi
    notarize_macos_binary "${binary_path}" >/dev/null
  fi
}

write_release_notes() {
  cat > "${RELEASE_DIR}/README.md" <<'EOF'
# Fangcloud CLI Release

This folder contains prebuilt Go CLI binaries for Fangcloud.

## Files

- `fangcloud-macos-amd64`: macOS Intel
- `fangcloud-macos-arm64`: macOS Apple Silicon
- `fangcloud-macos-amd64.zip`: notarized macOS Intel archive when notarization is enabled
- `fangcloud-macos-arm64.zip`: notarized macOS Apple Silicon archive when notarization is enabled
- `fangcloud-linux-amd64`: Linux x86_64
- `fangcloud-linux-arm64`: Linux ARM64
- `fangcloud-windows-amd64.exe`: Windows x86_64
- `fangcloud-windows-arm64.exe`: Windows ARM64

## Environment Variables

- `FANGCLOUD_USER_TOKEN`
- `FANGCLOUD_ADMIN_TOKEN` when calling admin URLs

## Download By Environment

Use download scripts to save the correct binary into this `release` directory:

```bash
./cli/scripts/download_release_binary.sh
```

Windows PowerShell:

```powershell
.\cli\scripts\download_release_binary.ps1
```

## Run Directly

```bash
chmod +x fangcloud-macos-arm64
./fangcloud-macos-arm64 --help
./fangcloud-macos-arm64 api GET /v2/user/info
```

Windows PowerShell:

```powershell
.\fangcloud-windows-amd64.exe --help
.\fangcloud-windows-amd64.exe api GET /v2/user/info
```
EOF
}

write_checksums() {
  (
    cd "${RELEASE_DIR}"
    shasum -a 256 \
      fangcloud-macos-amd64 \
      fangcloud-macos-arm64 \
      fangcloud-linux-amd64 \
      fangcloud-linux-arm64 \
      fangcloud-windows-amd64.exe \
      fangcloud-windows-arm64.exe > CHECKSUMS.txt
  )
}

copy_release_artifact() {
  local source_path="$1"
  local target_name
  target_name="$(basename "${source_path}")"
  cp "${source_path}" "${RELEASE_DIR}/${target_name}"
}

cd "${ROOT_DIR}"
build_one darwin amd64 fangcloud-macos-amd64
build_one darwin arm64 fangcloud-macos-arm64
build_one linux amd64 fangcloud-linux-amd64
build_one linux arm64 fangcloud-linux-arm64
build_one windows amd64 fangcloud-windows-amd64.exe
build_one windows arm64 fangcloud-windows-arm64.exe

process_macos_binary "${BUILD_DIR}/darwin/fangcloud-macos-amd64"
process_macos_binary "${BUILD_DIR}/darwin/fangcloud-macos-arm64"

write_release_notes
copy_release_artifact "${BUILD_DIR}/darwin/fangcloud-macos-amd64"
copy_release_artifact "${BUILD_DIR}/darwin/fangcloud-macos-arm64"
copy_release_artifact "${BUILD_DIR}/linux/fangcloud-linux-amd64"
copy_release_artifact "${BUILD_DIR}/linux/fangcloud-linux-arm64"
copy_release_artifact "${BUILD_DIR}/windows/fangcloud-windows-amd64.exe"
copy_release_artifact "${BUILD_DIR}/windows/fangcloud-windows-arm64.exe"
if [ "${MACOS_NOTARIZE}" = "1" ]; then
  copy_release_artifact "${BUILD_DIR}/darwin/fangcloud-macos-amd64.zip"
  copy_release_artifact "${BUILD_DIR}/darwin/fangcloud-macos-arm64.zip"
fi
write_checksums

echo "Release artifacts:"
find "${RELEASE_DIR}" -maxdepth 1 -type f | sort
if [ "${MACOS_SIGN}" = "1" ]; then
  echo ""
  echo "macOS signing enabled with identity: ${MACOS_SIGN_IDENTITY}"
fi
if [ "${MACOS_NOTARIZE}" = "1" ]; then
  echo "macOS notarization submitted with profile: ${MACOS_NOTARY_PROFILE}"
fi
