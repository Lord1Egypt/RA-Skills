#!/bin/bash
#
# 智能提示工具 - 分析项目状态并给出下一步建议
#
# 用法: bash scripts/suggest.sh [选项]
#   --all     显示所有建议
#   --next    只显示下一步建议
#   --fix     尝试自动修复

set -e

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
tip() { echo -e "💡 $1"; }

show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     💡 智能提示工具                              ║"
    echo "║     分析项目状态，给出下一步建议                 ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 分析TODO标记
analyze_todos() {
    local todos=()

    if [ -d "src" ]; then
        while IFS=: read -r file line content; do
            todos+=("$file:$line:$content")
        done < <(grep -rn "\[TODO\]" src/ 2>/dev/null | head -10)
    fi

    echo "${#todos[@]}"
}

# 获取TODO详情
get_todo_details() {
    grep -rn "\[TODO\]" src/ 2>/dev/null | head -5 | while IFS=: read -r file line content; do
        echo "  📍 $file:$line"
        echo "     $(echo "$content" | sed 's/.*\[TODO\]//')"
        echo ""
    done
}

# 分析测试覆盖率
analyze_tests() {
    local test_count=0
    local src_count=0

    if [ -d "test" ]; then
        test_count=$(find test -name "*.test.ts" -o -name "*.spec.ts" 2>/dev/null | wc -l)
    fi

    if [ -d "src/services" ]; then
        src_count=$(find src/services -name "*.ts" 2>/dev/null | wc -l)
    fi

    if [ "$src_count" -gt 0 ]; then
        local coverage=$((test_count * 100 / src_count))
        echo "$coverage"
    else
        echo "0"
    fi
}

# 分析编译状态
analyze_build() {
    if bash scripts/build-check.sh > /dev/null 2>&1; then
        echo "pass"
    else
        echo "fail"
    fi
}

# 分析规范得分
analyze_lint() {
    if [ -f "scripts/lint.sh" ]; then
        bash scripts/lint.sh --score 2>/dev/null || echo "0"
    else
        echo "N/A"
    fi
}

# 检测开发阶段
detect_stage() {
    local has_prd=0
    local has_code=0
    local has_test=0
    local has_doc=0

    [ -d "docs/prd" ] && [ "$(find docs/prd -name "*_PRD.md" 2>/dev/null | wc -l)" -gt 0 ] && has_prd=1
    [ -d "src/services" ] && [ "$(find src/services -name "*.ts" 2>/dev/null | wc -l)" -gt 0 ] && has_code=1
    [ -d "test" ] && [ "$(find test -name "*.test.ts" 2>/dev/null | wc -l)" -gt 0 ] && has_test=1
    [ -f "README.md" ] && has_doc=1

    if [ "$has_prd" -eq 0 ]; then
        echo "product"
    elif [ "$has_code" -eq 0 ]; then
        echo "generate"
    elif [ "$has_test" -eq 0 ]; then
        echo "implement"
    elif [ "$(analyze_build)" = "fail" ]; then
        echo "verify"
    elif [ "$has_doc" -eq 0 ]; then
        echo "document"
    else
        echo "complete"
    fi
}

# 生成下一步建议
generate_suggestions() {
    local stage=$(detect_stage)
    local todos=$(analyze_todos)
    local test_coverage=$(analyze_tests)
    local build_status=$(analyze_build)
    local lint_score=$(analyze_lint)

    echo "📊 项目状态分析"
    echo "==============="
    echo ""
    echo "当前阶段: $(case $stage in
        product) echo "📋 产品功能设计" ;;
        generate) echo "🏗️ 代码生成" ;;
        implement) echo "💻 功能实现" ;;
        verify) echo "✅ 验证测试" ;;
        document) echo "📝 文档完善" ;;
        complete) echo "🎉 项目完成" ;;
    esac)"
    echo "待办事项: $todos 个"
    echo "测试覆盖: $test_coverage%"
    echo "编译状态: $(if [ "$build_status" = "pass" ]; then echo "✅ 通过"; else echo "❌ 失败"; fi)"
    [ "$lint_score" != "N/A" ] && echo "规范得分: $lint_score/100"
    echo ""

    echo "🎯 下一步建议"
    echo "=============="
    echo ""

    local priority=1

    # 根据阶段给出建议
    case $stage in
        product)
            step "${priority}. 完成产品功能设计"
            tip "运行: bash scripts/quick.sh prd init '功能名称'"
            tip "参考: docs/workflow.md#阶段1-产品功能设计"
            ((priority++))
            ;;
        generate)
            step "${priority}. 生成代码骨架"
            tip "运行: bash scripts/quick.sh gen service YourService"
            tip "运行: bash scripts/quick.sh gen page YourPage"
            ((priority++))
            ;;
        implement)
            step "${priority}. 启动TDD开发流程"
            tip "运行: bash scripts/quick.sh tdd start YourService yourMethod"
            tip "运行: bash scripts/quick.sh tdd run"
            ((priority++))

            if [ "$todos" -gt 0 ]; then
                step "${priority}. 处理待办事项 ($todos 个)"
                get_todo_details
                ((priority++))
            fi
            ;;
        verify)
            step "${priority}. 修复编译错误"
            tip "运行: bash scripts/build-check.sh --verbose"
            ((priority++))
            ;;
        document)
            step "${priority}. 完善项目文档"
            tip "检查: README.md 是否完整"
            tip "检查: API文档是否更新"
            ((priority++))
            ;;
        complete)
            success "项目看起来已经完成！🎉"
            tip "建议运行: bash scripts/quick.sh health 进行全面检查"
            ;;
    esac

    # 通用建议
    if [ "$test_coverage" -lt 60 ] && [ "$stage" != "product" ] && [ "$stage" != "generate" ]; then
        step "${priority}. 提升测试覆盖率 (当前 $test_coverage%, 目标 60%+)"
        tip "运行: bash scripts/quick.sh gen test YourService"
        ((priority++))
    fi

    if [ "$build_status" = "pass" ] && [ "$lint_score" != "N/A" ] && [ "$lint_score" -lt 90 ]; then
        step "${priority}. 提升代码规范得分 (当前 $lint_score, 目标 90+)"
        tip "运行: bash scripts/quick.sh fix"
        ((priority++))
    fi

    if [ -d ".git" ]; then
        local uncommitted=$(git status --short 2>/dev/null | wc -l)
        if [ "$uncommitted" -gt 0 ]; then
            step "${priority}. 提交未保存的变更 ($uncommitted 个文件)"
            tip "运行: git add . && git commit -m '你的提交信息'"
            ((priority++))
        fi
    fi
}

