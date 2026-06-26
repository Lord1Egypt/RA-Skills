#!/bin/bash
#
# 项目健康检查 - 快速诊断项目状态
#
# 用法: bash scripts/health-check.sh
#

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     🏥 项目健康检查                              ║"
    echo "║     快速诊断项目状态                             ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 统计代码行数
count_lines() {
    local dir="${1:-src}"
    if [ -d "$dir" ]; then
        find "$dir" -name "*.ts" -o -name "*.ets" 2>/dev/null | \
        xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}'
    else
        echo "0"
    fi
}

# 统计文件数量
count_files() {
    local dir="$1"
    local pattern="$2"
    if [ -d "$dir" ]; then
        find "$dir" -name "$pattern" 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# 检查TODO数量
count_todos() {
    if [ -d "src" ]; then
        grep -r "\[TODO\]" src/ 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# 检查待办建议数量
count_suggestions() {
    if [ -d "docs/prd" ]; then
        find docs/prd -name "*_PRD.md" 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# 主检查流程
main() {
    show_banner

    local issues=0
    local warnings=0

    step "执行项目健康检查..."
    echo ""

    # 1. 项目结构检查
    info "1/6 项目结构检查"

    local dirs=("src" "test" "docs" "scripts")
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            echo "  ✅ $dir/"
        else
            echo "  ❌ $dir/ (缺失)"
            ((issues++))
        fi
    done

    # 2. 代码统计
    echo ""
    info "2/6 代码统计"

    local src_lines=$(count_lines "src")
    local src_files=$(count_files "src" "*.ts" 2>/dev/null)
    local src_ets=$(count_files "src" "*.ets" 2>/dev/null)
    local test_files=$(count_files "test" "*.test.ts" 2>/dev/null)

    echo "  📄 TypeScript文件: $src_files"
    echo "  📄 ArkTS文件: $src_ets"
    echo "  📝 源码总行数: $src_lines"
    echo "  🧪 测试文件: $test_files"

    if [ "$test_files" -eq 0 ]; then
        warn "  未找到测试文件"
        ((warnings++))
    fi

    # 3. 待办事项检查
    echo ""
    info "3/6 待办事项检查"

    local todo_count=$(count_todos)
    echo "  📝 代码中 [TODO] 数量: $todo_count"

    if [ "$todo_count" -gt 10 ]; then
        warn "  待办事项较多，建议清理"
        ((warnings++))
    elif [ "$todo_count" -eq 0 ]; then
        success "  没有待办事项"
    fi

    # 4. 文档检查
    echo ""
    info "4/6 文档检查"

    local prd_count=$(count_suggestions)
    echo "  📋 PRD文档: $prd_count"

    if [ -f "PROJECT.md" ]; then
        echo "  ✅ PROJECT.md"
    else
        warn "  ❌ PROJECT.md (缺失)"
        ((warnings++))
    fi

    if [ -f "README.md" ]; then
        echo "  ✅ README.md"
    else
        warn "  ❌ README.md (缺失)"
    fi

    # 5. 编译状态检查
    echo ""
    info "5/6 编译状态检查"

    if bash scripts/build-check.sh > /dev/null 2>&1; then
        success "  编译状态: 通过"
    else
        error "  编译状态: 失败"
        ((issues++))
    fi

    # 6. Git状态检查
    echo ""
    info "6/6 Git状态检查"

    if [ -d ".git" ]; then
        local uncommitted=$(git status --short 2>/dev/null | wc -l)
        if [ "$uncommitted" -gt 0 ]; then
            warn "  未提交变更: $uncommitted 个文件"
            ((warnings++))
        else
            success "  工作区干净"
        fi

        local branch=$(git branch --show-current 2>/dev/null)
        echo "  📌 当前分支: $branch"
    else
        warn "  未初始化Git仓库"
    fi

    # 总结
    echo ""
    echo "═══════════════════════════════════════════════════"

    if [ $issues -eq 0 ] && [ $warnings -eq 0 ]; then
        success "项目状态: 健康 ✅"
    elif [ $issues -eq 0 ]; then
        warn "项目状态: 良好，有 $warnings 个警告 ⚠️"
    else
        error "项目状态: 需要关注，有 $issues 个问题 ❌"
    fi

    echo "═══════════════════════════════════════════════════"
    echo ""

    # 建议操作
    if [ $issues -gt 0 ] || [ $warnings -gt 0 ]; then
        step "建议操作:"

        if [ -d "src" ] && [ "$(count_todos)" -gt 0 ]; then
            echo "  1. 处理代码中的 [TODO] 标记"
            echo "     grep -r '\[TODO\]' src/"
        fi

        if [ "$test_files" -eq 0 ]; then
            echo "  2. 添加单元测试"
            echo "     bash scripts/generate.sh test YourService"
        fi

        if ! bash scripts/build-check.sh > /dev/null 2>&1; then
            echo "  3. 修复编译错误"
            echo "     bash scripts/build-check.sh --verbose"
        fi

        echo "  4. 运行完整检查"
        echo "     bash scripts/quick.sh check"
    else
        info "建议: 定期运行 'bash scripts/health-check.sh' 监控项目健康"
    fi

    echo ""
}

main "$@"
