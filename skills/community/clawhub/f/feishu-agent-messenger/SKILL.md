# Feishu Agent Messenger - 飞书消息发送技能

🚀 **下载就能用！脚本可直接运行，自动读取配置文件。**

**注意**：技能本身不会自动回复消息，需要手动调用脚本或配置自动触发 hook。

飞书多 Agent 消息发送技能。让每个 Agent 用自己的飞书应用发送消息（群聊/私聊），解决 open_id 应用隔离问题。配合多网关架构实现自主协作：统筹 Agent 派发任务 → 执行 Agent 完成任务 → 自主调用本技能汇报结果。

---

## 📋 核心功能

- ✅ 使用当前 Agent 的飞书凭证发送消息
- ✅ 支持群聊和私聊两种模式
- ✅ 飞书显示当前 Agent 的机器人名字
- ✅ 解决 open_id 应用隔离问题
- ✅ **零配置** - 自动从 Agent 配置文件读取飞书凭证
- ✅ **脚本可直接运行** - 无需额外配置

---

## ⚠️ 重要说明

### "下载就能用"的含义

| 功能 | 是否自动 | 说明 |
|------|---------|------|
| 脚本可直接运行 | ✅ 是 | 下载后直接运行 `./send.sh` |
| 自动读取配置 | ✅ 是 | 自动从配置文件读取飞书凭证 |
| 自动回复消息 | ❌ 否 | 需要手动调用脚本 |

### 🚨 调用脚本 ≠ AI 回复

**重要**：
- ❌ **不要通过 AI 回复 sessions_send**（这只是文字回复，不会发送飞书消息）
- ✅ **要调用 send.sh 脚本**发送飞书群消息（这才是真正的发送）

**正确流程**：
1. 收到 Boss 的 sessions_send 消息
2. 执行任务
3. 完成后**调用脚本**：`./send.sh agent-b oc_xxx chat_id "消息内容"`
4. 群里显示消息，发送者为当前 Agent 的机器人名字

**错误示例**：
```
❌ 错误：sessions_send 回复 "任务已完成"
```

**正确示例**：
```bash
✅ 正确：./send.sh agent-b oc_xxx chat_id "任务已完成"
```

### 三种使用方式

**方式 1：手动调用脚本（立即可用）**
```bash
./send.sh agent-b oc_xxx chat_id "消息内容"
```

**方式 2：Boss 派发时明确要求调用（推荐）**
```javascript
sessions_send({
  sessionKey: "agent:agent-b:feishu:direct:ou_xxx",
  message: `【任务派发】
任务内容：检查系统状态

【回复要求】
完成后请调用脚本发送群消息：
./send.sh agent-b oc_xxx chat_id "任务已完成"`,
  timeoutSeconds: 0
})
```

**方式 3：配置自动触发 hook（需要 OpenClaw 支持）**
在 Agent 配置里添加 hook，收到消息时自动调用脚本。

---

## 🔧 配置自动回复（推荐）

### 步骤 1：编辑 Agent 配置文件

**文件位置**：`~/.openclaw/openclaw-{agentId}.json`

**添加 hooks 配置**：

```json
{
  "hooks": {
    "entries": {
      "auto-reply-feishu": {
        "enabled": true,
        "trigger": "message.received",
        "script": "~/.openclaw/workspace-{agentId}/skills/feishu-agent-messenger/send.sh",
        "args": ["{agentId}", "${sender.open_id}", "open_id", "收到您的消息，请稍后"]
      }
    }
  }
}
```

**参数说明**：
- `enabled`: 是否启用
- `trigger`: 触发条件（`message.received` 表示收到消息时）
- `script`: 脚本路径
- `args`: 脚本参数
  - `{agentId}`: Agent 标识（如 `agent-b`）
  - `${sender.open_id}`: 发送者 open_id（自动替换）
  - `open_id`: 消息类型（私聊）
  - `收到您的消息，请稍后`: 回复内容

### 步骤 2：重启 Agent 网关

```bash
systemctl --user restart openclaw-gateway-{agentId}.service
```

### 步骤 3：测试

发送消息给 Agent，检查是否自动回复。

---

## 📖 使用方法

### 方法 1：Boss 派发任务时明确要求调用（推荐）

**统筹 Agent 代码示例**：

```javascript
// 派发给执行 Agent-B
sessions_send({
  sessionKey: "agent:agent-b:feishu:direct:ou_xxx",
  message: `【任务派发】
任务 ID: TASK-001
任务内容：检查系统状态

【回复要求】
完成后请调用 feishu-agent-messenger 技能回复：
./send.sh agent-b ou_xxx open_id "任务已完成，系统运行正常"

【汇报格式】
【任务开始】
【任务完成】- 输出位置：[路径]`,
  timeoutSeconds: 0
})
```

