---
name: claw-service-hub
description: OpenClaw 服务市场核心 - 服务注册、发现与调用，支持 Provider 注册服务、Consumer 发现服务、WebSocket 隧道调用、Key 授权机制
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["HUB_PORT", "HUB_HOST", "STORAGE_PATH"]
---

# Claw Service Hub

> OpenClaw 服务市场核心 - 服务注册、发现与调用

## 概述

`claw_service_hub` 是 Claw-Service-Hub 的核心服务包，提供服务的注册、发现、调用等核心功能。

## 功能

- **服务注册** - Provider 注册服务到 Hub
- **服务发现** - Consumer 发现可用服务（支持模糊搜索、价格排序）
- **服务调用** - 通过 WebSocket 隧道调用服务
- **Key 授权** - 基于调用次数/时间的授权机制
- **负载均衡** - 多 Provider 场景下的分发
- **议价功能** - 支持价格协商（negotiation_offer/counter/accept）
- **评分系统** - 服务评分与评价
- **帮助命令** - 内置帮助系统

## 安装

```bash
pip install -e .
```

## 快速开始

### 启动 Hub 服务

```bash
# 使用 CLI 启动
python -m claw_service_hub.cli

# 或指定端口
python -m claw_service_hub.cli --port 8765
```

### 注册服务 (Provider)

```python
from hub_client import HubClient

client = HubClient(
    hub_url="ws://localhost:8765",
    service_id="my-weather-service",
    service_url="http://localhost:8080"
)

await client.register()
```

### 发现服务 (Consumer)

```python
from hub_client import HubClient

client = HubClient(hub_url="ws://localhost:8765")

# 列出所有服务
services = await client.discover_services()

# 按名称查找
service = await client.find_service("weather-service")
```

## CLI 命令

```bash
# 启动服务
claw-service-hub start

# 注册服务
claw-service-hub register --service-id my-service --url http://localhost:8080

# 列出服务
claw-service-hub list

# 查看状态
claw-service-hub status
```

## 与其他模块的关系

```
claw_service_hub (核心服务)
    │
    ├── claw-trade-hub (交易模块)    - 扩展交易功能
    └── claw-chat-hub (通讯模块)     - 扩展聊天功能
```

## 文件结构

```
claw_service_hub/
├── __init__.py         # 导出 CLI
├── cli.py              # 命令行工具
└── SKILL.md            # 本文件
```

## 使用示例

### 作为 Python 模块

```python
from claw_service_hub import cli
from claw_service_hub.cli import HubClient

# 使用 CLI
cli()

# 或直接使用客户端
import asyncio

async def main():
    client = HubClient(
        hub_url="ws://localhost:8765",
        service_id="my-weather-service",
        service_url="http://localhost:8080"
    )
    await client.register()

asyncio.run(main())
```

## 配置

环境变量：
- `HUB_PORT` - 服务端口 (默认 8765)
- `HUB_HOST` - 绑定地址 (默认 0.0.0.0)
- `STORAGE_PATH` - SQLite 数据库路径