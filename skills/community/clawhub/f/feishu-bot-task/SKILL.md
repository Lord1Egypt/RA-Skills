---
name: feishu-bot-task
version: 1.0.0
description: "飞书任务（Bot身份）：使用Bot/应用身份管理飞书任务，创建任务、查询任务列表、更新状态、分配成员等。本Skill专门使用v1 API，Bot身份可直接调用，解决了lark-task官方Skill使用v2接口无法支持Bot身份的问题。当需要以Bot身份（应用身份）操作任务时使用本Skill。"
metadata:
  requires:
    bins: ["python3"]
    env: ["FEISHU_APP_ID", "FEISHU_APP_SECRET"]
  openclaw:
    homepage: "https://github.com/lixiang92229/feishu-bot-task"
---

# feishu-task (Bot身份)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、身份选择和权限处理规则。**

> **与 lark-task 的区别**：lark-task 使用 v2 接口，只支持用户身份。feishu-task 使用 v1 接口，支持 Bot 身份。

> **适用场景**：Agent 以 Bot/应用身份（如项目经理Agent）派发和管理任务时使用。

## 背景

飞书官方 lark-cli 的 `task tasks list` 命令使用 v2 接口，该接口不支持 Bot 身份调用（会报错 `Invalid access token`）。

本 Skill 直接调用飞书 v1 API (`GET /task/v1/tasks`)，Bot 身份可以正常使用，可查询 Bot 自己作为负责人的任务列表。

## Shortcuts

- [`+bot-get-my-tasks`](./references/lark-task-bot-get-my-tasks.md) — Bot查询自己负责的任务列表（使用v1 API）

## API Resources

所有操作通过 Python 脚本调用 v1 API，不依赖 lark-cli：

| 操作 | 脚本 |
|------|------|
| 查询Bot任务列表 | `scripts/lark-task-bot-list.py` |

## 权限说明

- Bot 身份只需在飞书开放平台开通对应权限（`task:task:read` / `task:task:write`）
- 无需用户授权（`auth login`）
- 凭证从环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 读取

## 注意事项

- 所有脚本均读取 OpenClaw 飞书插件注入的环境变量，无需手动配置
- v1 API 与 v2 API 返回的数据格式略有差异，解析时注意字段名称（如 v1 用 `creator_id`，v2 用 `creator.id`）
