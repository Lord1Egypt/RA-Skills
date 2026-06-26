#!/bin/bash
# Edict 启动脚本

CONFIG_FILE="${1:-~/.edict/config/default.yaml}"

echo "🏛️ 启动 Edict 三省六部制系统..."
echo "📋 配置文件: $CONFIG_FILE"

# 检查配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    echo "请先运行安装脚本: ./scripts/install.sh"
    exit 1
fi

# 检查依赖
python3 -c "import yaml" 2>/dev/null || {
    echo "📦 安装依赖..."
    pip install -q pyyaml requests flask
}

# 启动服务
echo "🚀 启动服务..."
python3 << 'PYTHON_SCRIPT'
import sys
import os
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/edict'))

from edict import EdictSystem

print("✓ 初始化 Edict 系统...")
edict = EdictSystem()

print("✓ 启动治理体系...")
edict.launch_governance(
    dashboard=True,
    audit=True,
    auto_scale=True
)

print("\n🎉 Edict 系统已启动！")
print("📊 仪表板: http://localhost:8080")
print("📝 日志: ~/.edict/logs/")
print("\n按 Ctrl+C 停止服务")

# 保持运行
try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 正在停止服务...")
    edict.shutdown()
    print("✓ 服务已停止")
PYTHON_SCRIPT
