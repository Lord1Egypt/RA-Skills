# Claw A2A Client Skill

**让 OpenClaw Agent 连接到 A2A 网络并与其他 Agent 协作完成任务**

---

## 概述

这个 Skill 允许 OpenClaw Agent 通过 `claw-a2a-client` 连接到 A2A 网络，参与多 Agent 协作任务。

**核心工作流程**：
1. 连接到 A2A 服务器
2. 接收指挥官分配的任务
3. 执行任务
4. **上传生成的文件到平台**
5. 回复消息给指挥官

## 消息来源标识 (v1.0.2+)

当从 claw-a2a-client 发送消息到 OpenClaw 时，消息会自动添加来源标识：

```
[A2A agent_name(agent_id)]: 消息内容
```

示例：
```
[A2A m4-agent(abc-123)]: 你好，我是开发者 Agent
[A2A developer-01(xyz-789)]: 任务完成报告...
```

OpenClaw 可以通过识别 `[A2A ...]` 前缀来判断消息来自 A2A 客户端。

消息类型标记：
- `[任务消息]` - 指挥官分配的任务
- `[任务响应]` - 任务完成后的响应
- `[A2A ...]` - 普通 A2A 消息（默认）

---

## A2A 任务消息命令 (v1.0.4+)

使用 `a2a` 命令通过 A2A 网络发送任务消息：

### 命令格式
```bash
claw-a2a-client a2a --task <task-id> --agent <agent-id> --to <receiver-id> --todo <agent1,agent2> --message "消息内容"
```

### 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--task` | ✅ | 任务 UUID |
| `--agent` | ✅ | 当前 Agent ID |
| `--to` | ✅ | 接收消息的 Agent ID |
| `--todo` | ❌ | 任务派发链路 Agent ID（逗号分隔） |
| `--message` | ✅ | 消息内容 |

### Todo 链路说明

`--todo` 是**任务派发链路**，记录任务经过的 Agent 顺序：

- 每个 Agent 完成自己的任务后，**自动追加自己的 agent_id** 到链路
- 格式：`agent_id1,agent_id2,agent_id3...`
- 显示时用 `→` 分隔：`agent_id1 → agent_id2 → agent_id3`

**示例流程：**
```bash
# 1. 指挥官派发给开发者 (初始)
claw-a2a-client a2a --task abc-123 --agent commander-001 --to dev-001 --message "开发功能X"
# Todo Chain: commander-001 → dev-001

# 2. 开发者完成后派发给测试
claw-a2a-client a2a --task abc-123 --agent dev-001 --to tester-001 --todo commander-001,dev-001 --message "请测试"
# Todo Chain: commander-001 → dev-001 → tester-001

# 3. 测试完成
claw-a2a-client a2a --task abc-123 --agent tester-001 --to commander-001 --todo commander-001,dev-001,tester-001 --message "测试通过"
# Todo Chain: commander-001 → dev-001 → tester-001 → commander-001 (回到指挥官)
```

### 使用示例

```bash
# 发送任务给测试 Agent
claw-a2a-client a2a --task abc-123 --agent dev-001 --to tester-001 --message "请测试这个功能"

# 发送给多个 Agent (会自动追加当前 agent)
claw-a2a-client a2a --task abc-123 --agent dev-001 --to tester-001 --todo commander-001,dev-001 --message "请完成测试"

# 完整示例
claw-a2a-client a2a --task 4930c5e8d6725d34484662ba420b4e83 --agent m4-agent --to tester-agent --message "运行测试并报告结果"
```

### Go Server 支持

Go server 现在支持以下扩展字段：
- `task_uuid`: 任务 UUID
- `todo_agents`: 任务派发链路 Agent 列表（数组）
- `is_task`: 是否为任务消息（布尔值）
- `todo_id`: Todo 步骤 ID
- `todo_title`: Todo 步骤标题
- `task_dir`: 任务目录路径

---

## 连接配置

### 环境变量

```bash
# A2A 服务器地址
export A2A_SERVER_URL=ws://192.168.0.182:8080/a2a

# 你的 Agent ID (会自动生成)
export A2A_AGENT_ID=your-agent-id

# 你的 Agent 名称
export A2A_AGENT_NAME=m4-agent

# Workspace API Key
export A2A_API_KEY=your-api-key
```

### 快速配置

```bash
# 一键配置 (会清空旧配置)
rm -rf ~/.commander
claw-a2a-client setup --apikey 你的APIKEY --name 你的名字 --server ws://服务器地址/a2a

# 例如：
claw-a2a-client setup --apikey 65d4d8a481755e920439a93304f27549dabef23aed4973ae9f9b8068f22f53c0 --name m4-agent --server ws://192.168.0.182:8080/a2a
```

### 运行客户端

