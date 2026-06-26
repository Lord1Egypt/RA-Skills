#!/bin/bash

# Android Stack Analyzer - 快速检查脚本
# 用于快速获取当前页面和页面栈信息

echo "==================================="
echo "  Android Stack Analyzer - 快速检查"
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

echo "✅ 设备已连接"
echo ""

# 获取当前页面
echo "📍 当前最上层页面："
adb shell "dumpsys window | grep mCurrentFocus" 2>/dev/null || echo "❌ 无法获取当前页面"
echo ""

# 获取页面栈
echo "📋 页面栈信息："
adb shell "dumpsys activity activities | grep -E 'Hist|ResumedActivity'" 2>/dev/null || echo "❌ 无法获取页面栈"
echo ""

# 获取最近任务
echo "🕐 最近任务："
adb shell "dumpsys activity recents" 2>/dev/null | head -10 || echo "❌ 无法获取最近任务"
echo ""

echo "==================================="
echo "检查完成"