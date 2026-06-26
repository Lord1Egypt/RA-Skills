#!/bin/bash
# Flomo 自动同步设置向导

set -e

echo "======================================"
echo "🎉 Flomo 自动同步设置向导"
echo "======================================"
echo ""

# 进入脚本所在目录
cd "$(dirname "$0")"

# 1. 检查依赖
echo "📦 检查依赖..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python 3: $(python3 --version)"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误：未找到 pip3"
    exit 1
fi
echo "✅ pip3: $(pip3 --version)"

# 2. 安装 Python 依赖
echo ""
echo "📥 安装 Python 依赖..."
pip3 install playwright beautifulsoup4 markdownify -q
echo "✅ Python 依赖安装完成"

# 3. 安装 Playwright 浏览器
echo ""
echo "📥 安装 Playwright 浏览器（可能需要几分钟）..."
playwright install chromium
echo "✅ Playwright 浏览器安装完成"

# 4. 创建 .env 文件
echo ""
echo "======================================"
echo "⚙️  配置账号信息"
echo "======================================"
echo ""

if [ -f .env ]; then
    echo "⚠️  发现已存在的 .env 文件"
    read -p "是否覆盖？(y/N): " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo "跳过配置，使用现有 .env 文件"
    else
        rm .env
    fi
fi

if [ ! -f .env ]; then
    # 询问用户信息
    read -p "请输入 Flomo 邮箱: " FLOMO_EMAIL
    read -sp "请输入 Flomo 密码: " FLOMO_PASSWORD
    echo ""
    read -p "请输入 Obsidian vault 路径 [~/Documents/Obsidian/flomo]: " OBSIDIAN_VAULT
    OBSIDIAN_VAULT=${OBSIDIAN_VAULT:-"~/Documents/Obsidian/flomo"}
    read -p "请输入标签前缀 [flomo/]: " TAG_PREFIX
    TAG_PREFIX=${TAG_PREFIX:-"flomo/"}
    
    # 创建 .env 文件
    cat > .env << EOF
# Flomo 账号配置
FLOMO_EMAIL=$FLOMO_EMAIL
FLOMO_PASSWORD=$FLOMO_PASSWORD
OBSIDIAN_VAULT=$OBSIDIAN_VAULT
TAG_PREFIX=$TAG_PREFIX
EOF
    
    echo ""
    echo "✅ 配置文件已创建: .env"
    
    # 设置文件权限（仅所有者可读写）
    chmod 600 .env
    echo "✅ 已设置文件权限（600）"
fi

# 5. 测试同步
echo ""
echo "======================================"
echo "🧪 测试同步（显示浏览器窗口）"
echo "======================================"
echo ""
read -p "是否立即测试同步？(Y/n): " TEST_SYNC
if [ "$TEST_SYNC" != "n" ] && [ "$TEST_SYNC" != "N" ]; then
    echo ""
    echo "开始测试同步..."
    echo "提示：将显示浏览器窗口，请观察自动化过程"
    echo ""
    
    ./sync.sh --no-headless --verbose
    
    echo ""
    echo "======================================"
    echo "测试完成！"
    echo "======================================"
else
    echo "跳过测试"
fi

# 6. 设置定时任务
echo ""
echo "======================================"
echo "⏰ 设置定时任务"
echo "======================================"
echo ""
echo "是否设置定时任务（每天自动同步）？"
echo ""
echo "选项："
echo "  1) 每天晚上 10:00"
echo "  2) 每天晚上 11:00"
echo "  3) 每天凌晨 2:00"
echo "  4) 每 6 小时一次"
echo "  5) 自定义时间"
echo "  6) 跳过"
echo ""
read -p "请选择 [1-6]: " CRON_CHOICE

CRON_EXPR=""
case $CRON_CHOICE in
    1) CRON_EXPR="0 22 * * *" ;;
    2) CRON_EXPR="0 23 * * *" ;;
    3) CRON_EXPR="0 2 * * *" ;;
    4) CRON_EXPR="0 */6 * * *" ;;
    5)
        echo "请输入 cron 表达式（如：0 22 * * * 表示每天 22:00）"
        read -p "cron 表达式: " CRON_EXPR
        ;;
    *)
        echo "跳过定时任务设置"
        ;;
esac

if [ -n "$CRON_EXPR" ]; then
    SCRIPT_PATH="$(pwd)/sync.sh"
    LOG_PATH="/tmp/flomo_sync.log"
    CRON_LINE="$CRON_EXPR cd $(pwd) && $SCRIPT_PATH >> $LOG_PATH 2>&1"
    
    echo ""
    echo "将添加以下 cron 任务："
    echo "  $CRON_LINE"
    echo ""
    read -p "确认添加？(y/N): " CONFIRM_CRON
    
    if [ "$CONFIRM_CRON" = "y" ] || [ "$CONFIRM_CRON" = "Y" ]; then
        # 添加到 crontab
        (crontab -l 2>/dev/null || echo ""; echo "$CRON_LINE") | crontab -
        echo "✅ 定时任务已添加"
        echo ""
        echo "查看 crontab："
        crontab -l | grep flomo
        echo ""
        echo "查看日志："
        echo "  tail -f $LOG_PATH"
    else
        echo "已取消"
    fi
fi

# 完成
echo ""
echo "======================================"
echo "🎉 设置完成！"
echo "======================================"
echo ""
echo "下一步："
echo "  1. 手动同步: ./sync.sh"
echo "  2. 测试同步: ./sync.sh --no-headless"
echo "  3. 查看帮助: python scripts/auto_sync.py --help"
echo "  4. 查看日志: tail -f auto_sync.log"
echo ""
echo "文档："
echo "  - README.md      - 项目总览"
echo "  - AUTO_SYNC.md   - 自动同步详细文档"
echo "  - SKILL.md       - 完整功能说明"
echo ""
echo "祝使用愉快！"
