---
name: chatmerge
description: "汇总多平台聊天记录，生成结构化纪要（摘要、决策、行动项、风险）。Summarize multi-platform chats into structured minutes with summaries, decisions, action items, and risks."
metadata:
  openclaw:
    emoji: "💬📊"
    requires:
      tools: ["message"]
allowed-tools: ["message", "bash", "read", "write"]
---

# ChatMerge - 多渠道聊天纪要助手

## Overview

把多渠道聊天记录整理成可执行、可追溯、低幻觉的纪要。默认输出简体中文，适合站会纪要、项目同步、客户反馈汇总和管理层简报。

**核心能力：** 支持直接读取 OpenClaw 已配置的 20+ 聊天平台，或处理用户提供的导出文件/粘贴内容。

## Use This Skill When

- 用户要汇总 Discord、Slack、Telegram、企业微信、钉钉等多个来源的聊天内容
- 用户要把多群聊天整理成日报、周报、站会纪要、项目纪要、客户反馈摘要或高管简报
- 用户提到具体的频道/群组名称（如"Discord #project-alpha"）
- 用户提供导出文件、粘贴文本或 OCR 结果

## Input Modes

### 🚀 优先级 1：直接读取（最便捷）

使用 OpenClaw 的 `message` tool 直接读取已配置频道的消息。

**支持平台：** Discord, Slack, Telegram, 企业微信/Feishu, 钉钉, WhatsApp, Signal, iMessage, Google Chat, Microsoft Teams, Matrix, LINE, Mattermost, IRC 等 20+ 平台

**触发条件：**
- 用户提到具体平台和频道（如"Discord #project-alpha"、"Slack #team-chat"）
- 用户要求读取"最近 N 条消息"或"过去 24 小时的消息"

**实现方式：**
```json
{
  "action": "read",
  "channel": "discord",  // 或 "slack", "telegram" 等
  "to": "channel:123456",  // 频道 ID
  "limit": 100  // 消息数量
}
```

**错误处理：**
- 如果频道未配置或无权限，提示用户并降级到其他模式
- 如果用户没有提供频道 ID，尝试通过频道名称查找

### 📁 优先级 2：文件导入（最灵活）

用户提供导出的聊天记录文件。

**支持格式：**
- JSON (Slack/Discord 官方导出)
- CSV
- TXT (纯文本)
- HTML (Telegram 导出)

**触发条件：**
- 用户提供文件路径
- 用户上传文件
- 用户说"我有一个导出文件"

**实现方式：**
使用 `read` tool 读取文件，解析格式，提取消息

### 📋 优先级 3：手动粘贴（最简单）

用户直接粘贴聊天内容（降级方案）。

**触发条件：**
- 用户直接粘贴大段文本
- 前两种方式都不可用

**实现方式：**
直接处理用户提供的文本内容

---

**按需参考文档：**
- 处理复杂格式或需要归一化时 → [input-contract.md](references/input-contract.md)
- 用户要求可复用配置时 → [config-schema.md](references/config-schema.md)
- 需要 JSON 输出或特定格式时 → [output-examples.md](references/output-examples.md)

## Default Assumptions

- 未指定范围时，默认总结用户给出的全部消息；如果用户明确是定期纪要，再默认 `last_24h`
- 默认输出 `zh-CN` 和 `markdown`
- 默认包含 `核心摘要`、`关键讨论`、`决策记录`、`行动项`、`风险与阻塞`、`待跟进问题`
- 无法确认的负责人、截止时间、优先级统一写成 `待确认`
- 如果来源不全、时间戳缺失、渠道抓取失败或有 OCR 噪声，要在开头显式标注

## Workflow

### 1. 理解与准备（Understand & Prepare）
- 判断纪要类型：站会、项目同步、客户反馈、管理摘要或通用纪要
- 合并多来源消息，保留关键元数据（平台、频道、作者、时间）
- 过滤明显噪声（系统通知、广告），但保留短句确认/否决/升级信息

### 2. 分析与提取（Analyze & Extract）
- 基于回复关系、线程、提及、时间邻近度进行主题聚类
- 提取明确的决策、行动项、风险、阻塞、指标、客户反馈
- 行动项格式：`任务 / 负责人 / 截止时间 / 状态 / 来源`
- **保守原则：** 没有证据时，不擅自补全 owner、deadline、优先级

### 3. 生成与标注（Generate & Annotate）
- 输出结构：核心摘要（3-5 条）→ 关键讨论 → 决策 → 行动项 → 风险 → 待跟进
- 管理摘要优先结果和风险；执行纪要保留更多上下文
- 标注不确定性：缺失渠道、抓取失败、时间范围不明、推断结论

## Output Rules

**结构要求：**
- 核心摘要：3-5 条关键结论
- 关键讨论：按主题组织（非按平台机械分段）
- 决策记录：只收录明确结论（倾向性表态不算）
- 行动项：可执行优先，缺失字段写 `待确认`
- 风险与阻塞：只列真正影响推进的事项

**引用原则：**
- 优先引用高信号句，避免大段复述
- 保留来源（平台、频道、时间）方便追溯
- 不泄露 token、cookie、webhook、内部链接
- 未经要求不输出整段原始聊天记录
- 拒绝总结用户无权访问的渠道内容
