#!/bin/bash
# Flomo 自动同步到 Obsidian（安全模式 - 不保存密码）
# 首次使用需要手动登录，之后自动使用浏览器保存的登录状态

# 进入脚本所在目录
cd "$(dirname "$0")"

# 默认配置
OUTPUT_DIR="${FLOMO_OUTPUT_DIR:-/Users/ryanbzhou/mynote/flomo}"
TAG_PREFIX="${FLOMO_TAG_PREFIX:-flomo/}"
DOWNLOAD_DIR="${FLOMO_DOWNLOAD_DIR:-flomo_downloads}"
USER_DATA_DIR="${FLOMO_USER_DATA_DIR:-flomo_browser_data}"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}Flomo 自动同步（安全模式）${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${YELLOW}📌 安全特性：${NC}"
echo -e "  ✅ 不保存密码到配置文件"
echo -e "  ✅ 使用浏览器保存的登录状态"
echo -e "  ✅ 首次使用需要手动登录一次"
echo -e "  ✅ 后续自动同步"
echo ""
echo -e "${YELLOW}📂 配置：${NC}"
echo -e "  输出目录: ${OUTPUT_DIR}"
echo -e "  标签前缀: ${TAG_PREFIX}"
echo -e "  浏览器数据: ${USER_DATA_DIR}"
echo ""

# 检查是否首次使用
if [ ! -f ".flomo_sync_state.json" ]; then
    echo -e "${YELLOW}🔐 首次使用提示：${NC}"
    echo -e "  • 脚本将打开浏览器窗口"
    echo -e "  • 请在浏览器中手动登录 flomo"
    echo -e "  • 登录后，浏览器会记住你的登录状态"
    echo -e "  • 下次运行时将自动同步，无需再次登录"
    echo ""
    echo -e "${GREEN}按 Enter 键继续...${NC}"
    read
fi

# 始终显示浏览器（方便用户看到同步进度）
# 如果未登录，会自动提示用户登录
echo -e "${GREEN}🚀 开始同步...${NC}"
echo ""

python3 scripts/auto_sync_safe.py \
    --output "$OUTPUT_DIR" \
    --download-dir "$DOWNLOAD_DIR" \
    --user-data-dir "$USER_DATA_DIR" \
    --tag-prefix "$TAG_PREFIX" \
    --no-headless \
    "$@"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 同步完成！${NC}"
    echo ""
    echo -e "${YELLOW}💡 提示：${NC}"
    echo -e "  • 笔记已保存到: ${OUTPUT_DIR}"
    echo -e "  • 在 Obsidian 中打开即可查看"
    echo -e "  • 再次运行此脚本即可增量同步新笔记"
    echo ""
else
    echo ""
    echo -e "${RED}❌ 同步失败${NC}"
    echo -e "查看日志: auto_sync.log"
    echo ""
    exit 1
fi
