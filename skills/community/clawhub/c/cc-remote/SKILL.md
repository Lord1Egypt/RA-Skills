---
name: cc-remote
description: Claude Code 远程执行 Skill — 通过三通道（FastAPI/Redis/Screen）向远程机器上的 Claude Code 派发指令，支持重试机制。触发：博士让我"派发给 Claude Code"、"远程执行"、"让XX机器执行Claude Code"、remote cc。
---

# cc-remote

通过三通道向远程机器上的 Claude Code 派发指令，支持重试机制。

## 部署架构

```
我 (NAS/OpenClaw)
    │
    ├─→ FastAPI:18900 ──→ Worker 监听 Redis ──→ Claude Code 执行
    │       ↑
    │    HTTP POST
    │
    └─→ Redis LPUSH ──→ Worker BLPOP ──→ Claude Code 执行
            ↑
        直接写队列
```

远程机器需要运行：
- **FastAPI 服务**（端口 18900）
- **Redis Worker**（监听 Redis 队列）
- **Redis**（可连的队列服务）

## 首次部署（远程机器）

在远程机器上运行：

```bash
# 安装依赖
pip3 install redis uvicorn fastapi

# 启动 Worker（后台常驻）
nohup python3 cc_worker.py > worker.log 2>&1 &

# 启动 API
nohup python3 cc_api.py > api.log 2>&1 &
```

## 三通道（按优先级）

| 通道 | 原理 | 稳定性 |
|------|------|--------|
| **fastapi** | HTTP POST 到远程 API，Worker 执行 | ⭐⭐⭐ 最稳定 |
| **redis** | 直接 LPUSH 到 Redis 队列 | ⭐⭐ |
| **screen** | SSH Screen 后台执行 | ⭐ fallback |

## 重试机制

- 每个通道最多 **3 次重试**
- 失败后等待 **5~7 秒随机**
- 三通道全失败 → 返回错误

## 配置修改

首次使用前，编辑 `scripts/exec.py` 顶部配置：

```python
M1_HOST = "远程机器IP"        # 如 "192.168.0.128"
M1_API_PORT = 18900           # FastAPI 端口
REDIS_HOST = "Redis服务器IP"  # 如 "192.168.0.107"
REDIS_PORT = 11980            # Redis 端口
```

## 使用方式

```bash
python3 scripts/exec.py "你的指令"
```

### 参数

| 参数 | 说明 |
|------|------|
| `prompt` | 要执行的指令（必须） |
| `--task-id` | 指定任务ID |
| `--timeout` | 超时秒数（默认300） |
| `--channel` | 强制指定通道（fastapi/redis/screen） |

### 示例

```bash
# 基本用法（自动选择通道）
python3 scripts/exec.py "say hello"

# 强制用 fastapi
python3 scripts/exec.py "say hello" --channel fastapi

# 指定任务ID，方便查结果
python3 scripts/exec.py "修改 index.html" --task-id fix001
```

## 远程机器进程管理

```bash
# 查看进程
ssh 远程机器 "ps aux | grep cc_"

# 重启 Worker
ssh 远程机器 "pkill -f cc_worker; nohup python3 ~/cc_worker.py > ~/worker.log 2>&1 &"

# 重启 API
ssh 远程机器 "pkill -f cc_api; nohup python3 ~/cc_api.py > ~/api.log 2>&1 &"
```

## 故障排查

**任务提交成功但没结果**：
1. 查远程机器 Worker 日志：`ssh 远程机器 "tail worker.log"`
2. 查 API 状态：`curl http://远程机器IP:18900/health`
3. 查 Redis 队列：`redis-cli -h Redis服务器 -p 端口 LLEN claude_tasks`

**FastAPI 连不上**：
- 检查远程机器 API 是否在跑
- 重启 API

**Worker 不处理队列**：
- 检查 worker 是否在跑
- 重启 worker

## 指令构造技巧

发给 Claude Code 的指令要清晰：
- 说明要改哪个文件
- 说明改什么
- 说明期望效果
- 复杂任务加"逐步思考"

**好例子**：
```
修改 /path/to/project/web/index.html：

1. 找到 body 样式部分
2. 添加背景色：background: #f5f5f5
3. 确保在移动端也生效（响应式）

注意：先备份原文件。
```

## 文件说明

| 文件 | 功能 |
|------|------|
| `exec.py` | 三通道执行器（核心） |
| `deploy_m1.py` | 远程机器一键部署脚本 |
| `deploy_ssh.py` | SSH 强化配置（连接池复用） |
