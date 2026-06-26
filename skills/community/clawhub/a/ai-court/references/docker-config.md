# Docker 镜像配置指南

## 镜像信息

- **镜像名称**: `boluobobo/ai-court:latest`
- **GitHub**: https://github.com/wanikua/danghuangshang
- **Dockerfile**: https://github.com/wanikua/danghuangshang/blob/main/Dockerfile

---

## 快速开始

### 默认模式（独立运行）

```bash
docker run -d \
  --name ai-court \
  -p 127.0.0.1:18789:18789 \
  -p 127.0.0.1:18795:18795 \
  -v ai-court-config:/home/court/.openclaw \
  -v ai-court-workspace:/home/court/clawd \
  boluobobo/ai-court:latest
```

---

## 连接外部 OpenClaw

如果本地已有 OpenClaw 服务，可以使用外部模式（只运行 GUI，不启动内部 Gateway）：

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ENABLE_EXTERNAL_CLAW` | 启用外部 OpenClaw 模式 | `false` |
| `OPENCLAW_HOST` | 外部 OpenClaw 地址 | `host.docker.internal` |
| `OPENCLAW_PORT` | 外部 OpenClaw 端口 | `18789` |
| `OPENCLAW_API_TOKEN` | API 认证 Token（可选） | - |

### Docker CLI 示例

```bash
docker run -d \
  --name ai-court-external \
  -p 127.0.0.1:18796:18795 \
  -e ENABLE_EXTERNAL_CLAW=true \
  -e OPENCLAW_HOST=host.docker.internal \
  -e OPENCLAW_PORT=18789 \
  --add-host=host.docker.internal:host-gateway \
  boluobobo/ai-court:latest
```

### Docker Compose 示例

```yaml
version: '3.8'

services:
  ai-court:
    image: boluobobo/ai-court:latest
    container_name: ai-court-external
    ports:
      - "127.0.0.1:18796:18795"
    environment:
      - ENABLE_EXTERNAL_CLAW=true
      - OPENCLAW_HOST=host.docker.internal
      - OPENCLAW_PORT=18789
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

---

## 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 18789 | OpenClaw Gateway | 内部 Gateway（外部模式下不启动） |
| 18795 | 菠萝王朝 GUI | Web 管理界面 |

---

## 数据持久化

```yaml
volumes:
  - court-config:/home/court/.openclaw    # 配置文件
  - court-workspace:/home/court/clawd     # 工作空间
```

---

## 完整文档

详见：https://github.com/wanikua/danghuangshang/blob/main/EXTERNAL_CLAW.md
