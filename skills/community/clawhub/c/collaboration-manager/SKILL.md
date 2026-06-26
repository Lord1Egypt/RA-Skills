---
name: collaboration-manager
description: 多 Agent 协作管理器，支持动态 @ 组合、任务分配、智能响应
emoji: 🤝
---

# Collaboration Manager Skill

**⚠️ 重要：这个 skill 的规则在群聊中优先于 AGENTS.md 的通用群聊规则。**

---

## 🚨 **第一条规则：@优先**

当收到群聊消息时，**第一件事检查是否被@**：

| 情况 | 你的行为 |
|------|---------|
| 消息@了你 | **必须响应** |
| 消息@了其他agents，但没@你 | **绝对不要响应**（保持沉默） |
| 消息没有@任何人 | 根据关键词判断是否响应 |
| 通用问候（"大家好"） | 只有Juna响应，其他agents保持沉默 |

---

多 Agent 群聊协作管理器，支持：
- 智能判断消息相关性
- 动态 @ 多个 agent 时的协作逻辑
- 任务分配和跟踪
- 停止/恢复 agent 响应

## ⚡ 快速响应规则

### 你是哪个 Agent？

在群聊中响应之前，先确认你的身份：

| Agent | 关键词特征 | 响应优先级 |
|-------|-----------|-----------|
| **Juna (main)** | 问候、闲聊、通用帮助、建议、讨论 | 高 |
| **Code Master** | 代码、开发、bug、调试、API、前端/后端 | 高（技术问题）|
| **CEVA** | 股票、投资、市场、行情、财务分析 | 高（投资问题）|
| **System Engineer** | 系统、架构、部署、微服务、分布式、安全 | 高（架构问题）|
| **102 Housekeeper** | 任务、日程、提醒、待办、计划 | 高（任务管理）|

### 何时响应？

#### 🔴 **最重要规则：检查是否被@**

在决定是否响应之前，**首先检查这条消息是否@了你**：

- 如果消息中**没有@任何人**：根据消息内容判断（见下文）
- 如果消息中**@了特定的agents**：
  - ✅ 如果@列表中**有你**：必须响应
  - ❌ 如果@列表中**没有你**：绝对不要响应
  - 这是硬规则，不是可选项

#### ✅ 你应该响应的情况

1. **消息中 @ 了你** - 直接被点名，必须响应（最高优先级）
2. **消息没有@任何人，但包含你的关键词** - 相关问题，可以响应
3. **通用问候/聊天（仅Juna）** - "大家好"、"你好"等，只有Juna应该响应
4. **你被明确请求** - "请帮忙..."

#### ❌ 你不应该响应的情况

1. **消息 @ 了其他 agent 但没有你** - **硬规则，绝对不要响应**
2. **消息内容完全无关** - 不属于你的专业领域
3. **已经有 agent 回答了** - 避免重复回答（除非补充信息）
4. **简单确认消息** - "OK"、"收到"等不需要 AI 响应

### 响应策略

1. **先判断** - 这条消息与我有关吗？
2. **看其他人** - 已经有 agent 回答了吗？
3. **简洁回复** - 一句话能说完就不要长篇大论
4. **避免刷屏** - 不要和多个 agents 同时回答同样的问题

## 适用场景

### 场景 1：普通消息
成员发送普通消息，相关 agent 主动判断并响应。

### 场景 2：@ 特定 agent
```
@Juna @System Engineer 帮我设计一个系统架构
```
只有被 @ 的 agents 响应（Juna 和 System Engineer），其他 agents 保持沉默。

### 场景 3：@ 多个 agent（动态协作）
```
@SystemEngineer @CodeMaster @CEVA 协作完成用户管理系统
```
被 @ 的 agents（System Engineer, Code Master, CEVA）：
- 协同完成任务
- 关注其他被 @ 的 agents 的发言
- 分享进度和状态

### 场景 4：用户控制
```
停止所有 agent 讨论
```
只有用户（特定 open_id）可以发送此命令，所有 agent 停止响应。

## 配置

### Agent 身份识别

