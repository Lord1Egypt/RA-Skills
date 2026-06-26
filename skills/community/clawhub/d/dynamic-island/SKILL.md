---
name: dynamic-island
slug: dynamic-island
version: 1.0.0
description: macOS Dynamic Island desktop widget for OpenClaw. Real-time multi-agent status monitoring with frosted glass pill UI. Shows 5 states: idle, alert, thinking, done, error. Hover to expand agent list with recent messages. Triggers: "dynamic island", "灵动岛", "桌面小组件", "agent状态", "启动灵动岛", "打开灵动岛"
homepage: https://github.com/zhixiangshon-cell/openclaw-dynamic-island
metadata:
  openclaw:
    homepage: https://github.com/zhixiangshon-cell/openclaw-dynamic-island
---

# OpenClaw Dynamic Island

macOS Dynamic Island 风格的多 Agent 状态监控桌面小组件。

## 功能

- 毛玻璃药丸窗口，悬浮在屏幕顶部
- 5种状态自动切换：待命、收到消息、思考中、搞定了、出错了
- emolog 可爱图标
- 多 Agent 同时管理，鼠标悬停展开查看
- 每个 Agent 显示最近 2 条对话消息
- 光标跟随高亮 Agent
- 点击 Agent 跳转飞书聊天
- 任务完成晃动 + 音效提示

## 安装

一键安装（检查环境 + 编译 widget + 创建配置）：

```bash
cd ~/.openclaw/skills/dynamic-island
bash setup.sh
```

安装脚本会自动：
- 检查 macOS、Swift、Python3 环境
- 安装 websockets 依赖
- 编译 Swift widget
- 创建 config.json 配置文件

## 启动

```bash
./start.sh
```

## 停止

```bash
./start.sh stop
```

## 配置

复制 `config.example.json` 为 `config.json`：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "agents_dir": "~/.openclaw/agents",
  "http_port": 7788,
  "ws_port": 7789,
  "agent_names": {
    "my-agent-id": "My Bot"
  },
  "agent_links": {
    "my-agent-id": "lark://applink.feishu.cn/client/chat/open?openId=xxx"
  }
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `agents_dir` | OpenClaw agents 目录路径 | `~/.openclaw/agents` |
| `http_port` | HTTP 服务端口 | `7788` |
| `ws_port` | WebSocket 端口 | `7789` |
| `agent_names` | Agent ID → 显示名映射 | `{}` |
| `agent_links` | Agent ID → 飞书聊天链接（可点击跳转） | `{}` |

## 架构

```
setup.sh        — 一键安装脚本（环境检查 + 编译 + 配置）
start.sh        — 启动/停止脚本
server.py       — 监控 agent 会话 JSONL 文件，通过 WebSocket 推送事件
index.html      — 渲染 emolog 图标 + 多 Agent UI
widget.swift    — macOS 原生药丸窗口（NSPanel + 毛玻璃 + hover 检测）
emolog/         — emolog 自定义图标
config.json     — 本地配置（git-ignored）
```

## 使用场景

当你需要：
- 同时监控多个 OpenClaw Agent 的工作状态
- 在桌面上实时看到 Agent 的思考、执行、完成过程
- 通过飞书聊天链接快速跳转到对应 Agent

就说"启动灵动岛"或"打开 dynamic island"来激活此技能。
