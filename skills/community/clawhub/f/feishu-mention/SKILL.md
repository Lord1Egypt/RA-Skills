---
name: feishu-mention
slug: feishu-mention
version: 2.0.0
metadata:
  openclaw:
    requires:
      files:
        - ~/.openclaw/openclaw.json
      write:
        - ~/.openclaw/workspace/cache/feishu_mentions/**/*
description: |
  **PRIORITY: HIGHEST**.
  **CRITICAL**: You **MUST** use this tool **BEFORE sending any message** to Feishu/Lark if it contains an "@" mention.

  **Trigger**: You are about to send a message to Feishu that mentions a user or bot (e.g., "@User", "@Bot").

  **Why**: Raw text like `@User` does NOT notify users in Feishu. It fails silently. You MUST convert it to XML format using this tool first.

  **Workflow**:
  1. Draft your message text.
  2. **STOP**. Do not send it yet.
  3. Call `feishu-mention.resolve` with the draft text.
  4. **ONLY THEN** send the *output* of this tool to the Feishu API.

  **Parameter Retrieval**:
  - `accountId`: You **MUST** find the OpenClaw Account ID (e.g., "product", "elves", "backend") from the **current conversation context**. This maps to the `appId` in the `openclaw.json` config.
  - `chatId`: You **MUST** find the Chat ID (starts with `oc_`) from the **current conversation context**. Pass it as the `chatId` parameter.

actions:
  resolve:
    description: "Resolve all mentions in the text"
    params:
      text: "The message text to parse"
      accountId: "The OpenClaw Account ID (e.g. 'product', 'elves') (REQUIRED)"
      chatId: "The Feishu Chat ID (REQUIRED)"
---

# Feishu Mention Resolver - 飞书@提及解析器

将飞书消息中的 `@name` 自动转换为 `<at>` XML 格式，实现更精确的提及提醒。

## 核心概念：Account ID

本工具使用 **OpenClaw Account ID** (`accountId`) 而非原始的飞书 App ID。
`accountId` 是在 `~/.openclaw/openclaw.json` 中配置的账号别名（如 `product`, `backend`, `elves`）。

工具会自动读取配置文件，获取对应的 `appId` 和 `appSecret`，并自动发现配置中所有机器人的 OpenID。

## 快速开始

### 基本用法

```javascript
// JavaScript/Node.js
const { resolve } = require('./index.js');

async function processMessage() {
  const text = '你好 @product，请确认一下';
  const accountId = 'elves'; // 使用 'elves' 账号的凭证来调用 API
  const chatId = 'oc_1234567890abcdef';
  
  // 解析文本中的所有@提及
  // 系统会自动识别 @product 是另一个机器人，并获取其 OpenID
  const resolvedText = await resolve(text, accountId, chatId);
  
  console.log(resolvedText);
  // 输出: "你好 <at user_id="ou_c610...">product</at>，请确认一下"
}
```

## 优先级逻辑

1.  **已配置的机器人** (Priority 1): 自动匹配 `openclaw.json` 中配置的所有账号名称（如 `@product`、`@Product`、`@PRODUCT`），不区分大小写。
2.  **用户别名** (Priority 2): 匹配 `options.aliases` 中的别名配置。
3.  **群成员** (Priority 3): 检查本地缓存或调用飞书 API 获取群成员。

## API 参考

### `resolve(text, accountId, chatId, [options])`

批量解析文本中的所有 `@提及`。

**参数:**
- `text` (string): 输入文本
- `accountId` (string): OpenClaw 账号别名 (如 "elves")
- `chatId` (string): 会话 ID
- `options` (object): 可选配置
    - `aliases`: 额外的别名配置 `[{ name: '张三', alias: ['小王'] }]`

**返回值:**
- `Promise<string>`: 解析后的 XML 文本

---

**版本**: 2.0.0 (支持 Account ID 和自动发现)  
**作者**: OpenClaw AI Assistant  
**最后更新**: 2026-03-06
