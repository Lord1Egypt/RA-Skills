#!/bin/bash
#
# 编译验证脚本
# 检查项目是否能在DevEco中编译通过
#

set -e

PROJECT_DIR="${1:-.}"
VERBOSE=false

# 解析参数
if [ "$2" = "--verbose" ]; then
    VERBOSE=true
fi

echo "🔨 HarmonyOS 编译验证"
echo "======================"
echo "项目目录: $PROJECT_DIR"
echo ""

# 检查项目结构
echo "📁 检查项目结构..."
if [ ! -f "$PROJECT_DIR/entry/build-profile.json5" ]; then
    echo "❌ 错误: 未找到 entry/build-profile.json5"
    echo "   请确保在正确的HarmonyOS项目目录中运行此脚本"
    exit 1
fi
echo "✅ 项目结构检查通过"
echo ""

# 检查DevEco环境
echo "🔍 检查DevEco环境..."
if command -v devecoc &> /dev/null; then
    echo "✅ DevEco CLI 已安装"
    HAS_CLI=true
else
    echo "⚠️  DevEco CLI 未安装，将使用手动检查"
    HAS_CLI=false
fi
echo ""

# TypeScript类型检查
echo "📋 运行TypeScript类型检查..."
if [ -f "$PROJECT_DIR/package.json" ]; then
    if [ -d "$PROJECT_DIR/node_modules" ]; then
        cd "$PROJECT_DIR"
        if npm run lint 2>/dev/null; then
            echo "✅ TypeScript检查通过"
        else
            echo "⚠️  TypeScript检查发现问题（非阻塞）"
        fi
    else
        echo "⚠️  未找到node_modules，跳过TypeScript检查"
    fi
else
    echo "⚠️  未找到package.json，跳过TypeScript检查"
fi
echo ""

# 使用DevEco CLI编译（如果可用）
if [ "$HAS_CLI" = true ]; then
    echo "🏗️  使用DevEco CLI编译..."
    if devecoc build --project "$PROJECT_DIR/entry" 2>&1 | tee /tmp/build.log; then
        echo "✅ DevEco编译通过"
    else
        echo "❌ DevEco编译失败"
        if [ "$VERBOSE" = true ]; then
            echo ""
            echo "详细错误日志:"
            cat /tmp/build.log
        fi
        exit 1
    fi
else
    # 手动检查关键文件
    echo "🔍 手动检查关键文件..."

    # 检查ets文件语法
    ETS_FILES=$(find "$PROJECT_DIR/entry/src" -name "*.ets" 2>/dev/null | head -5)
    if [ -z "$ETS_FILES" ]; then
        echo "⚠️  未找到.ets文件"
    else
        echo "✅ 找到 $(find "$PROJECT_DIR/entry/src" -name "*.ets" | wc -l) 个.ets文件"
    fi

    # 检查关键配置文件
    CRITICAL_FILES=(
        "entry/build-profile.json5"
        "entry/hvigorfile.ts"
        "entry/src/main/module.json5"
    )

    for file in "${CRITICAL_FILES[@]}"; do
        if [ -f "$PROJECT_DIR/$file" ]; then
            echo "✅ $file 存在"
        else
            echo "❌ $file 缺失"
        fi
    done

    echo ""
    echo "⚠️  未安装DevEco CLI，无法自动编译"
    echo "   请手动在DevEco Studio中打开项目并编译"
fi

echo ""
echo "======================"
echo "✅ 编译验证完成"
echo ""
echo "下一步建议:"
echo "  1. 在DevEco Studio中打开项目"
echo "  2. 连接模拟器或真机"
echo "  3. 点击 Run → Run 'entry'"
echo "  4. 检查控制台是否有运行时错误"
