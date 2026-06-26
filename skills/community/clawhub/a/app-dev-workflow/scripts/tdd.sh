#!/bin/bash
#
# TDD (测试驱动开发) 流程脚本
# 支持: 生成测试 -> 红阶段(失败) -> 绿阶段(实现) -> 重构 循环
#
# 用法: bash scripts/tdd.sh <命令> [选项]
#   start <Service> <Method>    开始TDD流程
#   run                         运行测试
#   impl                        标记实现完成，进入重构阶段
#   refactor                    运行重构检查
#   status                      查看TDD状态
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_DIR="${PROJECT_DIR:-.}"
TDD_STATE_FILE=".tdd-state"

# 打印函数
info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

# 显示Banner
show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     🔄 TDD - 测试驱动开发流程                    ║"
    echo "║     Red → Green → Refactor                       ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 保存TDD状态
save_state() {
    local service="$1"
    local method="$2"
    local phase="$3"  # red/green/refactor
    local test_file="$4"
    local impl_file="$5"

    cat > "$TDD_STATE_FILE" << EOF
{
  "service": "$service",
  "method": "$method",
  "phase": "$phase",
  "testFile": "$test_file",
  "implFile": "$impl_file",
  "startTime": $(date +%s),
  "lastUpdate": $(date +%s)
}
EOF
}

# 读取TDD状态
load_state() {
    if [ -f "$TDD_STATE_FILE" ]; then
        cat "$TDD_STATE_FILE"
    else
        echo "{}"
    fi
}

# 清除状态
clear_state() {
    rm -f "$TDD_STATE_FILE"
}

# 获取当前阶段
get_phase() {
    load_state | grep -o '"phase": "[^"]*"' | cut -d'"' -f4
}

# 生成测试文件
generate_test() {
    local service="$1"
    local method="$2"

    step "生成测试文件"

    local test_file="test/${service}.${method}.test.ts"
    local case_file="templates/test-cases/${method}.cases.json"

    # 检查测试用例文件
    if [ ! -f "$case_file" ]; then
        warn "测试用例文件不存在: $case_file"
        warn "将生成基础测试框架"
        use_cases=false
    else
        use_cases=true
        info "找到测试用例: $case_file"
    fi

    mkdir -p test

    # 生成测试文件
    cat > "$test_file" << EOF
/**
 * TDD测试: ${service}.${method}
 * 生成时间: $(date)
 */

import { ${service} } from '../src/services/${service}';
import { $(echo $method | sed 's/^./\u&/')TestCases } from './test-cases/${method}.cases';

describe('${service}.${method}', () => {
  let service: ${service};

  beforeEach(() => {
    service = ${service}.getInstance();
    service.init();
  });

  afterEach(() => {
    service.destroyInstance();
  });

EOF

    if [ "$use_cases" = true ]; then
        # 从JSON生成测试用例
        local cases=$(cat "$case_file" | grep -o '"id": "[^"]*"' | cut -d'"' -f4)

        for case_id in $cases; do
            local case_name=$(cat "$case_file" | grep -A1 "\"id\": \"$case_id\"" | grep '"name":' | cut -d'"' -f4)
            local priority=$(cat "$case_file" | grep -A5 "\"id\": \"$case_id\"" | grep '"priority":' | cut -d'"' -f4)

            cat >> "$test_file" << EOF
  /**
   * 测试用例: $case_id
   * 描述: $case_name
   * 优先级: $priority
   */
  test('${case_id}: $case_name', async () => {
    // TODO: 实现测试
    // 参考: implementation-guides.md
    throw new Error('TDD Red Phase - 测试待实现');
  });

EOF
        done
    else
        # 生成基础测试
        cat >> "$test_file" << EOF
  /**
   * TDD Step 1: 编写失败测试
   * 参考: implementation-guides.md 中的测试示例
   */
  test('${method} should return correct result', async () => {
    // Arrange
    const input = {}; // TODO: 准备测试数据

    // Act
    const result = await service.${method}(input);

    // Assert
    expect(result).toBeDefined();
    // TODO: 添加更多断言
    throw new Error('TDD Red Phase - 请先实现业务逻辑');
  });

EOF
    fi

    cat >> "$test_file" << EOF
});
EOF

    success "测试文件生成: $test_file"
    echo "$test_file"
}

