# feishu-send-message Skill

飞书多 Agent 消息发送技能。让 Ass/Ops 用自己的飞书应用发送消息（群聊/私聊），解决 open_id 应用隔离问题。

## 核心功能

- 使用当前 Agent 的飞书凭证发送消息
- 支持群聊和私聊两种模式
- 飞书显示对应的机器人名字（如"小助手"或"运维助手"）

## 使用场景

- Boss 派发任务后，Ass/Ops 用自己的身份回复消息
- 需要显示不同机器人名字的场景

## 使用方法

### 方法 1：直接使用脚本

```bash
# 获取用户 open_id（从当前 Agent 网关日志）
journalctl --user -u openclaw-gateway-ass.service | grep "received message from"

# Ass 发送私聊消息
/home/admin/.openclaw/workspace-ass/skills/feishu-send-message/send.sh \
 ass <open_id> open_id "消息内容"

# Ass 发送群聊消息
/home/admin/.openclaw/workspace-ass/skills/feishu-send-message/send.sh \
 ass oc_88fbbe55e37eca3c3339b2f4bae1a8a9 chat_id "群聊消息"

# Ops 发送私聊消息
/home/admin/.openclaw/workspace-ops/skills/feishu-send-message/send.sh \
 ops <open_id> open_id "运维消息"
```

### 方法 2：直接使用 curl 命令

```bash
# 读取当前 Agent 配置（以 Ass 为例）
APP_ID=$(jq -r '.channels.feishu.appId' ~/.openclaw/openclaw-ass.json)
APP_SECRET=$(jq -r '.channels.feishu.appSecret' ~/.openclaw/openclaw-ass.json)

# 获取 token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/ \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')

# 发送私聊消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"ou_xxx\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"消息内容\\\"}\"}"

# 发送群聊消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"oc_xxx\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"群聊消息\\\"}\"}"
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| **agent** | Agent 类型：`ass` 或 `ops` | `ass` |
| **target** | 目标 ID（open_id 或 chat_id） | `<open_id>` 或 `<chat_id>` |
| **msg_type** | 消息类型：`open_id`（私聊）或 `chat_id`（群聊） | `open_id` |
| **message** | 消息内容 | `你好，这是测试消息` |

## 关键参数参考

| 参数 | Ass 值 | Ops 值 | 说明 |
|------|--------|--------|------|
| **App ID** | `cli_a924c897d4b89ceb` | `cli_a924d0d16bf99cee` | 当前 Agent 应用的 ID |
| **App Secret** | 从配置文件读取 | 从配置文件读取 | 当前 Agent 应用的密钥 |
| **用户 open_id** | 从日志获取 | 从日志获取 | 当前 Agent 应用中的用户 ID |
| **群聊 chat_id** | `oc_88fbbe55e37eca3c3339b2f4bae1a8a9` | 同左 | 群聊 ID（应用通用） |

## 获取用户 open_id

从当前 Agent 网关日志获取：

```bash
# Ass
journalctl --user -u openclaw-gateway-ass.service | grep "received message from"

# Ops
journalctl --user -u openclaw-gateway-ops.service | grep "received message from"
```

## 注意事项

1. **open_id 是应用隔离的**：
   - 每个应用有独立的用户 ID 体系
   - 必须使用当前 Agent 应用中的 open_id 发送私聊消息

2. **chat_id 是应用通用的**：
   - 同一个群聊，不同应用看到的是同一个 chat_id
   - 可以直接使用

3. **content 格式**：
   - 必须是**转义的 JSON 字符串**：`"{\"text\":\"消息内容\"}"`
   - 不是嵌套对象

4. **配置文件位置**：
   - Ass: `~/.openclaw/openclaw-ass.json`
   - Ops: `~/.openclaw/openclaw-ops.json`
   - Boss: `~/.openclaw/openclaw-boss.json`

## 自动化脚本

脚本位置：`/home/admin/.openclaw/workspace-{agent}/skills/feishu-send-message/send.sh`

```bash
#!/bin/bash
# 参数：$1=agent (ass/ops), $2=target (open_id 或 chat_id), $3=msg_type (open_id/chat_id), $4=message

AGENT=$1
TARGET=$2
MSG_TYPE=$3
MESSAGE=$4

# 读取配置
APP_ID=$(jq -r ".channels.feishu.appId" ~/.openclaw/openclaw-${AGENT}.json)
APP_SECRET=$(jq -r ".channels.feishu.appSecret" ~/.openclaw/openclaw-${AGENT}.json)

# 获取 token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/ \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')

# 发送消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${MSG_TYPE}" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"$TARGET\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"$MESSAGE\\\"}\"}" | jq '.data.message_id'
```
