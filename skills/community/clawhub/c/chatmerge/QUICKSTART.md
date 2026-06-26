# ChatMerge - 快速开始

## 🚀 5 分钟上手指南

---

## 方式 1：一键自动读取（推荐）⭐

### 最简单的使用

```
使用 $chatmerge，总结我昨天的讨论
```

ChatMerge 会自动：
1. 列出昨天有活动的所有频道
2. 让你选择要总结的频道
3. 生成智能纪要

### 指定频道

```
使用 $chatmerge，总结 Discord #project-alpha 和 Slack #team-chat 最近 100 条消息
```

---

## 方式 2：文件导入

如果你有导出的聊天记录文件：

```
使用 $chatmerge，总结这个文件：/path/to/chat-export.json
```

**支持格式：** JSON, CSV, TXT, HTML

---

## 方式 3：手动粘贴

直接粘贴聊天记录：

```
使用 $chatmerge

[粘贴你的聊天记录]
```

---

## 📋 常见场景

### 1. 每日站会纪要

```
使用 $chatmerge，总结昨天 Discord #dev-team 和 Slack #project-alpha 的讨论，生成站会纪要
```

### 2. 定时自动纪要 ⭐ 新功能

**设置一次，永久自动：**

```
使用 $chatmerge，设置每天早上 9 点自动生成站会纪要，包含 Discord #project-alpha 和 Slack #team-chat，发送到 Slack #standup-notes
```

**每天早上自动收到昨天的纪要！**

### 3. 实时监控 ⭐ 新功能

**关键事件立即通知：**

```
使用 $chatmerge，监控 Discord #project-alpha，有紧急情况通知我
```

**发现 P0 bug 立即通知！**

### 4. 行动项自动跟踪 ⭐ 新功能

**自动创建任务并跟踪：**

```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，并创建行动项到 Jira
```

**自动创建 Jira ticket + 日历提醒 + 进度跟踪！**

### 5. 客户反馈汇总

```
使用 $chatmerge，整理 Slack #customer-support 最近 200 条消息，提取客户反馈
```

### 6. 管理层周报

**CEO 视角，极简摘要：**

```
使用 $chatmerge，汇总本周 Telegram "产品讨论群" 的所有讨论，生成 CEO 视角周报
```

**只看关键结论和风险！**

---

## 🔧 首次使用配置

### 如果你还没有配置聊天平台

ChatMerge 需要 OpenClaw 已经配置好聊天平台才能直接读取消息。

**配置方法：**

1. 编辑 `~/.openclaw/openclaw.json`
2. 添加你要使用的平台配置

**Discord 示例：**
```json
{
  "channels": {
    "discord": {
      "token": "YOUR_DISCORD_BOT_TOKEN"
    }
  }
}
```

**Slack 示例：**
```json
{
  "channels": {
    "slack": {
      "botToken": "xoxb-your-bot-token",
      "appToken": "xapp-your-app-token"
    }
  }
}
```

**Telegram 示例：**
```json
{
  "channels": {
    "telegram": {
      "token": "YOUR_TELEGRAM_BOT_TOKEN"
    }
  }
}
```

