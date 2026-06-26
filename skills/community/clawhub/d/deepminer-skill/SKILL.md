---
name: DM-skills
version: 1.7.1
description: 通过 dm-cli 命令行工具与 DeepMiner (DM) 系统交互。**凡是涉及 DM/DeepMiner 系统的任务，必须先读此 Skill。** 触发条件：用户提到 "使用 DM"、"发给 DM"、"用 DM 问一下"、"DM 帮我..."、"DeepMiner 执行..." 等任何涉及 DM 系统的任务请求。即使对话历史中已使用过 dm-cli，也必须先读此 Skill 确保遵循完整指导。
---

# DM-skills

用于与 DM 系统交互的命令行工具。

## 🚀 从零开始（安装指南）

### 步骤 1：安装 dm-cli

```bash
npm install -g deepminer-cli
```

### 步骤 2：配置 AccessKey

```bash
dm-cli config init --endpoint <API端点> --accesskey <AccessKey> --json
```

### 步骤 3：验证配置

```bash
dm-cli auth status --json
```

---

## ⚠️ 核心规则

### 0. 任务终止（重要！）

**⚠️ 终止正在运行的任务必须用 `thread stop`，不能用发消息！**

**❌ 错误做法（只是发消息，不会终止任务）：**
```bash
dm-cli thread start --thread-id xxx --message "取消任务"
```

**✅ 正确做法：**
```bash
# 停止正在运行的 Agent
dm-cli thread stop --thread-id <thread_id>

# 取消异步标注任务（需要 task_id）
dm-cli task lifecycle --thread-id <thread_id> --task-id <task_id> --action cancel
```

**命令对照表：**

| 场景 | 命令 |
|------|------|
| 停止正在运行的 Agent | `dm-cli thread stop --thread-id <id>` |
| 取消异步标注任务 | `dm-cli task lifecycle --thread-id <id> --task-id <id> --action cancel` |

**为什么重要：**
- 发消息只是让 AI对话，不会真正终止任务
- 任务会继续运行，消耗资源和时间
- 会话数量达上限后无法创建新任务

---

### 1. 版本检查（每次使用必做）

**每次使用本 Skill 前，必须检查版本是否为最新。**

**检查方法：**

```bash
# 获取 ClawHub 上的最新版本（带缓存，每天最多检查一次）
CACHE_FILE="/tmp/dmskills_version_cache"
if [ -f "$CACHE_FILE" ] && [ $(( $(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE") )) -lt 86400 ]; then
  LATEST=$(cat "$CACHE_FILE")
else
  LATEST=$(curl -sL "https://clawhub.ai/dmpm-mininglamp/deepminer-skill" | grep -o 'version:"[^"]*"' | head -1 | cut -d'"' -f2)
  echo "$LATEST" > "$CACHE_FILE"
fi
```

**当前最新版本：** 读取本文件 frontmatter 中的 `version` 字段

**本地版本检查：**

读取本 SKILL.md 文件 frontmatter 中的 `version` 字段。

**版本不一致时：**

```
⚠️ DeepMiner-skills 版本过旧！

本地版本：<frontmatter 中的 version>
最新版本：<LATEST 变量值>

请访问 https://clawhub.ai/dmpm-mininglamp/deepminer-skill 下载最新版本，
或使用 clawhub CLI 更新：

  clawhub install dmpm-mininglamp/deepminer-skill

更新后继续执行任务。
```

**为什么重要：**
- 新版本可能修复关键 bug（如 async_tag_task 状态处理）
- 新版本可能增加重要功能（如新的轮询机制）
- 确保用户获得最新、最准确的指导

### 1. Prompt 原样传递（禁止修改）

用户的 prompt 必须原样传递给 DM，禁止任何改写、润色或添加解释。

### 2. DM 返回内容原样呈现

DM 返回的 `last_messages` 必须原样提取并返回，禁止省略、改写或总结。

