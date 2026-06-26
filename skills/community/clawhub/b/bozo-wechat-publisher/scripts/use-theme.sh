#!/bin/bash
###############################################################################
# bozo-wechat-publisher 主题切换脚本
# 用途：快速切换和预览可用主题
###############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 技能目录
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEMES_DIR="$SKILL_DIR/themes"
CONFIG_FILE="$THEMES_DIR/theme-config.json"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# 列出所有可用主题
list_themes() {
    print_header "可用主题列表"

    # 内置主题
    echo -e "${CYAN}📦 wenyan-cli 内置主题${NC}"
    echo "─────────────────────────────────────────────────────────"
    echo "   主题ID           名称                描述"
    echo "─────────────────────────────────────────────────────────"

    local builtin_themes=(
        "default:默认主题:A clean, classic layout ideal for long-form reading."
        "orangeheart:橙心:A vibrant and elegant theme in warm orange tones."
        "rainbow:彩虹:A colorful, lively theme with a clean layout."
        "lapis:青金石:A minimal and refreshing theme in cool blue tones."
        "pie:派派风格:Inspired by sspai.com — modern, sharp, and stylish."
        "maize:玉米色:A crisp, light theme with a soft maize palette."
        "purple:紫色:Clean and minimalist, with a subtle purple accent."
        "phycat:物理猫:A mint-green theme with clear structure and hierarchy."
    )

    for theme in "${builtin_themes[@]}"; do
        IFS=':' read -r id name desc <<< "$theme"
        printf "   ${GREEN}%-14s${NC} ${YELLOW}%-16s${NC} %s\n" "$id" "$name" "$desc"
    done

    echo ""
    echo -e "${CYAN}🎨 自定义卡片式主题${NC}"
    echo "─────────────────────────────────────────────────────────"
    echo "   主题ID              名称                    描述"
    echo "─────────────────────────────────────────────────────────"

    local custom_themes=(
        "card-tech-dark:卡片科技暗色:深色科技感卡片布局，适合技术文章"
        "card-neon-light:卡片霓虹浅色:浅色霓虹风格，清新现代"
    )

    for theme in "${custom_themes[@]}"; do
        IFS=':' read -r id name desc <<< "$theme"
        printf "   ${GREEN}%-18s${NC} ${YELLOW}%-20s${NC} %s\n" "$id" "$name" "$desc"
    done

    echo ""
}

# 显示主题详情
show_theme_info() {
    local theme_id="$1"

    print_header "主题详情: $theme_id"

    case "$theme_id" in
        card-tech-dark)
            cat << 'EOF'
🎨 卡片科技暗色主题

   样式：深色科技感卡片式布局
   适用：技术文章、AI 内容、开发教程

   特色功能：
   • 深色背景 (#0a0e27) 减少眼疲劳
   • 渐变强调色 (#6366f1 → #8b5cf6)
   • 卡片悬停动效
   • 响应式设计

   使用方法：
   1. 在 Markdown 中使用卡片语法
   2. 发布时指定主题

   示例：
   ##::card
   ### 标题
   内容...
   ##::end
EOF
            ;;
        card-neon-light)
            cat << 'EOF'
🎨 卡片霓虹浅色主题

   样式：浅色霓虹风格卡片布局
   适用：教程、指南、操作手册

   特色功能：
   • 浅色背景 (#f8fafc) 清新现代
   • 霓虹效果和渐变边框
   • 流畅的悬停动画
   • 移动端优化

   使用方法：
   1. 在 Markdown 中使用卡片语法
   2. 发布时指定主题

   示例：
   ##::card
   ### 标题
   内容...
   ##::end
EOF
            ;;
        *)
            print_error "未找到主题: $theme_id"
            echo ""
            echo "运行 '$0 list' 查看所有可用主题"
            ;;
    esac
}

# 应用主题到文章
apply_theme() {
    local markdown_file="$1"
    local theme_id="$2"

    if [[ ! -f "$markdown_file" ]]; then
        print_error "文件不存在: $markdown_file"
        exit 1
    fi

    print_info "正在应用主题: $theme_id"
    print_info "文章文件: $markdown_file"

    # 检查是否为内置主题
    case "$theme_id" in
        default|orangeheart|rainbow|lapis|pie|maize|purple|phycat)
            print_success "使用 wenyan-cli 内置主题"
            echo ""
            echo "发布命令："
            echo "  wenyan publish -f $markdown_file -t $theme_id"
            ;;
        card-tech-dark|card-neon-light)
            print_warning "自定义主题需要 HTML 注入"
            echo ""
            echo "使用步骤："
            echo "1. 先用 wenyan-cli 生成 HTML:"
            echo "   wenyan build -f $markdown_file -t default"
            echo ""
            echo "2. 然后注入自定义主题样式"
            echo ""
            echo "或者直接使用预处理的 HTML 模板"
            ;;
        *)
            print_error "未知主题: $theme_id"
            exit 1
            ;;
    esac
}

# 显示使用帮助
show_help() {
    cat << 'EOF'
bozo-wechat-publisher 主题切换工具

用法:
    use-theme.sh [命令] [选项]

命令:
    list                    列出所有可用主题
    info <theme_id>         显示主题详细信息
    apply <file> <theme>    应用主题到文章
    help                    显示此帮助信息

示例:
    use-theme.sh list
    use-theme.sh info card-tech-dark
    use-theme.sh apply article.md lapis

主题分类:
    内置主题: default, orangeheart, rainbow, lapis, pie, maize, purple, phycat
    自定义主题: card-tech-dark, card-neon-light

更多信息请查看:
    /Volumes/AI/AIGC/aigc/Skills/bozo-wechat-publisher/SKILL.md
EOF
}

# 主函数
main() {
    local command="${1:-help}"

    case "$command" in
        list)
            list_themes
            ;;
        info)
            if [[ -z "$2" ]]; then
                print_error "请指定主题 ID"
                echo "用法: $0 info <theme_id>"
                exit 1
            fi
            show_theme_info "$2"
            ;;
        apply)
            if [[ -z "$2" || -z "$3" ]]; then
                print_error "请指定文件和主题"
                echo "用法: $0 apply <markdown_file> <theme_id>"
                exit 1
            fi
            apply_theme "$2" "$3"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