# 生成最小实现
generate_minimal_impl() {
    local service="$1"
    local method="$2"

    step "生成最小实现"

    local impl_file="src/services/${service}.ts"
    local guide_ref=""

    # 查找实现指南引用
    case "$method" in
        analyzeFlavorFingerprint)
            guide_ref="implementation-guides.md#指南1口味指纹算法"
            ;;
        calculateSimilarity)
            guide_ref="implementation-guides.md#指南2相似度匹配算法"
            ;;
        *)
            guide_ref="implementation-guides.md"
            ;;
    esac

    info "最小实现模式: 返回硬编码值让测试通过"
    info "参考: $guide_ref"

    # 提示用户手动实现
    cat << EOF

${YELLOW}═══════════════════════════════════════════════════${NC}
${YELLOW}  📝 TDD Green Phase - 实现提示${NC}
${YELLOW}═══════════════════════════════════════════════════${NC}

请修改: ${impl_file}

方法: ${method}

实现策略:
1. 先返回硬编码的正确结果 (让测试变绿)
2. 逐步添加真实逻辑
3. 保持测试通过

参考代码:
  ${guide_ref}

完成后运行: bash scripts/tdd.sh run
${YELLOW}═══════════════════════════════════════════════════${NC}

EOF
}

# 运行测试
cmd_run() {
    local phase=$(get_phase)

    if [ -z "$phase" ]; then
        error "未启动TDD流程"
        info "请先运行: bash scripts/tdd.sh start <Service> <Method>"
        return 1
    fi

    step "运行测试 (当前阶段: $phase)"

    local state=$(load_state)
    local service=$(echo "$state" | grep -o '"service": "[^"]*"' | cut -d'"' -f4)
    local method=$(echo "$state" | grep -o '"method": "[^"]*"' | cut -d'"' -f4)
    local test_file=$(echo "$state" | grep -o '"testFile": "[^"]*"' | cut -d'"' -f4)

    info "测试: ${service}.${method}"

    # 运行测试
    if [ -f "package.json" ] && grep -q "test" package.json; then
        npm test -- "$test_file" 2>&1 | tee /tmp/tdd-test.log || true
    else
        warn "未配置测试运行器"
        info "请手动运行测试: $test_file"
    fi

    # 分析结果
    if grep -q "FAIL\|failed" /tmp/tdd-test.log 2>/dev/null; then
        echo ""
        warn "测试失败 - Red Phase ✅"
        info "接下来: 实现业务逻辑使测试通过"
        info "运行: bash scripts/tdd.sh impl"
    elif grep -q "PASS\|passed" /tmp/tdd-test.log 2>/dev/null; then
        echo ""
        success "测试通过 - Green Phase ✅"

        if [ "$phase" = "red" ]; then
            warn "首次通过！标记为Green Phase"
            save_state "$service" "$method" "green" "$test_file" "src/services/${service}.ts"
        fi

        info "接下来: 重构代码"
        info "运行: bash scripts/tdd.sh refactor"
    else
        warn "无法确定测试结果"
    fi
}

# 开始TDD流程
cmd_start() {
    local service="${1:-}"
    local method="${2:-}"

    if [ -z "$service" ] || [ -z "$method" ]; then
        error "缺少参数"
        info "用法: bash scripts/tdd.sh start <Service> <Method>"
        info "示例: bash scripts/tdd.sh start DIYCoffeeService analyzeFlavorFingerprint"
        return 1
    fi

    show_banner

    step "启动TDD流程: ${service}.${method}"

    # 生成测试文件
    local test_file=$(generate_test "$service" "$method")

    # 保存状态
    save_state "$service" "$method" "red" "$test_file" "src/services/${service}.ts"

    # 显示下一步
    cat << EOF

${GREEN}═══════════════════════════════════════════════════${NC}
${GREEN}  🎯 TDD流程已启动${NC}
${GREEN}═══════════════════════════════════════════════════${NC}

当前阶段: 🔴 Red Phase (编写失败测试)

下一步:
1. 查看生成的测试文件: ${test_file}
2. 完善测试用例
3. 运行测试确认失败: bash scripts/tdd.sh run
4. 开始实现: bash scripts/tdd.sh impl

${GREEN}═══════════════════════════════════════════════════${NC}

EOF
}

# 标记实现阶段
cmd_impl() {
    local phase=$(get_phase)

    if [ "$phase" != "red" ]; then
        error "当前不是Red Phase，无法开始实现"
        info "请先运行: bash scripts/tdd.sh start"
        return 1
    fi

    local state=$(load_state)
    local service=$(echo "$state" | grep -o '"service": "[^"]*"' | cut -d'"' -f4)
    local method=$(echo "$state" | grep -o '"method": "[^"]*"' | cut -d'"' -f4)

    show_banner
    step "进入实现阶段: ${service}.${method}"

    generate_minimal_impl "$service" "$method"
}

