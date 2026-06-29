#!/usr/bin/env bash
# 打入 ClawBBA OpenClaw runtime patch 并验证；失败则自动重试一次（供 install / one-shot 调用）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUX_ONLY=0
INSTALL=0
for arg in "$@"; do
  case "$arg" in
    --flux-only) FLUX_ONLY=1 ;;
    --install) INSTALL=1 ;;
  esac
done

if ! command -v node >/dev/null 2>&1; then
  echo "[clawbba-api] error: node is required" >&2
  exit 1
fi

if [[ -f "${SCRIPT_DIR}/../references/openclaw-release-manifest.json" ]]; then
  if ! node "${SCRIPT_DIR}/detect-openclaw-version.mjs" --strict --quiet 2>/dev/null; then
    echo "[clawbba-api] x OpenClaw version mismatch; run install-clawbba-api.sh first" >&2
    echo "[clawbba-api]   diagnose: node ${SCRIPT_DIR}/detect-openclaw-version.mjs" >&2
    exit 1
  fi
fi

apply_patches() {
  node "$SCRIPT_DIR/patch-flux-critical.mjs"
  node "$SCRIPT_DIR/patch-openclaw-media-delivery.mjs"
  node "$SCRIPT_DIR/repair-video-validate-runtime.mjs"
}

run_verify() {
  local extra=()
  if [[ "$INSTALL" -eq 1 ]]; then
    extra=(--install)
  elif [[ "$FLUX_ONLY" -eq 1 ]]; then
    extra=(--flux-only)
  fi
  CLAWBBA_INSTALL_SILENT_HINT=1 node "$SCRIPT_DIR/verify-openclaw-patch.mjs" "${extra[@]}"
}

apply_patches
if run_verify; then
  if [[ "$INSTALL" -eq 1 ]]; then
    node "$SCRIPT_DIR/audit-openclaw-compat.mjs" --strict || exit 1
  fi
  exit 0
fi

echo "[clawbba-api] patch verify failed, retrying..." >&2
apply_patches
if run_verify; then
  if [[ "$INSTALL" -eq 1 ]]; then
    node "$SCRIPT_DIR/audit-openclaw-compat.mjs" --strict || exit 1
  fi
  exit 0
fi

echo "[clawbba-api] x patch not ready. Ensure openclaw is installed: openclaw --version" >&2
exit 1
