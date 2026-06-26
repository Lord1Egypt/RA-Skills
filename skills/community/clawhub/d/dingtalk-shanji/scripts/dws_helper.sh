#!/bin/bash
# 钉钉闪记数据提取辅助脚本
# 使用 dws CLI 工具

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 dws 是否已安装
check_dws() {
    if command -v dws &> /dev/null; then
        info "dws 已安装: $(dws --version 2>/dev/null || echo '未知版本')"
        return 0
    else
        warn "dws 未安装"
        return 1
    fi
}

# 安装 dws
install_dws() {
    info "开始安装 dws..."

    # 方式1：尝试 npm 安装
    if command -v npm &> /dev/null; then
        info "使用 npm 安装..."
        if npm install -g dingtalk-workspace-cli; then
            info "npm 安装成功"
            return 0
        else
            warn "npm 安装失败，尝试 sh 脚本安装..."
        fi
    else
        warn "npm 未安装，尝试 sh 脚本安装..."
    fi

    # 方式2：使用 sh 脚本安装
    info "使用 sh 脚本安装..."
    if curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh; then
        info "sh 脚本安装成功"
        return 0
    else
        error "安装失败"
        return 1
    fi
}

# 登录认证
login() {
    info "开始登录认证..."
    dws login
}

# 列出听记
list_minutes() {
    local type=${1:-"mine"}
    local format=${2:-"table"}
    local max=${3:-"20"}

    case $type in
        all)
            dws minutes list all --max $max -f $format
            ;;
        mine)
            dws minutes list mine --max $max -f $format
            ;;
        shared)
            dws minutes list shared --max $max -f $format
            ;;
        *)
            error "未知类型: $type"
            echo "用法: $0 list [all|mine|shared] [json|table|raw] [max]"
            exit 1
            ;;
    esac
}

# 获取转写文本
get_transcription() {
    local id=$1

    if [ -z "$id" ]; then
        error "请提供听记ID (taskUuid)"
        echo "用法: $0 transcription <taskUuid>"
        exit 1
    fi

    dws minutes get transcription --id "$id"
}

# 获取摘要
get_summary() {
    local id=$1

    if [ -z "$id" ]; then
        error "请提供听记ID (taskUuid)"
        echo "用法: $0 summary <taskUuid>"
        exit 1
    fi

    dws minutes get summary --id "$id"
}

# 获取待办
get_todos() {
    local id=$1

    if [ -z "$id" ]; then
        error "请提供听记ID (taskUuid)"
        echo "用法: $0 todos <taskUuid>"
        exit 1
    fi

    dws minutes get todos --id "$id"
}

# 获取详情
get_info() {
    local id=$1
    local format=${2:-"table"}

    if [ -z "$id" ]; then
        error "请提供听记ID (taskUuid)"
        echo "用法: $0 info <taskUuid> [json|table|raw]"
        exit 1
    fi

    dws minutes get info --id "$id" -f $format
}

# 搜索听记
search_minutes() {
    local keyword=$1
    local format=${2:-"table"}

    if [ -z "$keyword" ]; then
        error "请提供搜索关键词"
        echo "用法: $0 search <keyword> [json|table|raw]"
        exit 1
    fi

    dws minutes list all --keyword "$keyword" -f $format
}

# 显示帮助
show_help() {
    echo "钉钉闪记数据提取辅助脚本"
    echo ""
    echo "用法: $0 <command> [options]"
    echo ""
    echo "命令:"
    echo "  check                         检查 dws 是否已安装"
    echo "  install                       安装 dws"
    echo "  login                         登录认证"
    echo "  list [type] [format] [max]    列出听记 (type: all|mine|shared, format: json|table|raw, max: 数量)"
    echo "  info <taskUuid> [format]      获取听记详情"
    echo "  transcription <taskUuid>      获取转写文本"
    echo "  summary <taskUuid>            获取摘要"
    echo "  todos <taskUuid>              获取待办事项"
    echo "  search <keyword> [format]     搜索听记"
    echo "  help                          显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 check"
    echo "  $0 install"
    echo "  $0 login"
    echo "  $0 list mine json 10"
    echo "  $0 transcription 76327569643331323336383832345f3237323535323932305f32"
    echo "  $0 search 医美"
}

# 主函数
main() {
    local command=$1
    shift || true

    case $command in
        check)
            check_dws
            ;;
        install)
            install_dws
            ;;
        login)
            login
            ;;
        list)
            list_minutes "$@"
            ;;
        info)
            get_info "$@"
            ;;
        transcription)
            get_transcription "$@"
            ;;
        summary)
            get_summary "$@"
            ;;
        todos)
            get_todos "$@"
            ;;
        search)
            search_minutes "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