**执行 Agent 收到后**：
1. 执行任务
2. 完成后调用 `send.sh` 脚本回复
3. 消息以 Agent-B 自己的身份发送

---

### 方法 2：定时进度汇报（每 5 分钟）

**统筹 Agent 定时发送指令**：

```javascript
// 每 5 分钟发送一次，要求执行 Agent 汇报进度
setInterval(() => {
  sessions_send({
    sessionKey: "agent:agent-b:feishu:direct:ou_xxx",
    message: `【进度汇报要求】
任务 ID: TASK-001

【汇报要求】
请调用 feishu-agent-messenger 技能汇报当前进度：
./send.sh agent-b oc_xxx chat_id "【进度汇报】TASK-001 - 完成 50%，正在进行中..."`,
    timeoutSeconds: 0
  })
}, 5 * 60 * 1000) // 每 5 分钟
```

**执行 Agent 收到后**：
1. 检查当前任务进度
2. 调用 `send.sh` 脚本汇报进度
3. 消息以 Agent-B 自己的身份发送到群里

---

### 方法 3：直接调用脚本

**Agent-B 发送私聊消息**：
```bash
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b ou_xxx open_id "私聊消息内容"
```

**Agent-B 发送群聊消息（进度汇报）**：
```bash
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b oc_xxx chat_id "【进度汇报】TASK-001 - 完成 50%，正在进行中..."
```

---

### 方法 2：直接调用脚本

**Agent-B 发送私聊消息**：
```bash
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b ou_xxx open_id "私聊消息内容"
```

**Agent-B 发送群聊消息**：
```bash
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b oc_xxx chat_id "群聊消息内容"
```

---

### 方法 2：直接调用脚本

**Agent-B 发送私聊消息**：
```bash
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b ou_xxx open_id "私聊消息内容"
```

**Agent-B 发送群聊消息**：
```bash
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b oc_xxx chat_id "群聊消息内容"
```

**Agent-C 发送私聊消息**：
```bash
~/.openclaw/workspace-agent-c/skills/feishu-agent-messenger/send.sh \
  agent-c ou_xxx open_id "私聊消息内容"
```

**Agent-C 发送群聊消息**：
```bash
~/.openclaw/workspace-agent-c/skills/feishu-agent-messenger/send.sh \
  agent-c oc_xxx chat_id "群聊消息内容"
```

---

### 方法 3：直接调用飞书 API

**发送私聊消息**：
```bash
# 读取当前 Agent 配置
APP_ID=$(jq -r '.channels.feishu.appId' ~/.openclaw/openclaw-{agentId}.json)
APP_SECRET=$(jq -r '.channels.feishu.appSecret' ~/.openclaw/openclaw-{agentId}.json)

# 获取 token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/ \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')

# 发送私聊消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"ou_xxx\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"消息内容\\\"}\"}"
```

**发送群聊消息**：
```bash
# 获取 token（同上）

# 发送群聊消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"oc_xxx\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"消息内容\\\"}\"}"
```

---

## ⚙️ 配置说明

### 下载就能用吗？

**是的！下载后无需额外配置，但需要满足以下条件**：

#### 前置条件（必须）

1. **已配置飞书应用**
   - 在飞书开放平台创建应用
   - 获取 App ID 和 App Secret
   - 在 Agent 配置文件中配置飞书凭证

2. **Agent 配置文件存在**
   - 位置：`~/.openclaw/openclaw-{agentId}.json`
   - 包含飞书配置：`channels.feishu.appId` 和 `channels.feishu.appSecret`

#### 自动回复条件（可选）

如果希望自动回复消息，需要：

1. **配置自动触发 hook**
   - 在 Agent 配置文件中添加 hooks 配置
   - 指定触发条件和脚本路径

2. **Agent 网关运行中**
   - 确保 Agent 网关服务正常运行
   - 飞书 WebSocket 连接正常

---

### 配置文件示例

**Agent 配置文件** (`~/.openclaw/openclaw-{agentId}.json`)：

```json
{
  "agents": {
    "list": [{
      "id": "agent-b",
      "name": "执行助手",
      "workspace": "/home/admin/.openclaw/workspace-agent-b"
    }],
    "defaults": {
      "model": { "primary": "dashscope-coding/qwen3.5-plus" },
      "workspace": "/home/admin/.openclaw/workspace-agent-b"
    }
  },
  "gateway": {
    "port": 19923,
    "auth": {
      "mode": "token",
      "token": "agent-b-token-19923"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "dmPolicy": "open"
    }
  },
  "skills": {
    "entries": {
      "feishu-agent-messenger": {
        "enabled": true
      }
    }
  },
  "hooks": {
    "entries": {
      "auto-reply-feishu": {
        "enabled": true,
        "trigger": "message.received",
        "script": "~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh",
        "args": ["agent-b", "${sender.open_id}", "open_id", "收到您的消息"]
      }
    }
  }
}
```

