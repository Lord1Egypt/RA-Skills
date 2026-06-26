#!/bin/bash

# Android Stack Analyzer - 实时页面监控脚本
# 用于监控页面切换和Activity变化

echo "==================================="
echo "  Android Stack Analyzer - 实时监控"
echo "==================================="
echo ""

# 检查ADB是否可用
if ! command -v adb &> /dev/null; then
    echo "❌ ADB 未找到，请确保已安装Android SDK"
    exit 1
fi

# 检查设备是否连接
if ! adb devices | grep -q "device$"; then
    echo "❌ 未检测到已连接的Android设备"
    exit 1
fi

echo "🔄 开始实时监控页面切换..."
echo "按 Ctrl+C 停止监控"
echo ""

# 实时监控当前页面
adb shell "while true; do echo \"[\$(date '+%H:%M:%S')] \$(dumpsys window | grep mCurrentFocus)\"; sleep 1; done"