---
name: feishu-group-memory-system
description: 飞书群聊上下文持久化技能。当用户在群聊中说"保存上下文"时保存当前群聊对话；在私聊中会根据用户意图分流到手动群聊存档或其他操作。
version: 1.0.0
author: Zheli
---

# 飞书群聊记忆管理

## 核心功能

本技能解决飞书群聊中 OpenClaw 凌晨 4 点清理上下文导致对话断裂的问题。通过将群聊历史总结保存到 memory 文件，实现跨 session 的上下文连续性。

## 环境检测（前置步骤）

### 第一步：判断当前环境

从 inbound context 获取 `chat_id`：
- **群聊**（`oc_` 开头）→ 继续执行本 skill 的群聊保存逻辑
- **私聊**（`user:` 开头）→ 进入「私聊分流逻辑」

### 私聊分流逻辑

如果检测到是私聊环境，检查用户输入：
→ 回复："这是私聊环境。如需保存当前对话，我会记录到日记。如需批量保存群聊记忆，请说'手动飞书群聊存档'。

## 触发条件

### 保存上下文（手动）（仅群聊环境）
当用户说以下任一内容时触发保存：
- "保存上下文"
- "保存对话"
- "记住这次对话"
- "保存到群记忆"

### 加载上下文（手动）
当用户说以下任一内容时触发加载：
- "加载上下文"
- "加载记忆"
- "读取群记忆"
- "上次说到哪了"

### 自动保存（心跳）
在心跳检查时，如果当前是群聊环境且有未保存的重要对话，自动执行保存。

### 自动加载（Session 启动）
每次 session 启动时，如果检测到是群聊环境（chat_id 以 `oc_` 开头），自动读取对应的记忆文件。

## 初始化设置

首次使用本技能前，请完成以下设置：

### 1. 创建存储目录

```bash
mkdir -p ~/.openclaw/workspace/memory/FeishuGroupMemory
```

### 2. 配置 AGENTS.md

在 `AGENTS.md` 的「Every Session」部分添加：

```markdown
## Every Session

1. 读取 `SOUL.md`
2. 读取 `USER.md`
3. 读取 `memory/YYYY-MM-DD.md`（今天 + 昨天）
4. **群聊记忆**：如果是群聊环境（chat_id 以 `oc_` 开头）：
   - **读取记忆**：加载 `memory/FeishuGroupMemory/{chat_id}.md` 恢复上下文
   - **系统指令处理**：收到 `[SYSTEM]` 开头的消息时执行对应操作（如保存记忆）
```

### 3. 配置 SOUL.md

在 `SOUL.md` 中添加群聊感知规则：

```markdown
## 群聊感知

**识别群聊环境**：检查 inbound context 中的 `chat_id`，如果以 `oc_` 开头则是群聊。

**Session 启动时**：如果是群聊环境，自动读取 `memory/FeishuGroupMemory/{chat_id}.md` 恢复上下文。

**保存记忆**：当用户说"保存上下文"或心跳检查时，将对话总结保存到 `memory/FeishuGroupMemory/{chat_id}.md`。

**加载记忆**：当用户说"加载上下文"时，读取对应群聊的记忆文件。

**系统指令识别**：收到 `[SYSTEM]` 开头的消息时：
- **不回复给用户**（这是内部指令，不是用户消息）
- **识别指令类型**：
  - `[SYSTEM] 执行群聊记忆保存` → 执行保存逻辑
  - 其他 `[SYSTEM]` 指令 → 根据指令内容执行对应操作
```

### 4. 配置 HEARTBEAT.md（可选）

如果希望在心跳时自动保存群聊记忆，在 `HEARTBEAT.md` 中添加：

```markdown
## Heartbeat 检查项

1. 检查主会话新消息
2. **群聊记忆保存**：如果当前是群聊环境且距离上次保存超过阈值，执行保存
3. 保存 summary 到 memory/YYYY-MM-DD.md
```

## 存储路径

```
memory/FeishuGroupMemory/{chat_id}.md
```

