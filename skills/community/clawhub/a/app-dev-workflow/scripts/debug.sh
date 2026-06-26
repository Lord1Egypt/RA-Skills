#!/bin/bash
#
# 调试诊断工具
# 用法: bash scripts/debug.sh [logs|state|perf|analyze|help]
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目目录
PROJECT_DIR="${1:-.}"
shift || true

# 命令
COMMAND="${1:-help}"

# 帮助信息
show_help() {
    echo "🔧 豆因DeveloperSkill - 调试诊断工具"
    echo "======================================"
    echo ""
    echo "用法: bash scripts/debug.sh [项目目录] <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  logs [数量]       查看应用日志 (默认50条)"
    echo "  state             检查Service和状态"
    echo "  perf              性能热点分析"
    echo "  analyze           全面分析诊断"
    echo "  guide <Service>   显示Service实现指南"
    echo "  check             快速健康检查"
    echo "  help              显示此帮助"
    echo ""
    echo "示例:"
    echo "  bash scripts/debug.sh . logs 100"
    echo "  bash scripts/debug.sh . state"
    echo "  bash scripts/debug.sh . guide DIYCoffeeService"
    echo ""
}

# 检查hdc连接
check_hdc() {
    if ! command -v hdc &> /dev/null; then
        echo -e "${YELLOW}⚠️  hdc 命令未找到${NC}"
        echo "   请确保HarmonyOS SDK已正确安装"
        echo "   hdc 通常在: ~/HarmonyOS/sdk/版本/toolchains"
        return 1
    fi

    if ! hdc list targets 2>/dev/null | grep -q "device"; then
        echo -e "${YELLOW}⚠️  未找到连接的设备${NC}"
        echo "   请连接模拟器或真机"
        return 1
    fi

    return 0
}

# 查看日志
cmd_logs() {
    local lines="${1:-50}"

    echo "📋 查看应用日志 (最近 $lines 条)"
    echo "================================"
    echo ""

    if check_hdc; then
        echo "🔍 过滤关键词: Coffee, DIY, Error, Warn"
        echo ""

        hdc hilog | grep -E "Coffee|DIY|Error|Warn|Agent|Skill" | tail -n "$lines" || true

        echo ""
        echo "📊 错误统计:"
        hdc hilog | grep -c "E/Coffee" 2>/dev/null || echo "0"
    else
        # 本地日志文件分析
        if [ -f "entry/build/outputs/entry.log" ]; then
            tail -n "$lines" entry/build/outputs/entry.log
        else
            echo -e "${YELLOW}⚠️  未找到日志文件${NC}"
            echo "   请确保应用已运行或在DevEco中查看"
        fi
    fi
}

