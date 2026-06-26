# Docker 部署指南

在容器中运行 OpenClaw Agent。

## 快速开始

```dockerfile
FROM node:22-slim

# 安装 OpenClaw
RUN npm install -g openclaw

# 创建工作目录
WORKDIR /app

# 复制导出的 agent
COPY agent-export/ /app/agent/

# 恢复 agent
RUN cd /app/agent && ./restore.sh /root/.openclaw

# 暴露 Gateway 端口
EXPOSE 18789

# 启动
CMD ["openclaw", "gateway", "start"]
```

## 构建和运行

```bash
# 构建
docker build -t my-agent .

# 运行
docker run -d \
  -p 18789:18789 \
  -v agent-data:/root/.openclaw \
  --name my-agent \
  my-agent
```

## Docker Compose

```yaml
version: '3.8'
services:
  agent:
    build: .
    ports:
      - "18789:18789"
    volumes:
      - agent-data:/root/.openclaw
      - ./workspace:/root/.openclaw/workspace:rw
    environment:
      - OPENCLAW_GATEWAY_TOKEN=${GATEWAY_TOKEN}
    restart: unless-stopped

volumes:
  agent-data:
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENCLAW_GATEWAY_TOKEN` | Gateway 认证令牌 |
| `OPENCLAW_MODEL_API_KEY` | AI 模型 API 密钥 |
| `OPENCLAW_LOG_LEVEL` | 日志级别 (debug/info/warn) |

## 数据持久化

必须持久化的目录：
- `/root/.openclaw/workspace` - Agent 核心文件
- `/root/.openclaw/openclaw.json` - 配置文件

可选持久化：
- `/root/.openclaw/agents` - Session 历史
- `/root/.openclaw/backups` - 备份文件
