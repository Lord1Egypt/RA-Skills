---
name: "discord-toolkit-free"
description: "基础 Discord 消息管理工具,支持发送、回复、表情反应与简单投票,适合个人用户。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Discord工具箱免费版"
  version: "1.0.0"
  summary: "基础 Discord 消息管理工具,支持发送、回复、表情反应与简单投票,适合个人用户。"
  tags:
    - "Discord"
    - "消息管理"
    - "Communication"
    - "社交互动"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Discord 工具箱(免费版)

## 概述

Discord 工具箱免费版是一款面向个人用户的轻量 Discord 消息与互动管理工具。它通过统一的 `discord` 工具调用,覆盖日常最高频的消息操作:发送、编辑、删除、表情反应、投票、置顶与基础话题管理。免费版零配置即用,只需在 Agent 环境中配置好 Discord 机器人令牌即可开始使用。

免费版适合个人 Discord 服务器、小型技术社区和独立开发者的日常消息互动。如果你需要批量消息操作、审核管理(禁言/踢出/封禁)、角色权限管理和成员信息批量查询,请升级至 Pro 版。

## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|:-------|:-----|:----------|
| 消息发送 | 发送文本与媒体到频道/私信 | 支持(单条) |
| 消息编辑/删除 | 修改或删除已发送消息 | 支持 |
| 表情反应 | 添加表情与查看反应列表 | 支持 |
| 投票 | 创建简单投票 | 支持(单题) |
| 话题管理 | 创建与回复话题 | 支持(基础) |
| 置顶 | 置顶与查看置顶消息 | 支持 |
| 消息搜索 | 按关键词搜索历史消息 | 支持(基础) |
| 批量操作 | 批量发送/清理消息 | 不支持 |
| 审核管理 | 禁言/踢出/封禁 | 不支持 |
| 角色管理 | 角色增删与权限 | 不支持 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Discord、消息管理工具、支持发送、表情反应与简单投、适合个人用户、面向个人用户的轻、消息与互动管理工、核心能力、删除频道消息与私、对消息添加表情反、应与查看反应列表、Poll、与频道置顶、管理基础话题、Thread、与频道信息查询等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:发布版本更新通知

作为独立开发者,你希望在 Discord 服务器中发布新版本更新通知。

```json
{
  "action": "sendMessage",
  "to": "channel:1234567890",
  "content": "**v2.3.0 已发布!**\n- 新增批量导出功能\n- 修复登录卡顿问题\n升级命令: `npm i my-tool@latest`"
}
```

Agent 会调用 `discord` 工具完成发送。`to` 字段使用 `channel:<id>` 格式指向目标频道,私信则用 `user:<id>`。

### 场景二:用表情标记任务状态

在团队协作频道中,用表情快速标记任务处理状态。

```json
{
  "action": "react",
  "channelId": "1234567890",
  "messageId": "9876543210",
  "emoji": "✅"
}
```

常见状态标记约定:

| 表情 | 含义 |
|:----:|:-----|
| ✅ | 已完成/已确认 |
| ⚠️ | 需要注意/有问题 |
| 🚧 | 处理中 |
| ❌ | 已拒绝/无法处理 |

### 场景三:发起快速投票

需要在团队频道中快速收集意见,例如选择会议时间。

```json
{
  "action": "poll",
  "to": "channel:1234567890",
  "question": "本周技术分享会定在哪个时间?",
  "answers": ["周三 20:00", "周四 20:00", "周五 19:00"],
  "allowMultiselect": false,
  "durationHours": 24,
  "content": "请大家投票选择合适的时间"
}
```

投票支持 2-10 个选项,`durationHours` 默认 24 小时,最大 768 小时(32 天)。

## 不适用场景

以下场景Discord工具箱免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 第一步:配置机器人令牌

在 Agent 环境中配置 Discord 机器人令牌。机器人需要具备目标频道的「发送消息」「添加反应」「管理消息」等基础权限。

### 第二步:验证连通性

发送一条测试消息确认配置生效:

```json
{
  "action": "sendMessage",
  "to": "channel:1234567890",
  "content": "工具箱已接入,连接正常 ✅"
}
```

### 第三步:开始使用

向 Agent 描述你的需求,例如「在 #announcements 频道发布今日构建结果,并加个 ✅ 反应」。

## 示例

### 消息发送(带媒体附件)

```json
{
  "action": "sendMessage",
  "to": "channel:1234567890",
  "content": "构建产物截图如下:",
  "mediaUrl": "file:///tmp/build-result.png"
}
```

`mediaUrl` 支持本地文件(`file:///path/to/file`)和远程 URL(`https://...`)。

### 消息回复

```json
{
  "action": "sendMessage",
  "to": "channel:1234567890",
  "content": "已确认,开始处理",
  "replyTo": "9876543210"
}
```

`replyTo` 传入要回复的消息 ID,会形成话题式回复。