# 尝试自动修复
auto_fix() {
    step "尝试自动修复..."

    # 修复规范问题
    if [ -f "scripts/lint.sh" ]; then
        info "修复规范问题..."
        bash scripts/lint.sh --fix 2>/dev/null || warn "无法自动修复规范问题"
    fi

    # 生成缺失的测试模板
    local services_without_tests=()
    if [ -d "src/services" ]; then
        for service in src/services/*.ts; do
            local name=$(basename "$service" .ts)
            if [ ! -f "test/unittest/${name}.test.ts" ]; then
                services_without_tests+=("$name")
            fi
        done
    fi

    if [ ${#services_without_tests[@]} -gt 0 ]; then
        info "生成缺失的测试文件..."
        for name in "${services_without_tests[@]}"; do
            bash scripts/generate.sh test "$name" 2>/dev/null
            success "生成: test/unittest/${name}.test.ts"
        done
    fi

    success "自动修复完成"
    tip "运行 'bash scripts/suggest.sh' 查看剩余建议"
}

# 主函数
main() {
    show_banner

    local mode="all"

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                mode="all"
                shift
                ;;
            --next)
                mode="next"
                shift
                ;;
            --fix)
                auto_fix
                exit 0
                ;;
            --help|-h)
                echo "用法: bash scripts/suggest.sh [选项]"
                echo ""
                echo "选项:"
                echo "  --all     显示所有建议 (默认)"
                echo "  --next    只显示下一步建议"
                echo "  --fix     尝试自动修复"
                echo "  --help    显示帮助"
                exit 0
                ;;
            *)
                error "未知选项: $1"
                echo "运行 'bash scripts/suggest.sh --help' 查看用法"
                exit 1
                ;;
        esac
    done

    # 检查项目
    if [ ! -f "PROJECT.md" ] && [ ! -d "src" ]; then
        error "未检测到项目结构"
        tip "请先运行: bash scripts/init-project.sh ./MyApp MyFeature"
        exit 1
    fi

    if [ "$mode" = "next" ]; then
        # 只显示下一步
        local stage=$(detect_stage)
        case $stage in
            product)
                echo "下一步: 完成产品功能设计"
                echo "  bash scripts/quick.sh prd init '功能名称'"
                ;;
            generate)
                echo "下一步: 生成代码骨架"
                echo "  bash scripts/quick.sh gen service YourService"
                ;;
            implement)
                echo "下一步: 启动TDD开发"
                echo "  bash scripts/quick.sh tdd start YourService yourMethod"
                ;;
            verify)
                echo "下一步: 修复编译错误"
                echo "  bash scripts/build-check.sh --verbose"
                ;;
            document)
                echo "下一步: 完善文档"
                echo "  编辑 README.md 和 API文档"
                ;;
            complete)
                echo "项目已完成！建议:"
                echo "  bash scripts/quick.sh health"
                ;;
        esac
    else
        # 显示完整分析
        generate_suggestions
    fi

    echo ""
    echo "═══════════════════════════════════════════════════"
    tip "随时运行 'bash scripts/suggest.sh' 查看最新建议"
    echo "═══════════════════════════════════════════════════"
    echo ""
}

main "$@"
