#!/bin/bash
#
# 自动化流水线 - 一键执行多阶段开发任务
#
# 用法: bash scripts/pipeline.sh <命令> [选项]
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

show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     🚀 自动化流水线                              ║"
    echo "║     一键执行多阶段开发任务                       ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 显示帮助
show_help() {
    echo "自动化流水线 - 串联多个开发阶段"
    echo ""
    echo "用法: bash scripts/pipeline.sh <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  run [阶段范围]     执行流水线"
    echo "  status             查看流水线状态"
    echo "  reset              重置流水线状态"
    echo "  list               列出所有阶段"
    echo ""
    echo "阶段范围:"
    echo "  --from=<阶段>      起始阶段 (默认: 当前阶段)"
    echo "  --to=<阶段>        结束阶段 (默认: verify)"
    echo ""
    echo "示例:"
    echo "  bash scripts/pipeline.sh run                    # 从当前阶段执行到verify"
    echo "  bash scripts/pipeline.sh run --from=generate    # 从generate阶段开始"
    echo "  bash scripts/pipeline.sh run --to=implement     # 执行到implement阶段"
    echo "  bash scripts/pipeline.sh run --from=generate --to=verify"
    echo ""
    echo "阶段列表:"
    echo "  1. product    - 产品功能设计"
    echo "  2. generate   - 代码生成"
    echo "  3. implement  - 功能实现"
    echo "  4. verify     - 验证测试"
    echo "  5. integrate  - 版本集成"
    echo ""
}

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 状态文件
STATE_FILE=".pipeline-state"

# 定义阶段
STAGES=("product" "generate" "implement" "verify" "integrate")
STAGE_NAMES=("产品功能设计" "代码生成" "功能实现" "验证测试" "版本集成")

# 保存状态
save_state() {
    local current_stage="$1"
    local status="$2"
    echo "{\"stage\": \"$current_stage\", \"status\": \"$status\", \"timestamp\": $(date +%s)}" > "$STATE_FILE"
}

# 读取状态
load_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "{\"stage\": \"product\", \"status\": \"pending\"}"
    fi
}

# 获取当前阶段索引
get_stage_index() {
    local stage="$1"
    for i in "${!STAGES[@]}"; do
        if [ "${STAGES[$i]}" = "$stage" ]; then
            echo "$i"
            return
        fi
    done
    echo "0"
}

# 获取阶段名称
get_stage_name() {
    local index="$1"
    echo "${STAGE_NAMES[$index]}"
}

