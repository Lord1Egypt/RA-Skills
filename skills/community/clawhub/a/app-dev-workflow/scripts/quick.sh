#!/bin/bash
#
# 快捷命令集 - 常用操作一键执行
#
# 用法: bash scripts/quick.sh <命令> [参数]
#

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

show_help() {
    echo "AppDev Skill 快捷命令"
    echo ""
    echo "用法: bash scripts/quick.sh <命令> [参数]"
    echo ""
    echo "代码生成:"
    echo "  gen model <Name>        生成数据模型"
    echo "  gen service <Name>      生成服务类"
    echo "  gen page <Name>         生成页面"
    echo "  gen viewmodel <Name>    生成ViewModel"
    echo ""
    echo "开发测试:"
    echo "  test [name]             运行测试"
    echo "  tdd start <S> <M>       启动TDD流程"
    echo "  tdd run                 运行TDD测试"
    echo ""
    echo "质量检查:"
    echo "  check                   编译+规范检查"
    echo "  lint                    规范检查"
    echo "  fix                     自动修复规范问题"
    echo "  health                  项目健康检查"
    echo ""
    echo "产品文档:"
    echo "  prd init <name>         初始化PRD"
    echo "  prd flow <name>         生成用户流程"
    echo "  prd tracking <name>     生成埋点设计"
    echo ""
    echo "其他:"
    echo "  build                   编译项目"
    echo "  clean                   清理构建缓存"
    echo "  update <type> <msg>     更新版本"
    echo "  wizard                  交互式向导"
    echo ""
    echo "v1.2 新增:"
    echo "  viz                     生成架构可视化图"
    echo "  viz html                生成 HTML 预览"
    echo "  mock start              启动 Mock 服务器"
    echo "  mock stop               停止 Mock 服务器"
    echo "  report                  生成质量报告"
    echo "  hooks install           安装 Git Hooks"
    echo "  suggest                 智能建议"
    echo "  pipeline                运行自动化流水线"
    echo ""
    echo "v2.0 新增 (AI辅助):"
    echo "  ai service --prd=<>     AI生成服务代码"
    echo "  ai page --prd=<>        AI生成页面代码"
    echo "  ai tests --for=<>       AI生成测试用例"
    echo "  ai impl --method=<>     AI辅助实现方法"
    echo "  sync status             查看协作状态"
    echo "  sync check              检查冲突风险"
    echo "  perf analyze            分析代码性能"
    echo "  perf report             生成性能报告"
    echo ""
}

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 代码生成快捷命令
cmd_gen() {
    local type="$1"
    local name="$2"

    if [ -z "$type" ] || [ -z "$name" ]; then
        error "缺少参数"
        echo "用法: quick gen <type> <name>"
        echo "类型: model, service, page, viewmodel, test"
        return 1
    fi

    step "生成 $type: $name"
    bash "$SCRIPT_DIR/generate.sh" "$type" "$name"
}

# 测试快捷命令
cmd_test() {
    local name="${1:-}"

    if [ -n "$name" ]; then
        step "运行测试: $name"
        bash "$SCRIPT_DIR/test.sh" "$name"
    else
        step "运行所有测试"
        bash "$SCRIPT_DIR/tdd.sh" run 2>/dev/null || npm test 2>/dev/null || warn "未配置测试运行器"
    fi
}

# TDD快捷命令
cmd_tdd() {
    local action="$1"
    shift || true

    case "$action" in
        start)
            local service="$1"
            local method="$2"
            if [ -z "$service" ] || [ -z "$method" ]; then
                error "缺少参数: tdd start <Service> <Method>"
                return 1
            fi
            step "启动TDD: $service.$method"
            bash "$SCRIPT_DIR/tdd.sh" start "$service" "$method"
            ;;
        run)
            step "运行TDD测试"
            bash "$SCRIPT_DIR/tdd.sh" run
            ;;
        impl)
            step "进入实现阶段"
            bash "$SCRIPT_DIR/tdd.sh" impl
            ;;
        refactor)
            step "重构检查"
            bash "$SCRIPT_DIR/tdd.sh" refactor
            ;;
        *)
            error "未知TDD命令: $action"
            echo "可用: start, run, impl, refactor"
            return 1
            ;;
    esac
}