### 3. 追问 vs 新会话判断

- 用户说"再..."、"那..."、"继续..."等信号词时，用 `--thread-id` 追问
- 完全独立的新主题时，新开 thread

### 4. 默认使用 subagent 执行任务

**⚠️ 除非用户明确要求在主 session 执行，否则一律使用 subagent！**

**原因**：
- DM 任务执行时间不可预知（几秒到几分钟不等）
- 主 session 被占用时，用户无法继续对话
- 用户可能在等待期间追问或发出新指令

**使用 subagent 的方式**：

```typescript
sessions_spawn({
  runtime: "subagent",
  task: "使用 dm-cli 执行 DM 任务：{用户原始请求}",
  mode: "run"
})
```

**例外情况（可以在主 session 执行）**：
- 用户明确说"直接执行"、"不要用 subagent"
- 任务非常简单且预计秒级返回（如查询状态）

**为什么重要**：
- 保持主 session 响应能力
- 用户体验更好（不用等待轮询完成才能继续聊）

### 5. 追问前必须检查状态

**⚠️ 追问前必须先检查上一次任务状态！**

**原因**：如果上一次任务还在 `running`，直接追问可能会失败或被拒绝。

**流程**：

```
1. 用户发送追问指令
   ↓
2. 检查上一次 DM 任务状态
   dm-cli thread result --thread-id <id> --json
   ↓
3. 根据 state 决定下一步：
   - running → 需要使用 --force（见下方说明）
   - ask_human/completed/failed → 直接追问
```

**代码示例**：

```bash
# 追问前检查状态
prev_result=$(dm-cli thread result --thread-id "$thread_id" --json)
prev_state=$(echo "$prev_result" | jq -r '.data.state')

case "$prev_state" in
    "running")
        # 需要告知用户风险，确认后使用 --force
        echo "⚠️ 上一次任务仍在执行中，追问会中断当前任务。"
        echo "是否继续？(使用 --force 强制追问)"
        # 等待用户确认后执行
        dm-cli thread start --thread-id "$thread_id" --message "追问内容" --force --json
        ;;
    "ask_human"|"completed"|"failed")
        # 直接追问
        dm-cli thread start --thread-id "$thread_id" --message "追问内容" --json
        ;;
esac
```

### 5. `--force` 参数说明

**作用**：强制停止当前正在运行的 agent_run，立即接受新消息。

**使用场景**：
- 上一次任务还在 `running` 状态
- 用户想要追加新指令或改变方向

**风险**：
- ⚠️ 正在执行的任务会被**中断**
- 可能丢失中间结果
- 应该告知用户这个风险

**示例**：

```bash
# 不带 --force（running 状态可能失败）
dm-cli thread start --thread-id abc123 --message "新问题" --json
# 可能返回错误：会话正在运行中

# 带 --force（强制中断当前任务）
dm-cli thread start --thread-id abc123 --message "新问题" --force --json
# 成功，但之前的任务被中断
```

**最佳实践**：
1. 先检查状态，告知用户风险
2. 用户确认后再使用 `--force`
3. 如果任务很重要，建议等 `completed` 后再追问

### 6. 异步任务的两步确认机制

**⚠️ 启动异步任务必须用 CLI 命令，不能用追问消息！**

**背景**：DM 对大规模异步任务（如批量标注）设计了双重确认机制，防止误触发消耗大量积分。

---

**❌ 错误做法（会导致任务被取消）**

```bash
# 错误：用追问消息启动任务
dm-cli thread start --thread-id "$thread_id" --message "请开始执行异步标注任务"
# 结果：任务被取消，状态变为 rejected
```

---

**✅ 正确流程**

| 步骤 | 命令 | 状态变化 |
|------|------|---------|
| **1️⃣** | `thread start --message "确认执行全量标注"` | `ask_human` → `async_tag_task` |
| **2️⃣** | 等待状态稳定，获取 task_id | `PENDING` |
| **3️⃣** | `task lifecycle --action start` | `PENDING` → `RUNNING`（真正启动） |