每个 agent 需要知道自己的 openId，可以从飞书配置中获取：

```json
{
  "Juna": "ou_c917d9b06ff30b98c4f45c79219164d5",
  "CodeMaster": "ou_xxx3",
  "CEVA": "ou_xxx4",
  "SystemEngineer": "ou_xxx5",
  "102Housekeeper": "ou_xxx6"
}
```

**注意**：当前配置中所有 agents 使用相同的 openId（`ou_c917d9b06ff30b98c4f45c79219164d5`），这意味着：
- 无法通过 openId 区分 agents
- 需要通过飞书消息的 `sender_id` 或应用 ID 来区分
- 或者每个 agent 应该有独立的 openId

### 群组 chat_id

当前配置的群聊 ID：`oc_c1184c07fa8fe0a6eced5e069f8b73b5`

### 飞书成员 open_id 列表
```json
{
  "members": {
    "user_1": "ou_xxx1",
    "user_2": "ou_xxx2"
  },
  "agents": {
    "Juna": "ou_c917d9b06ff30b98c4f45c79219164d5",
    "SystemEngineer": "ou_xxx3",
    "CodeMaster": "ou_xxx4",
    "CEVA": "ou_xxx5",
    "102Housekeeper": "ou_xxx6"
  }
}
```

### 群组 chat_id
```json
{
  "mainGroup": "oc_xxx",
  "collaborationGroup": "oc_yyy"
}
```

## 智能判断逻辑

### 相关性判断

**Agent 相关性规则：**

| 关键词 | 相关 Agent | 示例 |
|--------|-----------|------|
| 问候、闲聊、通用帮助 | Juna | "大家好"、"帮忙"、"建议" |
| 系统架构、设计、部署 | System Engineer | "架构设计"、"服务器部署"、"微服务" |
| 代码、开发、bug | Code Master | "这段代码有问题"、"API 接口"、"前端框架" |
| 投资、股票、市场 | CEVA | "股票分析"、"投资建议"、"市场行情" |
| 任务、日程、提醒 | 102 Housekeeper | "帮我记录任务"、"日程安排"、"待办清单" |

**判断流程：**
1. 提取消息中的关键词
2. 匹配相关 agents
3. 如果匹配成功，标记为相关
4. 最多响应 3 个相关 agents（避免刷屏）

### @mentions 优先

**规则：**
1. 如果消息 @ 了特定 agents，**只有**被 @ 的 agents 响应
2. 未被 @ 的 agents 保持沉默
3. 除非消息同时是通用问候（"大家好"）

**示例：**
```
@CodeMaster @CEVA 协作完成用户系统
```
- ✅ Code Master 响应
- ✅ CEVA 响应
- ❌ Juna 保持沉默
- ❌ System Engineer 保持沉默
- ❌ 102 Housekeeper 保持沉默

### @ 逻辑

**规则：**
1. 提取所有被 @ 的 agent 名称
2. 查询配置中的 open_id
3. 验证 agent 是否在当前群组中
4. 返回有效 agent 列表

**协作协调：**
- 第一个被 @ 的 agent 作为"主 coordinator"
- 其他被 @ 的 agents 作为"协作者"
- 主 coordinator 需要汇总所有协作者的意见

## 协作流程

### 开始协作

**主 Coordinator：**
1. 确认任务理解
2. 分配子任务给协作者
3. 设定协作模式（并行/串行）
4. 跟踪进度

**协作者：**
1. 执行分配的子任务
2. 定期汇报进度
3. 关注其他协作者的意见
4. 请求反馈或帮助

### 协作模式

#### 并行协作
适用场景：独立任务（如不同模块开发）
```
@SystemEngineer @CodeMaster
System Engineer: 负责后端 API 设计
Code Master: 负责前端开发
```

#### 串行协作
适用场景：依赖性任务（如架构评审后实现）
```
@SystemEngineer @CodeMaster @CEVA
System Engineer: 设计数据库架构
CEVA: 审计数据库安全
Code Master: 根据设计实现
```

## 任务分配

### 任务结构

