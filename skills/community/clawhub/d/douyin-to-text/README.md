# dytext-skill

<div align="center">

**抖音文案提取** - OpenClaw AI Agent 技能

提取抖音视频的文案/字幕

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![npm version](https://img.shields.io/npm/v/dytext-cli.svg)](https://www.npmjs.com/package/dytext-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 功能特性

- **文案提取** - 输入抖音分享链接，自动提取视频文案
- **多语言支持** - 支持中、英、日、韩等多种语言
- **余额查询** - 随时查看剩余积分
- **历史记录** - 查看之前的转写记录
- **一键注册** - `npx dytext-cli setup` 即可开始使用

## 快速开始

### 1. 安装技能

```bash
# 方法 1：从 GitHub 安装
cd ~/.openclaw/workspace
git clone https://github.com/xwchris/dytext-skill.git skills/dytext

# 方法 2：通过 ClawHub 安装
clawhub install dytext
```

### 2. 配置（自动引导）

首次使用时自动引导注册：

```bash
npx dytext-cli setup
```

注册即获免费积分，API Key 自动保存到 `~/.dycaption`，无需手动配置。

## 使用示例

### 在 OpenClaw 中使用

| 你说 | AI 会做的 |
|------|-----------|
| "帮我提取这个抖音视频的文案 https://v.douyin.com/xxxxx/" | 自动调用转写并返回文案 |
| "查询我的 dytext 余额" | 显示剩余积分 |
| "看看我最近转写了哪些视频" | 显示历史记录 |

### 命令行直接使用

```bash
# 提取文案
npx dytext-cli transcribe "https://v.douyin.com/xxxxx/"

# 指定语言
npx dytext-cli transcribe "https://v.douyin.com/xxxxx/" zh-CN

# 查询余额
npx dytext-cli balance

# 查看历史
npx dytext-cli history 20
```

## 架构

```
OpenClaw Agent
    ↓  读取 SKILL.md，识别意图
npx dytext-cli（npm 包，Node.js）
    ↓
api.dytext.cn REST API
    ↓
语音识别 → 返回字幕文本
```

跨平台支持，Node.js >= 18 即可。

## 数据安全

> **重要提示**：本技能需要将您的 API Key 和抖音分享链接发送到 dytext.cn 服务进行处理。

- 仅在使用时发送必要数据
- 不会存储或分享您的 API Key
- 请确保您信任 dytext.cn 服务后再使用

## 相关链接

- 官网：[dytext.cn](https://dytext.cn)
- CLI 工具：[github.com/xwchris/dytext](https://github.com/xwchris/dytext)
- npm 包：[npmjs.com/package/dytext-cli](https://www.npmjs.com/package/dytext-cli)

## License

MIT
