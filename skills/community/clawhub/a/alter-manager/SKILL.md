---
name: session-manager
description: 分身管理 - 创建、列出、删除独立的 agent session（分身）。触发场景：用户要求创建分身、创建独立 session、管理多个对话、列出分身、删除分身、移除 session。支持 label 从用户指令中识别或主动询问。
---

# 分身管理

管理当前 agent 的独立 session（分身），实现多任务并行处理。

## 功能

| 功能 | 说明 |
|------|------|
| 创建分身 | 创建一个新的独立 session，可指定 label |
| 列出分身 | 显示当前 agent 的所有 session |
| 删除分身 | 归档并删除指定 session |
| 软切换 | 设置路由目标，后续消息自动转发给指定分身 |
| 退出路由 | 清除路由目标，回到主会话对话模式 |

## 创建分身

使用 `sessions_spawn` 创建独立 session：

```
sessions_spawn(label="<label>", task="等待进一步指令。")
```

**Label 获取方式**：
1. 从用户指令中提取（如"创建一个数据分析分身"→ label="数据分析"）
2. 若无法识别，主动询问用户："请为这个分身提供一个名称："

**示例**：
- 用户："创建一个数据分析分身" → label="数据分析"
- 用户："帮我开一个写文档的分身" → label="写文档"
- 用户："创建分身"（无明确名称）→ 询问用户提供 label

## 列出分身

**重要：只列出活跃的分身，不使用 childSessions 数组（可能有残留记录）。**

从 `sessions.json` 中筛选以 `agent:<agentId>:subagent:` 开头的条目，这些才是实际存在的活跃分身：

```
读取 ~/.openclaw/agents/main/sessions/sessions.json
筛选 key 以 "agent:main:subagent:" 开头的条目
```

**不要使用 sessions_list 的 childSessions 数组**，因为它可能包含已删除 session 的残留记录。

## 删除分身

使用 Gateway RPC `sessions.delete` 删除 session：

**CLI 命令**：
```bash
openclaw gateway call sessions.delete --params '{"key": "<sessionKey>", "deleteTranscript": true}'
```

**流程**：
1. 确认删除：询问用户确认
2. 执行 CLI 命令删除
3. 说明结果：已归档 transcript 并删除 session 条目

**返回示例**：
```json
{
  "ok": true,
  "key": "agent:main:subagent:xxx",
  "deleted": true,
  "archived": ["/path/to/transcript.jsonl.deleted.<timestamp>"]
}
```

**注意**：
- 删除操作会归档 transcript 文件（重命名为 `.jsonl.deleted.<timestamp>`）
- 删除后 session 从列表中移除，transcript 文件保留可恢复

## 工作流程

### 创建分身流程

1. 识别或询问 label
2. 调用 `sessions_spawn` 创建 session
3. 返回新 session 的 key 给用户

### 列出分身流程

1. 读取 `~/.openclaw/agents/main/sessions/sessions.json`
2. 筛选 key 以 `agent:main:subagent:` 开头的条目
3. 以表格形式展示：label | key | 更新时间

**注意**：不要使用 sessions_list 的 childSessions 数组，因为它可能包含已删除 session 的残留记录。

### 删除分身流程

1. 列出分身供用户选择
2. 确认删除意向
3. 执行删除（需要通过 Gateway RPC 或引导用户在 Control UI 操作）
4. 返回操作结果

## 使用示例

**创建分身**：
```
用户：创建一个数据分析分身
助手：好的，正在创建"数据分析"分身...
[sessions_spawn(label="数据分析", task="等待指令")]
助手：已创建分身"数据分析"，session key: agent:main:subagent:xxx
```

**列出分身**：
```
用户：列出我的分身
助手：
| 标签 | Session Key | 最后更新 |
|------|-------------|----------|
| 数据分析 | agent:main:subagent:abc123 | 2026-04-03 12:00 |
| 文档助手 | agent:main:subagent:def456 | 2026-04-03 11:30 |
```

**删除分身**：
```
用户：删除数据分析分身
助手：确认要删除分身"数据分析"吗？这将归档对话记录并移除分身。
用户：确认
助手：已删除分身"数据分析"，对话记录已归档。
```

## 与 Main Session 的区别

| 特性 | Main Session | 分身 Session |
|------|-------------|--------------|
| MEMORY.md | ✅ 加载 | ❌ 不加载 |
| 对话历史 | 独立 | 独立 |
| 访问方式 | 直接对话 | sessions_send |
| 创建方式 | 默认存在 | sessions_spawn |

分身 session 不加载 MEMORY.md，适合处理独立的、不需要个人长期记忆的任务。

## 软切换（路由模式）

软切换是一种"路由模式"：不真正切换 session，而是将后续消息自动转发给指定分身，再把分身回复返回给用户。

### 路由状态存储

路由状态保存在 `<WORKSPACE>/session-manager.state.json`：

```json
{
  "targetSessionKey": "agent:main:subagent:xxx",
  "targetLabel": "测试",
  "updatedAt": "2026-04-03T13:42:00+08:00"
}

### 切换分身

用户指令："切换分身 xxx" 或 "切换到 xxx"

**流程**：
1. 识别目标分身 label
2. 查找对应的 session key
3. 写入 `session-manager.state.json`
4. 告知用户已进入路由模式

**示例**：
```
用户：切换分身测试
助手：已切换到"测试"分身，后续消息会自动转发给它。
```

### 消息转发

当路由状态存在时，收到普通消息的处理流程：

1. 读取 `session-manager.state.json` 获取目标 session key
2. 用 `sessions_send` 转发消息给目标分身
3. 等待分身回复
4. 将回复发送给用户

**注意**：如果消息包含 `#分身名` 后缀，则临时切换目标（不更新 `session-manager.state.json`）。

### ⚠️ 路由静默规则

**一旦进入路由模式，主会话只做转发，不产生任何多余回复。**

| 场景 | 主会话行为 |
|------|----------|
| 用户发送普通消息 | 仅转发，不添加任何前缀/后缀/说明 |
| 分身回复到达 | 仅展示分身回复内容，不加任何解释 |
| 路由命令（切换/列出等） | 正常回复，因为这是管理操作 |

**正确示例**：
```
用户：你好
[sessions_send 给分身]
助手：（直接展示分身回复，无任何附加说明）
> 你好主人！我是测试分身，有什么需要帮忙的吗？
```

**错误示例**（禁止）：
```
用户：你好
助手：我帮你转发给测试分身...
[sessions_send]
助手：测试分身回复如下：
> 你好主人！
```

**核心原则**：用户感觉像在直接和分身对话，主会话是透明的路由器。

### 退出路由

用户指令："切换回来"、"退出分身"、"回到主会话"

**流程**：
1. 删除 `session-manager.state.json`
2. 告知用户已退出路由模式

**示例**：
```
用户：切换回来
助手：已退出路由模式，现在直接和我对话。
```

### Session Startup 检查

每次 session 启动时，检查 `session-manager.state.json` 是否存在：
- 如果存在：告知用户当前处于路由模式，正在转发给哪个分身
- 如果不存在：正常对话