# 执行单个阶段
execute_stage() {
    local stage="$1"
    local name=$(get_stage_name $(get_stage_index "$stage"))

    step "执行阶段: $name ($stage)"
    echo ""

    case "$stage" in
        product)
            echo "📋 产品功能设计阶段"
            echo ""
            read -p "请输入功能名称 (或按Enter跳过): " feature_name
            if [ -n "$feature_name" ]; then
                bash "$SCRIPT_DIR/quick.sh" prd init "$feature_name" || return 1
                bash "$SCRIPT_DIR/quick.sh" prd flow "$feature_name" || true
                bash "$SCRIPT_DIR/quick.sh" prd tracking "$feature_name" || true
            else
                info "跳过产品功能设计"
            fi
            ;;

        generate)
            echo "🏗️ 代码生成阶段"
            echo ""
            read -p "请输入模型名称: " model_name
            if [ -n "$model_name" ]; then
                bash "$SCRIPT_DIR/quick.sh" gen model "$model_name" || return 1
            fi

            read -p "请输入服务名称 (如${model_name}Service): " service_name
            if [ -n "$service_name" ]; then
                bash "$SCRIPT_DIR/quick.sh" gen service "$service_name" || return 1
            fi

            read -p "请输入页面名称: " page_name
            if [ -n "$page_name" ]; then
                bash "$SCRIPT_DIR/quick.sh" gen page "$page_name" || return 1
            fi
            ;;

        implement)
            echo "💻 功能实现阶段"
            echo ""
            info "启动TDD开发流程"
            echo ""

            # 查找可测试的服务
            local services=()
            if [ -d "src/services" ]; then
                for f in src/services/*.ts; do
                    [ -f "$f" ] && services+=("$(basename "$f" .ts)")
                done
            fi

            if [ ${#services[@]} -eq 0 ]; then
                error "未找到服务文件，请先执行generate阶段"
                return 1
            fi

            echo "可用的服务:"
            for i in "${!services[@]}"; do
                echo "  $((i+1)). ${services[$i]}"
            done
            echo ""

            read -p "请选择服务 (1-${#services[@]}): " service_idx
            if [ -n "$service_idx" ] && [ "$service_idx" -ge 1 ] && [ "$service_idx" -le "${#services[@]}" ]; then
                local service_name="${services[$((service_idx-1))]}"
                read -p "请输入要测试的方法名: " method_name
                if [ -n "$method_name" ]; then
                    bash "$SCRIPT_DIR/quick.sh" tdd start "$service_name" "$method_name" || return 1
                    bash "$SCRIPT_DIR/quick.sh" tdd run || return 1
                fi
            fi
            ;;

        verify)
            echo "✅ 验证测试阶段"
            echo ""

            info "1/3 编译检查"
            if bash "$SCRIPT_DIR/quick.sh" check; then
                success "编译检查通过"
            else
                error "编译检查失败"
                return 1
            fi
            ;;

        integrate)
            echo "📦 版本集成阶段"
            echo ""

            read -p "请输入版本更新类型 (patch/minor/major): " version_type
            read -p "请输入版本更新说明: " version_msg

            if [ -n "$version_type" ] && [ -n "$version_msg" ]; then
                bash "$SCRIPT_DIR/quick.sh" update "$version_type" "$version_msg" || return 1
            else
                warn "跳过版本更新"
            fi
            ;;
    esac

    echo ""
    success "阶段 $name 完成"
    echo ""

    return 0
}

# 运行流水线
cmd_run() {
    local from_stage=""
    local to_stage="verify"

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --from=*)
                from_stage="${1#*=}"
                shift
                ;;
            --to=*)
                to_stage="${1#*=}"
                shift
                ;;
            *)
                shift
                ;;
        esac
    done

    # 如果没指定from，从当前状态或product开始
    if [ -z "$from_stage" ]; then
        local state=$(load_state)
        from_stage=$(echo "$state" | grep -o '"stage": "[^"]*"' | cut -d'"' -f4)
        [ -z "$from_stage" ] && from_stage="product"
    fi

    show_banner

    step "启动自动化流水线"
    echo "  起始阶段: $from_stage"
    echo "  结束阶段: $to_stage"
    echo ""

    local from_idx=$(get_stage_index "$from_stage")
    local to_idx=$(get_stage_index "$to_stage")

    if [ "$from_idx" -gt "$to_idx" ]; then
        error "起始阶段不能在结束阶段之后"
        return 1
    fi

    # 执行各阶段
    for ((i=from_idx; i<=to_idx; i++)); do
        local stage="${STAGES[$i]}"
        local name=$(get_stage_name "$i")

        echo "═══════════════════════════════════════════════════"
        echo "  阶段 $((i+1))/${#STAGES[@]}: $name"
        echo "═══════════════════════════════════════════════════"
        echo ""

        if execute_stage "$stage"; then
            save_state "$stage" "completed"
        else
            error "阶段 $name 执行失败"
            save_state "$stage" "failed"
            echo ""
            tip "修复问题后，可以重新运行:"
            tip "  bash scripts/pipeline.sh run --from=$stage"
            return 1
        fi
    done

    echo "═══════════════════════════════════════════════════"
    success "🎉 流水线执行完成！"
    echo "═══════════════════════════════════════════════════"
    echo ""

    bash "$SCRIPT_DIR/quick.sh" health 2>/dev/null || true
}

# 查看状态
cmd_status() {
    show_banner

    local state=$(load_state)
    local current_stage=$(echo "$state" | grep -o '"stage": "[^"]*"' | cut -d'"' -f4)
    local status=$(echo "$state" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)

    echo "📊 流水线状态"
    echo "=============="
    echo ""
    echo "当前阶段: $(get_stage_name $(get_stage_index "$current_stage"))"
    echo "状态: $status"
    echo ""

    echo "阶段进度:"
    for i in "${!STAGES[@]}"; do
        local stage="${STAGES[$i]}"
        local name=$(get_stage_name "$i")
        local icon="⏳"

        local stage_idx=$(get_stage_index "$current_stage")
        if [ "$i" -lt "$stage_idx" ]; then
            icon="✅"
        elif [ "$i" -eq "$stage_idx" ]; then
            if [ "$status" = "completed" ]; then
                icon="✅"
            elif [ "$status" = "failed" ]; then
                icon="❌"
            else
                icon="🔄"
            fi
        fi

        echo "  $icon $((i+1)). $name"
    done

    echo ""
    echo "下一步:"
    bash "$SCRIPT_DIR/suggest.sh" --next
}

# 重置流水线
cmd_reset() {
    rm -f "$STATE_FILE"
    success "流水线状态已重置"
    info "下次将从 product 阶段开始"
}

# 列出阶段
cmd_list() {
    echo "📋 流水线阶段列表"
    echo "=================="
    echo ""

    for i in "${!STAGES[@]}"; do
        echo "$((i+1)). ${STAGES[$i]} - ${STAGE_NAMES[$i]}"
    done
}

# 主函数
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        run)
            cmd_run "$@"
            ;;
        status)
            cmd_status
            ;;
        reset)
            cmd_reset
            ;;
        list)
            cmd_list
            ;;
        help|--help|-h)
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