---

**完整代码示例**

```bash
# 步骤 1：第一次追问（提交异步任务）
dm-cli thread start --thread-id "$thread_id" --message "确认执行全量标注" --json

# 步骤 2：等待状态稳定，获取 task_id
sleep 10
result=$(dm-cli thread result --thread-id "$thread_id" --json)
state=$(echo "$result" | jq -r '.data.state')
task_id=$(echo "$result" | jq -r '.data.status_info.task_id')

if [ "$state" = "async_tag_task" ]; then
    # 步骤 3：用 CLI 命令启动任务（关键！）
    dm-cli task lifecycle --thread-id "$thread_id" --task-id "$task_id" --action start --json
    
    echo "✅ 异步任务已启动执行！"
    echo "任务ID: $task_id"
fi
```

---

**关键命令：task lifecycle**

| 参数 | 说明 |
|------|------|
| `--thread-id` | 会话 ID |
| `--task-id` | 异步任务 ID（从 status_info.task_id 获取） |
| `--action` | 操作类型：`start`（启动）、`interrupt`（中断）、`resume`（恢复）、`cancel`（取消） |

---

**状态说明**

| 任务状态 | 可执行操作 |
|---------|-----------|
| `PENDING` | ✅ `start`（启动） |
| `RUNNING` | ✅ `interrupt`（中断） |
| `INTERRUPTED` | ✅ `resume`（恢复）或 `cancel`（取消） |
| `rejected` | ❌ 无法启动（任务已取消） |

---

**常见错误**

| 错误 | 结果 |
|------|------|
| ❌ 用追问消息启动 | 任务被取消，状态变为 `rejected` |
| ❌ 不等待状态稳定 | task_id 未返回，无法启动 |
| ❌ 任务状态不是 `PENDING` | CLI 返回 "Cannot start task in xxx state" |

---

**通知用户**

第一次追问后：
```
📋 异步任务已提交（PENDING）

任务ID: xxx
预估积分: 45-90 credits

等待 CLI 启动命令执行...
```

CLI 启动后：
```
✅ 异步任务已启动执行！

任务ID: xxx
请等待完成，轮询子代理会通知结果。
```

---

**为什么重要**
- 防止误触发大规模任务消耗积分
- 用追问消息会取消任务（系统设计）
- CLI 命令是唯一正确的启动方式
- 给用户第二次思考的机会
- 确保用户明确知道任务将要执行

---

## 异步任务管理命令（task 系列）

### task info - 查询任务信息

**用途**：实时查询异步任务的状态、进度、统计数据。

```bash
dm-cli task info --thread-id <thread_id> --task-id <task_id> --json
```

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | 任务 ID |
| `task_name` | string | 任务名称 |
| `state` | string | 任务状态（running/success/failed/interrupted） |
| `total` | int | 总数据量 |
| `completed` | int | 已完成数量 |
| `failed` | int | 失败数量 |
| `download_total` | int | 已下载数量 |
| `estimate_time` | string | 预估耗时（秒） |
| `estimate_points` | string | 预估积分范围（如 "245~490"） |
| `file_path` | string | 结果文件 URL |

**使用场景**：
- 监控任务实时进度
- 查询任务是否完成
- 获取预估积分消耗

**示例输出**：
```json
{
  "ok": true,
  "data": {
    "tasks": [{
      "task_id": "xxx",
      "task_name": "产品评价情感分析",
      "state": "running",
      "total": 500,
      "completed": 89,
      "failed": 0,
      "estimate_time": "120",
      "estimate_points": "245~490"
    }]
  }
}
```

---

### task lifecycle - 任务生命周期管理

**用途**：管理异步任务的启动、中断、恢复、取消。