---

## 📝 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| **agentId** | Agent 标识 | `agent-b` |
| **target** | 目标 ID（open_id 或 chat_id） | `ou_xxx` |
| **msg_type** | 消息类型：`open_id`（私聊）或 `chat_id`（群聊） | `open_id` |
| **message** | 消息内容 | `你好，这是测试消息` |

---

## 🔑 关键参数参考

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **App ID** | 当前 Agent 应用的 ID | 飞书开放平台 |
| **App Secret** | 当前 Agent 应用的密钥 | 飞书开放平台 |
| **用户 open_id** | 当前 Agent 应用中的用户 ID | Agent 网关日志 |
| **群聊 chat_id** | 群聊 ID（应用通用） | 飞书开放平台 |

---

## 🔍 获取用户 open_id

从当前 Agent 网关日志获取：

```bash
journalctl --user -u openclaw-gateway-{agentId}.service | grep "received message from"
```

---

## ⚠️ 注意事项

### 1. open_id 是应用隔离的

- ❌ 不同应用的用户 open_id 不同
- ✅ 必须使用当前 Agent 应用中的 open_id 发送私聊消息
- ✅ chat_id 是应用通用的，可以直接使用

### 2. content 格式

- ✅ 必须是**转义的 JSON 字符串**：`"{\"text\":\"消息内容\"}"`
- ❌ 不是嵌套对象

### 3. 配置文件位置

- Agent-B: `~/.openclaw/openclaw-agent-b.json`
- Agent-C: `~/.openclaw/openclaw-agent-c.json`
- 其他 Agent: `~/.openclaw/openclaw-{agentId}.json`

---

## 🧪 测试流程

### 步骤 1：测试脚本

```bash
# 发送群聊测试消息
~/.openclaw/workspace-agent-b/skills/feishu-agent-messenger/send.sh \
  agent-b oc_xxx chat_id "测试：Agent-B 以自己的身份发送群聊消息"
```

**预期结果**：
- ✅ 输出 "发送成功！"
- ✅ 飞书群里显示消息，发送者为当前 Agent 的机器人名字

### 步骤 2：测试自动回复

**配置 hook 后**，发送消息给 Agent。

**预期结果**：
- ✅ Agent 自动回复消息
- ✅ 日志里显示脚本执行记录

---

## 📚 相关技能

- **setup-multi-gateway** - 多网关配置，配合本技能实现多 Agent 协作
- **skill-vetter** - 技能安全审查，安装前自动检查

---

## 🆘 常见问题

### Q1: 发送失败，提示"配置文件不存在"
**A**: 检查 Agent 配置文件是否存在：
```bash
ls -la ~/.openclaw/openclaw-{agentId}.json
```

### Q2: 发送失败，提示"无法获取 token"
**A**: 检查飞书配置是否正确：
```bash
jq '.channels.feishu.appId' ~/.openclaw/openclaw-{agentId}.json
jq '.channels.feishu.appSecret' ~/.openclaw/openclaw-{agentId}.json
```

### Q3: 消息发送成功，但显示的是其他 Agent 的身份
**A**: 确保使用的是当前 Agent 的脚本和配置，不是其他 Agent 的。

### Q4: open_id 发送失败
**A**: 确保使用的是当前 Agent 应用中的 open_id，不是其他 Agent 的 open_id。

### Q5: 下载后不知道怎么用
**A**: 
1. 确保已配置飞书应用（App ID 和 App Secret）
2. 确保 Agent 配置文件存在
3. 测试脚本：`./send.sh agent-b oc_xxx chat_id "测试"`
4. 如果成功，说明配置正确

### Q6: 配置了 hook 但不自动回复
**A**: 
1. 检查 hook 配置是否正确
2. 检查 Agent 网关是否重启
3. 查看日志：`journalctl --user -u openclaw-gateway-{agentId}.service -f`
4. 确认触发条件是否匹配

---

## 📝 更新日志

### v1.0.2 (2026-03-20)
- 添加"配置自动回复"章节
- 详细说明 hook 配置方法
- 添加常见问题 Q6
- 明确说明"下载就能用"的含义

### v1.0.1 (2026-03-20)
- 去掉 Boss/Ass/Ops 等本地 Agent 名称，改用通用名称
- 明确说明"下载就能用"的含义和前置条件
- 添加配置说明章节
- 添加常见问题 Q5: 下载后不知道怎么用
- 优化文档结构，更清晰易懂

### v1.0.0 (2026-03-20)
- 初始版本
- 支持多 Agent 发送消息
- 支持群聊和私聊两种模式
- 自动从配置文件读取飞书凭证
- 支持 sessions_send 自动调用
- 添加完整使用流程说明
- 添加测试流程和常见问题解答
