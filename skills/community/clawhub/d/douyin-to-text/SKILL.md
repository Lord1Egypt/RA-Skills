---
name: dytext
version: 1.0.0
description: 抖音文案提取。使用场景：(1) 用户要求提取抖音视频文案/字幕 (2) 用户发送抖音分享链接需要转文字 (3) 用户查询积分余额或转写历史。首次使用会自动引导注册。
requires:
  binaries:
    - npx
sendsDataTo:
  - https://api.dytext.cn
---

# 抖音文案提取

通过 `npx dytext-cli` 提取抖音视频文案/字幕。首次使用自动引导注册，跨平台支持。

> **注意**：本技能需要将您的 API Key 和抖音分享链接发送到 dytext.cn 服务。请确保您信任该服务后再使用。

## 环境要求

- Node.js >= 18（用于 npx）

## 首次使用

如果未配置 API Key，运行以下命令注册并自动配置：

```bash
npx dytext-cli setup
```

注册即获免费积分。

## 快速使用

```bash
# 提取文案（支持抖音分享链接或包含链接的整段文案）
npx dytext-cli transcribe "https://v.douyin.com/xxxxx/"

# 指定语言
npx dytext-cli transcribe "6.44 复制打开抖音，看看【xxx】 https://v.douyin.com/xxxxx/" zh-CN

# 查询余额
npx dytext-cli balance

# 查看历史
npx dytext-cli history
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

本技能通过 `npx dytext-cli` 调用 `api.dytext.cn` REST API，将抖音分享链接和 API Key 发送到服务端进行语音转文字处理。

## 相关链接

- 官网：https://dytext.cn
- CLI 工具：https://github.com/xwchris/dytext
- npm 包：https://www.npmjs.com/package/dytext-cli
