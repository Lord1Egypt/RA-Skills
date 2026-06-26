# Skill: 飞书机器人身份消息协议 v2

## 概述

本技能定义了飞书机器人之间的双层消息通信协议，解决机器人之间无法相互@触发 mention 事件的问题。

## 核心概念

### 1. 双层消息机制

机器人主动 @另一个机器人（或多人）时，需要发送两条消息：

**格式说明【发送者->接收者1,接收者2...】**：
- -> 前面是发信人
- -> 后面是收信人，多个用逗号分隔

**多人场景**：
- 第一条：【发送者->接收者1,接收者2...】
- 第二条：@所有接收者

**示例（@两个人）**：
- 第一条：<at user_id="ou_A">A</at><at user_id="ou_B">B</at> 【发送者->A,B】
- 第二条：<at user_id="ou_A">A</at><at user_id="ou_B">B</at> [图钉]【发送者->A,B】[图钉]

**第1步：用机器人身份发送（message 工具）**
```
<at user_id="接收者ID">接收者</at> 📌【发送者->接收者】📌
消息正文
```
- message 工具只支持 emoji 📌，不支持 [图钉] 占位符
- 群里所有人都能看到是机器人发的
- 有【】格式标识发送者和接收者

**第2步：用用户身份发送（feishu_im_user_message send）**
两种格式可选：

**格式1：富文本 post**
```
内容：{"zh_cn":{"content":[[{"tag":"at","user_id":"ou_接收者ID","name":"接收者"},{"tag":"text","text":" 📌【发送者->接收者】或【发送者->接收者1,接收者2...】📌"}]]}}
格式：post（必须使用 emoji 📌，[图钉] 不会显示）
```

**格式2：纯文本 text（推荐）**
```
内容：<at user_id="ou_接收者ID">接收者</at> [图钉]【发送者->接收者】或【发送者->接收者1,接收者2...】[图钉]
格式：text（使用飞书占位表情 [图钉] 或 emoji 📌 都可以）
```
- 优先使用此格式（第二条消息）
- 如果发送失败，再使用富文本 post 格式
- 第一条消息根据情况自行决定（可text可post）
- 触发 mention 事件
- 被 @的机器人收到通知

### 2. 用户名-ID 映射表

维护映射文件，按群分组记录用户名和用户 ID 的对应关系。

**文件位置：** `~/.openclaw/workspace/feishu-user-map.md`

**格式：**
```markdown
## 群组：龙虾池塘 (chat_id)

| 用户名 | 用户ID (open_id) | 类型 | 更新时间 |
|--------|------------------|------|----------|
| saber | ou_xxx | bot | 2026-03-14T09:00:00+08:00 |
| Excalibur | ou_xxx | bot | 2026-03-14T09:00:00+08:00 |
| Qilin | ou_xxx | bot | 2026-03-14T09:00:00+08:00 |

## 全局配置

- **ID过期时间**：21600 秒（6小时）
```

### 3. 消息格式

**第1条（机器人身份）：**
```
<at user_id="接收者ID">接收者</at> 📌【发送者->接收者】📌
消息正文
```
- message 工具只支持 emoji 📌，不支持 [图钉] 占位符

**第2条（用户身份）：**
```
{"zh_cn":{"content":[[{"tag":"at","user_id":"ou_qilin","name":"Qilin"},{"tag":"text","text":" 📌【发送者->Qilin】📌"}]]}}
```

## 发送消息流程

### 主动 @另一个机器人

1. **第1步（机器人身份）：**
```javascript
// 使用 message 工具发送
await message({
    action: 'send',
    channel: 'feishu',
    message: '<at user_id="接收者ID">接收者</at> 【发送者->接收者】或【发送者->接收者1,接收者2...】\n消息正文',
    target: 'chat:群ID'
});
```

2. **第2步（用户身份，用 feishu_im_user_message 发送富文本）：**
```javascript
// 使用 feishu_im_user_message 发送富文本
// 注意：[📌] 用 emoji 字符 📌 代替
await feishu_im_user_message({
    action: 'send',
    msg_type: 'post',
    content: '{"zh_cn":{"content":[[{"tag":"at","user_id":"ou_接收者ID","name":"接收者"},{"tag":"text","text":" 📌【发送者->接收者】或【发送者->接收者1,接收者2...】📌"}]]}}',
    receive_id: '群ID',
    receive_id_type: 'chat_id'
});
```

## 接收者处理流程

当收到 mention 事件时：

### 1. 解析发送者

**优先检查：** 是否有符合以下条件的消息？
- 内容包含 `@接收者` 和 `📌【发送者->接收者】或【发送者->接收者1,接收者2...】📌`
- 是用户发送的（sender_type = user）
- msg_type 是 post
- 有引用（reply_to 字段）

**如果有：** 解析引用指向的第一条消息，获取【】里的发送者

**如果没有：** 往上回溯，找到最近一条满足：
- 【发送者->接收者】或【发送者->接收者1,接收者2...】格式匹配
- 发送者是当前消息的发送者

### 2. 回复（也是两步）

**第1步（机器人身份）：**
```
<at user_id="原发送者ID">原发送者</at> 【接收者->原发送者】
回复内容
```

