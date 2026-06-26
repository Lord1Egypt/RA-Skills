---
name: external-receiver
description: >
  通用外部数据接收 Skill。
  在服务器上启动 HTTP 服务，接收外部文件上传和消息，
  自动将内容推送到 OpenClaw 用户会话。
  支持：文件上传、文本消息、Webhook JSON、curl / wget 客户端。
---

# External Receiver

> 从外部接收文件 / 消息 → 推送到 OpenClaw 会话

## 功能

- 🌐 启动 HTTP 服务器（监听端口）
- 📁 接收文件上传（multipart/form-data）
- 💬 接收文本/JSON 消息
- → 自动转发到 OpenClaw 当前会话

## 快速使用

```bash
clawhub install external-receiver
cd skills/external-receiver
bash scripts/start.sh                    # 启动接收服务
```

## 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 服务状态页 |
| GET | `/health` | 健康检查 |
| POST | `/upload` | 上传文件 |
| POST | `/message` | 发送文本消息 |
| POST | `/webhook` | 接收 JSON Webhook |
| GET | `/download/<filename>` | 下载已接收文件 |

---

## API 详情

### 上传文件

```bash
curl -X POST http://你的服务器:8080/upload \
  -F "file=@/path/to/file.txt"
```

响应：
```json
{
  "ok": true,
  "filename": "file.txt",
  "size": 12345,
  "path": "/home/user/.openclaw/workspace/received/file.txt"
}
```

### 发送文本消息

```bash
curl -X POST http://你的服务器:8080/message \
  -d "text=Hello from outside!"
```

或 JSON：
```bash
curl -X POST http://你的服务器:8080/webhook \
  -H "Content-Type: application/json" \
  -d '{"text": "Webhook message", "from": "external-system"}'
```

### OpenClaw 收到推送后自动显示

```
📥 收到外部消息:
Hello from outside!

📎 收到文件:
file.txt (12KB)
路径: /home/user/.openclaw/workspace/received/file.txt
```

## 配置

```bash
# 环境变量
export RECEIVER_PORT=8080                    # 监听端口（默认 8080）
export RECEIVER_HOST=0.0.0.0               # 监听地址（默认 0.0.0.0）
export RECEIVER_DIR=/home/user/received     # 文件存储目录
export RECEIVER_SECRET=your_secret_key      # 访问密钥（可选）
```

## 安全建议

- ✅ 生产环境务必设置 `RECEIVER_SECRET` 并在请求时附带
- ✅ 使用防火墙限制只开放 8080 端口给信任的 IP
- ✅ 定期清理 `received/` 目录中的文件

## Python 调用示例

```python
import requests

# 发送消息
requests.post("http://服务器:8080/message", data={"text": "警报：价格突破"})

# 上传文件
with open("report.pdf", "rb") as f:
    requests.post("http://服务器:8080/upload", files={"file": f})

# Webhook 方式
requests.post("http://服务器:8080/webhook", json={
    "event": "trade",
    "symbol": "BTC/USDT",
    "side": "buy",
    "amount": 0.01
})
```