```bash
dm-cli task lifecycle --thread-id <thread_id> --task-id <task_id> --action <action> --json
```

**action 参数**：

| action | 说明 | 适用状态 |
|--------|------|---------|
| `start` | 启动任务 | PENDING |
| `interrupt` | 中断任务 | running |
| `resume` | 恢复任务 | interrupted |
| `cancel` | 取消任务 | running/interrupted |

**状态转换**：

```
PENDING → start → running
running → interrupt → interrupted
interrupted → resume → running
running → cancel → rejected
interrupted → cancel → rejected
```

**使用场景**：
- `start`：启动已提交的异步任务（替代追问消息）
- `interrupt`：临时暂停任务（可恢复）
- `resume`：恢复被中断的任务
- `cancel`：彻底取消任务（不可恢复）

---

### task files - 任务产物文件

**⚠️ 注意**：`task files` 仅适用于**批量下载/采集类任务**，标注任务不支持。

**标注任务的文件获取方式**：
```bash
dm-cli thread file-list --thread-id <thread_id> --json
```

---

## 执行流程

### 标准流程（非阻塞轮询）

```
1. 用户发送任务
   ↓
2. dm-cli thread start --message "用户原话" --json
   ↓
3. 获取 thread_id
   ↓
4. 启动轮询子代理（sessions_spawn）
   ↓
5. 告知用户 "DM 任务已提交..."
   ↓
6. 主代理保持响应，等待子代理通知
   ↓
7. 子代理检测到状态变化 → sessions_send 通知主会话
   ↓
8. 主代理收到通知，处理并返回结果
```

---

## 非阻塞轮询实现（核心）

### ⚠️ 必须使用 sessions_spawn 轮询

**原因**：
1. 同步 exec 会阻塞主代理，用户无法中断
2. 后台 exec 完成后只是系统消息，主代理不会自动响应
3. 需要子代理通过 `message` 工具**直接通知用户**

### 完整实现代码

**步骤 1：提交任务**

```bash
result=$(dm-cli thread start --message "用户原话" --json)
thread_id=$(echo "$result" | jq -r '.data.thread_id')

if [ -z "$thread_id" ] || [ "$thread_id" = "null" ]; then
    echo "❌ 任务提交失败"
    return
fi
```

**步骤 2：启动轮询子代理（关键！）**

使用 `sessions_spawn` 启动子代理，子代理会**直接向用户发送结果**：

```json
{
  "action": "sessions_spawn",
  "runtime": "subagent",
  "mode": "run",
  "label": "dm-poll-${thread_id}",
  "timeoutSeconds": 3600,
  "task": "你是 DM 轮询子代理。\n\n## 任务\n轮询 DM 任务状态，完成后**直接通知用户**。\n\n## 参数\n- thread_id: \"${thread_id}\"\n\n## 轮询流程\n\n1. 调用 `dm-cli thread result --thread-id ${thread_id} --json` 获取状态\n2. 如果 state 是 running，等待后继续轮询（间隔 5/10/20/40/60 秒递增）\n3. 如果 state 变化：\n   - **使用 message 工具通知用户**：`{\"action\": \"send\", \"message\": \"结果内容\"}`\n   - 如果是终止状态（completed/ask_human/failed），退出\n\n## 状态处理\n\n| 状态 | 动作 |\n|------|------|\n| running | 继续轮询 |\n| async_tag_task | 通知用户去 GUI 确认（附具体链接 https://deepminer.com.cn/agents/${thread_id}），继续轮询 |\n| ask_human | 通知用户问题，退出 |\n| completed | 通知用户结果（含文件链接），退出 |\n| failed | 通知用户错误，退出 |\n\n## 通知格式示例\n\n**完成时**：\n```\n✅ DM 任务完成\n\nthread_id: xxx\n\n结果：...\n\n📄 文件：[链接]\n```\n\n**需要用户输入时**：\n```\n⏸️ DM 需要您的回复\n\n[问题内容]\n\n请回复后继续。\n```\n\n**重要**：必须使用 message 工具直接发送给用户，不要只是输出到 stdout！\n\n开始执行轮询。"
}
```

**步骤 3：告知用户任务已提交**

```
⏳ DM 任务已提交，正在后台处理中...
```

**步骤 4：主代理保持响应**

- 子代理在后台轮询
- 完成后子代理**直接向用户发消息**
- 主代理无需介入，用户直接收到结果

**步骤 5：用户可随时中断**

```
用户: "停止"
主代理: subagents kill dm-poll-${thread_id}
```

---

## 轮询子代理 Task 模板

**主代理 spawn 子代理时，直接使用此模板作为 task 参数：**

```
你是 DM 轮询子代理。

