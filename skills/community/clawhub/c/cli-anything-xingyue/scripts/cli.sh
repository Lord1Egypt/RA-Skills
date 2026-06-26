#!/bin/bash
# CLI-Anything OpenClaw Skill Launcher
# 使用方法: uv run cli-anything.py <command> <args>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_ANYTHING_DIR="${HOME}/.openclaw/cli-anything"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# 确保 CLI-Anything 仓库存在
ensure_cli_anything() {
    if [ ! -d "$CLI_ANYTHING_DIR" ]; then
        log_info "正在克隆 CLI-Anything 仓库..."
        git clone https://github.com/HKUDS/CLI-Anything.git "$CLI_ANYTHING_DIR"
    else
        log_info "更新 CLI-Anything 仓库..."
        cd "$CLI_ANYTHING_DIR" && git pull
    fi
}

# 构建 CLI
cmd_build() {
    local target="$1"
    
    if [ -z "$target" ]; then
        log_error "请指定软件路径或 GitHub 仓库 URL"
        echo "用法: /cli-build ./gimp"
        echo "     /cli-build https://github.com/blender/blender"
        return 1
    fi
    
    ensure_cli_anything
    
    log_info "开始为 $target 构建 CLI..."
    log_info "这可能需要几分钟时间..."
    
    # 复制到临时目录并构建
    local target_name
    target_name=$(basename "$target")
    
    echo ""
    log_success "请在支持 Claude Code 或 Codex 的环境中运行以下命令："
    echo ""
    echo "  /cli-anything:cli-anything $target"
    echo ""
    log_info "或者手动执行:"
    echo "  cd $CLI_ANYTHING_DIR"
    echo "  /cli-anything $target"
    echo ""
    log_warn "注意: CLI-Anything 完整功能需要 Claude Code 或 Codex"
}

# 优化 CLI
cmd_refine() {
    local target="$1"
    local focus="$2"
    
    if [ -z "$target" ]; then
        log_error "请指定软件路径"
        return 1
    fi
    
    ensure_cli_anything
    
    echo ""
    log_success "优化 CLI: $target"
    
    if [ -n "$focus" ]; then
        log_info "优化重点: $focus"
    fi
    
    echo ""
    log_success "请在支持 Claude Code 或 Codex 的环境中运行以下命令："
    echo ""
    echo "  /cli-anything:refine $target $focus"
    echo ""
}

# 验证 CLI
cmd_validate() {
    local target="$1"
    
    if [ -z "$target" ]; then
        log_error "请指定软件路径"
        return 1
    fi
    
    local harness_dir="$target/agent-harness"
    
    if [ ! -d "$harness_dir" ]; then
        log_error "未找到 agent-harness 目录"
        log_info "请先使用 /cli-build 构建 CLI"
        return 1
    fi
    
    echo "🔍 验证 CLI: $target"
    echo ""
    
    # 检查必要文件
    local checks=0
    local passed=0
    
    ((checks++))
    if [ -f "$harness_dir/setup.py" ]; then
        log_success "setup.py 存在"
        ((passed++))
    else
        log_error "setup.py 缺失"
    fi
    
    ((checks++))
    if [ -d "$harness_dir/cli_anything" ]; then
        log_success "cli_anything 命名空间包存在"
        ((passed++))
    else
        log_error "cli_anything 命名空间包缺失"
    fi
    
    ((checks++))
    if [ -f "$harness_dir/README.md" ]; then
        log_success "README.md 存在"
        ((passed++))
    else
        log_warn "README.md 缺失"
    fi
    
    echo ""
    echo "验证结果: $passed/$checks 通过"
    
    if [ $passed -eq $checks ]; then
        log_success "CLI 验证通过！"
        return 0
    else
        log_error "CLI 验证失败"
        return 1
    fi
}

# 列出 CLI
cmd_list() {
    echo "📋 已生成的 CLI 工具:"
    echo ""
    
    local found=0
    for dir in */agent-harness; do
        if [ -d "$dir" ]; then
            local name="${dir%/agent-harness}"
            echo "  • $name"
            found=1
        fi
    done
    
    if [ $found -eq 0 ]; then
        echo "  (无)"
        echo ""
        log_info "使用 /cli-build <路径> 构建新的 CLI"
    fi
}

# 主入口
main() {
    local command="${1:-}"
    shift || true
    
    case "$command" in
        build)
            cmd_build "$@"
            ;;
        refine)
            cmd_refine "$@"
            ;;
        validate)
            cmd_validate "$@"
            ;;
        list)
            cmd_list
            ;;
        help|--help|-h)
            echo "CLI-Anything for OpenClaw"
            echo ""
            echo "用法:"
            echo "  /cli-build <路径>     - 构建 CLI"
            echo "  /cli-refine <路径>    - 优化 CLI"
            echo "  /cli-validate <路径>  - 验证 CLI"
            echo "  /cli-list             - 列出已构建的 CLI"
            ;;
        "")
            cmd_list
            ;;
        *)
            log_error "未知命令: $command"
            echo "使用 help 查看用法"
            ;;
    esac
}

main "$@"
