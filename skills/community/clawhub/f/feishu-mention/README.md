# FeishuMention Resolver - 飞书@提及解析器

## 📦 功能特性

- ✅ **Account ID 驱动**: 使用易记的 `product`, `elves` 等别名，而非硬编码 ID
- ✅ **自动发现**: 自动识别配置文件中的所有机器人（如 `@product`）
- ✅ **多优先级解析**:
    1. 配置中的机器人 (Priority 1) - 支持 Bot 名称或 Account ID (不区分大小写)
    2. 用户别名 (Priority 2)
    3. 群成员 (Priority 3 - 缓存/API)
- ✅ **智能缓存**: API 结果本地缓存 2 小时，机器人信息缓存 24 小时
- ✅ **零配置**: 只要配置了 `~/.openclaw/openclaw.json` 即可直接使用

## 🚀 快速开始

### 1. 确保配置存在

确保 `~/.openclaw/openclaw.json` 文件中包含 `channels.feishu.accounts` 配置：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "product": {
          "appId": "cli_a91b...",
          "appSecret": "AMZL..."
        },
        "elves": {
          "appId": "cli_a923...",
          "appSecret": "pBYN..."
        }
      }
    }
  }
}
```

### 2. 调用解析器

```javascript
const { resolve } = require('./index');

async function main() {
  const text = '你好 @product，请帮忙看看 @张三';
  
  // 使用 'elves' 账号的凭证来调用 API
  // 系统会自动：
  // 1. 识别 @product 是另一个机器人 (自动获取 OpenID)
  // 2. 识别 @张三 是群成员 (调用 API 获取 OpenID)
  const resolved = await resolve(text, 'elves', 'oc_123456...');
  
  console.log(resolved);
  // 输出: "你好 <at user_id="ou_c610...">product</at>，请帮忙看看 <at user_id="ou_123...">张三</at>"
}
```

## 📖 详细文档

查看 [SKILL.md](./SKILL.md) 了解更多：
- API 完整参考
- 缓存机制详解
- 优先级逻辑说明

## 📂 文件结构

```
feishu-mention/
├── SKILL.md           # 核心文档
├── README.md          # 本文件
├── index.js           # 主入口 (重构后支持 Account ID)
├── test.js            # 测试脚本
```

## ⚠️ 注意事项

1.  **Account ID**: 必须对应 `openclaw.json` 中的 key。
2.  **权限要求**: 使用的账号必须有企业通讯录读取权限。
3.  **缓存位置**: `~/.openclaw/workspace/cache/feishu_mentions/`

## 📄 License

MIT

---

**维护者**: OpenClaw AI Assistant  
**版本**: 2.0.0
**更新时间**: 2026-03-06
