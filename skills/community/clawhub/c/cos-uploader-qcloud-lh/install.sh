#!/bin/bash
# ============================================================
# OpenClaw Skill 安装脚本
# 功能：自动安装 Python 依赖、创建虚拟环境、设置权限
# 用法：./install.sh
# ============================================================

set -euo pipefail

echo "=============================================="
echo "  COS Photo Uploader - Skill 安装脚本"
echo "=============================================="
echo ""

# 获取脚本所在目录
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${SKILL_DIR}"

# ==================== 检查 Python3 ====================
echo "[1/5] 检查 Python3 环境..."
if ! command -v python3 &>/dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.6+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "  ✅ Python ${PYTHON_VERSION}"

# ==================== 创建虚拟环境 ====================
echo ""
echo "[2/5] 创建 Python 虚拟环境..."
if [ ! -d "${SKILL_DIR}/venv" ]; then
    python3 -m venv "${SKILL_DIR}/venv"
    echo "  ✅ 虚拟环境已创建: ${SKILL_DIR}/venv"
else
    echo "  ⏭️  虚拟环境已存在，跳过创建"
fi

# 激活虚拟环境
source "${SKILL_DIR}/venv/bin/activate"

# ==================== 安装 Python 依赖 ====================
echo ""
echo "[3/5] 安装 Python 依赖..."
pip install --upgrade pip -q
pip install -r "${SKILL_DIR}/scripts/requirements.txt" -q
echo "  ✅ 依赖安装完成"

# 验证关键依赖
python3 -c "from qcloud_cos import CosConfig, CosS3Client; print('  ✅ cos-python-sdk-v5 验证通过')"
python3 -c "from cryptography.fernet import Fernet; print('  ✅ cryptography 验证通过')"

# ==================== 设置文件权限 ====================
echo ""
echo "[4/5] 设置文件权限..."
chmod +x "${SKILL_DIR}/run.sh"
chmod +x "${SKILL_DIR}/install.sh"
chmod 644 "${SKILL_DIR}/scripts/skill_handler.py"
chmod 644 "${SKILL_DIR}/scripts/cos_uploader.py"
chmod 644 "${SKILL_DIR}/scripts/config.py"
chmod 644 "${SKILL_DIR}/scripts/setup_config.py"
echo "  ✅ 权限设置完成"

# ==================== 创建必要目录 ====================
echo ""
echo "[5/5] 创建运行时目录..."
mkdir -p "${SKILL_DIR}/scripts/conf"
mkdir -p "${SKILL_DIR}/scripts/logs"
chmod 700 "${SKILL_DIR}/scripts/conf"
echo "  ✅ 目录创建完成"

# ==================== 安装完成 ====================
echo ""
echo "=============================================="
echo "  ✅ Skill 安装完成！"
echo "=============================================="
echo ""
echo "📋 后续步骤："
echo ""
echo "  1. 配置 COS 信息（桶名 + 密钥，首次必须执行）："
echo "     ${SKILL_DIR}/venv/bin/python3 ${SKILL_DIR}/scripts/setup_config.py"
echo ""
echo "  2. 在 OpenClaw 中注册 Skill："
echo "     入口脚本: ${SKILL_DIR}/run.sh"
echo "     触发条件: 图片消息"
echo ""
echo "  3. 测试上传（可选）："
echo "     ${SKILL_DIR}/run.sh --file /path/to/test.jpg"
echo ""

# 反激活虚拟环境
deactivate 2>/dev/null || true