## ⚠️ 核心规则

1. **必须遍历所有 last_messages**，不能只看第一条
2. **必须原样呈现**，禁止总结、省略、改写 DM 的回复
3. **必须提取所有文件链接**，不能遗漏任何 attachment

## 参数

- thread_id: ${thread_id}

## 轮询流程

1. 使用 `exec` 工具调用 `dm-cli thread result --thread-id ${thread_id} --json`
2. 解析 `.data.state` 字段
3. 根据 state 处理：

| state | 动作 |
|-------|------|
| running | 等待 5/10/20/40/60 秒后继续轮询 |
| async_tag_task | 通知用户去 GUI 确认（链接：https://deepminer.com.cn/agents/${thread_id}），继续轮询 |
| ask_human | 输出问题，停止 |
| completed | 输出结果，停止 |
| failed | 输出错误，停止 |

## ⚠️ 通知方式

**直接输出以下格式的文本**（会自动推送给主代理，主代理转发给用户）：

```
✅ DM 任务完成

thread_id: ${thread_id}

**结果：**

[遍历 last_messages，原样输出每条 assistant 消息的 content]

**文件：**

[遍历 last_messages，提取所有 tool 消息的 artifact.attachments，列出所有文件链接]
```

## ⚠️ 关键提醒

- **不要调用 message 或 sessions_send 工具**
- **直接输出文本**，系统会自动推送
- 停止后你的输出会通过 subagent_announce 发送给主代理
- 主代理收到后会转发给用户

开始执行轮询任务。
```

---

## 主代理调用示例

```json
{
  "action": "sessions_spawn",
  "runtime": "subagent",
  "mode": "run",
  "label": "dm-poll-${thread_id}",
  "timeoutSeconds": 3600,
  "task": "<上面的模板内容，替换 ${thread_id} 为实际值>"
}
```

---

## 用户中断处理

当用户发送"停止"、"中止"指令时：

```bash
subagents kill --target dm-poll-${thread_id}
```

---

## 状态处理总结

| 状态 | 类型 | 子代理行为 | 主代理动作 |
|------|------|-----------|-----------|
| `running` | 执行中 | 继续轮询 | 等待 |
| `async_tag_task` | 待 GUI 确认 | 通知用户去 GUI 确认（附链接 https://deepminer.com.cn/agents/${thread_id}），继续轮询 | 告知用户去 GUI 确认，附具体会话链接 |
| `ask_human` | 等待输入 | 输出问题，停止 | 返回问题，等待追问 |
| `completed` | 成功 | 输出结果，停止 | 提取结果，返回用户 |
| `failed` | 失败 | 输出错误，停止 | 返回错误信息 |

---

## 异步任务轮询特殊处理（async_tag_task）

### 问题背景

DM 的**打标注任务**会进入 `async_tag_task` 状态，此时需要用户在 GUI 上确认后才能继续执行。这带来一个设计难题：

| 方案 | 结果 |
|------|------|
| 遇到 `async_tag_task` 立即停止并通知 | ✅ 用户知道去 GUI 确认<br>❌ 但没人继续跟踪任务完成 |
| 遇到 `async_tag_task` 继续静默轮询 | ✅ 能跟踪到最终完成<br>❌ 用户不知道要去 GUI 确认 |

### 解决方案：分层轮询设计

**核心原则：** 子代理**只输出、不停留**，主代理负责决策和重启轮询。

```
流程：
1. 启动子代理轮询
2. 子代理检测到 `async_tag_task`
3. 子代理输出通知 → 停止（触发 subagent_announce）
4. 主代理收到通知，告知用户去 GUI 确认
5. 【关键】主代理提示："去 GUI 确认后，请发送 '继续'"
6. 用户去 GUI 确认，回来后发送 "继续"
7. 主代理启动新子代理，继续轮询到 completed
```

### 子代理 Task 模板（正确版本）

```
你是 DM 轮询子代理。

