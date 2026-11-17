---
slug: "discord-free"
name: "discord-free"
version: "1.0.0"
displayName: "Discord 基础控制"
summary: "通过discord工具控制机器人,收发消息、表情回应、读取与置顶消息等基础操作。discord-free 提供 Discord 机器人的基础控制能力,覆盖消息收发与编辑、 表情回应、消息读取"
summary_zh: "通过discord工具控制机器人,收发消息、表情回应、读取与置顶消息等基础操作。discord-free 提供 Discord 机器人的基础控制能力,覆盖消息收发与编辑、 表情回应、消息读取"
license: "MIT"
description: "|-. 适用于需要discord相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  discord-free 提供 Discord 机器人的基础控制能力,覆盖消息收发与编辑、
  表情回应、消息读取、置顶管理等常用操作。适合个人开发者与小型社区进行
  通知推送、简单互动与消息归档。投票、线程、审核、表情包上传、角色变更等
  高级能力需升级到付费版 discord.
tags:
  - Communication
  - discord
  - automation
  - productivity
  - developer-tools
  - 社交
  - 通信
  - channelid
  - sendmessage
  - channel
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
pricing_tier: free
---
# Discord 基础控制

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Discord 基础控制处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 概述

`discord-free` 提供 Discord 机器人的基础消息与互动能力,以 JSON action 的形式发送/编辑/删除消息、对消息添加表情回应、读取频道最近消息、置顶消息。所有操作依赖为 Clawdbot 配置的 bot token.
## 核心能力

### 消息收发
- `sendMessage`:向频道 `channel:<id>` 或私信 `user:<id>` 发送消息,支持 `content` 文本与 `replyTo` 回复指定消息.
- `editMessage`:按 `channelId` + `messageId` 编辑已发消息.
- `deleteMessage`:按 `channelId` + `messageId` 删除消息.
- `readMessages`:按 `channelId` 拉取最近消息,支持 `limit`.
### 表情回应
- `react`:对指定消息添加 emoji(如 `✅`、`👍`).
- `reactions`:列出某条消息的回应及对应用户列表.
### 置顶管理
- `pinMessage`:置顶指定消息.
- `listPins`:列出频道置顶消息.

### 频道权限检查
- `permissions`:检查机器人在指定频道的权限,用于发送前确认.

### 消息写作风格
- 短句优先(1~3 句),多条快回复优于一大段文字.
- 用 **粗体** 强调,用 `code` 标注技术术语,用 `> ` 引用他人发言.
- 链接用 `<https://...>` 抑制预览嵌入.
- 避免 markdown 表格(Discord 会渲染成原始 `|` 文本)和 `##` 标题.

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

### 场景一:通知推送
- 输入:通知文本、目标频道 `channel:9876543210`.
- 输出:机器人向频道发送通知消息并对该消息 react ✅ 标记已发送.
### 场景二:消息归档
- 输入:频道 `channelId=123`、需要归档的条数 `limit=20`.
- 输出:读取最近 20 条消息,关键字段提取后写入本地归档文件.
## 使用流程

1. **检查权限**:对目标频道调用 `permissions`,确认机器人具备查看与发送权限.
2. **定位目标**:发消息用 `to: "channel:<id>"`;读取/编辑/删除/回应用 `channelId` 直传,两者格式不可混用.
3. **发送与跟进**:`sendMessage` 后记录返回的 `messageId`,用于后续 `react`、`pinMessage`、`editMessage`.
4. **归档收尾**:按需 `readMessages` 拉取历史并 `listPins` 整理置顶内容.
## 案例展示

### 案例 1:发送通知并置顶
目标:向 `#announcements`(`channel:9876543210`)发送周会通知并置顶.
```json
{
  "action": "sendMessage",
  "to": "channel:9876543210",
  "content": "**本周五 15:00 周会**\n议题:Q3 进度同步,会议室 B-301"
}
```

返回 `messageId=1122334455667788` 后:

```json
{ "action": "pinMessage", "channelId": "9876543210", "messageId": "1122334455667788" }
```

结果:频道出现周会通知并置顶,成员进频道即可见.
### 案例 2:读取最近消息并回应
目标:读取 `#general`(`channelId=123`)最近 10 条并对最后一条报 bug 的消息标记 ⚠️.
```json
{ "action": "readMessages", "channelId": "123", "limit": 10 }
```

从返回结果定位到 bug 报告消息 `messageId=998877`:

```json
{ "action": "react", "channelId": "123", "messageId": "998877", "emoji": "⚠️" }
```

## 异常处理

| 错误场景 | 触发原因 | 处理方式 |
|:-----|:-----|:-----|
| `Missing Access` / `50001` | 机器人缺少该频道查看或发送权限 | 先 `permissions` 核对权限位,联系服务器管理员补齐频道权限 |
| `to` 与 `channelId` 混用 | `sendMessage` 误传 `channelId` 而 `react` 误传 `to` | `sendMessage` 用 `to: "channel:<id>"`;`react/readMessages/editMessage/deleteMessage` 用 `channelId` |
| `Unknown Message` / `10008` | `editMessage`/`deleteMessage`/`react` 指向已删除消息 | 先 `readMessages` 确认消息存在,已删除则跳过 |
| emoji 不存在 | `react` 传入了服务器没有的自定义表情 | 改用标准 unicode emoji(如 ✅、👍),或确认自定义表情 ID 正确 |
| 频道不存在 | `channelId` 或 `to` 中的 ID 拼写错误 | 通过 `listPins` 或服务器界面核对频道 ID 后检查网络连接和配置后重试 |

## 常见问题

### Q1:`sendMessage` 和 `readMessages` 的目标参数为什么不一样?
`sendMessage` 用 `to: "channel:<id>"`(带 `channel:` 前缀,也支持 `user:<id>` 私信),`readMessages` 用裸 `channelId`。这是工具设计,混用会报错.
### Q2:免费版能创建投票或线程吗?
不能。投票(`poll`)、线程(`threadCreate`/`threadReply`)、审核(`timeout`/`kick`/`ban`)、表情包与贴纸上传、角色变更等属于付费版 discord 的高级能力,免费版仅支持基础消息与表情互动.
### Q3:发送消息时如何避免链接预览撑爆频道?
在链接外包裹 `<>`,例如 `<https://example.com>`,Discord 会抑制链接嵌入预览.
### Q4:置顶消息有数量上限吗?
Discord 单频道置顶上限为 50 条,超出需先 `listPins` 取消旧置顶再添加新的.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 仅支持基础消息操作(收发/编辑/删除/读取)、表情回应、置顶与权限检查,不含投票、线程、审核、上传、角色、搜索等高级能力.
- 所有操作依赖为 Clawdbot 配置的 bot token.
- `sendMessage` 的 `to` 与其他 action 的 `channelId` 格式不同,混用会报错.
- 受 Discord 速率限制,高频发送会被 429 限流.
- markdown 表格在 Discord 渲染为原始 `|` 文本,通知类消息应改用列表或粗体.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.