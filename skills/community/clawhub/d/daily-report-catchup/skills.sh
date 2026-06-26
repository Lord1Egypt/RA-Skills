#!/bin/bash
#=========================================
# openclaw skills 管理助手 v1.3.0
# 老板友好的技能管理界面
#=========================================

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

show_banner() {
    echo -e "${CYAN}"
    echo "  ╔═══════════════════════════════════════╗"
    echo "  ║   🦞 OpenClaw Skills 管理助手 v1.3.0 ║"
    echo "  ╚═══════════════════════════════════════╝"
    echo -e "${NC}"
}

show_help() {
    echo "用法: skills <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  list              查看已安装的技能"
    echo "  search <关键词>   搜索技能（显示版本）"
    echo "  info <技能名>     查看技能详细信息和版本"
    echo "  install <技能名>  安装技能"
    echo "  update [技能名]   更新技能"
    echo "  uninstall <技能名> 卸载技能"
    echo ""
    echo "示例:"
    echo "  skills list                          # 查看已安装"
    echo "  skills search daily-report            # 搜索技能"
    echo "  skills info daily-report-catchup      # 查看版本信息"
}

case "$1" in
    list)
        echo ""
        echo "📦 已安装的技能"
        echo "=========================================="
        # 过滤警告信息（符号链接解析警告等）
        openclaw skills list 2>/dev/null | grep -v "^🦞" | grep -v "^$" | grep -v "Run 'openclaw" | grep -v "Skipping escaped skill path" | grep -v "reason=symlink-escape" | while read line; do
            if [ -n "$line" ]; then
                echo "  $line"
            fi
        done
        echo ""
        ;;
    search)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请输入搜索关键词${NC}"
            echo "   示例: skills search daily-report"
            exit 1
        fi
        echo ""
        echo "🔍 搜索: $2"
        echo "=========================================="
        # 使用 clawhub inspect 配合 grep 获取版本信息
        RESULT=$(openclaw skills search "$2" 2>&1 | grep -v "^🦞" | grep -v "^$" | grep -v "Run 'openclaw" | grep -v "Options:" | grep -v "Commands:" | grep -v "^-")
        echo "$RESULT" | head -20
        echo ""
        echo "💡 查看版本详情: skills info <技能名>"
        echo ""
        ;;
    info)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请输入技能名${NC}"
            exit 1
        fi
        echo ""
        echo "📋 技能详情: $2"
        echo "=========================================="
        clawhub inspect "$2" 2>&1
        echo ""
        ;;
    install)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请输入要安装的技能名${NC}"
            echo "   示例: skills install daily-report-catchup"
            exit 1
        fi
        echo ""
        echo -e "${GREEN}📥 正在安装: $2${NC}"
        echo "=========================================="
        openclaw skills install "$2" 2>&1
        echo ""
        ;;
    update)
        echo ""
        echo -e "${YELLOW}🔄 正在检查更新...${NC}"
        echo "=========================================="
        if [ -z "$2" ]; then
            openclaw skills update 2>&1 | grep -v "^🦞"
        else
            openclaw skills update "$2" 2>&1 | grep -v "^🦞"
        fi
        echo ""
        ;;
    uninstall)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请输入要卸载的技能名${NC}"
            exit 1
        fi
        echo ""
        echo -e "${RED}🗑️  正在卸载: $2${NC}"
        openclaw skills uninstall "$2" 2>&1 | grep -v "^🦞"
        echo ""
        ;;
    help|--help|-h)
        show_banner
        show_help
        ;;
    *)
        show_banner
        show_help
        ;;
esac
