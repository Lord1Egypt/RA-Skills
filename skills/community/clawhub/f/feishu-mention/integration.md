# FeishuMention Resolver - 集成指南 (v2.0)

## 🎯 核心功能

FeishuMention Resolver 是 OpenClaw 平台中专门用于将 `@name` 自动转换为 `<at>` 标签的技能。
它能够根据 OpenClaw 配置中的账号信息，自动发现并解析机器人和真人用户。

### 处理流程

```mermaid
graph TD
    A[用户输入: "你好 @product"] --> B(查找 Account ID 'product' 配置)
    B -- 找到 --> C(匹配到 Bot ID 'cli_...')
    C --> D(输出: <at user_id="ou_...">product</at>)
    
    A -- 未找到 --> E(查找 Aliases)
    E -- 找到别名 --> F(转换为真实名: "@张三")
    F --> G(查找群成员 Cache/API)
    G --> H(输出: <at user_id="ou_...">张三</at>)
    
    A -- 都未找到 --> I(输出原样 "@product")
```

## 🛠️ 集成方式

### 1. 确保插件已启用

在 `~/.openclaw/openclaw.json` 中：

```json
"plugins": {
  "allow": ["feishu-mention"],
  "entries": {
    "feishu-mention": { "enabled": true }
  }
}
```

### 2. 准备账号凭证

同样在 `~/.openclaw/openclaw.json` 中配置您的飞书账号：

```json
"channels": {
  "feishu": {
    "accounts": {
      "product": {
        "appId": "cli_prod...",
        "appSecret": "..."
      },
      "elves": {
        "appId": "cli_elves...",
        "appSecret": "..."
      }
    }
  }
}
```

### 3. 在 Agent 中调用

无论您的 Agent 是基于 Javascript 还是 Python 编写，只要能调用 `resolve` 工具即可。

**Javascript / Node.js:**

```javascript
const { resolve } = require('@openclaw/skills/feishu-mention'); // 或相对路径

// 在回复消息前调用
const replyText = await resolve(originalText, 'elves', currentChatId);
await sendMessage(replyText);
```

**Python (通过 Skills API):**

```python
# 假设您有一个 Skills wrapper
text = "@product 请查一下这个"
# accountId='elves'
# chatId='oc_123...'
resolved = skills.feishu_mention.resolve(text, "elves", "oc_123...")

# 发送 resolved
```

## 🔑 关键特性 (v2.0)

### 1. 自动机器人发现 (Auto-Discovery)
无需手动维护 ID 映射表。系统启动时会自动扫描 `openclaw.json` 中的所有账号，获取它们的 OpenID。
这意味着只要配置了 `product` 账号，您就可以直接 `@product`。

### 2. Account ID 驱动
不再需要在代码中硬编码 `cli_` 开头的 App ID。
使用易读的 `accountId` (如 `elves`, `backend`)，系统会自动查找对应的凭证。

### 3. 智能缓存策略
- **Bot Info**: 缓存 24 小时 (位于 `~/.openclaw/workspace/cache/feishu_mentions/bots_info.json`)
- **Group Members**: 缓存 2 小时 (位于 `~/.openclaw/workspace/cache/feishu_mentions/<hash>.json`)

## ⚠️ 注意事项

1.  **Account ID 必须匹配**: `resolve` 函数传入的 `accountId` 必须与 `openclaw.json` 中的 key 完全一致。
2.  **权限要求**: 使用的账号必须拥有「获取群组成员」权限，否则无法解析真人用户。
3.  **缓存刷新**: 如果修改了群成员或机器人配置，可能需要等待缓存过期或手动删除缓存文件。

---

**版本**: 2.0.0
**更新时间**: 2026-03-06
