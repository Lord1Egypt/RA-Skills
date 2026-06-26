#!/bin/bash
# ACE-Step 1.5 Docker 一键部署脚本 for Mac Mini M2
# 完全隔离，不影响系统 Python

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🐳 ACE-Step 1.5 Docker 部署程序"
echo "================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "${RED}错误: Docker 未安装${NC}"
    echo "请先安装 Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "${RED}错误: Docker 服务未运行${NC}"
    echo "请启动 Docker Desktop"
    exit 1
fi

echo "✅ Docker 检查通过"

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "${YELLOW}警告: Docker Compose 未找到${NC}"
    echo "将使用 docker compose (Docker Desktop 内置)"
fi

# 设置目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${INSTALL_DIR:-$HOME/workspace/ace-step-docker}"

echo ""
echo "📁 安装目录: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 复制文件
echo "📋 复制配置文件..."
cp "$SCRIPT_DIR/Dockerfile" .
cp "$SCRIPT_DIR/docker-compose.yml" .

# 创建启动脚本
cat > start.sh << 'EOF'
#!/bin/bash
# 启动 ACE-Step Docker

echo "🚀 启动 ACE-Step Docker..."

# 检查容器是否已在运行
if docker ps | grep -q ace-step-server; then
    echo "ACE-Step 已在运行！"
    echo ""
    echo "访问地址:"
    echo "  - Web UI: http://localhost:7860"
    echo "  - API:    http://localhost:8000"
    exit 0
fi

# 启动服务
docker-compose up -d --build

echo ""
echo "✅ ACE-Step 启动成功！"
echo ""
echo "访问地址:"
echo "  - Web UI: http://localhost:7860"
echo "  - API:    http://localhost:8000"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
EOF

chmod +x start.sh

# 创建停止脚本
cat > stop.sh << 'EOF'
#!/bin/bash
# 停止 ACE-Step Docker

echo "🛑 停止 ACE-Step Docker..."
docker-compose down
echo "✅ 已停止"
EOF

chmod +x stop.sh

# 创建 API 测试脚本
cat > test-api.sh << 'EOF'
#!/bin/bash
# 测试 ACE-Step API

echo "🧪 测试 ACE-Step API..."

# 等待服务启动
echo "等待服务启动 (10秒)..."
sleep 10

# 测试生成
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A peaceful piano melody",
    "duration": 10,
    "temperature": 0.8
  }' \
  -o test-output.json

if [ -f test-output.json ]; then
    echo "✅ API 测试成功！"
    cat test-output.json
else
    echo "❌ API 测试失败"
fi
EOF

chmod +x test-api.sh

# 创建一键生成脚本
cat > generate.sh << 'EOF'
#!/bin/bash
# 使用 ACE-Step 生成音乐

if [ $# -lt 1 ]; then
    echo "用法: ./generate.sh \"你的音乐描述\" [时长秒数]"
    echo "示例: ./generate.sh \"Upbeat electronic music\" 30"
    exit 1
fi

PROMPT="$1"
DURATION="${2:-30}"
OUTPUT_FILE="$HOME/Music/ACE-Step/generated_$(date +%s).wav"

mkdir -p "$HOME/Music/ACE-Step"

echo "🎵 生成音乐..."
echo "描述: $PROMPT"
echo "时长: ${DURATION}s"

# 在容器中生成
docker exec ace-step-server python cli.py \
  --prompt "$PROMPT" \
  --duration "$DURATION" \
  --output "/app/output/$(basename $OUTPUT_FILE)"

# 复制到主机
if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ 生成成功！"
    echo "文件: $OUTPUT_FILE"
else
    echo "❌ 生成失败"
fi
EOF

chmod +x generate.sh

# 创建卸载脚本
cat > uninstall.sh << 'EOF'
#!/bin/bash
# 卸载 ACE-Step Docker

echo "🗑️  卸载 ACE-Step Docker..."
read -p "确定要删除所有数据吗？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down -v
    docker rmi ace-step-m2:latest 2>/dev/null || true
    echo "✅ 卸载完成"
else
    echo "取消卸载"
fi
EOF

chmod +x uninstall.sh

echo ""
echo "${GREEN}✅ Docker 部署准备完成！${NC}"
echo ""
echo "📋 可用命令:"
echo "  ./start.sh      - 启动 ACE-Step"
echo "  ./stop.sh       - 停止 ACE-Step"
echo "  ./generate.sh   - 生成音乐"
echo "  ./test-api.sh   - 测试 API"
echo "  ./uninstall.sh  - 完全卸载"
echo ""
echo "🚀 现在启动吗？(Y/n)"
read -r -n 1
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    ./start.sh
fi
