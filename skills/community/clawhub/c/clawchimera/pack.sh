#!/usr/bin/env bash
# =============================================================================
# pack.sh — 将 ClawChimera ECS Skill 打包为可上传至 clawhub.ai 的 zip
# 用法: bash pack.sh
# 产物: clawchimera.zip（当前目录）
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZIP_NAME="clawchimera.zip"
TMP_DIR=$(mktemp -d)

echo "→ 准备打包文件..."

# 复制到临时目录
cp "${SCRIPT_DIR}/SKILL.md"   "${TMP_DIR}/"
cp "${SCRIPT_DIR}/skill.json" "${TMP_DIR}/"
cp "${SCRIPT_DIR}/run.sh"     "${TMP_DIR}/"
cp "${SCRIPT_DIR}/analyze.sh" "${TMP_DIR}/"
cp "${SCRIPT_DIR}/README.md"  "${TMP_DIR}/"

# 确保脚本有执行权限
chmod +x "${TMP_DIR}/run.sh"
chmod +x "${TMP_DIR}/analyze.sh"

# 打包
cd "${TMP_DIR}"
zip -r "${SCRIPT_DIR}/${ZIP_NAME}" .
cd "${SCRIPT_DIR}"

# 清理
rm -rf "${TMP_DIR}"

echo "✔ 打包完成: ${SCRIPT_DIR}/${ZIP_NAME}"
echo "  包含文件:"
unzip -l "${ZIP_NAME}" | grep -v "^Archive" | grep -v "^\-\-\-" | grep -v "files$"
echo ""
echo "→ 现在可将 ${ZIP_NAME} 上传到 https://clawhub.ai/upload"
