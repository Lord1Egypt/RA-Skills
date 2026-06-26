#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
RELEASE_MANIFEST="${SKILL_DIR}/vendor/caduceusmail-release.json"
INSTALL_ROOT="${XDG_DATA_HOME:-${HOME}/.local/share}/caduceusmail-skill/toolchains"

log() {
  echo "[☤ caduceusmail-skill] $*" >&2
}

ensure_private_dir() {
  mkdir -p "$1"
  chmod 700 "$1" 2>/dev/null || true
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log "missing required command: $1"
    exit 1
  fi
}

read_manifest() {
  mapfile -t RELEASE_FIELDS < <(python3 - "${RELEASE_MANIFEST}" <<'PY'
import json
import pathlib
import sys

manifest = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for key in ("name", "version", "filename", "integrity", "shasum", "repository", "commit"):
    print(manifest[key])
PY
)

  if [[ "${#RELEASE_FIELDS[@]}" -ne 7 ]]; then
    log "release manifest is malformed: ${RELEASE_MANIFEST}"
    exit 1
  fi

  PACKAGE_NAME="${RELEASE_FIELDS[0]}"
  PACKAGE_VERSION="${RELEASE_FIELDS[1]}"
  PACKAGE_FILENAME="${RELEASE_FIELDS[2]}"
  PACKAGE_INTEGRITY="${RELEASE_FIELDS[3]}"
  PACKAGE_SHASUM="${RELEASE_FIELDS[4]}"
  PACKAGE_REPOSITORY="${RELEASE_FIELDS[5]}"
  PACKAGE_COMMIT="${RELEASE_FIELDS[6]}"
  PACKAGE_TARBALL="${SKILL_DIR}/vendor/${PACKAGE_FILENAME}"
  INSTALL_DIR="${INSTALL_ROOT}/${PACKAGE_NAME}-${PACKAGE_VERSION}"
  ENTRYPOINT="${INSTALL_DIR}/package/dist/cli.js"
}

verify_vendored_release() {
  python3 - "${PACKAGE_TARBALL}" "${PACKAGE_INTEGRITY}" "${PACKAGE_SHASUM}" <<'PY'
import base64
import hashlib
import pathlib
import sys

tarball = pathlib.Path(sys.argv[1])
expected_integrity = sys.argv[2]
expected_shasum = sys.argv[3]

payload = tarball.read_bytes()
sha1 = hashlib.sha1(payload).hexdigest()
sha512 = base64.b64encode(hashlib.sha512(payload).digest()).decode("ascii")

if sha1 != expected_shasum:
    raise SystemExit(f"vendored release sha1 mismatch: {sha1} != {expected_shasum}")
if f"sha512-{sha512}" != expected_integrity:
    raise SystemExit("vendored release integrity mismatch")
PY
}

installed_release_is_valid() {
  [[ -f "${ENTRYPOINT}" ]] || return 1

  python3 - "${INSTALL_DIR}" "${PACKAGE_NAME}" "${PACKAGE_VERSION}" "${PACKAGE_INTEGRITY}" <<'PY' >/dev/null
import json
import pathlib
import sys

install_dir = pathlib.Path(sys.argv[1])
expected_name = sys.argv[2]
expected_version = sys.argv[3]
expected_integrity = sys.argv[4]

package_json = install_dir / "package" / "package.json"
release_json = install_dir / ".release.json"
if not package_json.exists() or not release_json.exists():
    raise SystemExit(1)

package_meta = json.loads(package_json.read_text(encoding="utf-8"))
release_meta = json.loads(release_json.read_text(encoding="utf-8"))

if package_meta.get("name") != expected_name or package_meta.get("version") != expected_version:
    raise SystemExit(1)
if release_meta.get("integrity") != expected_integrity:
    raise SystemExit(1)
PY
}

install_vendored_release() {
  local temp_root
  local temp_install
  temp_root="$(mktemp -d "${TMPDIR:-/tmp}/caduceusmail-skill.XXXXXX")"
  temp_install="${temp_root}/install"
  trap 'rm -rf "${temp_root}"' RETURN

  python3 - "${PACKAGE_TARBALL}" "${temp_install}" "${PACKAGE_NAME}" "${PACKAGE_VERSION}" "${RELEASE_MANIFEST}" <<'PY'
import json
import os
import pathlib
import shutil
import stat
import sys
import tarfile

tarball = pathlib.Path(sys.argv[1]).resolve()
dest = pathlib.Path(sys.argv[2]).resolve()
expected_name = sys.argv[3]
expected_version = sys.argv[4]
manifest_path = pathlib.Path(sys.argv[5]).resolve()

dest.mkdir(parents=True, exist_ok=True)

with tarfile.open(tarball, "r:gz") as tf:
    for member in tf.getmembers():
        target = (dest / member.name).resolve()
        if target != dest and dest not in target.parents:
            raise SystemExit(f"unsafe tar entry: {member.name}")
    extract_kwargs = {}
    if "filter" in tarfile.TarFile.extractall.__code__.co_varnames:
        extract_kwargs["filter"] = "data"
    tf.extractall(dest, **extract_kwargs)

package_root = dest / "package"
package_json = package_root / "package.json"
if not package_json.exists():
    raise SystemExit("vendored release is missing package/package.json")

package_meta = json.loads(package_json.read_text(encoding="utf-8"))
if package_meta.get("name") != expected_name or package_meta.get("version") != expected_version:
    raise SystemExit("vendored release metadata does not match pinned manifest")

release_json = json.loads(manifest_path.read_text(encoding="utf-8"))
(dest / ".release.json").write_text(json.dumps(release_json, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

for current in [dest, *dest.rglob("*")]:
    if current.is_symlink():
        continue
    current_mode = stat.S_IMODE(current.stat().st_mode)
    if current.is_dir():
        os.chmod(current, 0o700)
    else:
        os.chmod(current, (current_mode & 0o700) or 0o600)
PY

  if [[ -e "${INSTALL_DIR}" ]]; then
    rm -rf "${INSTALL_DIR}"
  fi

  mv "${temp_install}" "${INSTALL_DIR}"
  ensure_private_dir "${INSTALL_DIR}"
  rm -rf "${temp_root}"
  trap - RETURN
}

main() {
  require_cmd node
  require_cmd python3
  read_manifest
  ensure_private_dir "${INSTALL_ROOT}"
  verify_vendored_release

  if installed_release_is_valid; then
    log "audited release ready: ${PACKAGE_NAME}@${PACKAGE_VERSION}"
  else
    log "extracting audited ${PACKAGE_NAME}@${PACKAGE_VERSION} from vendored artifact"
    log "source: ${PACKAGE_REPOSITORY} @ ${PACKAGE_COMMIT}"
    install_vendored_release
  fi

  printf '%s\n' "${ENTRYPOINT}"
}

main "$@"