## 任务
轮询 DM 任务状态，**关键状态变化后立即停止并输出**。

## 参数
- thread_id: ${thread_id}

## 状态处理规则

| state | 动作 |
|-------|------|
| running | sleep 15秒，继续轮询 |
| async_tag_task | **输出通知 + 停止**（等待用户 GUI 操作） |
| ask_human | 输出问题 + 停止 |
| completed | 输出完整结果（含文件链接）+ 停止 |
| failed | 输出错误 + 停止 |

## ⚠️ 关键要求

- 遍历所有 last_messages，原样呈现
- 提取所有文件附件链接
- **非终止状态（running）才继续轮询**
- 遇到 async_tag_task/ask_human/completed/failed **立即停止**

开始执行轮询。
```

### 主代理处理模板

```typescript
// 1. 首次启动轮询
sessions_spawn({
  runtime: "subagent",
  mode: "run",
  label: "dm-poll-${thread_id}",
  timeoutSeconds: 600,
  task: "<上面的子代理模板>"
})

// 2. 收到 subagent_announce 后判断
if (result.contains("async_tag_task")) {
  // 通知用户去 GUI 确认
  reply("⏸️ 需要你去 GUI 确认...\n\n确认后请发送 '继续'")
} else if (result.contains("completed")) {
  // 任务完成，输出结果
  reply("✅ 任务完成...")
}

// 3. 用户发送 "继续" 后，启动新轮询
if (user_message == "继续") {
  sessions_spawn({
    runtime: "subagent",
    mode: "run",
    label: "dm-poll-${thread_id}-2",
    timeoutSeconds: 600,
    task: "<同上>"
  })
}
```

### 关键点

1. **子代理不要用 message 工具** —— subagent 模式没有 message 工具
2. **子代理遇到 async_tag_task 必须停止** —— 才能触发 subagent_announce 通知主代理
3. **主代理必须提示用户 "完成后发送继续"** —— 否则用户不知道要回来触发新轮询
4. **用递增的 label** —— 如 `dm-poll-xxx-2`、`dm-poll-xxx-3`，避免冲突

---

## 关键优势

| 问题 | 解决方案 |
|------|----------|
| 主代理阻塞 | 使用 `sessions_spawn` 子代理轮询 |
| 无法中断 | `subagents kill` 终止子代理 |
| 通知延迟/丢失 | 子代理直接输出文本，auto-announce 推送 |
| 无限重试 | timeoutSeconds 限制，或用户手动终止 |
| **async_tag_task 无法通知** | **分层设计：停止→通知→重启轮询** |



---

## 🔍 未知命令发现原则（重要！）

**当没有已知命令能完成用户的需求时，优先使用 `help` 找命令。**

**⚠️ message 并不能操作 agent 状态！** 发消息只是让 AI 对话，不会真正改变任务状态、停止任务、或控制异步任务。

**正确做法：**

```bash
# 1. 先看顶层帮助
dm-cli --help

# 2. 看子命令帮助
dm-cli thread --help
dm-cli task --help
dm-cli agent --help

# 3. 看具体命令帮助
dm-cli thread start --help
dm-cli task lifecycle --help

