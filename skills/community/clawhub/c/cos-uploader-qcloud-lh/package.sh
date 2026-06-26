#!/bin/bash
# ============================================================
# Skill 打包脚本
# 功能：将 Skill 打包为标准的 .tar.gz 包，可直接部署
# 用法：./package.sh
# ============================================================

set -euo pipefail

SKILL_NAME="cos-photo-uploader"
VERSION=$(grep '^version:' SKILL.md | head -1 | awk '{print $2}' 2>/dev/null || echo "1.0.0")
PACKAGE_NAME="${SKILL_NAME}-v${VERSION}.tar.gz"

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${SKILL_DIR}"

echo "=============================================="
echo "  打包 Skill: ${SKILL_NAME} v${VERSION}"
echo "=============================================="
echo ""

# 需要打包的文件/目录列表
FILES=(
    "SKILL.md"
    "README.md"
    "run.sh"
    "install.sh"
    "scripts/skill_handler.py"
    "scripts/cos_uploader.py"
    "scripts/config.py"
    "scripts/setup_config.py"
    "scripts/requirements.txt"
    "screenshots/.gitkeep"
)

# 检查文件完整性
echo "[1/2] 检查文件完整性..."
missing=0
for file in "${FILES[@]}"; do
    if [ -f "${file}" ]; then
        echo "  ✅ ${file}"
    else
        echo "  ❌ 缺少: ${file}"
        missing=$((missing + 1))
    fi
done

if [ ${missing} -gt 0 ]; then
    echo ""
    echo "❌ 有 ${missing} 个文件缺失，无法打包"
    exit 1
fi

# 打包
echo ""
echo "[2/2] 创建压缩包..."
tar czf "${PACKAGE_NAME}" "${FILES[@]}"

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "  ✅ 打包成功！"
    echo "=============================================="
    echo ""
    echo "  📦 文件名: ${PACKAGE_NAME}"
    echo "  📏 大小: $(du -h ${PACKAGE_NAME} | cut -f1)"
    echo ""
    echo "  📋 部署步骤："
    echo "  1. 上传到目标服务器："
    echo "     scp ${PACKAGE_NAME} root@<服务器IP>:/opt/openclaw/skills/"
    echo ""
    echo "  2. 在服务器上解压："
    echo "     cd /opt/openclaw/skills/"
    echo "     mkdir -p ${SKILL_NAME} && tar xzf ${PACKAGE_NAME} -C ${SKILL_NAME}"
    echo ""
    echo "  3. 执行安装："
    echo "     cd ${SKILL_NAME} && ./install.sh"
    echo ""
    echo "  4. 配置 COS 信息（桶名 + 密钥）："
    echo "     ./venv/bin/python3 scripts/setup_config.py"
    echo ""
else
    echo "❌ 打包失败"
    exit 1
fi
