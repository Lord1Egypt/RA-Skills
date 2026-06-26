---
name: feishu-task-workbench
description: 在单个 Feishu/OpenClaw 对话窗口中运行多任务工作台，让用户在一个窗口里完成任务新建、切换、继续、总结、关闭与归档，并通过 `sessions_spawn`、`sessions_send`、`sessions_history` 把每个任务路由到独立会话。**当用户发送“任务列表 / 新建任务 / 切到 #id / 总结 #id / 关闭 #id / 归档 #id / 继续 / 任务状态”时应优先使用此技能。** Feishu 与 Weixin 通道的任务 registry 必须相互独立，不互通。
---

# 飞书任务工作台

在一个 Feishu/OpenClaw 对话窗口中运行**单入口、多任务**工作台。

对用户只暴露任务概念：**新建**、**列表**、**切换**、**继续**、**总结**、**关闭**、**归档**。

任务状态以 `scripts/task_registry.py` 为唯一事实来源。

## 触发信号（强匹配）

当用户出现以下任一表达时，应优先激活本技能，而不是进入泛化问答澄清：

- `任务列表`
- `新建任务：...`
- `切到 #<id>` / `切换到 #<id>`
- `继续`（在任务上下文中）
- `总结 #<id>`
- `关闭 #<id>`
- `归档 #<id>`
- `任务状态`

同义英文命令（`task list`、`task new`、`task use` 等）同样适用。

## 强制能力门禁（必需）

如果缺少以下任一会话工具，本技能必须**阻断执行**：

- `sessions_spawn`
- `sessions_send`
- `sessions_history`

执行规则：

1. 在会话中的**第一次任务命令**时检查能力。
2. 如果缺任何工具，立即停止并返回阻断提示。
3. 阻断状态下不允许创建或更新任务 registry。
4. 明确提示如何修复主机配置（`tools.allow`、`agentToAgent`、`sessions.visibility`）。

禁止静默降级为 registry-only 模式。

## 主机配置提醒

要获得真实任务隔离，通常需要：

- agent allowlist 包含 `sessions_spawn`、`sessions_send`、`sessions_history`，通常还需要 `sessions_list`
- `tools.agentToAgent.enabled=true`
- `tools.sessions.visibility=all`

参考配置：

```json
{
  "tools": {
    "agentToAgent": { "enabled": true },
    "sessions": { "visibility": "all" }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "allow": [
            "sessions_spawn",
            "sessions_send",
            "sessions_history",
            "sessions_list"
          ]
        }
      }
    ]
  }
}
```

## 核心运行模型

- 一个用户可见的飞书聊天窗口
- 每个飞书账号+联系人对应一个任务 registry 文件
- 一个当前任务指针
- 每个任务对应一个独立会话
- 非全局命令默认路由到当前任务

除非用户明确要求查看实现细节，否则不要暴露 `sessionKey`。

## Registry 路径策略

使用“联系人隔离”路径：

```text
tasks/feishu/<account>/<peer>.json
```

规则：

- `<account>` 使用当前飞书账号 id
- `<peer>` 使用当前飞书用户 id（例如 `ou_xxx`），并做文件名安全化
- 不同 `account+peer` 严禁共享同一 registry 文件
- Feishu 与 Weixin 使用不同根目录，严禁共用同一 registry

首次使用先初始化：

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json init
```

## 标准命令

- `新建任务：<title>`
- `任务列表`
- `切到 #<id>`
- `继续`
- `总结 #<id>`
- `关闭 #<id>`
- `归档 #<id>`
- `任务状态`

可兼容英文等价命令（如 `task new`、`task list`、`task use`）。

## 控制面动作

### 1. 新建任务

1. 先执行能力门禁（仅首次任务命令）
2. 用 `sessions_spawn` 创建任务专属会话
3. 用 registry `add --session-key ... --make-current` 持久化任务
4. 回执任务 id 与当前任务

### 2. 查看任务列表

执行：

```bash
python3 scripts/task_registry.py --registry <path> list
```

返回精简列表，并标记当前任务。

### 3. 切换任务

执行：

```bash
python3 scripts/task_registry.py --registry <path> switch <id>
```

回执已切换目标。

### 4. 继续当前任务

1. 读取当前任务（`show`）
2. 使用 `sessions_send` 把消息路由到当前任务 `sessionKey`
3. 需要时将状态更新为 `in_progress`

若无当前任务，提示先新建或先查看列表。

### 5. 总结任务

1. 读取 registry（`summarize <id>`）
2. 需要时调用 `sessions_history` 补充上下文
3. 输出“进展/产出/阻塞/下一步”
4. 可选写回 `update --summary`

### 6. 关闭 / 归档任务

执行：

```bash
python3 scripts/task_registry.py --registry <path> close <id> --summary "..."
python3 scripts/task_registry.py --registry <path> archive <id> --summary "..."
```

### 7. 任务状态（替代 `/status` 的任务视图）

当用户发送 `任务状态` 时：

1. 读取 `show`（当前任务）+ `list`（任务清单）
2. 返回当前任务编号、标题、状态
3. 返回当前任务绑定的 `sessionKey`（仅用于排障）
4. 返回 registry 路径（便于定位持久化文件）

说明：`/status` 是 OpenClaw 全局会话状态，不等价于任务工作台的任务路由状态。

## 回复样式约束

对于路由到具体任务的非全局回复，必须加任务头：

```text
[任务:#2 周报]
```

该任务头需要在每次任务回复中可见，便于用户核对路由是否正确。