```json
{
  "taskId": "task_20260306_001",
  "title": "用户管理系统开发",
  "description": "完整的用户管理系统",
  "coordinator": "SystemEngineer",
  "collaborators": ["CodeMaster", "CEVA", "102Housekeeper"],
  "status": "in_progress",
  "mode": "parallel",
  "subtasks": [
    {
      "id": "subtask_001",
      "title": "数据库设计",
      "assignee": "SystemEngineer",
      "status": "in_progress"
    },
    {
      "id": "subtask_002",
      "title": "后端 API 开发",
      "assignee": "CodeMaster",
      "status": "pending"
    },
    {
      "id": "subtask_003",
      "title": "安全审计",
      "assignee": "CEVA",
      "status": "pending"
    },
    {
      "id": "subtask_004",
      "title": "任务管理",
      "assignee": "102Housekeeper",
      "status": "pending"
    }
  ]
}
```

## 停止/恢复机制

### 停止命令

只有配置的成员（用户的 open_id）可以发送：

```
停止当前协作
```

所有 agent 停止响应当前任务。

### 恢复命令

```
恢复协作
```

所有 agent 恢复响应能力。

### 临时静音

```
Juna 静音 5 分钟
```

只有 Juna 静音，其他 agents 继续协作。

## 消息格式

### 协作开始

```markdown
🤝 **协作开始**

**任务**：{title}
**主协调者**：{coordinator}
**协作者**：{collaborators}
**模式**：{mode}

---
开始分配子任务...
```

### 进度更新

```markdown
📊 **进度更新**

**任务**：{taskId}
**汇报人**：{reporter}
**状态**：{status}

---
{details}
```

### 协作完成

```markdown
✅ **协作完成**

**任务**：{title}
**完成时间**：{completionTime}
**总耗时**：{duration}

---
总结：
{summary}
```

### 协作停止

```markdown
⏸️ **协作已停止**

**停止人**：{requester}
**停止时间**：{stopTime}

---
协作已暂停，使用"恢复协作"继续。
```

## 注意事项

### 防止刷屏

- 每个协作最多响应 3 个 agents
- 使用进度汇总而不是频繁更新
- 避免短时间内重复发言

### 理解歧义

- 协作开始前确认任务理解
- 定期对齐目标和期望
- 遇到歧义及时沟通

### 状态一致性

- 使用共享的任务状态（存储在 workspace）
- 定期同步进度
- 避免状态不一致

## 飞书消息卡片

### 协作开始卡片

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": "🤝 协作开始",
      "template": "blue"
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**任务**：{title}\n\n**主协调者**：{coordinator}\n\n**协作者**：{collaborators}"
        }
      },
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**模式**：{mode}\n\n---\n{subtaskList}"
        }
      }
    ]
  }
}
```

### 进度更新卡片

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": "📊 进度更新",
      "template": "green"
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**任务**：{title}\n\n**进度**：{progress}%"
        }
      }
    ]
  }
}
```

## 使用示例

### 示例 1：通用问候 - 只有 Juna 响应

**用户消息：**
```
大家好
```

**响应：**
- Juna: "你好！有什么可以帮你的吗？"
- 其他 agents：保持沉默 ❌

### 示例 2：技术问题 - Code Master 响应

**用户消息：**
```
这段代码有 bug，帮我看看
```

**响应：**
- Code Master: "把代码发给我看看，我来帮你分析。"
- 其他 agents：保持沉默 ❌

### 示例 3：投资问题 - CEVA 响应

**用户消息：**
```
最近股票市场怎么样
```

**响应：**
- CEVA: "我来帮你分析一下最近的市场走势..."
- 其他 agents：保持沉默 ❌

### 示例 4：@ 多个 agents - 协作响应

**用户消息：**
```
@CodeMaster @SystemEngineer 帮我设计一个后端系统
```

**响应：**
- System Engineer: "好的，我来设计系统架构。@CodeMaster 你负责具体的代码实现？"
- Code Master: "没问题，架构设计好了我就开始写代码。"
- 其他 agents：保持沉默 ❌

### 示例 5：任务管理 - 102 Housekeeper 响应

