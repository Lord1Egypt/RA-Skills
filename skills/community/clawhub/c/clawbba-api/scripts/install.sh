#!/usr/bin/env bash
# ClawBBA clawbba-api 一键安装 + 配置（OpenClaw 机器上运行）
# 公网: curl -fsSL https://www.clawbba.com/downloads/install-clawbba-api.sh | bash
set -euo pipefail

VERSION="${CLAWBBA_SKILL_VERSION:-2.0.31}"
INSTALL_BASE="${CLAWBBA_INSTALL_BASE:-https://www.clawbba.com/downloads}"
ZIP_NAME="clawbba-api-${VERSION}.zip"
ZIP_URL="${CLAWBBA_SKILL_ZIP_URL:-${INSTALL_BASE}/${ZIP_NAME}}"
SKILL_DIR="${OPENCLAW_SKILL_DIR:-${HOME}/.openclaw/skills/clawbba-api}"
KEY="${CLAWBBA_API_KEY:-}"

echo "=========================================="
echo " ClawBBA clawbba-api ${VERSION} install"
echo "=========================================="

if [[ -z "$KEY" ]]; then
  echo "" >&2
  echo "Create a Platform API Key: https://www.clawbba.com/agent/api-keys" >&2
  echo "" >&2
  echo "Then run:" >&2
  echo "  export CLAWBBA_API_KEY='cbb_sk_live_YOUR_KEY'" >&2
  echo "  curl -fsSL ${INSTALL_BASE}/install-clawbba-api.sh | bash" >&2
  exit 1
fi

if [[ "$KEY" != cbb_sk_live_* ]]; then
  echo "error: CLAWBBA_API_KEY must start with cbb_sk_live_" >&2
  exit 1
fi

for bin in node curl unzip openclaw; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "error: missing $bin (install OpenClaw CLI, Node.js, curl, unzip)" >&2
    exit 1
  fi
done

# 与 openclaw-release-manifest.mjs 保持一致（解压前轻量预检用）
OPENCLAW_COMPAT_MIN_VERSION="${OPENCLAW_COMPAT_MIN_VERSION:-2026.5.28}"
OPENCLAW_PINNED_VERSION="${OPENCLAW_PINNED_VERSION:-2026.6.1}"
OPENCLAW_NPM_ALIGN_SPEC="${OPENCLAW_NPM_ALIGN_SPEC:-openclaw@2026.6.1}"

openclaw_version_meets_min() {
  local current="${1:?}"
  local min="${2:-$OPENCLAW_COMPAT_MIN_VERSION}"
  node -e "
const current = process.argv[1];
const min = process.argv[2];
function parse(v) {
  const m = String(v || '').trim().match(/^(\\d+)\\.(\\d+)\\.(\\d+)/);
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
}
function cmp(a, b) {
  for (let i = 0; i < 3; i++) if (a[i] !== b[i]) return a[i] - b[i];
  return 0;
}
const pa = parse(current);
const pb = parse(min);
if (!pa || !pb) process.exit(3);
process.exit(cmp(pa, pb) >= 0 ? 0 : 2);
" "$current" "$min"
}

openclaw_print_unsupported_upgrade_hint() {
  local version="${1:-unknown}"
  cat >&2 <<EOF

==========================================
 OpenClaw version too old for ClawBBA
==========================================

  Current OpenClaw: ${version}
  Minimum required: OpenClaw ${OPENCLAW_COMPAT_MIN_VERSION}+
  Recommended pin:  OpenClaw ${OPENCLAW_PINNED_VERSION} (pairs with clawbba-api ${VERSION})

ClawBBA needs OpenClaw image_generate / video_generate and WebChat delivery patches.
Older OpenClaw builds cannot apply runtime patches correctly.

Steps:

  1. Align OpenClaw
     npm i -g ${OPENCLAW_NPM_ALIGN_SPEC}
     openclaw --version

  2. Re-install ClawBBA
     export CLAWBBA_API_KEY='cbb_sk_live_YOUR_KEY'
     curl -fsSL ${INSTALL_BASE}/install-clawbba-api.sh | bash

  3. Restart Gateway
     openclaw gateway restart

Docs: https://docs.openclaw.ai

EOF
}

