#!/bin/bash
# 测试服务器连接和环境

SSH_KEY="$HOME/.ssh/server_deploy"
SERVER_HOST="192.168.1.168"
SERVER_USER="root"
SERVER_PORT="22"

echo "========================================"
echo "  服务器连接测试"
echo "========================================"
echo ""

# 测试 SSH 连接
echo "📌 测试 SSH 连接..."
if ssh -i "$SSH_KEY" -p "$SERVER_PORT" -o ConnectTimeout=5 "$SERVER_USER@$SERVER_HOST" "echo 成功" 2>/dev/null; then
    echo "✅ SSH 连接正常"
else
    echo "❌ SSH 连接失败"
    exit 1
fi

echo ""
echo "📌 检查系统环境..."

# 检查各项环境
ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" << 'EOF'
echo ""
echo "=== 系统信息 ==="
cat /etc/os-release | grep PRETTY_NAME
uname -r

echo ""
echo "=== Node.js ==="
if command -v node &> /dev/null; then
    echo "✓ Node.js: $(node -v)"
    echo "✓ npm: $(npm -v)"
else
    echo "✗ Node.js: 未安装"
fi

echo ""
echo "=== Java ==="
if command -v java &> /dev/null; then
    echo "✓ Java: $(java -version 2>&1 | head -1)"
else
    echo "✗ Java: 未安装"
fi

echo ""
echo "=== Maven ==="
if command -v mvn &> /dev/null; then
    echo "✓ Maven: $(mvn -v 2>&1 | head -1)"
else
    echo "✗ Maven: 未安装"
fi

echo ""
echo "=== PM2 ==="
if command -v pm2 &> /dev/null; then
    echo "✓ PM2: $(pm2 -v)"
    pm2 list
else
    echo "✗ PM2: 未安装"
fi

echo ""
echo "=== 目录检查 ==="
if [ -d "/www/wwwroot" ]; then
    echo "✓ /www/wwwroot 存在"
    ls -la /www/wwwroot
else
    echo "✗ /www/wwwroot 不存在"
fi

echo ""
echo "=== 磁盘空间 ==="
df -h / | tail -1
EOF

echo ""
echo "========================================"
echo "  测试完成"
echo "========================================"
echo ""
echo "📝 下一步："
echo ""
echo "如果 Node.js/Maven/PM2 未安装，请在服务器上运行："
echo "  bash /tmp/install-server-env.sh"
echo ""
echo "然后选择选项 1) 全部安装"
echo ""
