# feishu-group-helper

飞书群管理 skill。用于维护群信息、处理群事件、发送群消息。

## 触发条件

- 用户提到"飞书群管理"、"群信息"、"加入群"、"移出群"
- 用户要求"发消息到群里"或"发送群消息"
- ~~飞书事件：bot 被加入群、bot 被移出群~~（需升级）

## 核心功能

### 1. 群信息维护

群信息文件：各 agent 的 workspace 下 `~/openclaw/workspace/feishu-groups.json`

**注意：** 每个 agent 的群信息独立维护，存储在该 agent 的 workspace 目录下。

记录格式：
```json
{
  "groups": {
    "oc_xxx": {
      "chat_id": "oc_xxx",
      "name": "群名称",
      "member_count": 5,
      "added_at": "2026-01-01T00:00:00Z",
      "removed_at": null,
      "status": "active"
    }
  }
}
```

### 2. 记录新群

当 bot 被加入群或被要求记住群时：
1. 调用 `feishu_chat` 获取群信息
2. 调用 `addGroup(chatId, name, memberCount)` 添加到当前 agent 的群信息文件

### 3. 更新群信息

当 bot 被移出群或被要求注销群时：
1. 调用 `removeGroup(chatId)` 标记为已移除

### 4. 发送群消息

**用户指定群名：**
1. 用 `findGroupByName(name)` 查找群
2. 用 `isInGroup(chatId)` 确认在群里
3. 用 `message` 发送消息到 `chat:xxx`

**用户未指定群：**
1. 用 `getActiveGroups()` 获取活跃群列表
2. 列出群名让用户确认

### 5. 查看群信息

**查看所有群：**
1. 用 `listAllGroups()` 获取所有群信息（含状态）
2. 用 `getActiveGroups()` 获取仅活跃群

**查看 bot 在哪些群：**
1. 调用飞书 API 获取 bot 所在的所有群
2. 与记录中的群对比

## 事件监听（需升级）

### 需要的飞书权限

需要在飞书开放平台添加以下权限：
- `im:chat.memberbot.created` - 机器人被添加到群
- `im:chat.memberbot.deleted` - 机器人被移出群
- `im:chat.members:bot_access` - 已有的

### 事件类型

| 事件 | 说明 | 处理 |
|------|------|------|
| `im.chat.member_bot.created` | bot 被添加到群 | 自动调用 `addGroup()` |
| `im.chat.member_bot.deleted` | bot 被移出群 | 自动调用 `removeGroup()` |

### 升级步骤

1. 在飞书开放平台配置事件订阅
2. 设置回调 URL（需要公网域名）
3. 在 OpenClaw 中添加事件处理能力
4. 更新本 skill 支持自动处理

## 飞书权限说明

### 当前已拥有权限

| 权限名称 | 说明 | 用途 |
|----------|------|------|
| `im:chat` | 群聊管理 | 获取群信息 |
| `im:chat.members:bot_access` | 群成员列表 | 查看群成员 |
| `im:message:send_as_bot` | 发消息 | 发送群消息 |
| `im:message.group_msg` | 接收群消息 | 接收群消息 |

### 当前缺少权限（事件监听用）

| 权限名称 | 说明 | 如何获取 |
|----------|------|----------|
| `im:chat.memberbot.created` | 监听入群事件 | 在飞书开放平台申请 |
| `im:chat.memberbot.deleted` | 监听退群事件 | 在飞书开放平台申请 |

### 权限检查

在 OpenClaw 中检查权限：
```javascript
feishu_app_scopes()
```

### 权限申请引导

如需开启事件监听功能，请按以下步骤操作：

1. **登录飞书开放平台** https://open.feishu.cn/
2. **进入应用** → 选择你的应用
3. **添加权限** → 搜索并添加：
   - `im:chat.memberbot.created`
   - `im:chat.memberbot.deleted`
4. **发布新版本** → 提交审批
5. **配置事件订阅** → 设置回调 URL（需公网域名）

### 事件订阅配置（进阶）

配置回调 URL 后，飞书会 POST 事件到你的服务器：

```json
// 机器人被添加入群事件
{
  "schema": "2.0",
  "header": {
    "event_type": "im.chat.member_bot.created"
  },
  "event": {
    "chat_id": "oc_xxx",
    "operator_id": "ou_xxx"
  }
}

// 机器人被移出群事件
{
  "schema": "2.0",
  "header": {
    "event_type": "im.chat.member_bot.deleted"
  },
  "event": {
    "chat_id": "oc_xxx",
    "operator_id": "ou_xxx"
  }
}
```

收到事件后调用：
- 入群：`addGroup(chatId, name, memberCount)`
- 退群：`removeGroup(chatId)`

## 工具使用

```javascript
// 添加群
const { addGroup } = require('./scripts/groupManager.js');
addGroup('oc_xxx', '群名', 5);

// 移除群
const { removeGroup } = require('./scripts/groupManager.js');
removeGroup('oc_xxx');

// 查找群
const { findGroupByName } = require('./scripts/groupManager.js');
findGroupByName('GoGoGo');

// 获取活跃群
const { getActiveGroups } = require('./scripts/groupManager.js');
getActiveGroups();

// 检查是否在群
const { isInGroup } = require('./scripts/groupManager.js');
isInGroup('oc_xxx');

// 查看所有群（含状态）
const { listAllGroups } = require('./scripts/groupManager.js');
listAllGroups();
```