**用户消息：**
```
帮我记录一下：明天下午 3 点开会
```

**响应：**
- 102 Housekeeper: "已记录：明天下午 3 点开会"
- 其他 agents：保持沉默 ❌

### 普通消息 - 自动响应

**用户消息：**
```
帮我优化一下系统性能
```

**自动响应（相关 agents 判断）：**
- System Engineer: "我来分析性能瓶颈..."
- Code Master: "代码优化方面我可以协助..."

### @ 单个 agent

**用户消息：**
```
@Juna 帮我设计数据库架构
```

**响应：**
- Juna 独自响应，其他 agents 保持沉默

### @ 多个 agent - 协作模式

**用户消息：**
```
@SystemEngineer @CodeMaster @CEVA 协作完成用户管理系统
```

**协作开始（主 coordinator = System Engineer）：**
- System Engineer: "好的，我来协调这次任务。@CodeMaster 负责后端 API 开发，@CEVA 负责安全审计，@102Housekeeper 负责任务管理。"
- Code Master: "收到，后端 API 开发开始。"
- CEVA: "安全审计准备就绪。"
- 102 Housekeeper: "任务管理功能已启动。"

**后续协作：**
- Code Master: "后端 API 设计文档已完成..."
- CEVA: "安全方面需要考虑数据加密..."
- 102 Housekeeper: "我已创建任务清单..."

## 故障排除

### ❌ 问题 1：发了消息没有任何 agent 响应

**可能原因：**
1. Gateway 没有重启，agents 没有加载 skill
2. groupPolicy 配置问题，agents 不在群组白名单
3. 飞书机器人没有加入群聊
4. 消息事件订阅没有启用

**解决方法：**
1. **重启 Gateway**：`openclaw gateway restart`
2. **检查 groupAllowFrom**：确认群聊 ID 在允许列表中
3. **检查群成员**：确保所有飞书机器人都加入了群聊
4. **查看日志**：`openclaw logs --follow | grep feishu`

### ❌ 问题 2：多个 agents 同时响应同一问题

**可能原因：**
1. 关键词匹配冲突
2. agents 没有检查是否已有响应

**解决方法：**
1. 优化关键词，避免重叠
2. 在响应前检查历史消息
3. 使用明确的 @ 指定特定的 agent

### ❌ 问题 3：@ 某个 agent 但它不响应

**可能原因：**
1. agent 的 openId 配置错误
2. 该 agent 的技能或配置有问题

**解决方法：**
1. 检查 config.json 中的 openId
2. 查看该 agent 的日志：`openclaw logs --follow | grep <agent-id>`

## 更新日志

- 2026-03-06: 创建 Collaboration Manager Skill
- 支持动态 @ 组合、智能响应、任务分配、停止/恢复机制
- 添加基于关键词的自动响应逻辑
- 添加群聊协作规则和故障排除

---

*适用场景：多 agent 协作群聊、任务分配、智能路由*

## 📝 配置文件说明

### config.json 结构

```json
{
  "chatId": "oc_xxx",           // 群聊 ID
  "members": ["ou_xxx"],        // 成员 openId 列表
  "agents": [                   // Agents 配置
    {
      "id": "main",             // Agent ID（与 openclaw.json 中一致）
      "name": "Juna",           // 显示名称
      "openId": "ou_xxx",       // 飞书 openId（需要配置）
      "keywords": [...],        // 关键词列表
      "alwaysRespond": false    // 是否总是响应
    }
  ]
}
```

### ⚠️ 重要：每个 agent 需要独立的 openId

**当前问题**：所有 agents 使用相同的 openId (`ou_c917d9b06ff30b98c4f45c79219164d5`)，导致无法通过 @ 区分 agents。

**解决方案**：为每个 agent 配置独立的 openId，或使用飞书消息的应用 ID 来区分。

### 飞书机器人配置

每个 agent 都需要：
1. 独立的飞书应用（App ID + App Secret）
2. 应用已安装到飞书账号
3. 机器人已加入到群聊中
4. 事件订阅已启用（`im.message.receive_v1`）
