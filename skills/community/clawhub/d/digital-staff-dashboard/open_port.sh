#!/bin/bash
# 开放 Dashboard 端口给局域网访问

PORT=5181
LAN_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K\S+')

echo "=========================================="
echo "  Dashboard 端口开放工具"
echo "=========================================="
echo "本机局域网 IP: $LAN_IP"
echo "端口号: $PORT"
echo ""

# 检查服务器是否运行
if ! ss -tlnp | grep -q ":$PORT"; then
    echo "❌ 警告: 端口 $PORT 没有服务在监听"
    echo "   请先启动 dashboard_server.py"
    exit 1
fi

echo "✅ 服务正在监听端口 $PORT"

# 检查防火墙并开放端口
if command -v ufw &> /dev/null; then
    echo ""
    echo "检测到 ufw 防火墙，正在开放端口..."
    sudo ufw allow from 192.168.0.0/16 to any port $PORT comment 'Dashboard LAN access'
    sudo ufw reload
    echo "✅ ufw 规则已添加"
fi

# 同时添加到 iptables
echo ""
echo "添加 iptables 规则..."
sudo iptables -C INPUT -p tcp --dport $PORT -j ACCEPT 2>/dev/null || {
    sudo iptables -I INPUT -p tcp --dport $PORT -j ACCEPT
    echo "✅ iptables 规则已添加"
}

echo ""
echo "=========================================="
echo "  配置完成！"
echo "=========================================="
echo ""
echo "局域网访问地址:"
echo "  → http://$LAN_IP:$PORT"
echo ""
echo "测试命令（在其他终端执行）:"
echo "  curl http://$LAN_IP:$PORT/api/config"
echo ""