# 重构检查
cmd_refactor() {
    local phase=$(get_phase)

    if [ "$phase" != "green" ]; then
        error "当前不是Green Phase，无法重构"
        info "请先让测试通过: bash scripts/tdd.sh run"
        return 1
    fi

    show_banner
    step "重构阶段"

    local state=$(load_state)
    local service=$(echo "$state" | grep -o '"service": "[^"]*"' | cut -d'"' -f4)
    local impl_file=$(echo "$state" | grep -o '"implFile": "[^"]*"' | cut -d'"' -f4)

    info "检查重构机会..."

    # 运行规范检查
    if [ -f "scripts/lint.sh" ]; then
        bash scripts/lint.sh "$impl_file" || true
    fi

    # 检查复杂度
    local lines=$(wc -l < "$impl_file")
    if [ "$lines" -gt 200 ]; then
        warn "文件行数较多 ($lines)，考虑拆分"
    fi

    cat << EOF

${CYAN}═══════════════════════════════════════════════════${NC}
${CYAN}  🔧 重构检查清单${NC}
${CYAN}═══════════════════════════════════════════════════${NC}

代码质量:
  [ ] 消除重复代码
  [ ] 优化命名
  [ ] 简化复杂逻辑
  [ ] 提取公共函数

设计原则:
  [ ] 单一职责
  [ ] 开闭原则
  [ ] 避免过度设计

测试保持:
  [ ] 重构后测试仍通过
  [ ] 不添加新功能

完成后运行: bash scripts/tdd.sh run
${CYAN}═══════════════════════════════════════════════════${NC}

EOF
}

# 查看状态
cmd_status() {
    show_banner

    local state=$(load_state)

    if [ "$state" = "{}" ]; then
        info "未启动TDD流程"
        info "运行: bash scripts/tdd.sh start <Service> <Method>"
        return 0
    fi

    local service=$(echo "$state" | grep -o '"service": "[^"]*"' | cut -d'"' -f4)
    local method=$(echo "$state" | grep -o '"method": "[^"]*"' | cut -d'"' -f4)
    local phase=$(echo "$state" | grep -o '"phase": "[^"]*"' | cut -d'"' -f4)
    local test_file=$(echo "$state" | grep -o '"testFile": "[^"]*"' | cut -d'"' -f4)
    local start_time=$(echo "$state" | grep -o '"startTime": [0-9]*' | grep -o '[0-9]*')
    local elapsed=$(( $(date +%s) - start_time ))

    echo "当前TDD状态:"
    echo "============"
    echo "Service: $service"
    echo "Method:  $method"
    echo "Test:    $test_file"
    echo "耗时:    ${elapsed}秒"
    echo ""

    case "$phase" in
        red)
            echo -e "阶段: ${RED}🔴 Red Phase${NC}"
            echo "任务: 编写失败测试"
            echo "下一步: bash scripts/tdd.sh impl"
            ;;
        green)
            echo -e "阶段: ${GREEN}🟢 Green Phase${NC}"
            echo "任务: 测试通过，准备重构"
            echo "下一步: bash scripts/tdd.sh refactor"
            ;;
        refactor)
            echo -e "阶段: ${YELLOW}🟡 Refactor Phase${NC}"
            echo "任务: 重构代码"
            echo "下一步: bash scripts/tdd.sh run"
            ;;
    esac
}

# 帮助
cmd_help() {
    show_banner
    echo "TDD (测试驱动开发) 流程脚本"
    echo ""
    echo "用法: bash scripts/tdd.sh <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  start <Service> <Method>  启动TDD流程"
    echo "  run                       运行测试"
    echo "  impl                      进入实现阶段"
    echo "  refactor                  重构检查"
    echo "  status                    查看当前状态"
    echo "  help                      显示帮助"
    echo ""
    echo "示例:"
    echo "  bash scripts/tdd.sh start DIYCoffeeService analyzeFlavorFingerprint"
    echo "  bash scripts/tdd.sh run"
    echo "  bash scripts/tdd.sh impl"
    echo ""
    echo "流程:"
    echo "  1. start -> 生成测试文件 (Red Phase)"
    echo "  2. run   -> 确认测试失败"
    echo "  3. impl  -> 实现最小代码"
    echo "  4. run   -> 确认测试通过 (Green Phase)"
    echo "  5. refactor -> 重构优化"
    echo "  6. run   -> 确认测试仍通过"
    echo ""
}

# 主程序
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        start)
            cmd_start "$@"
            ;;
        run)
            cmd_run
            ;;
        impl)
            cmd_impl
            ;;
        refactor)
            cmd_refactor
            ;;
        status)
            cmd_status
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            error "未知命令: $cmd"
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