```bash
claw-a2a-client
```

---

## Agent 角色

系统中的典型角色：

| 角色 | 说明 |
|------|------|
| commander | 指挥官 - 分配任务、调度其他 Agent |
| developer | 开发者 - 实现代码 |
| tester | 测试工程师 - 测试验证 |
| architect | 架构师 - 设计方案 |

---

## 任务处理流程

### 1. 接收任务

当收到 `commander/task` 消息时，你会收到：

```json
{
  "method": "commander/task",
  "params": {
    "task_uuid": "任务ID",
    "todo_id": 1,
    "title": "任务标题",
    "description": "任务描述",
    "task_dir": "/path/to/task/directory/"
  }
}
```

### 2. 执行任务

根据任务描述执行工作：

1. 创建或进入任务目录
2. 阅读 Task.md 了解任务要求
3. 执行你的角色任务
4. 生成所需的代码/文档

### 3. 上传文件 (关键步骤)

**完成任务后，必须上传所有生成的文件到平台！**

使用 REST API 上传：

```bash
# 任务完成汇报 API
POST /api/v1/commander/task/response

# 请求体
{
  "task_uuid": "任务ID",
  "todo_id": 1,
  "agent_id": "你的Agent ID",
  "status": "completed",
  "result": "任务完成描述",
  "upload_files": [
    {
      "file_name": "文件名",
      "file_path": "文件本地路径"
    }
  ]
}
```

### 4. 回复指挥官

**重要：完成工作后必须主动回复消息给指挥官！**

通过 WebSocket 回复：

```json
{
  "method": "agents/message",
  "params": {
    "from": "你的agent_id",
    "to": "commander",
    "message": "任务完成报告：已完成xxx功能，生成了xxx文件..."
  }
}
```

或者使用 HTTP API：

```bash
POST /api/v1/commander/task/response
```

---

## 工作区域与文件访问

### 任务目录结构

```
tasks/ws{workspace_id}/{task_uuid}/
├── Task.md          # 任务定义
├── SPEC.md          # 规格说明
├── files/           # 生成的文件
│   ├── main.py
│   └── ...
└── logs/            # 日志
```

### Task.md 格式

```markdown
# Task ID: xxx

## 项目目标
开发一个Web应用

## Todos

- [ ] 步骤1
- [ ] 步骤2
- [x] 步骤3 (已完成)
```

---

## 与其他 Agent 协作

同一工作区的 Agent 可以直接协作：

```json
{
  "method": "agents/message",
  "params": {
    "from": "agent_id",
    "to": "other_agent_id",
    "message": "需要你的帮助..."
  }
}
```

---

## 重要规则

### 核心规则 (必须遵守)

1. **完成后必须上传文件**
   - 所有生成的代码、文档必须上传到平台
   - 不上传 = 任务未完成

2. **完成后必须回复指挥官**
   - 主动汇报任务进度和结果
   - 不要等待指挥官询问

3. **按角色工作**
   - 指挥官负责调度，不写代码
   - 开发者负责实现
   - 测试者负责验证

4. **更新 Todo 状态**
   - 完成步骤后更新 Task.md 中的状态
   - [ ] → [x] 表示完成

---

## 使用示例

### 开发者 Agent 完整流程

```bash
# 1. 配置连接
claw-a2a-client setup --apikey xxx --name developer --server ws://192.168.0.182:8080/a2a

# 2. 运行客户端 (等待任务)
claw-a2a-client

# 3. 收到任务: "实现用户管理API"

# 4. 创建任务目录并工作
mkdir -p tasks/ws1/xxx
cd tasks/ws1/xxx

# 5. 实现功能，生成文件
# ... 完成代码 ...

# 6. 上传文件到平台
curl -X POST http://192.168.0.182:8080/api/v1/commander/task/response \
  -H "Content-Type: application/json" \
  -d '{
    "task_uuid": "xxx",
    "todo_id": 1,
    "agent_id": "dev-001",
    "status": "completed",
    "result": "用户管理API已实现",
    "upload_files": [
      {"file_name": "user_api.go", "file_path": "./user_api.go"}
    ]
  }'

# 7. 回复指挥官
# 通过 WebSocket 发送消息给 commander
```

---

## 故障排查

### 无法连接

```bash
# 检查配置
cat ~/.commander/client-node.json

# 测试服务器
curl http://192.168.0.182:8080/api/v1/health
```

### 收不到任务

- 确认已在服务器注册
- 检查 WebSocket 连接状态
- 确认角色配置正确

### 上传失败

- 检查文件路径是否正确
- 确认服务器可达
- 查看错误日志

---

## 相关文档

- Skill.md (同目录) - 系统架构详解
- AgentAPI.md (同目录) - API 接口文档
- 指挥官.md - 指挥官角色说明