# 质量检查快捷命令
cmd_check() {
    step "执行质量检查..."

    echo ""
    info "1/3 编译检查"
    if bash "$SCRIPT_DIR/build-check.sh"; then
        success "编译通过"
    else
        error "编译失败"
        return 1
    fi

    echo ""
    info "2/3 规范检查"
    if bash "$SCRIPT_DIR/lint.sh"; then
        success "规范检查通过"
    else
        warn "规范检查发现问题，运行 'quick fix' 自动修复"
    fi

    echo ""
    info "3/3 健康检查"
    bash "$SCRIPT_DIR/health-check.sh" 2>/dev/null || warn "健康检查脚本不存在"

    echo ""
    success "质量检查完成"
}

# 规范修复
cmd_fix() {
    step "自动修复规范问题..."

    if [ -f "$SCRIPT_DIR/lint.sh" ]; then
        bash "$SCRIPT_DIR/lint.sh" --fix 2>/dev/null || warn "自动修复不支持，请手动修复"
    else
        warn "lint.sh 不存在"
    fi
}

# PRD快捷命令
cmd_prd() {
    local action="$1"
    local name="$2"

    if [ -z "$action" ]; then
        error "缺少参数: prd <action> [name]"
        return 1
    fi

    case "$action" in
        init|flow|tracking)
            if [ -z "$name" ]; then
                error "缺少功能名称"
                return 1
            fi
            bash "$SCRIPT_DIR/prd.sh" "$action" "$name"
            ;;
        checklist)
            bash "$SCRIPT_DIR/prd.sh" checklist "$name"
            ;;
        *)
            error "未知PRD命令: $action"
            echo "可用: init, flow, tracking, checklist"
            return 1
            ;;
    esac
}

# 编译
cmd_build() {
    step "编译项目"
    bash "$SCRIPT_DIR/build-check.sh"
}

# 清理
cmd_clean() {
    step "清理构建缓存"

    # 清理常见缓存目录
    rm -rf build/ 2>/dev/null || true
    rm -rf .cache/ 2>/dev/null || true
    rm -rf node_modules/.cache/ 2>/dev/null || true

    success "清理完成"
}

# 更新版本
cmd_update() {
    local type="$1"
    local msg="$2"

    if [ -z "$type" ] || [ -z "$msg" ]; then
        error "缺少参数: update <type> <message>"
        echo "类型: patch, minor, major"
        return 1
    fi

    bash "$SCRIPT_DIR/update.sh" "$type" "$msg"
}

# 健康检查
cmd_health() {
    if [ -f "$SCRIPT_DIR/health-check.sh" ]; then
        bash "$SCRIPT_DIR/health-check.sh"
    else
        error "健康检查脚本不存在"
        echo "创建中..."

        # 创建简易版健康检查
        cat > "$SCRIPT_DIR/health-check.sh" << 'EOF'
#!/bin/bash
echo "🏥 项目健康检查"
echo "==============="

todo_count=$(grep -r "\[TODO\]" src/ 2>/dev/null | wc -l)
echo "📝 待办事项: $todo_count"

if [ -d "test" ]; then
    test_count=$(find test -name "*.test.ts" 2>/dev/null | wc -l)
    echo "🧪 测试文件: $test_count"
fi

src_files=$(find src -name "*.ts" -o -name "*.ets" 2>/dev/null | wc -l)
echo "📄 源码文件: $src_files"

echo ""
echo "建议: 定期运行 'quick check' 确保代码质量"
EOF
        chmod +x "$SCRIPT_DIR/health-check.sh"
        bash "$SCRIPT_DIR/health-check.sh"
    fi
}