# ── Phase 1: 轻量版本探测（解压 skill 前）────────────────────────────
OPENCLAW_VERSION_PREVIEW="$(openclaw --version 2>/dev/null | sed -n 's/.*OpenClaw \([0-9]\{4\}\.[0-9]\+\.[0-9]\+\).*/\1/p' | head -n1 || true)"
if [[ -z "$OPENCLAW_VERSION_PREVIEW" ]]; then
  echo "error: cannot parse OpenClaw version; run openclaw --version" >&2
  exit 1
fi
echo "-> OpenClaw precheck: ${OPENCLAW_VERSION_PREVIEW}"
if ! openclaw_version_meets_min "$OPENCLAW_VERSION_PREVIEW"; then
  openclaw_print_unsupported_upgrade_hint "$OPENCLAW_VERSION_PREVIEW"
  exit 1
fi

STAGE="$(mktemp -d)"
cleanup() { rm -rf "$STAGE"; }
trap cleanup EXIT

echo "-> Download ${ZIP_URL} ..."
curl -fsSL "$ZIP_URL" -o "${STAGE}/${ZIP_NAME}"

if [[ ! -s "${STAGE}/${ZIP_NAME}" ]]; then
  echo "error: empty download: ${ZIP_URL}" >&2
  exit 1
fi
if ! unzip -tq "${STAGE}/${ZIP_NAME}" >/dev/null 2>&1; then
  echo "error: ${ZIP_NAME} is not a valid zip (site may not have published this version yet)" >&2
  echo "  URL: ${ZIP_URL}" >&2
  exit 1
fi

echo "-> Extract ..."
unzip -qo "${STAGE}/${ZIP_NAME}" -d "$STAGE/extract"
if [[ ! -f "${STAGE}/extract/SKILL.md" ]]; then
  echo "error: invalid zip layout (SKILL.md must be at zip root)" >&2
  exit 1
fi
EXTRACT_ROOT="${STAGE}/extract"
MANIFEST_JSON="${EXTRACT_ROOT}/references/openclaw-release-manifest.json"
if [[ ! -f "$MANIFEST_JSON" ]] && [[ -f "${EXTRACT_ROOT}/scripts/write-openclaw-release-manifest-json.mjs" ]]; then
  echo "-> Generate release manifest (legacy zip) ..."
  (cd "$EXTRACT_ROOT" && node scripts/write-openclaw-release-manifest-json.mjs) || true
fi
if [[ ! -f "$MANIFEST_JSON" ]]; then
  echo "" >&2
  echo "error: missing references/openclaw-release-manifest.json" >&2
  echo "  re-download: ${ZIP_URL}" >&2
  exit 1
fi

# ── Phase 2: release manifest 版本对齐 ───────────────────────────────
echo "-> Align OpenClaw version (clawbba-api ${VERSION}) ..."
echo "  detected:          ${OPENCLAW_VERSION_PREVIEW}"
export CLAWBBA_SKILL_EXTRACT_ROOT="$EXTRACT_ROOT"
node "${EXTRACT_ROOT}/scripts/openclaw-align-version.mjs" "$EXTRACT_ROOT"
OPENCLAW_VERSION_PREVIEW="$(openclaw --version 2>/dev/null | sed -n 's/.*OpenClaw \([0-9]\{4\}\.[0-9]\+\.[0-9]\+\).*/\1/p' | head -n1 || true)"
echo "  after align:       ${OPENCLAW_VERSION_PREVIEW:-unknown}"

# ── Phase 3: compat profile ───────────────────────────────────────────
echo "-> Detect compat profile ..."
# shellcheck disable=SC1091
source "${STAGE}/extract/scripts/openclaw-detect-version.sh"
if ! openclaw_detect_version_from_skill "${STAGE}/extract" 1; then
  exit 1
fi
echo "  OpenClaw version:  ${OPENCLAW_VERSION}"
echo "  install profile:   ${OPENCLAW_COMPAT_PROFILE_ID}"
echo "  profile label:     ${OPENCLAW_COMPAT_PROFILE_LABEL}"
echo "  tools bundle:      ${OPENCLAW_COMPAT_TOOLS_BUNDLE}"
if [[ "${OPENCLAW_COMPAT_SUPPORTS_SYSTEM_PROMPT_OVERRIDE}" == "1" ]]; then
  echo "  config strategy:   write agents.defaults.systemPromptOverride"
