#!/usr/bin/env bash
# 打包 clawbba-api 并复制到 public/downloads/（发布前在仓库根或本目录执行）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(node -e "import('${ROOT}/scripts/clawbba-openclaw-media-catalog.mjs').then(m=>console.log(m.CLAWBBA_SKILL_VERSION))")"
OUT_ZIP="$(cd "$ROOT/.." && pwd)/clawbba-api-${VERSION}.zip"
PUBLIC_DIR="$(cd "$ROOT/../../public/downloads" && pwd)"

cd "$ROOT"
echo "→ 校验 skill scripts 引用完整性…"
node scripts/verify-skill-script-imports.mjs --entry patch-openclaw-media-delivery.mjs --entry patch-flux-critical.mjs
echo "→ 生成静态 media-capabilities（bundled + 离线兜底）…"
node scripts/write-static-media-capabilities.mjs
echo "→ 生成 OpenClaw release manifest JSON…"
node scripts/write-openclaw-release-manifest-json.mjs
rm -f "$OUT_ZIP"
zip -r "$OUT_ZIP" . \
  -x '*.DS_Store' \
  -x 'clawbba-openclaw.patch.json' \
  -x '*.tgz' \
  -x 'openclaw-*.tgz' \
  -x 'PUBLISH.md' \
  -x 'scripts/test-*.mjs' \
  -x 'scripts/install-clawbba-codex.cmd' \
  -x 'scripts/install-clawbba-codex.sh' \
  -x 'scripts/clawbba-codex-install-lib.py'

cp "$OUT_ZIP" "${PUBLIC_DIR}/clawbba-api-${VERSION}.zip"
unzip -tq "${PUBLIC_DIR}/clawbba-api-${VERSION}.zip" >/dev/null

# 公网 install-clawbba-api.sh 须与 CLAWBBA_SKILL_VERSION 一致
INSTALL_SRC="${ROOT}/scripts/install.sh"
for DEST in "${PUBLIC_DIR}/install-clawbba-api.sh" "${ROOT}/../../dist/downloads/install-clawbba-api.sh"; do
  mkdir -p "$(dirname "$DEST")"
  sed "s/\${CLAWBBA_SKILL_VERSION:-[^}]*}/\${CLAWBBA_SKILL_VERSION:-${VERSION}}/" "$INSTALL_SRC" > "$DEST"
  chmod +x "$DEST"
done
cp "$OUT_ZIP" "${ROOT}/../../dist/downloads/clawbba-api-${VERSION}.zip" 2>/dev/null || true
for WIN_INSTALL in install-clawbba-api.ps1 install-clawbba-api.cmd; do
  if [[ -f "${PUBLIC_DIR}/${WIN_INSTALL}" ]]; then
    cp -f "${PUBLIC_DIR}/${WIN_INSTALL}" "${ROOT}/../../dist/downloads/${WIN_INSTALL}" 2>/dev/null || true
  fi
done

echo "✓ ${PUBLIC_DIR}/clawbba-api-${VERSION}.zip ($(du -h "${PUBLIC_DIR}/clawbba-api-${VERSION}.zip" | cut -f1))"
echo "✓ ${PUBLIC_DIR}/install-clawbba-api.sh (default VERSION=${VERSION})"
echo "✓ ${PUBLIC_DIR}/install-clawbba-api.ps1 + .cmd (Windows)"
echo "→ 发布：将 public/downloads/clawbba-api-${VERSION}.zip 部署到生产 www.clawbba.com 后，用户方可 curl 安装。"