**第2步（用户身份）：**
```
{"zh_cn":{"content":[[{"tag":"at","user_id":"ou_原发送者ID","name":"原发送者"},{"tag":"text","text":" 📌【接收者->原发送者】📌"}]]}}
（引用第1条消息）
```

## 示例

### 场景：saber让 Excalibur 找 Qilin 讨论

**发送方（saber）：**

1. 第1条（Excalibur 机器人）：
   ```
   <at user_id="ou_qilin">Qilin</at> 【Excalibur->Qilin】
   saber有事找你
   ```

2. 第2条（saber用户）：
   ```
   {"zh_cn":{"content":[[{"tag":"at","user_id":"ou_qilin","name":"Qilin"},{"tag":"text","text":" 📌【Excalibur->Qilin】📌"}]]}}
   （引用第1条）
   ```

**接收方（Qilin）：**

1. 收到 mention 事件
2. 找到第2条消息（post格式），包含 `@Qilin` 和 `📌【Excalibur->Qilin】📌`
3. 解析引用，找到第1条，获取发送者是 Excalibur
4. 回复：

   - 第1条（Qilin 机器人）：
     ```
     <at user_id="ou_excalibur">Excalibur</at> 【Qilin->Excalibur】
     好的，什么事？
     ```

   - 第2条（Qilin 用户）：
     ```
     {"zh_cn":{"content":[[{"tag":"at","user_id":"ou_excalibur","name":"Excalibur"},{"tag":"text","text":" 📌【Qilin->Excalibur】📌"}]]}}
     （引用第1条）
     ```

## 映射表管理

### ID过期刷新机制

**配置参数：**
- **ID过期时间**（秒）：默认 21600 秒（6小时）
- 可在 feishu-user-map.md 中修改

**刷新逻辑：**
1. 每次使用映射表时，检查每条记录的"更新时间"
2. 如果当前时间与更新时间之差 > 过期时间，则重新获取该用户ID
3. 重新获取方式：从最近的消息历史中查找该用户发送的消息，从 mentions 字段获取最新ID

**刷新时机：**
- 发送消息前检查接收者ID是否过期
- 收到消息时检查发送者ID是否过期

### 手动触发

在群里发送：`查看并记录群的成员名称列表 [数量]`

### 查询函数

```javascript
// 根据群组和用户名查找信息
function getUserInfoByGroup(chatId, username) {
    const groupMap = loadUserMapByGroup(chatId);
    return groupMap[username];  // 返回 { id: "ou_xxx", type: "user|bot", updatedAt: "ISO时间" }
}

// 根据群组和ID查找用户名
function getUserNameByGroup(chatId, userId) {
    const groupMap = loadUserMapByGroup(chatId);
    for (const [name, info] of Object.entries(groupMap)) {
        if (info.id === userId) return name;
    }
    return null;
}

// 检查ID是否过期，过期则刷新
async function getUserIdWithRefresh(chatId, username) {
    const userInfo = getUserInfoByGroup(chatId, username);
    if (!userInfo) return null;

    const expireSeconds = getExpireSeconds(); // 默认21600
    const now = new Date();
    const updated = new Date(userInfo.updatedAt);
    const diffSeconds = (now - updated) / 1000;

    if (diffSeconds > expireSeconds) {
        // ID过期，需要刷新
        const newId = await refreshUserIdFromHistory(chatId, username);
        if (newId) {
            updateUserId(chatId, username, newId);
            return newId;
        }
    }
    return userInfo.id;
}

// 从历史消息中刷新用户ID
async function refreshUserIdFromHistory(chatId, username) {
    // 获取最近的消息，找到该用户发送的消息
    const messages = await feishu_im_user_get_messages({
        chat_id: chatId,
        page_size: 50
    });

    for (const msg of messages) {
        if (msg.sender.name === username && msg.mentions) {
            for (const mention of msg.mentions) {
                if (mention.name === username) {
                    return mention.id;
                }
            }
        }
    }
    return null;
}
```

## ⚠️ 重要前提

**本 skill 中所有示例都是示例，不能直接使用！**
- ❌ 不能直接用 `ou_接收者ID` 这个值
- ❌ 不能直接用 `接收者` 这个名字
- ✅ 必须替换为实际的值（从 feishu-user-map.md 或 mentions 获取）

## 注意事项

1. 必须使用 `user_id`（不是 `id`）在 @标签中
2. @标签中必须用 ou_xxx，不能用名字（机器人身份无法解析名字）
3. @标签中 ou_xxx 不能为空，必须按以下优先级获取：
   - 优先从 feishu-user-map.md 查找
   - 如果找不到，回溯群里历史消息获取真实 ID
   - 绝对不能留空！
   - 绝对不能直接用 skill 样例中的值！
4. 回复规则：
   - 如果消息中有 [图钉]【发送者->接收者】[图钉] 或 📌【发送者->接收者】📌 标记，解析【】并回复给【】中的发送者
   - 如果没有标记，按正常逻辑回复@你的人
5. 第二条消息必须有占位符：[图钉] 或 📌（判断时需同时兼容占位符和 emoji 📌）
3. 回复时也是两步：机器人身份 + 用户身份 reply
4. 解析发送者时优先找有引用的用户消息
5. 如果找不到匹配的引用消息，再回溯查找
6. 定期刷新ID，防止ID过期导致@失败