# 交互式向导
cmd_wizard() {
    if [ -f "$SCRIPT_DIR/wizard.sh" ]; then
        bash "$SCRIPT_DIR/wizard.sh"
    else
        error "向导脚本不存在"
        echo "请直接运行具体命令，或查看: quick --help"
    fi
}

# 架构可视化
cmd_viz() {
    local action="${1:-all}"

    if [ -f "$SCRIPT_DIR/visualize.sh" ]; then
        bash "$SCRIPT_DIR/visualize.sh" "$action"
    else
        error "可视化脚本不存在"
        info "运行: bash scripts/visualize.sh $action"
    fi
}

# Mock 服务器
cmd_mock() {
    local action="${1:-status}"
    shift || true

    if [ -f "$SCRIPT_DIR/mock-server.sh" ]; then
        bash "$SCRIPT_DIR/mock-server.sh" "$action" "$@"
    else
        error "Mock 服务器脚本不存在"
    fi
}

# 质量报告
cmd_report() {
    if [ -f "$SCRIPT_DIR/quality-report.sh" ]; then
        bash "$SCRIPT_DIR/quality-report.sh" "$@"
    else
        error "质量报告脚本不存在"
    fi
}

# Git Hooks
cmd_hooks() {
    local action="${1:-status}"

    if [ -f "$SCRIPT_DIR/setup-hooks.sh" ]; then
        bash "$SCRIPT_DIR/setup-hooks.sh" "$action"
    else
        error "Git Hooks 脚本不存在"
    fi
}

# 智能建议
cmd_suggest() {
    if [ -f "$SCRIPT_DIR/suggest.sh" ]; then
        bash "$SCRIPT_DIR/suggest.sh" "$@"
    else
        error "智能建议脚本不存在"
    fi
}

# 自动化流水线
cmd_pipeline() {
    if [ -f "$SCRIPT_DIR/pipeline.sh" ]; then
        bash "$SCRIPT_DIR/pipeline.sh" "$@"
    else
        error "流水线脚本不存在"
    fi
}

# v2.0 AI辅助生成
cmd_ai() {
    local type="$1"
    shift || true

    if [ -f "$SCRIPT_DIR/ai-generate.sh" ]; then
        bash "$SCRIPT_DIR/ai-generate.sh" "$type" "$@"
    else
        error "AI生成脚本不存在"
    fi
}

# v2.0 协作同步
cmd_sync() {
    if [ -f "$SCRIPT_DIR/sync.sh" ]; then
        bash "$SCRIPT_DIR/sync.sh" "$@"
    else
        error "协作同步脚本不存在"
    fi
}

# v2.0 性能报告
cmd_perf() {
    if [ -f "$SCRIPT_DIR/perf-report.sh" ]; then
        bash "$SCRIPT_DIR/perf-report.sh" "$@"
    else
        error "性能报告脚本不存在"
    fi
}

# 主函数
main() {
    local cmd="${1:-}"
    shift || true

    case "$cmd" in
        gen)
            cmd_gen "$@"
            ;;
        test)
            cmd_test "$@"
            ;;
        tdd)
            cmd_tdd "$@"
            ;;
        check)
            cmd_check
            ;;
        lint)
            bash "$SCRIPT_DIR/lint.sh"
            ;;
        fix)
            cmd_fix
            ;;
        health)
            cmd_health
            ;;
        prd)
            cmd_prd "$@"
            ;;
        build)
            cmd_build
            ;;
        clean)
            cmd_clean
            ;;
        update)
            cmd_update "$@"
            ;;
        wizard)
            cmd_wizard
            ;;
        viz)
            cmd_viz "$@"
            ;;
        mock)
            cmd_mock "$@"
            ;;
        report)
            cmd_report "$@"
            ;;
        hooks)
            cmd_hooks "$@"
            ;;
        suggest)
            cmd_suggest "$@"
            ;;
        pipeline)
            cmd_pipeline "$@"
            ;;
        ai)
            cmd_ai "$@"
            ;;
        sync)
            cmd_sync "$@"
            ;;
        perf)
            cmd_perf "$@"
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            error "未知命令: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
