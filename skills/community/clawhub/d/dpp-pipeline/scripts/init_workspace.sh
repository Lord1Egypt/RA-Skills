#!/usr/bin/env bash
set -euo pipefail

infer_skill_root() {
  local script_dir
  script_dir="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  (cd "$script_dir/.." && pwd)
}

SKILL_ROOT="${DPP_SKILL_ROOT:-$(infer_skill_root)}"
RUNTIME_DIR="${DPP_RUNTIME_DIR:-${SKILL_ROOT}/runtime}"
WORKDIR_INPUT="${1:-${DPP_WORKDIR:-$(pwd)}}"

mkdir -p "${WORKDIR_INPUT}"
WORKDIR="$(cd "${WORKDIR_INPUT}" && pwd)"

mkdir -p \
  "${WORKDIR}/assets" \
  "${WORKDIR}/video" \
  "${WORKDIR}/configs" \
  "${WORKDIR}/output"

if [[ -f "${RUNTIME_DIR}/configs/placement_material.json" ]] && [[ ! -f "${WORKDIR}/configs/placement_material.json" ]]; then
  cp "${RUNTIME_DIR}/configs/placement_material.json" "${WORKDIR}/configs/placement_material.json"
fi

if [[ -f "${RUNTIME_DIR}/env-example.txt" ]] && [[ ! -f "${WORKDIR}/.env.example" ]]; then
  cp "${RUNTIME_DIR}/env-example.txt" "${WORKDIR}/.env.example"
fi

echo "${WORKDIR}"
