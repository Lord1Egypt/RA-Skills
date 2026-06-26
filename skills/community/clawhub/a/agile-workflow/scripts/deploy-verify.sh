#!/bin/bash
# 生产部署验证脚本

echo "========================================="
echo "  多 Agent 架构优化 - 部署验证"
echo "========================================="
echo ""

cd /home/ubutu/.openclaw/workspace/skills/agile-workflow/core

# 检查核心模块
echo "📦 检查核心模块..."
modules=(
  "context-router.js"
  "prompt-cache.js"
  "message-bus.js"
  "memory-manager.js"
  "llm-gateway.js"
  "integration-adapter.js"
  "cache-backend.js"
  "agile-workflow-engine-v7.js"
  "monitoring-alert-system.js"
  "performance-tuner.js"
)

for module in "${modules[@]}"; do
  if [ -f "$module" ]; then
    size=$(stat -c%s "$module")
    echo "  ✅ $module ($size bytes)"
  else
    echo "  ❌ $module 缺失"
  fi
done

echo ""
echo "🧪 运行引擎健康检查..."
node agile-workflow-engine-v7.js health 2>&1 | head -10

echo ""
echo "✅ 部署验证完成！"
echo ""
echo "📋 下一步:"
echo "  1. 安装 Redis: bash scripts/install-redis.sh (需手动创建)"
echo "  2. 性能调优：node performance-tuner.js recommend"
echo "  3. 启动引擎：node agile-workflow-engine-v7.js start"