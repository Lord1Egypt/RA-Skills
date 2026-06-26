---
name: 跨平台内容自动发布
slug: cross-platform-auto-poster
description: 跨平台内容自动化发布工作流，支持AI原创内容生成、视频制作、自动发布到小红书、抖音等平台，支持国内视频搬运去重后发布到TikTok/YouTube。
version: 1.0.0
author: xiatian5
tags: [automation, cross-platform, social-media, xiaohongshu, tiktok, youtube, publish, video]
---

# 跨平台内容自动发布 📤🎬

全自动化跨平台内容发布工作流，支持AI原创内容生产 + 自动发布，也支持国内视频搬运去重后发布到海外平台。一键完成从选题到发布全流程，帮你轻松做内容变现。

## 触发词

当用户说这些话时，调用这个技能：
- "跨平台自动发布"
- "自动发布小红书"
- "视频搬运自动化"
- "TikTok自动发布"
- "YouTube自动上传"
- "内容自动化变现"
- "小红书自动发文"

## 功能特性

| 功能 | 说明 |
|------|------|
| **AI原创小红书图文** | 从选题→文案→封面→发布全自动 |
| **AI生成口播视频** | 文案转语音+配图生成视频 |
| **视频搬运去重** | 自动下载→去重处理→改文案→发布 |
| **多平台支持** | 小红书、抖音、TikTok、YouTube |
| **账号隔离** | 支持多账号管理，保存登录状态 |
| **数据统计** | 自动记录互动数据，生成报表 |

## 支持的工作流

### 工作流1: AI原创小红书图文 (推荐新手快速起步)

```
1. 热点选题 → 抓取小红书热搜，推荐热门选题
2. 内容生成 → 生成符合小红书风格的文案
3. 封面制作 → AI生成封面图
4. 自动发布 → 浏览器自动登录，上传图文发布
5. 数据记录 → 记录链接和发布时间
```

### 工作流2: AI原创小红书口播视频

```
1. 选题文案 → 同图文工作流
2. 语音合成 → 文案转自然语音
3. 配图生成 → 根据文案生成配图
4. 视频合成 → 语音+配图+字幕 → 输出视频
5. 自动发布 → 上传视频发布
```

### 工作流3: 国内视频搬运到TikTok/YouTube

```
1. 视频采集 → 按关键词下载热门视频
2. AI去重 → 裁切+翻转+调色+换BGM
3. 翻译改写 → 中文标题文案翻译成英文
4. 自动上传 → 发布到TikTok/YouTube
```

## 依赖

- `xiaohongshu-content-automation` - 小红书内容生成
- `playwright-browser-automation` - 浏览器自动化发布
- `image_generate` - AI生成封面图
- `remotion-video-toolkit` - 视频合成剪辑
- `openai-whisper-api` - 语音识别（字幕生成）
- `ffmpeg` - 视频处理（需要安装）

## 配置说明

### 首次使用

1. 安装依赖 `npm install` 安装 Node 依赖
2. 安装 playwright 浏览器 `npx playwright install chromium`
3. 安装 ffmpeg 并添加到 PATH
4. 配置账号信息在 `config/accounts.json`

### 账号配置模板

```json
{
  "xiaohongshu": [
    {
      "name": "账号1",
      "cookiePath": "./auth/xiaohongshu-account1.json"
    }
  ],
  "tiktok": [],
  "youtube": []
}
```

## 使用示例

### 生成并发布一篇小红书图文

```javascript
const workflow = require('./src/workflows/xiaohongshu-text-image');

await workflow.run({
  topic: "新手健身5个误区",
  style: "干货",
  accountIndex: 0
});
```

### 批量搬运视频到TikTok

```javascript
const搬运工作流 = require('./src/workflows/video-cross-post');

await 搬运工作流.run({
  sourceKeyword: "fitness tips",
  sourcePlatform: "douyin",
  targetPlatform: "tiktok",
  count: 5
});
```

## 最佳实践

1. **垂直领域** - 专注一个领域比如健身、美妆、美食，更容易做起来
2. **批量生产** - 一次生成10-20篇，定时分批发布
3. **数据驱动** - 看哪个选题互动好，多做同类内容
4. **账号安全** - 一个账号不要发太频繁，避免风控

## 更新日志

### v1.0.0 (2026-03-30)
- 初始版本
- 完整的AI原创小红书图文工作流
- 支持多账号管理
- 预留了视频搬运和多平台接口

## 相关技能

- [xiaohongshu-content-automation](https://clawhub.ai/skills/xiaohongshu-content-automation) - 小红书内容生成
- [playwright-browser-automation](https://clawhub.ai/skills/playwright-browser-automation) - 浏览器自动化
- [remotion-video-toolkit](https://clawhub.ai/skills/remotion-video-toolkit) - 视频制作工具
- [image_generate](https://clawhub.ai/skills/image-generate) - AI图片生成

---

*如果你觉得这个技能有用，请给它点个星，谢谢！⭐*
