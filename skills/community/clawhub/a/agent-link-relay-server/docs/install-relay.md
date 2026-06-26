# 中转服务器安装说明

## 前置要求

- Python 3.7+
- 公网服务器（有固定 IP 或域名）
- 防火墙开放相应端口（默认 8765）

## 快速安装

### 1. 上传文件

将以下文件上传到服务器：

```
skills/agent-link/scripts/relay-server/
├── relay_server.py
└── relay-config.example.json
```

### 2. 安装依赖

```bash
pip install websockets
```

### 3. 配置

复制配置示例文件：

```bash
cp relay-config.example.json relay-config.json
```

编辑 `relay-config.json`：

```json
{
  "port": 8765,
  "secret": "your-strong-secret-key-here",
  "registered_instances": [
    {
      "instance_id": "instance-001",
      "name": "晨辉的 MacBook",
      "public_key": ""
    }
  ]
}
```

**重要配置项说明：**

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `port` | 监听端口 | 是 |
| `secret` | 共享密钥（所有 agent 使用相同的密钥） | 是 |
| `registered_instances` | 预注册的 OpenClaw 实例列表 | 否 |

### 4. 启动服务器

#### 前台运行（测试用）

```bash
python3 relay_server.py --config relay-config.json
```

#### 后台运行（生产用）

使用 systemd 服务（推荐）：

创建 `/etc/systemd/system/agent-link-relay.service`：

```ini
[Unit]
Description=Agent Link Relay Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/agent-link/relay-server
ExecStart=/usr/bin/python3 /path/to/agent-link/relay-server/relay_server.py --config relay-config.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable agent-link-relay
sudo systemctl start agent-link-relay
```

查看状态：

```bash
sudo systemctl status agent-link-relay
sudo journalctl -u agent-link-relay -f
```

### 5. 防火墙配置

开放端口（以 ufw 为例）：

```bash
sudo ufw allow 8765/tcp
```

或者使用 iptables：

```bash
sudo iptables -A INPUT -p tcp --dport 8765 -j ACCEPT
```

### 6. 测试连接

在本地 agent 机器上测试：

```bash
python3 agent_link.py --config agent-link-config.json --test
```

## 安全建议

1. **密钥安全**
   - 使用强密钥（至少 32 字符）
   - 定期更换密钥
   - 不要将密钥提交到版本控制

2. **网络安全**
   - 使用 WSS (WebSocket Secure) 而非 WS
   - 配置防火墙只允许可信 IP 访问
   - 考虑使用 VPN 或内网穿透

3. **访问控制**
   - 只注册需要的实例
   - 定期清理不再使用的实例注册
   - 监控连接日志

## 故障排除

### 服务器无法启动

- 检查端口是否被占用：`netstat -tulpn | grep 8765`
- 检查防火墙设置
- 查看日志文件

### Agent 无法连接

- 检查服务器地址和端口是否正确
- 检查网络连接
- 检查密钥是否匹配
- 查看服务器日志

### 消息发送失败

- 检查目标实例是否在线
- 检查消息签名
- 查看服务器和客户端日志

## 管理命令

### 查看已连接实例

服务器日志中会显示连接和断开事件。

### 优雅关闭

```bash
sudo systemctl stop agent-link-relay
```

或者发送 SIGINT 信号（Ctrl+C）。

## 更新日志

- **1.0.0** (2026-04-04)
  - 初始版本
  - 支持实例注册和验证
  - 支持消息签名验证
  - 支持消息转发