else
  echo "  config strategy:   skip systemPromptOverride (skill always:true)"
fi
if [[ "${OPENCLAW_COMPAT_NEWER_THAN_TESTED:-0}" == "1" ]]; then
  echo "  warn: OpenClaw newer than tested; recommend: npm i -g ${OPENCLAW_NPM_ALIGN_SPEC}"
fi
if [[ -f "$MANIFEST_JSON" ]]; then
  MANIFEST_PAIR="$(node -e "import fs from 'fs';const m=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));console.log(m.versionPairLabel||'')" "$MANIFEST_JSON")"
  if [[ -n "$MANIFEST_PAIR" ]]; then
    echo "  version pair:      ${MANIFEST_PAIR}"
  fi
fi
node "${STAGE}/extract/scripts/detect-openclaw-version.mjs"

echo "-> Install to ${SKILL_DIR} ..."
mkdir -p "$(dirname "$SKILL_DIR")"
rm -rf "$SKILL_DIR"
mkdir -p "$SKILL_DIR"
cp -a "${STAGE}/extract/." "$SKILL_DIR/"
if [[ ! -f "${SKILL_DIR}/references/media-capabilities.json" ]]; then
  echo "error: zip missing references/media-capabilities.json (need clawbba-api 2.0.0+)" >&2
  exit 1
fi

export CLAWBBA_API_BASE="${CLAWBBA_API_BASE:-https://www.clawbba.com/api/v1}"
export CLAWBBA_API_KEY="$KEY"
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-$CLAWBBA_API_KEY}"
export OPENCLAW_VERSION
export OPENCLAW_COMPAT_PROFILE_ID
export OPENCLAW_COMPAT_PROFILE_TIER
export OPENCLAW_COMPAT_TOOLS_BUNDLE
export OPENCLAW_COMPAT_SUPPORTS_SYSTEM_PROMPT_OVERRIDE
export OPENCLAW_COMPAT_VIDEO_EXECUTE_ARGS
export OPENCLAW_COMPAT_NEWER_THAN_TESTED

echo "-> Verify API key ..."
"$SKILL_DIR/scripts/verify-key.sh"

echo "-> Write OpenClaw config (profile=${OPENCLAW_COMPAT_PROFILE_ID}) ..."
"$SKILL_DIR/scripts/one-shot-setup.sh"

echo "-> Apply ClawBBA runtime patches (profile=${OPENCLAW_COMPAT_PROFILE_ID}) ..."
bash "$SKILL_DIR/scripts/ensure-openclaw-patches.sh" --install

echo "-> Verify provider config ..."
node "$SKILL_DIR/scripts/verify-openclaw-runtime.mjs" || true

if [[ "${SKIP_GATEWAY_RESTART:-}" != "1" ]]; then
  echo "-> Restart Gateway ..."
  if ! openclaw gateway restart; then
    echo "[clawbba-api] x Gateway restart failed; run openclaw config validate" >&2
    exit 1
  fi
fi

node "$SKILL_DIR/scripts/write-clawbba-compat-lock.mjs" "$SKILL_DIR"

echo ""
echo "ok install complete (OpenClaw ${OPENCLAW_VERSION} profile ${OPENCLAW_COMPAT_PROFILE_ID})"
echo "  skill: ${SKILL_DIR}"
echo "  models: openclaw models list | grep clawbba"
echo "  verify: new chat -> /model status (should show clawbba/...)"
echo "  diagnose: node ${SKILL_DIR}/scripts/detect-openclaw-version.mjs"
echo "  diagnose: node ${SKILL_DIR}/scripts/verify-openclaw-patch.mjs"
echo "  diagnose: node ${SKILL_DIR}/scripts/verify-openclaw-runtime.mjs"
echo ""
echo "Image gen: use openrouter/<model-id> in image_generate (NOT clawbba/ prefix)."
echo "Restart gateway after config changes: openclaw gateway restart"
