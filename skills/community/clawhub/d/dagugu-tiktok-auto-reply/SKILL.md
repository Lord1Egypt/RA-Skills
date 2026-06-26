---
slug: tiktok-auto-reply
name: TikTok 自动回复
version: 1.0.0
author: dagugu
license: MIT
tags: [tiktok, auto-reply, social-media, automation]
---

# TikTok 自动回复技能

⚠️ **风险提示**：使用此技能可能导致账号被 TikTok 限制或封禁。请谨慎使用，后果自负。

## 功能

- 监控指定关键词的热门视频
- 自动获取视频评论
- 根据配置自动回复评论

## 前置条件

1. TikTok 企业开发者账号
2. TikTok API 访问令牌
3. Node.js 环境

## 安装

```bash
cd ~/.openclaw/workspace/skills/tiktok-auto-reply
npm install
```

## 配置

复制配置模板：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "tiktok": {
    "accessToken": "YOUR_ACCESS_TOKEN",
    "clientKey": "YOUR_CLIENT_KEY",
    "clientSecret": "YOUR_CLIENT_SECRET"
  },
  "keywords": ["热门关键词1", "关键词2"],
  "replyTemplates": [
    "视频太棒了！🔥",
    "学到了！感谢分享 👍",
    "有意思～"
  ],
  "checkIntervalMinutes": 30,
  "maxRepliesPerHour": 10
}
```

## 使用

```bash
# 手动运行一次
node index.js

# 或作为定时任务
node watch.js
```

## 注意事项

- 不要设置过高的回复频率
- 避免完全相同的回复内容
- 定期更换回复模板
- 监控账号状态

## API 文档

[TikTok for Developers](https://developers.tiktok.com/)

---

**免责声明**：本技能仅供学习研究使用。使用本技能产生的任何后果由使用者自行承担。