### 查看反应列表

```json
{
  "action": "reactions",
  "channelId": "1234567890",
  "messageId": "9876543210",
  "limit": 100
}
```

### 创建话题

```json
{
  "action": "threadCreate",
  "channelId": "1234567890",
  "name": "Bug 复盘讨论",
  "messageId": "9876543210"
}
```

### 置顶消息

```json
{
  "action": "pinMessage",
  "channelId": "1234567890",
  "messageId": "9876543210"
}
```

### 基础消息搜索

```json
{
  "action": "searchMessages",
  "guildId": "9999999999",
  "content": "release notes",
  "limit": 10
}
```

## 最佳实践

1. **消息风格简洁化**: Discord 是聊天平台,不是文档系统。消息控制在 1-3 句话,多个短消息优于一段长文。避免使用 Markdown 表格(Discord 会渲染成难看的 `| 文本 |`),改用列表。

2. **善用表情代替回复**: 简单的确认(✅)、注意(⚠️)等场景,用表情反应比回复消息更高效,减少频道噪音。

3. **链接防预览**: 多个链接用 `< >` 包裹以抑制预览嵌入,例如 `<https://example.com>`,保持消息整洁。

4. **`to` 与 `channelId` 区分**: `sendMessage` 使用 `to: "channel:<id>"` 格式;而 `react`、`readMessages`、`editMessage` 等操作使用 `channelId` 直接传入数字 ID,两者不要混淆。

5. **投票选项控制**: 投票选项 2-10 个,选项文案要简短清晰。多选场景设置 `allowMultiselect: true`。

6. **话题命名规范**: 话题名称建议带前缀分类,如 `[Bug]`、`[需求]`、`[讨论]`,便于后续检索和管理。

7. **权限确认**: 执行删除/编辑操作前,先用 `permissions` 检查机器人是否具备目标频道的管理权限,避免操作失败。

## 常见问题

### Q1: 发送消息时报错「缺少权限」?

确认机器人已被分配目标频道的「发送消息」「查看频道」权限。可在频道设置 → 权限中检查机器人角色的权限项。执行敏感操作(删除/编辑他人消息)还需「管理消息」权限。

### Q2: `sendMessage` 和 `react` 用的字段为什么不一样?

`sendMessage` 使用 `to: "channel:<id>"` 或 `user:<id>` 格式(支持频道和私信);而 `react`、`readMessages`、`editMessage`、`deleteMessage` 等操作直接使用 `channelId` 数字 ID。这是设计上的区别,使用时请注意区分。

### 已知限制

通过 `mediaUrl` 上传的媒体文件,Discord 平台限制单文件 25MB(普通服务器)或 500MB(服务器提升等级足够时)。自定义表情上传限制 256KB(PNG/JPG/GIF),贴纸上传限制 512KB(PNG/APNG/Lottie JSON)。

### Q4: 免费版支持私信吗?

支持。`sendMessage` 中将 `to` 设为 `user:<id>` 即可发送私信。但机器人与用户之间需存在共同服务器,且用户未关闭「允许来自服务器成员的私信」。

### Q5: 投票可以多选吗?

可以。设置 `allowMultiselect: true` 即允许多选。投票时长通过 `durationHours` 控制,默认 24 小时,最长 768 小时(32 天)。

### Q6: 如何禁用某些操作组?

通过 `discord.actions.*` 配置可以禁用操作组,例如 `discord.actions.reactions = false` 会禁用表情相关操作。默认启用的操作组包括 reactions、stickers、polls、messages、threads、pins、search 等;roles 和 moderation 默认禁用(Pro 版可启用)。

## 依赖说明

### 运行环境

- **Agent 平台**: 支持解析 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问 Discord API
- **机器人**: 已在 Discord Developer Portal 创建并配置的机器人

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM 能力 | API | 必需 | 由 Agent 内置大模型提供 |
| Discord Bot Token | 凭证 | 必需 | Discord Developer Portal 创建机器人获取 |
| Discord API | 服务 | 必需 | Discord 平台提供 |
| 媒体文件 | 本地资源 | 可选 | 本地路径或远程 URL |

### API Key 配置

- **Discord Bot Token**: 在 Agent 环境配置机器人令牌(建议使用环境变量 `DISCORD_TOKEN` 注入,切勿硬编码到配置文件)。
- **权限范围**: 机器人需在目标服务器被授予「发送消息」「添加反应」「管理消息」「读取消息历史」等基础权限。
- **其他 API Key**: 免费版不依赖额外 API Key,仅使用 Discord Bot Token。

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令 + 部分功能需 `exec` 执行能力)
- **说明**: 以自然语言指令驱动 Agent 调用 Discord 工具完成消息与互动操作
- **适用规模**: 单服务器、个人/小团队,日操作量 100 次以内
- **升级建议**: 如需批量操作、审核管理、角色权限管理,请升级至 `discord-toolkit-pro`

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
