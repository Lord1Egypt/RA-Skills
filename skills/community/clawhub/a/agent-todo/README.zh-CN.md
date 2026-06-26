# agent-todo

> **面向 OpenClaw agent 的本地优先执行队列。**
> 每个 agent 在自己的 workspace 里维护自己的任务队列，由 heartbeat 认领执行；需要时再把任务分发给其他 agent。

## 核心设计

- **本地优先**：每个 workspace 自己维护 `.agent-todo/tasks.json`
- **安装即用**：单 workspace 场景下，`clawhub install` 后即可直接使用
- **多 agent 按需开启**：只有调用 `dispatch --to-agent` 时才需要发现其他 workspace
- **OpenClaw 原生发现**：不再维护额外 registry，直接从 `~/.openclaw/openclaw.json` 读取已注册 workspace
- **托管 heartbeat 块**：`setup-heartbeat --all --write` 只追加或更新托管块，不覆盖整份 `HEARTBEAT.md`

## 运行时数据

```text
<workspace>/
  .agent-todo/
    tasks.json
    local.json   # 可选，本地身份声明
```

- `tasks.json`：当前 workspace 的任务队列
- `local.json`：可选，例如 `{"agent_id":"coding","label":"Coding Agent"}`

## 快速开始

```bash
bash ./script.sh init
bash ./script.sh doctor
bash ./script.sh setup-heartbeat --write
```

### 添加本地任务

```bash
bash ./script.sh add "修复 forum 通知去重" \
  --task-type coding \
  --source "chat:direct" \
  --next-action "检查未读通知生成逻辑" \
  --success-criteria "重复通知不再出现"
```

### 分发给其他 agent

```bash
bash ./script.sh dispatch "复核发版结果" \
  --to-agent reviewer \
  --task-type review \
  --source "chat:direct" \
  --next-action "复核 release 产物" \
  --success-criteria "完成反馈"
```

### heartbeat 认领任务

```bash
bash ./script.sh run-pending --claim
```

## 常用命令

```bash
bash ./script.sh add ...
bash ./script.sh dispatch --to-agent <agent_id> ...
bash ./script.sh plan ...
bash ./script.sh run-pending --claim
bash ./script.sh done <id> --note "..."
bash ./script.sh block <id> --reason "..."
bash ./script.sh report <id>
bash ./script.sh setup-heartbeat --write
bash ./script.sh setup-heartbeat --all --write
bash ./script.sh agents list
```
```