# 4. 输出完整 Schema（供 AI 系统解析）
dm-cli schema --pretty
```

**`dm-cli schema` 命令（⚠️ 重要！）**

- 输出 dm-cli 的完整结构化 Schema（JSON 格式）
- 包含所有命令、参数、返回字段、验证规则
- **供 AI 系统或自动化工具动态发现命令使用**
- 当 AI 不确定有什么命令可用时，应调用此命令

```bash
# 压缩输出（默认）
dm-cli schema

# 格式化输出（人类可读）
dm-cli schema --pretty
```

**为什么重要：**
- AI 不能依赖训练时的命令记忆（CLI 会更新）
- schema 是 CLI 的「能力说明书」，始终反映最新版本
- 遇到未知需求时，先查 schema/help，不要猜测命令

---

## 完整命令参考

### dm-cli 全局参数

| 参数 | 说明 |
|------|------|
| `--json` | 以 JSON 格式输出（脚本调用必加） |
| `--help` / `-h` | 显示帮助 |

### config 系列

| 命令 | 说明 |
|------|------|
| `dm-cli config init --endpoint <url> --accesskey <key> [--poll-timeout <min>]` | 初始化配置（默认 endpoint: https://deepminer.com.cn，默认 poll-timeout: 60 分钟） |
| `dm-cli config show [--json]` | 显示当前配置 |

### auth 系列

| 命令 | 说明 |
|------|------|
| `dm-cli auth status [--json]` | 显示鉴权状态 |

### thread 系列

| 命令 | 说明 |
|------|------|
| `dm-cli thread start --message <text> [--thread-id <id>] [--file <path> ...] [--agent-mode auto\|cooperation] [--force] [--json]` | 发起/继续 AI 会话 |
| `dm-cli thread result --thread-id <id> [--json]` | 获取会话结果和状态 |
| `dm-cli thread stop --thread-id <id> [--json]` | 停止正在运行的 Agent |
| `dm-cli thread list [--name <keyword>] [--json]` | 获取项目会话列表，支持按名称模糊搜索 |
| `dm-cli thread file-list --thread-id <id> [--json]` | 获取会话的文件列表（文件空间） |

**thread start 完整参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--message` | string | ✅ | 发送给 AI 的文本消息 |
| `--thread-id` | string | | 已有会话 ID，用于追问 |
| `--file` | string[] | | 本地文件路径（可多次指定） |
| `--agent-mode` | auto/cooperation | | Agent 运行模式，默认 auto |
| `--force` | boolean | | 会话运行中强制发送新问题 |

**文件大小限制：**
- 视频（mp4）: 500 MB
- 音频（mp3/wav/aac）: 100 MB
- 其他文件: 300 MB

### task 系列
| 命令 | 说明 |
|------|------|
| `dm-cli task info --thread-id <id> [--task-id <id>] [--json]` | 查询异步任务信息（不传 task-id 返回会话下所有任务） |
| `dm-cli task lifecycle --thread-id <id> --task-id <id> --action start\|interrupt\|resume\|cancel [--json]` | 管理异步任务生命周期 |
| `dm-cli task files --thread-id <id> --task-id <id> [--page <n>] [--size <n>] [--json]` | 列出任务产物文件（支持分页，默认 page=1, size=10） |

### 其他命令

| 命令 | 说明 |
|------|------|
| `dm-cli schema [--pretty]` | 输出完整 CLI Schema（供 AI 系统动态发现命令） |
| `dm-cli version` | 显示版本号 |

---


---

## 错误处理

| Exit Code | 处理方式 |
|-----------|---------|
| 0 | 成功 |
| 2 | 校验错误，检查参数 |
| 3 | 认证失败，重新配置 Access Key |
| 4 | 网络错误，检查 endpoint |
| 5 | 内部错误，检查文件路径/权限 |
| 6 | 权限不足 |