# 检查状态
cmd_state() {
    echo "🔍 Service状态检查"
    echo "=================="
    echo ""

    # 检查项目结构
    echo "📁 项目结构:"
    if [ -d "entry/src/main/ets/services" ]; then
        SERVICE_COUNT=$(find entry/src/main/ets/services -name "*Service.ts" | wc -l)
        echo -e "  ${GREEN}✅${NC} 找到 $SERVICE_COUNT 个Service"
        find entry/src/main/ets/services -name "*Service.ts" -exec basename {} \; | sed 's/^/     - /'
    else
        echo -e "  ${RED}❌${NC} Service目录不存在"
    fi
    echo ""

    # 检查关键文件初始化状态
    echo "🔧 关键组件:"

    # 检查DIYCoffeeService是否有核心方法
    if [ -f "entry/src/main/ets/services/DIYCoffeeService.ts" ]; then
        if grep -q "analyzeFlavorFingerprint" entry/src/main/ets/services/DIYCoffeeService.ts; then
            echo -e "  ${GREEN}✅${NC} DIYCoffeeService - analyzeFlavorFingerprint 已定义"
        else
            echo -e "  ${YELLOW}⚠️${NC}  DIYCoffeeService - analyzeFlavorFingerprint 未实现"
            echo "     💡 参考: implementation-guides.md 指南1"
        fi

        if grep -q "calculateSimilarity" entry/src/main/ets/services/DIYCoffeeService.ts; then
            echo -e "  ${GREEN}✅${NC} DIYCoffeeService - calculateSimilarity 已定义"
        else
            echo -e "  ${YELLOW}⚠️${NC}  DIYCoffeeService - calculateSimilarity 未实现"
        fi
    fi

    # 检查Agent
    if [ -f "entry/src/main/ets/agent/CoffeeAgent.ts" ]; then
        if grep -q "process\|handleIntent" entry/src/main/ets/agent/CoffeeAgent.ts; then
            echo -e "  ${GREEN}✅${NC} CoffeeAgent - 已定义响应方法"
        else
            echo -e "  ${YELLOW}⚠️${NC}  CoffeeAgent - 响应方法未定义"
        fi
    fi

    # 检查Mock数据
    if [ -f "entry/src/main/ets/mocks/coffeeShops.mock.ts" ]; then
        SHOP_COUNT=$(grep -c "mock_shanghai" entry/src/main/ets/mocks/coffeeShops.mock.ts 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✅${NC} Mock咖啡店数据 - $SHOP_COUNT 家"
    else
        echo -e "  ${RED}❌${NC} Mock数据未创建"
        echo "     💡 运行: bash scripts/generate.sh mock MapSkill"
    fi

    echo ""

    # DevMode状态
    echo "🎮 开发模式:"
    if grep -r "DevMode.enable()" entry/src/main/ets/ 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️${NC}  DevMode可能在代码中被启用"
    else
        echo -e "  ${GREEN}✅${NC} DevMode未硬编码启用"
    fi
}

# 性能分析
cmd_perf() {
    echo "📊 性能热点分析"
    echo "==============="
    echo ""

    # 代码量统计
    echo "📝 代码统计:"
    if [ -d "entry/src/main/ets" ]; then
        ETS_FILES=$(find entry/src/main/ets -name "*.ets" | wc -l)
        TS_FILES=$(find entry/src/main/ets -name "*.ts" | wc -l)
        TOTAL_LINES=$(find entry/src/main/ets \( -name "*.ets" -o -name "*.ts" \) -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')

        echo "  - .ets 文件: $ETS_FILES"
        echo "  - .ts 文件: $TS_FILES"
        echo "  - 总行数: $TOTAL_LINES"
    fi
    echo ""

    # 潜在性能问题检查
    echo "⚠️  潜在性能问题:"

    # 检查大循环
    if grep -r "for.*await" entry/src/main/ets/ 2>/dev/null; then
        echo -e "  ${YELLOW}!${NC} 发现循环中使用await (PERF-001)"
    fi

    # 检查ForEach（应该用LazyForEach）
    FOREACH_COUNT=$(grep -r "ForEach" entry/src/main/ets/pages/ 2>/dev/null | wc -l)
    LAZY_COUNT=$(grep -r "LazyForEach" entry/src/main/ets/pages/ 2>/dev/null | wc -l)
    if [ "$FOREACH_COUNT" -gt 5 ] && [ "$LAZY_COUNT" -eq 0 ]; then
        echo -e "  ${YELLOW}!${NC} 大量使用ForEach，建议考虑LazyForEach优化"
    fi

    # 检查硬编码字符串
    HARDCODED=$(grep -r '"[^"]*coffee[^"]*"' entry/src/main/ets/ 2>/dev/null | grep -v "\$r(" | wc -l)
    if [ "$HARDCODED" -gt 0 ]; then
        echo -e "  ${YELLOW}!${NC} 发现 $HARDCODED 处可能硬编码的字符串"
    fi

    echo ""
    echo "💡 优化建议:"
    echo "  1. 大列表使用LazyForEach"
    echo "  2. 图片资源使用ImageCache"
    echo "  3. 避免在循环中使用await"
}

# 全面分析
cmd_analyze() {
    echo "🔬 全面诊断分析"
    echo "==============="
    echo ""

    # 执行所有检查
    cmd_state
    echo ""
    cmd_perf
    echo ""

    # 风险评级
    echo "🎯 风险评级"
    echo "==========="

    RISKS=()

    # 检查关键风险点
    if [ ! -f "entry/src/main/ets/services/DIYCoffeeService.ts" ]; then
        RISKS+=("🔴 DIYCoffeeService不存在 - 阻塞演示")
    fi

    if [ ! -f "entry/src/main/ets/mocks/coffeeShops.mock.ts" ]; then
        RISKS+=("🟡 Mock数据未准备 - API故障时无Fallback")
    fi

    if ! grep -q "FallbackService\|DevMode" entry/src/main/ets/services/*.ts 2>/dev/null; then
        RISKS+=("🟡 Fallback机制未集成 - 外部依赖风险")
    fi

    if [ ${#RISKS[@]} -eq 0 ]; then
        echo -e "${GREEN}✅ 未发现重大风险${NC}"
    else
        for risk in "${RISKS[@]}"; do
            echo "  $risk"
        done
    fi

    echo ""
    echo "📋 下一步建议:"
    echo "  1. 运行: bash scripts/build-check.sh (编译验证)"
    echo "  2. 运行: bash scripts/lint.sh (规范检查)"
    echo "  3. 运行: bash scripts/demo-checklist.sh (演示准备)"
}

# 显示指南
cmd_guide() {
    local service="${1:-DIYCoffeeService}"

    echo "📖 $service 实现指南"
    echo "===================="
    echo ""

    case "$service" in
        DIYCoffeeService)
            echo "📍 参考文件: references/implementation-guides.md"
            echo ""
            echo "关键方法实现顺序:"
            echo "  1. analyzeFlavorFingerprint() - 指南1.2 章节"
            echo "     └─ 输入: DIYCoffee对象"
            echo "     └─ 输出: FlavorFingerprint对象"
            echo "     └─ 关键: 12维向量构建、风格分类"
            echo ""
            echo "  2. calculateSimilarity() - 指南2.1 章节"
            echo "     └─ 输入: 两个FlavorFingerprint"
            echo "     └─ 输出: 相似度分数 (0-100)"
            echo "     └─ 关键: 加权欧氏距离"
            echo ""
            echo "  3. matchNearbyShops() - 指南1.3 章节"
            echo "     └─ 输入: DIY记录ID、位置、半径"
            echo "     └─ 输出: CoffeeShopMatch数组"
            echo "     └─ 关键: 调用MapSkill或Fallback"
            echo ""
            ;;
        CoffeeAgent)
            echo "📍 参考文件: references/implementation-guides.md"
            echo ""
            echo "关键方法实现顺序:"
            echo "  1. process() - 指南3 章节"
            echo "     └─ 简化版: 命令模式"
            echo "     └─ 完整版: ReAct循环"
            echo ""
            echo "  2. parseIntent() - 意图识别"
            echo "     └─ 关键词匹配 或 LLM识别"
            echo ""
            ;;
        MapSkill)
            echo "📍 参考文件: references/mock-and-fallback.md"
            echo ""
            echo "关键实现:"
            echo "  1. discoverNearby() - 发现附近咖啡店"
            echo "     └─ 真实API失败时调用FallbackService"
            echo ""
            echo "  2. getCurrentLocation() - 获取位置"
            echo "     └─ 权限拒绝时返回默认位置"
            echo ""
            ;;
        *)
            echo "❌ 未知的Service: $service"
            echo "   支持的Service: DIYCoffeeService, CoffeeAgent, MapSkill"
            ;;
    esac
}

# 快速健康检查
cmd_check() {
    echo "⚡ 快速健康检查"
    echo "==============="
    echo ""

    local issues=0

    # 快速检查关键点
    [ -f "entry/src/main/ets/services/DIYCoffeeService.ts" ] || ((issues++))
    [ -f "entry/src/main/ets/pages/DIYPage.ets" ] || ((issues++))
    [ -f "entry/build-profile.json5" ] || ((issues++))

    if [ $issues -eq 0 ]; then
        echo -e "${GREEN}✅ 快速检查通过${NC}"
        return 0
    else
        echo -e "${RED}❌ 发现 $issues 个问题${NC}"
        return 1
    fi
}

# 主程序
case "$COMMAND" in
    logs)
        cmd_logs "${2:-50}"
        ;;
    state)
        cmd_state
        ;;
    perf)
        cmd_perf
        ;;
    analyze)
        cmd_analyze
        ;;
    guide)
        cmd_guide "$2"
        ;;
    check)
        cmd_check
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $COMMAND${NC}"
        show_help
        exit 1
        ;;
esac
