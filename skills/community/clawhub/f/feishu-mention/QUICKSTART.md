# FeishuMention Resolver - 快速参考 (v2.0)

## 🚀 30 秒上手

### 1. 确认 OpenClaw 配置

本技能依赖 `~/.openclaw/openclaw.json` 中的配置。请确保您的 `feishu.accounts` 块已正确配置：

```json
"accounts": {
  "product": { "appId": "...", "appSecret": "..." },
  "elves": { "appId": "...", "appSecret": "..." }
}
```

### 2. 基础使用（零配置）

无需手动映射机器人或设置 ID，直接使用 Account ID（如 `elves`）即可：

```javascript
const { resolve } = require('./index.js');

// 场景：Elves 机器人收到消息，需要回复并 @product 和 @张三
const text = '你好 @product，请协助 @张三';
const accountId = 'elves'; // 使用 Elves 的身份
const chatId = 'oc_123456...';

const result = await resolve(text, accountId, chatId);
// → "你好 <at user_id="ou_product_id">product</at>，请协助 <at user_id="ou_zhangsan_id">张三</at>"
```

### 3. 支持别名（可选）

虽然不需要配置机器人，但如果您需要支持同事的昵称，仍可传入 `aliases`：

```javascript
// 张三的昵称是 "老张"
const aliases = [{ name: '张三', alias: ['老张'] }];

const result = await resolve('呼叫 @老张', 'elves', chatId, { aliases });
// → "呼叫 <at user_id="ou_zhangsan_id">张三</at>"
```

---

## 📋 功能对比 (v1 vs v2)

| 功能 | 旧版 (v1.x) | 新版 (v2.0) |
|------|------------|------------|
| **身份认证** | 需手动传入 App ID/Secret | **自动** (使用 Account ID) |
| **机器人映射** | 需手动维护 JSON 映射表 | **自动** (从配置中发现) |
| **真人解析** | 支持 | 支持 |
| **配置来源** | 环境变量/代码参数 | **`openclaw.json`** |

---

## 🔍 提及解析优先级

系统按以下顺序尝试解析 `@name`：

1.  **已配置机器人** (Priority 1)
    *   检查 `openclaw.json` 中的所有账号。
    *   匹配 `Agent ID` (如 `@product`) 或 `Bot Name` (如 `@Product Bot`)。
    *   *不区分大小写*。

2.  **用户别名** (Priority 2)
    *   检查传入的 `options.aliases`。
    *   将别名转换为真实姓名后，递归解析。

3.  **企业通讯录** (Priority 3)
    *   检查本地缓存。
    *   调用飞书 API 获取群成员 (使用 `accountId` 对应的凭证)。

4.  **原样输出** (Fallback)
    *   如果都未匹配，保留原文本 (如 `@UnknownUser`)。

---

## ⚠️ 常见问题

**Q: 为什么 `@product` 没有变色？**
A: 请检查 `openclaw.json` 中是否配置了 `product` 账号，并且该账号对应的 Bot 在飞书后台的名称是否与 `@` 的内容匹配（或使用 Account ID）。

**Q: 为什么无法解析群成员？**
A: 请确保您使用的 `accountId` (例如 `elves`) 对应的飞书机器人已加入该群，并且拥有「获取群组成员」的权限。

**Q: 缓存多久更新？**
A: 群成员缓存 2 小时；机器人信息缓存 24 小时。重启应用或手动删除缓存文件可强制刷新。
