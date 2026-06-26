---
name: article-publisher
description: 自媒体文章多平台发布工具，支持知乎、Bilibili、百家号、头条号、小红书等平台的一键发布。使用Playwright实现浏览器自动化，支持扫码登录和Cookie持久化。
license: GPL-3.0
metadata:
  author: OpenClaw
  tags: ["auto-publish", "article", "zhihu", "bilibili", "baijiahao", "toutiao", "xiaohongshu", "playwright"]
---

# Article Publisher - 自媒体文章发布助手

一键发布文章到知乎、Bilibili、百家号、头条号、小红书等平台。

## Features

- ✅ **多平台支持** - 知乎、Bilibili、百家号、头条号、小红书
- ✅ **一键发布** - 一次操作，多平台同步
- ✅ **扫码登录** - 安全便捷，无需密码
- ✅ **Cookie持久化** - 登录状态自动保存，免重复登录
- ✅ **登录状态检查** - 检查各平台的登录状态

## Quick Start

### 1. 安装依赖

```bash
npm install
npx playwright install chromium
```

### 2. 登录平台

首次使用需要扫码登录各平台：

```
请帮我登录知乎
```

### 3. 发布文章

```
帮我发布一篇文章到知乎，标题是"xxx"，内容是"xxx"
```

### 4. 一键发布到所有平台

```
把这篇文章发布到所有已登录的平台
```

## Platform Support

| Platform | Login | Features |
|----------|-------|----------|
| 知乎 | QR Code | 标题、内容、封面、标签 |
| Bilibili | QR Code | 标题、内容、封面 |
| 百家号 | QR Code | 标题、内容、封面、摘要、分类、标签 |
| 头条号 | QR Code | 标题、内容、封面、标签 |
| 小红书 | QR Code | 标题、内容、封面、标签 |

## Scripts

- `src/index.ts` - 主入口文件
- `src/adapters/*.ts` - 各平台适配器
- `src/lib/*.ts` - 工具库

## Config

- Cookie 自动保存在本地，确保安全和隐私

## Commands / Triggers

Use this skill when:
- "发布文章到知乎"
- "帮我发布文章"
- "一键发布到所有平台"
- "检查登录状态"

## Security Notes

- Cookie 保存在本地，注意保密
- 定期更新登录状态
- 不要分享账号配置文件

## Troubleshooting

### Login timeout
- Check network connection
- Manually visit the platform website
- Re-run and scan QR code again

### Publish failed
- Check article content format
- View browser window for error details

### Playwright errors
```bash
npm install playwright
npx playwright install chromium
```

---

_Ready to automate your article publishing? Let's go! 🚀_
