---
name: douyin-to-text
version: 1.1.3
description: 抖音/短视频转文字。使用场景：(1) 用户要求提取抖音、TikTok、YouTube、小红书等视频文案/字幕 (2) 用户发送视频分享链接需要转文字 (3) 用户查询 Videosays 积分余额或转写历史。首次使用会自动引导注册。
requires:
  binaries:
    - npx
sendsDataTo:
  - https://api.videosays.com
---

# 抖音文案提取

使用 `npx videosays` 提取抖音、TikTok、YouTube、小红书等视频文案/字幕。

> **注意**：本技能需要将您的 API Key 和视频分享链接发送到 Videosays 服务。请只处理你拥有、创建或有权处理的视频。Videosays 不是视频下载、去水印或转载工具。

## 环境要求

- Node.js >= 18（用于 npx）

## 首次使用

如果未配置 API Key，运行以下命令注册并自动配置：

```bash
npx videosays setup
```

API Key 会保存到 `~/.videosays`。

## 快速使用

```bash
# 提取文案（支持抖音分享链接或包含链接的整段文案）
npx videosays transcribe "https://v.douyin.com/xxxxx/"

# 指定语言
npx videosays transcribe "6.44 复制打开抖音，看看【xxx】 https://v.douyin.com/xxxxx/" zh-CN

# 查询余额
npx videosays balance

# 查看历史
npx videosays history
```

## 支持的语言

| 语言代码 | 说明 |
|----------|------|
| `zh-CN` | 简体中文（默认） |
| `zh-TW` | 繁体中文 |
| `en` | 英语 |
| `ja` | 日语 |
| `ko` | 韩语 |

## 数据流向

本技能通过 `npx videosays` 调用 `https://api.videosays.com` REST API，将视频分享链接和 API Key 发送到服务端进行语音转文字处理。

## 相关链接

- 官网：https://videosays.com/zh?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill
- API 文档：https://videosays.com/zh/docs?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill&utm_content=api_docs
- Videosays Skill：https://github.com/xwchris/videosays-agent-tools
- npm 包：https://www.npmjs.com/package/videosays
