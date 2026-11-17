# douyin-to-text

<div align="center">

**抖音/短视频文案提取**

提取抖音、TikTok、YouTube、小红书等视频的文案/字幕

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![npm version](https://img.shields.io/npm/v/videosays.svg)](https://www.npmjs.com/package/videosays)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 功能特性

- **文案提取** - 输入视频分享链接，自动提取视频文案
- **多语言支持** - 支持中、英、日、韩等多种语言
- **余额查询** - 随时查看剩余积分
- **历史记录** - 查看之前的转写记录
- **一键注册** - `npx videosays setup` 即可开始使用

## 快速开始

### 1. 安装技能

```bash
# 方法 1：从 GitHub 安装
cd ~/.openclaw/workspace
git clone https://github.com/xwchris/douyin-to-text.git skills/douyin-to-text

# 方法 2：通过 ClawHub 安装
clawhub install douyin-to-text
```

### 2. 配置（自动引导）

首次使用时自动引导注册：

```bash
npx videosays setup
```

注册即获免费积分，API Key 自动保存到 `~/.videosays`，无需手动配置。

## 使用示例

### 在 OpenClaw 中使用

| 你说 | AI 会做的 |
|------|-----------|
| "帮我提取这个抖音视频的文案 https://v.douyin.com/xxxxx/" | 自动调用 Videosays 转写并返回文案 |
| "查询我的 Videosays 余额" | 显示剩余积分 |
| "看看我最近转写了哪些视频" | 显示历史记录 |

### 命令行直接使用

```bash
# 提取文案
npx videosays transcribe "https://v.douyin.com/xxxxx/"

# 指定语言
npx videosays transcribe "https://v.douyin.com/xxxxx/" zh-CN

# 查询余额
npx videosays balance

# 查看历史
npx videosays history 20
```

## 架构

```
OpenClaw Agent
    ↓  读取 SKILL.md，识别意图
npx videosays（npm 包，Node.js）
    ↓
api.videosays.com REST API
    ↓
语音识别 → 返回字幕文本
```

跨平台支持，Node.js >= 18 即可。

## 数据安全

> **重要提示**：本技能需要将您的 API Key 和视频分享链接发送到 Videosays 服务进行处理。

- 仅在使用时发送必要数据
- 不会存储或分享您的 API Key
- 请只处理你拥有、创建或有权处理的视频

## 相关链接

- 官网：[videosays.com](https://videosays.com/zh?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill)
- API 文档：[videosays.com/zh/docs](https://videosays.com/zh/docs?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill&utm_content=api_docs)
- Videosays Skill：[videosays-agent-tools](https://github.com/xwchris/videosays-agent-tools)
- npm 包：[npmjs.com/package/videosays](https://www.npmjs.com/package/videosays)

## License

MIT
