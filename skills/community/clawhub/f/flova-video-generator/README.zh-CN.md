# Flova Video Generator -- OpenClaw Skill

[English](README.md) | **中文** | [日本語](README.ja.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill Version](https://img.shields.io/badge/skill_version-0.2.9-green.svg)](SKILL.md)
[![ClawHub](https://img.shields.io/badge/ClawHub-marketplace-brightgreen.svg)](https://clawhub.com)
[![Flova](https://img.shields.io/badge/Flova-video_platform-00bcd4.svg)](https://www.flova.ai)

一个 [OpenClaw](https://openclaw.ai) 技能插件，让 AI 智能体能够通过 [Flova](https://www.flova.ai) 创建、编辑和导出视频 -- Flova 是全球首个一站式 AI 视频创作平台，集构思、分镜、拍摄、剪辑于一体，让创意自由呈现。

> *人人都是自己的创意导演，轻松创作精彩故事。*

**兼容：** OpenClaw | Claude Code | Codex | Cursor | Windsurf | Cline | 以及更多

## 简介

这是一个 [OpenClaw](https://openclaw.ai) 技能 -- 一个基于 Markdown 的指令文件，赋予 AI 智能体调用 Flova API 的能力。加载技能后，你的 AI 助手即可创建视频项目、发送创作指令、上传文件、导出成品视频、管理订阅 -- 全程通过自然对话完成。兼容所有支持工具调用或 URL 读取的 AI 编程助手。

## 安装方式

### 通过 ClawHub（推荐）

在 [ClawHub](https://clawhub.com) 搜索 **flova** 并点击安装。

### 直接对话 AI 助手

将以下消息直接发送给你的 AI 助手：

> 学习 https://s.flova.ai/SKILL.md 然后按照 Skill 文档指引，进行一站式视频创作

### 手动安装

下载 `SKILL.md` 并放置到项目的技能目录中：

```bash
curl -o SKILL.md https://s.flova.ai/SKILL.md
```

## 快速开始

1. **获取 API Token：** 访问 [flova.ai/openclaw](https://www.flova.ai/openclaw/?action=token)
2. **设置环境变量：**
   ```bash
   export FLOVA_API_TOKEN="your_token_here"
   ```
3. **开始创作：** 告诉你的 AI 助手你想要什么视频！

## 功能特性

- **自然语言视频创作** -- 描述你的想法，生成视频
- **文件上传** -- 支持图片、视频、音频和文档
- **导出与下载** -- 导出成品视频并下载项目素材
- **项目管理** -- 列出、恢复和切换视频项目
- **订阅与积分** -- 查看状态、订阅套餐、购买积分

## 工作流概览

```
创建项目 -> 对话（描述你的视频） -> 流式响应（SSE）
    -> 导出视频 -> 轮询状态 -> 获取视频地址
```

所有创作交互（编写脚本、选择模型、编辑分镜等）都通过对话式 `/chat` 接口完成 -- 无需调用其他接口。

## 仓库结构

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 技能定义文件，包含 API 参考和工作流说明 |
| `api_curl_commands.md` | 调试用 curl 命令，用于手动 API 测试 |
| `LICENSE` | MIT 许可证 |

## API 接口

| 接口 | 说明 |
|---|---|
| `POST /user` | 获取用户信息和积分 |
| `POST /create` | 创建视频项目 |
| `POST /projects` | 列出已有项目 |
| `POST /project_info` | 获取项目元数据和分镜 |
| `POST /chat_history` | 获取对话历史（分页） |
| `POST /upload` | 上传文件（图片、视频、音频） |
| `POST /chat` | 发送创作指令 |
| `POST /chat_stream` | 消费 SSE 响应流 |
| `POST /export_video` | 开始导出视频 |
| `POST /export_status` | 轮询导出进度 |
| `POST /download_all` | 下载项目资源 |
| `POST /download_status` | 轮询下载进度 |
| `POST /products` | 列出可用套餐和积分包 |
| `POST /subscribe` | 发起订阅结账 |
| `POST /credits_buy` | 购买积分 |

## 贡献

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/your-change`）
3. 提交更改并发起 Pull Request

**注意：** `SKILL.md` 必须使用纯 ASCII 字符。

## 相关链接

- [Flova 平台](https://www.flova.ai)
- [价格与套餐](https://www.flova.ai/pricing/)
- [文档中心](https://www.flova.ai/docs/)
- [Token 管理](https://www.flova.ai/openclaw/?action=token)

## 许可证

[MIT](LICENSE)