详细配置请参考 [OpenClaw 文档](https://docs.openclaw.com)

### 如果你不想配置

没问题！使用**文件导入**或**手动粘贴**方式，无需任何配置。

---

## 📊 输出内容

### 基础纪要
- 📊 核心摘要（3-5 条关键结论）
- 💬 关键讨论（按主题分组）
- ✅ 决策记录
- 📋 行动项（任务/负责人/截止时间/状态）
- ⚠️ 风险与阻塞（分级：高/中/低）
- ❓ 待跟进问题

### 高级分析 ⭐ V2.0 新增
- 🔄 跨平台讨论追踪（识别同一讨论）
- 👥 人员分析（发言统计、活跃时段、沉默成员）
- 😊 情绪分析（整体情绪、焦虑话题、积极话题）
- ⚡ 效率分析（决策效率、行动项完成率）
- 🤖 AI 智能建议（效率、风险、流程）

---

## 🎯 高级用法

### 指定输出格式

```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，输出 JSON 格式
```

### 指定纪要类型

```
使用 $chatmerge，生成简洁版站会纪要（Discord #dev-team，最近 50 条）
```

### 指定视角 ⭐ 新功能

```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，CEO 视角
```

**三种视角：**
- **CEO 视角：** 极简，只看结果和风险
- **项目经理视角：** 详细，关注进度和资源
- **开发者视角：** 技术细节

### 多渠道汇总

```
使用 $chatmerge，汇总以下渠道的讨论：
- Discord #project-alpha
- Slack #team-chat
- Telegram "产品讨论群"
```

### 包含多维度分析 ⭐ 新功能

```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，包含多维度分析
```

---

## 🆕 V2.0 新功能快速体验

### 1. 智能频道发现

```
使用 $chatmerge，总结我昨天的讨论
```

ChatMerge 会自动列出昨天有活动的频道，让你选择。

### 2. 定时纪要

```
使用 $chatmerge，设置每天早上 9 点自动生成站会纪要
```

设置一次，永久自动！

### 3. 实时监控

```
使用 $chatmerge，监控 Discord #project-alpha，有紧急情况通知我
```

关键事件立即通知！

### 4. 行动项跟踪

```
使用 $chatmerge，总结 Discord #project-alpha 最近 100 条消息，并创建行动项到 Jira
```

自动创建任务并跟踪进度！

### 5. 管理定时任务

**查看所有定时任务：**
```
使用 $chatmerge，显示所有定时纪要
```

**暂停定时任务：**
```
使用 $chatmerge，暂停"每日站会纪要"
```

**删除定时任务：**
```
使用 $chatmerge，删除"每日站会纪要"
```

### 6. 管理监控任务

**查看所有监控：**
```
使用 $chatmerge，显示所有监控任务
```

**停止监控：**
```
使用 $chatmerge，停止监控 Discord #project-alpha
```

---

## ⚠️ 注意事项

1. **权限：** 确保你有权限访问要读取的频道
2. **配置：** 直接读取模式需要先配置聊天平台（或使用文件导入/手动粘贴）
3. **隐私：** 本 Skill 不会存储你的聊天记录
4. **限制：** 建议一次处理 500 条消息以内，超过 1000 条建议分批
5. **授权：** 行动项跟踪需要配置 Jira/Notion/GitHub 的 API token

---

## 🆘 常见问题

### Q: 提示"频道未配置"怎么办？
A: 需要先在 OpenClaw 中配置该平台，或使用文件导入/手动粘贴方式。

### Q: 如何获取频道 ID？
A: 大多数情况下可以直接使用频道名称（如 #project-alpha），ChatMerge 会自动查找。

### Q: 支持私聊吗？
A: 支持，但需要确保 Bot 有权限访问私聊消息。

### Q: 可以处理多少条消息？
A: 建议 500 条以内效果最好，超过 1000 条建议分批处理。

### Q: 定时纪要会自动发送吗？
A: 是的，设置后会按时自动生成并发送到指定目标（Slack、邮件等）。

### Q: 实时监控会一直运行吗？
A: 是的，直到你手动停止监控。

### Q: 行动项跟踪需要什么配置？
A: 需要配置 Jira/Notion/GitHub 的 API token，详见 [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)。

### Q: 如何查看我的定时任务和监控任务？
A: 使用命令：
```
使用 $chatmerge，显示所有定时纪要
使用 $chatmerge，显示所有监控任务
```

---

## 📚 更多文档

- [README.md](README.md) - 完整项目介绍
- [SKILL.md](SKILL.md) - 详细功能说明
- [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) - 高级功能配置指南
- [配置参考](references/config-schema.md) - 详细配置选项
- [输出示例](references/output-examples.md) - 真实场景示例

---

## 🎉 开始使用

现在就试试吧！

```
使用 $chatmerge，总结我昨天的讨论
```

**10 秒生成智能纪要！**

---

**需要帮助？** 查看 [README.md](README.md) 或 [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)
