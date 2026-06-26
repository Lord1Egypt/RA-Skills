# Agent Manager - OpenClaw Agent 管理工具

自主添加、管理、对话 OpenClaw Agent 的轻量级工具。

## 功能

- ✅ 添加新 Agent（配置工作区、飞书配对）
- ✅ 查看所有已注册 Agent
- ✅ 与 Agent 直接对话
- ✅ 删除/停用 Agent
- ✅ 查看 Agent 状态

## 快速开始

```bash
# 1. 安装依赖
cd ~/.openclaw/workspace/agent-manager
npm install

# 2. 启动服务
node server.js

# 3. 访问界面
# Web 界面：http://localhost:3000
# CLI 模式：node cli.js
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/agents` | 获取所有 Agent 列表 |
| POST | `/api/agents` | 添加新 Agent |
| GET | `/api/agents/:id` | 获取单个 Agent 详情 |
| POST | `/api/agents/:id/chat` | 与 Agent 对话 |
| DELETE | `/api/agents/:id` | 删除 Agent |
| POST | `/api/agents/:id/pair` | 生成飞书配对码 |

## 配置

编辑 `config.json`:
```json
{
  "openclawGateway": "http://127.0.0.1:18789",
  "openclawToken": "ZZitPPb3LZmDH2c_jYl9Xbub2NO1CrqntpGgF-LBEGM",
  "port": 3000
}
```
