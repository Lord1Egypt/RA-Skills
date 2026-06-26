#!/bin/bash
# feishu-doc-creator Skill 安装脚本
# 适用于 Mac / Linux / 云端 OpenClaw 实例

set -e

SKILL_NAME="feishu-doc-creator"
SKILLS_DIR="${HOME}/.agents/skills"
DEST="${SKILLS_DIR}/${SKILL_NAME}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🦞 安装 ${SKILL_NAME} skill..."
echo ""

# 1. 确保目标目录存在
mkdir -p "${SKILLS_DIR}"

# 2. 复制 skill 文件（当前目录 → skills 目录）
if [ "${SCRIPT_DIR}" = "${DEST}" ]; then
  echo "✓ 已在 skills 目录中，跳过复制"
else
  cp -r "${SCRIPT_DIR}" "${DEST}"
  echo "✓ 文件已复制到 ${DEST}"
fi

# 3. 安装 Python 依赖
echo ""
echo "安装 Python 依赖..."
if command -v pip3 &>/dev/null; then
  pip3 install -r "${DEST}/scripts/requirements.txt" --quiet
elif command -v pip &>/dev/null; then
  pip install -r "${DEST}/scripts/requirements.txt" --quiet
else
  echo "⚠️  未找到 pip，请手动执行: pip3 install requests"
fi
echo "✓ 依赖安装完成"

# 4. 验证脚本可运行
echo ""
echo "验证脚本..."
python3 "${DEST}/scripts/create-document.py" --help > /dev/null 2>&1 \
  && echo "✓ 脚本验证通过" \
  || echo "⚠️  脚本验证失败，请检查 Python 环境"

echo ""
echo "✅ ${SKILL_NAME} 安装完成！"
echo ""
echo "下一步："
echo "  openclaw gateway --force   # 重启 gateway 使 skill 生效"
echo "  openclaw skills info ${SKILL_NAME}   # 确认 skill 已加载"
