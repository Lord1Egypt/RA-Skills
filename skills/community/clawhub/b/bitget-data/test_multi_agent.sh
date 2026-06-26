#!/bin/bash
# Bitget 多 Agent 测试脚本

echo "======================================"
echo "🤖 Bitget 多 Agent 系统测试"
echo "======================================"
echo ""

cd /Users/zongzi/.openclaw/workspace/bitget_data

# 测试 1: 网格监控 Agent
echo "1️⃣  测试网格监控 Agent..."
node multi_agent_controller.js monitor 2>&1 | head -30
echo ""

# 测试 2: 技术分析 Agent
echo "2️⃣  测试技术分析 Agent..."
node multi_agent_controller.js analysis 2>&1 | head -30
echo ""

# 测试 3: 网格优化 Agent
echo "3️⃣  测试网格优化 Agent..."
node multi_agent_controller.js optimizer 2>&1 | head -20
echo ""

# 测试 4: 日报 Agent
echo "4️⃣  测试日报 Agent..."
node multi_agent_controller.js report 2>&1 | head -30
echo ""

echo "======================================"
echo "✅ 多 Agent 测试完成！"
echo "======================================"
