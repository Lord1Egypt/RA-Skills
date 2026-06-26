#!/bin/bash

# Android Stack Analyzer - Linux/macOS快速启动脚本
# 一键检查ADB环境并运行快速检查

echo "==================================="
echo "  Android Stack Analyzer - 快速启动"
echo "==================================="
echo ""

# 检查ADB是否可用
if ! command -v adb &> /dev/null; then
    echo "❌ ADB 未找到，请先运行INSTALL.md中的安装步骤"
    echo ""
    echo "请按以下步骤安装："
    echo "1. 下载Android SDK Platform Tools"
    echo "2. 解压到 ~/AndroidSDK/platform-tools"
    echo "3. 添加到PATH环境变量"
    echo ""
    read -p "按回车键继续..."
    exit 1
fi

echo "✅ ADB 已安装"
echo ""

# 检查设备是否连接
if ! adb devices | grep -q "device$"; then
    echo "❌ 未检测到已连接的Android设备"
    echo ""
    echo "请按以下步骤连接设备："
    echo "1. 开启手机的开发者选项和USB调试"
    echo "2. 使用USB连接手机到电脑"
    echo "3. 在手机上授权电脑连接"
    echo ""
    read -p "按回车键继续..."
    exit 1
fi

echo "✅ 设备已连接"
echo ""

# 运行快速检查
echo "🔄 开始快速检查..."
echo ""
if [ -f "$(dirname "$0")/examples/cross-platform-check.sh" ]; then
    bash "$(dirname "$0")/examples/cross-platform-check.sh"
else
    echo "❌ 找不到快速检查脚本"
    exit 1
fi

echo ""
echo "==================================="
echo "快速检查完成！"
echo ""
echo "如需实时监控，请运行："
echo "$(dirname "$0")/examples/cross-platform-monitor.sh"
echo ""
read -p "按回车键继续..."