例如：
- `memory/FeishuGroupMemory/oc_1736efe0d350b597267e3ed5xxxxxxxx.md`
- `memory/FeishuGroupMemory/oc_f1098998d86e69b7a5043a61xxxxxxxx.md`

## 保存流程

1. **检测环境**：从 inbound context 中获取 `chat_id`
2. **读取历史**：使用 `sessions_history` 读取当前会话历史
3. **AI 总结**：将对话总结为结构化要点（见下方格式）
4. **写入文件**：保存到 `memory/FeishuGroupMemory/{chat_id}.md`
5. **记录日志**：在当天的 `memory/YYYY-MM-DD.md` 中记录保存操作（必须执行）

### 当日记忆记录格式

在 `memory/YYYY-MM-DD.md` 中添加对话重点内容，作为日记的一部分：

```markdown
## 群聊对话记录

**群聊**: {群聊名称或 ID}
**时间**: HH:mm

{对话的重点内容、决策、进展等，作为当天的生活/工作记录}
```

这一步不能省略，当日记忆文件是用户的日记，需要记录实际内容，而不仅是保存操作的时间线。

### 总结格式

```markdown
# {群聊名称或 ID} - 对话记忆

## 最后更新时间
YYYY-MM-DD HH:mm

## 关键决策
- 决策 1
- 决策 2

## 待办事项
- [ ] 任务 1
- [ ] 任务 2

## 重要上下文
- 背景信息 1
- 背景信息 2

## 对话摘要
简要描述这次对话的核心内容和进展
```

## 加载流程

1. **检测环境**：从 inbound context 中获取 `chat_id`
2. **检查文件**：确认 `memory/FeishuGroupMemory/{chat_id}.md` 是否存在
3. **读取内容**：使用 `memory_get` 读取记忆文件
4. **恢复上下文**：将关键信息整合到当前对话中

## 群聊识别

飞书群聊的 `chat_id` 格式：
- 群聊：`oc_` 开头，如 `oc_1736efe0d350b597267e3ed59bccxxxx`
- 私聊：`user:` 开头，如 `user:ou_xxxxxxxxxxxxxxxxxxxxxx`

**仅对群聊环境启用本技能**，私聊不需要群记忆。

## 已知群聊

参考 [references/group-ids.md](references/group-ids.md) 记录已知群聊 ID 和用途。

## 与 HEARTBEAT.md 的协调

- **HEARTBEAT.md**：用于通用定时任务（如每晚检测手动完成的任务）
- **本技能**：专门处理群聊上下文保存
- **不冲突**：心跳时可以触发本技能的保存逻辑，但 HEARTBEAT.md 不直接写入群记忆文件

## 注意事项

### ⚠️ 重要：追加而不是覆盖（2026-03-17 更新）

**错误做法**：
```python
# ❌ 错误：直接 write 会覆盖整个文件，丢失历史记录
write(
    file_path="memory/FeishuGroupMemory/{chat_id}.md",
    content="新生成的内容"
)
```

**正确做法**：
```python
# ✅ 正确：先读取现有内容，再追加/合并
# 步骤 1：读取现有记忆文件
existing = read(file_path="memory/FeishuGroupMemory/{chat_id}.md")

# 步骤 2：解析现有内容，保留历史部分
# - 保留：关键决策、待办事项、重要上下文
# - 追加：新的对话摘要到"历史对话记录"部分

# 步骤 3：更新"最后更新时间"为当前时间

# 步骤 4：写入合并后的完整内容
write(
    file_path="memory/FeishuGroupMemory/{chat_id}.md",
    content="合并后的完整内容"
)
```

**或者使用 edit 工具**：
```python
# ✅ 替代方案：使用 edit 追加到文件末尾
edit(
    file_path="memory/FeishuGroupMemory/{chat_id}.md",
    oldText="## 对话摘要\n{旧内容}",
    newText="## 对话摘要\n{旧内容}\n\n### 2026-03-17\n{新内容}"
)
```

### 其他注意事项

1. **时间戳**：每次保存都要更新"最后更新时间"
2. **简洁总结**：保持总结精炼，避免冗余
3. **群聊感知**：session 启动时主动检查是否是群聊环境
