#!/bin/bash
# Edict 安装脚本

set -e

echo "🏛️ 安装 Edict 三省六部制多智能体编排系统..."

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本: $python_version"

# 安装依赖
echo "📦 安装依赖..."
pip install -q pyyaml requests flask prometheus-client 2>/dev/null || pip install -q --break-system-packages pyyaml requests flask prometheus-client 2>/dev/null || echo "⚠️ 依赖安装跳过，请手动安装: pip install pyyaml requests flask prometheus-client"

# 创建配置目录
mkdir -p ~/.edict/config
mkdir -p ~/.edict/logs
mkdir -p ~/.edict/data

# 复制默认配置
cat > ~/.edict/config/default.yaml << 'EOF'
# Edict 默认配置
system:
  name: "Edict Multi-Agent System"
  version: "1.0.0"
  log_level: "INFO"

dashboard:
  enabled: true
  host: "0.0.0.0"
  port: 8080
  refresh_interval: 5

audit:
  enabled: true
  storage: "database"
  retention_days: 2555  # 7年
  encryption: true

agents:
  zhongshu:
    enabled: true
    model: "gpt-4"
  menxia:
    enabled: true
    model: "gpt-4"
  shangshu:
    enabled: true
    model: "gpt-4"
  libu:
    enabled: true
    model: "gpt-3.5-turbo"
  hubu:
    enabled: true
    model: "gpt-3.5-turbo"
  libu_rites:
    enabled: true
    model: "gpt-3.5-turbo"
  bingbu:
    enabled: true
    model: "gpt-4"
  xingbu:
    enabled: true
    model: "gpt-4"
  gongbu:
    enabled: true
    model: "gpt-4"

models:
  default: "gpt-4"
  fallback: "gpt-3.5-turbo"
  routing_strategy: "smart"

resources:
  max_agents: 100
  max_concurrent_tasks: 50
  auto_scale: true
EOF

echo "✓ 默认配置已创建"

# 创建启动脚本
cat > ~/.edict/start.sh << 'EOF'
#!/bin/bash
cd ~/.edict
python3 -m edict.server --config ~/.edict/config/default.yaml
EOF
chmod +x ~/.edict/start.sh

echo "✓ 启动脚本已创建"

echo ""
echo "🎉 Edict 安装完成！"
echo ""
echo "使用方法:"
echo "  1. 启动服务: ~/.edict/start.sh"
echo "  2. 访问仪表板: http://localhost:8080"
echo "  3. 查看文档: skillhub docs edict"
echo ""
