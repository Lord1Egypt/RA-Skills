---
slug: "discord-chat-free"
name: "discord-chat-free"
version: "1.0.0"
displayName: "Discord Chat 基础"
summary: "通过message工具在Discord频道发送消息、回复、读取历史与表情回应。discord-chat-free 提供 Discord 频道的基础聊天能力,覆盖消息发送、 线程回复、历史读取"
summary_zh: "通过message工具在Discord频道发送消息、回复、读取历史与表情回应。discord-chat-free 提供 Discord 频道的基础聊天能力,覆盖消息发送、 线程回复、历史读取"
license: "MIT"
description: "|-. 适用于需要discord chat相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  discord-chat-free 提供 Discord 频道的基础聊天能力,覆盖消息发送、
  线程回复、历史读取与表情回应。适合个人开发者与小型社区进行通知推送、
  简单答疑与消息确认。全文搜索、消息编辑与删除、频道管理、消息特效等
  高级能力需升级到付费版 discord-chat.
tags:
  - Communication
  - discord
  - chat
  - automation
  - productivity
  - 社交
  - 通信
  - action
  - message
  - target
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
pricing_tier: free
---
# Discord Chat 基础

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Discord Chat 基础处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 概述

`discord-chat-free` 通过 Clawdbot 的 `message` 工具与 Discord 频道进行基础交互。指定 `channel=discord` 后,工具自动路由到已配置的 Discord 插件。支持以频道名(`#name`)或频道 ID 作为 `target`,覆盖发送、回复、读取与表情回应操作.
## 核心能力

### 消息发送
```bash
message action=send channel=discord target="#channel-name" message="你的消息"
message action=send channel=discord target="1234567890" message="按 ID 发送"
```
- `target` 支持带 `#` 前缀的频道名或裸频道 ID.
- 多链接用 `<>` 包裹抑制预览:`<https://example.com>`.
- 不支持 markdown 表格,改用项目符号列表.

### 线程回复
```# 网络连接示例(已移除潜在风险命令)
```
- `replyTo` 以指定消息 ID 创建线程式回复,适合上下文关联的答疑.

### 历史读取
```bash
message action=read channel=discord target="#channel-name" limit=20
```
- 拉取频道最近消息,`limit` 控制条数.

### 表情回应
```bash
message action=react channel=discord messageId="1234567890" emoji="👍"
```
- 对指定消息添加 emoji,用于快速确认或标记.

### 消息写作风格
- 短句优先(1~3 句),多条快回复优于一大段文字.
- 用 **粗体** 强调,用 `code` 标注技术术语.
- 链接用 `<https://...>` 抑制预览嵌入.
- 避免 markdown 表格(Discord 渲染成原始 `|` 文本)和 `##` 标题.

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

### 场景一:通知推送
- 输入:通知文本"今晚 20:00 维护"、频道 `#announcements`.
- 输出:机器人 `action=send` 发送通知,`action=react emoji="📌"` 标记.
### 场景二:简单答疑
- 输入:用户提问、提问消息 ID、频道 `#support`.
- 输出:机器人 `action=send replyTo` 回复提问消息,附上简要解答.
## 使用流程

1. **确认配置**:Discord bot 已在 gateway config 中配置,`channel=discord` 能正确路由.
2. **定位目标频道**:优先用 `target="#频道名"`(更可读);需精确控制时用频道 ID.
3. **发送与回复**:`action=send` 发新消息;需关联某条消息用 `replyTo`;纯确认用 `action=react` 优于回复.
4. **读取历史**:答疑前先 `action=read limit=N` 查看近期上下文,避免重复.
**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 案例展示

### 案例 1:发送通知并标记
目标:向 `#announcements` 发送维护通知并标记.
```bash
message action=send channel=discord target="#announcements" message="**今晚 20:00-22:00 维护**,期间服务暂停"
```

返回消息 ID `4455667788` 后:

```bash
message action=react channel=discord messageId="4455667788" emoji="📌"
```

结果:公告频道出现维护通知并带 📌 标记,成员一目了然.
### 案例 2:回复提问
目标:用户在 `#support` 提问"如何重置密码",消息 ID `1122334455`,机器人回复.
```bash
message action=read channel=discord target="#support" limit=5
```

确认提问内容后回复:

```bash
message action=send channel=discord target="#support" message="重置密码见 <https://docs.example.com/reset>,按步骤操作即可" replyTo="1122334455"
```

结果:提问消息下出现线程式回复,附带文档链接.
## 异常处理

| 错误场景 | 触发原因 | 处理方式 |
|:-----|:-----|:-----|
| 频道名找不到 | `target="#name"` 拼写错误或机器人不在该服务器 | 核对频道名拼写;确认机器人已加入目标服务器 |
| `replyTo` 无效 | 指定的 message-id 不存在或已删除 | 先 `action=read` 确认消息存在;`replyTo` 消息须与 `target` 同频道 |
| emoji 不存在 | `react` 传入了服务器没有的自定义表情 | 改用标准 unicode emoji(如 👍、✅) |
| 消息发送被拒 | 机器人缺少该频道发送权限 | 联系服务器管理员授予 `SEND_MESSAGES` 权限 |
| 链接预览撑爆频道 | 未用 `<>` 包裹链接 | 在链接外包裹 `<>`,如 `<https://example.com>` |

## 常见问题

### Q1:`target` 用频道名和频道 ID 有什么区别?
频道名带 `#` 前缀(如 `#general`)更可读;频道 ID(纯数字)更精确,适合频道名含特殊字符或存在重名的场景。两者效果一致.
### Q2:免费版能搜索历史消息吗?
不能。全文搜索(`action=search`)、消息编辑(`action=edit`)、消息删除(`action=delete`)、频道管理(`channel-list`/`channel-info`)、消息特效等属于付费版 discord-chat 的高级能力。免费版仅支持发送、回复、读取与表情回应.
### Q3:`replyTo` 的消息必须在同一频道吗?
是的。`replyTo` 指定的消息 ID 必须与 `target` 频道一致,跨频道回复会报错。跨频道内容应先 `action=read` 取出再 `action=send` 到目标频道.
### Q4:为什么我的消息里表格显示成一堆竖线?
Discord 不渲染 markdown 表格,会把 `| 列 | 列 |` 原样显示。应改用项目符号列表(`- 项目`)或粗体分组来呈现结构化信息.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 仅支持消息发送、线程回复、历史读取与表情回应,不含搜索、编辑、删除、频道管理、消息特效等高级能力.
- 所有操作依赖 gateway config 中配置的 Discord bot token.
- `replyTo` 消息须与 `target` 同一频道,跨频道回复会报错.
- `limit` 有上限,大量历史需分页读取.
- markdown 表格不被渲染,结构化内容应改用列表.
- 受 Discord 速率限制,高频发送会被 429 限流.
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