# feishu-bot-task

[English](#english) | [中文](#中文)

---

## English

### Overview

`feishu-bot-task` is an OpenClaw Skill that enables Bot/Application identity operations on Feishu (Lark) Tasks.

This Skill solves a critical limitation: Feishu's official `lark-task` Skill uses the v2 API (`GET /task/v2/tasks`), which **does not support Bot identity** and will fail with `Invalid access token`. This Skill uses the v1 API (`GET /task/v1/tasks`) which **fully supports Bot identity**.

### Why This Exists

| Approach | API Version | Bot Identity | User Identity |
|----------|-------------|-------------|---------------|
| Official `lark-task` | v2 | ❌ Not supported | ✅ Supported |
| `feishu-bot-task` | v1 | ✅ Fully supported | ❌ Not needed |

### Features

- **List Bot Tasks**: Query all tasks where the Bot is the assignee
- **Bot-native**: No user login required — uses `tenant_access_token` directly
- **Pagination**: Automatically handles paginated results
- **v1 API compatible**: Works around v2 API limitations

### Requirements

- Python 3
- Environment variables:
  - `FEISHU_APP_ID` — Feishu application ID
  - `FEISHU_APP_SECRET` — Feishu application secret

These are automatically injected by the OpenClaw Feishu plugin.

### Usage

```bash
python3 skills/feishu-bot-task/scripts/lark-task-bot-list.py
```

Output (JSON):
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": "task_guid",
        "summary": "Task Title",
        "due": {"time": "1234567890", "is_all_day": true},
        "members": [...],
        "create_time": "...",
        "complete_time": "..."
      }
    ],
    "total": 10
  }
}
```

### File Structure

```
feishu-bot-task/
├── SKILL.md                                    # OpenClaw Skill definition
├── README.md                                   # This file
├── _meta.json                                  # ClawHub metadata
├── references/
│   └── lark-task-bot-get-my-tasks.md          # Command reference
└── scripts/
    └── lark-task-bot-list.py                  # Main script
```

### Installation

```bash
# From ClawHub
npx clawhub install feishu-bot-task

# Or from GitHub
npx skills add https://github.com/lixiang92229/feishu-bot-task -y -g
```

### Permissions

In Feishu Open Platform, grant these scopes to your application:

- `task:task:read` — Read task information
- `task:task:write` — Create/update tasks

No user login (`auth login`) is required.

---

## 中文

### 概述

`feishu-bot-task` 是一个 OpenClaw Skill，支持以 Bot/应用身份操作飞书任务。

### 为什么需要这个 Skill

飞书官方的 `lark-task` 使用 v2 API（`GET /task/v2/tasks`），该接口**不支持 Bot 身份**，会报错 `Invalid access token`。本 Skill 使用 v1 API（`GET /task/v1/tasks`），**完全支持 Bot 身份**。

### 功能

- **查询 Bot 负责的任务**：列出 Bot 作为负责人的所有任务
- **Bot 原生**：无需用户登录，直接使用 `tenant_access_token`
- **自动分页**：自动处理分页，获取完整结果

### 环境要求

- Python 3
- 环境变量（OpenClaw 飞书插件自动注入）：
  - `FEISHU_APP_ID` — 飞书应用 ID
  - `FEISHU_APP_SECRET` — 飞书应用密钥

### 使用方法

```bash
python3 skills/feishu-bot-task/scripts/lark-task-bot-list.py
```

### 权限配置

在飞书开放平台，为应用开通以下权限：

- `task:task:read` — 查看任务信息
- `task:task:write` — 创建和更新任务

无需进行用户授权（`auth login`）。

### 安装

```bash
# 从 ClawHub 安装
npx clawhub install feishu-bot-task

# 或从 GitHub 安装
npx skills add https://github.com/lixiang92229/feishu-bot-task -y -g
```

### 文件结构

```
feishu-bot-task/
├── SKILL.md                                    # OpenClaw Skill 定义
├── README.md                                   # 双语文档
├── _meta.json                                  # ClawHub 元数据
├── references/
│   └── lark-task-bot-get-my-tasks.md          # 命令参考文档
└── scripts/
    └── lark-task-bot-list.py                  # 主脚本
```

### 适用场景

- Agent 作为"包工头"角色，向其他 Agent 分发任务
- 主 Agent 查询各子 Agent 的任务进度
- 定时巡检 Bot 自己负责的任务完成状态
