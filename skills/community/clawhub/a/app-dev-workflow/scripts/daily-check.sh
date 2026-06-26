#!/bin/bash
#
# 每日检查脚本
# 用法: bash scripts/daily-check.sh [day1|day2|day3]
#

DAY="${1:-all}"

echo "📅 豆因项目 - Day $DAY 检查"
echo "=============================="
echo ""

# Day 1 检查
if [ "$DAY" = "day1" ] || [ "$DAY" = "all" ]; then
    echo "🔨 Day 1 检查清单"
    echo "------------------"

    # 编译检查
    if [ -d "entry/build" ]; then
        echo "✅ DevEco项目可编译"
    else
        echo "❌ DevEco项目未编译"
    fi

    # DIY核心算法检查
    if [ -f "entry/src/main/ets/services/DIYCoffeeService.ts" ]; then
        if grep -q "analyzeFlavorFingerprint" entry/src/main/ets/services/DIYCoffeeService.ts; then
            echo "✅ 口味指纹算法已实现"
        else
            echo "❌ 口味指纹算法未实现"
        fi
    else
        echo "❌ DIYCoffeeService不存在"
    fi

    # 简化版检查
    if grep -q "simplified\|简化" entry/src/main/ets/services/DIYCoffeeService.ts 2>/dev/null; then
        echo "ℹ️  使用简化版实现"
    fi

    echo ""
fi

# Day 2 检查
if [ "$DAY" = "day2" ] || [ "$DAY" = "all" ]; then
    echo "🤖 Day 2 检查清单"
    echo "------------------"

    # Agent检查
    if [ -f "entry/src/main/ets/agent/CoffeeAgent.ts" ]; then
        echo "✅ Agent文件存在"
        if grep -q "process\|handle" entry/src/main/ets/agent/CoffeeAgent.ts; then
            echo "✅ Agent有响应方法"
        fi
    else
        echo "❌ Agent文件不存在"
    fi

    # DIY页面检查
    if [ -f "entry/src/main/ets/pages/DIYPage.ets" ]; then
        echo "✅ DIYPage存在"
        STEP_COUNT=$(grep -c "buildStep" entry/src/main/ets/pages/DIYPage.ets 2>/dev/null || echo "0")
        if [ "$STEP_COUNT" -ge 4 ]; then
            echo "✅ DIYPage有4步骤"
        else
            echo "⚠️  DIYPage步骤可能不完整 ($STEP_COUNT)"
        fi
    else
        echo "❌ DIYPage不存在"
    fi

    # Mock数据检查
    if [ -f "entry/src/main/ets/mocks/coffeeShops.mock.ts" ]; then
        echo "✅ Mock数据已准备"
    else
        echo "❌ Mock数据未准备"
    fi

    echo ""
fi

# Day 3 检查
if [ "$DAY" = "day3" ] || [ "$DAY" = "all" ]; then
    echo "🎬 Day 3 检查清单"
    echo "------------------"

    # 应用运行检查
    if [ -f "entry/build/outputs/default/entry-default-signed.hap" ]; then
        echo "✅ HAP包已生成"
    else
        echo "❌ HAP包未生成"
    fi

    # 核心流程检查
    echo "🧪 核心流程检查:"
    echo "  [ ] DIY表单可填写"
    echo "  [ ] 口味指纹能生成"
    echo "  [ ] 匹配结果可展示"
    echo "  [ ] 导航功能可用"

    # Demo数据检查
    DEMO_RECORDS=$(find entry/src/main/ets -name "*.ets" -exec grep -l "mock\|demo\|示例" {} \; 2>/dev/null | wc -l)
    if [ "$DEMO_RECORDS" -gt 0 ]; then
        echo "✅ 有Demo数据 ($DEMO_RECORDS 个文件)"
    fi

    # 视频脚本检查
    echo ""
    echo "🎥 演示准备:"
    echo "  [ ] 视频脚本已准备"
    echo "  [ ] Plan B方案已测试"
    echo "  [ ] 3分钟演示流程已演练"

    echo ""
fi

echo "=============================="
echo "✅ Day $DAY 检查完成"
echo ""
echo "💡 提示: 发现问题请及时修复，必要时启用Fallback方案"
