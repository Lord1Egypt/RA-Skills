---
name: feishu-user-md
description: 飞书端读取USER.md任务清单。当用户说"查看任务"、"我的任务"时触发，实时解析并返回格式化的分类任务列表，让用户快速了解当前所有可用任务和技能。
version: 1.1.0
author: 349840432m-dev
license: MIT
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "📋"
    files: ["scripts/*"]
---

# Feishu User.md Reader - 飞书任务清单查询

实时读取 `~/.openclaw/workspace/USER.md`，解析任务清单并格式化为分类列表返回。

## 核心功能

### 实时任务解析
从 `~/.openclaw/workspace/USER.md` 读取三类数据源：
1. **常规任务清单表格** → 提取任务名、频率、技能名、描述
2. **日常自动化表格** → 提取定时任务时间和名称
3. **手动触发指令表格** → 提取触发词映射

### 智能分类
任务按用途自动归类：
- 📝 **内容创作** — 图片提示词、API图片、知识漫画、信息图
- 📕 **小红书运营** — 完整运营、发布、卡片生成
- 📤 **内容发布** — 微信公众号、Markdown转HTML
- 🔧 **工具** — 翻译、图片压缩、网页抓取、数据导出
- 📰 **新闻与SEO** — 添加/撰写新闻、SEO文章
- 📂 **日常管理** — 对话归档、Token统计、周报、日历
- 📁 **其他** — 未匹配的任务

### 输出格式

**注意**：返回内容动态读取 USER.md 实际内容，不硬编码。

```
📋 您的任务清单（共N项）

【定时自动化】
• 0:00 对话记录自动归档
• 9:00 Token日报生成

【内容创作】
• 图片提示词生成 - 说"生成图片提示词"
• API图片生成 - 说"生成图片"

💡 直接发送任务关键词即可触发
```

## 触发指令

| 指令 | 说明 |
|------|------|
| `查看任务` | 基础触发指令 |
| `我的任务` | 简写形式 |
| `有什么技能` | 查看可用技能 |
| `帮助` / `?` | 帮助信息 |

## 使用方法

```bash
node scripts/feishu-user-md.js read   # 格式化输出
node scripts/feishu-user-md.js json   # JSON 输出
```

## 技术实现

- Node.js 脚本，仅使用内置模块（`fs`、`path`、`os`），无第三方依赖
- 正则表达式解析 Markdown 表格
- 按关键词自动归类任务
- 每次调用**实时读取** USER.md，无缓存

### 解析流程
1. `readUserMd()` — 读取文件内容
2. `parseUserMd(content)` — 提取常规任务、定时任务、触发指令
3. `categorize(tasks)` — 按用途关键词分类
4. `formatForFeishu(data)` — 格式化为飞书消息文本

## 文件位置

- **技能目录**: `skills/feishu-user-md/`
- **脚本文件**: `skills/feishu-user-md/scripts/feishu-user-md.js`
- **数据源**: `~/.openclaw/workspace/USER.md`

## 注意事项

1. **无缓存** — 每次调用都实时读取 USER.md，更新后立即生效
2. **动态触发** — 所有触发指令从 USER.md 的"手动触发指令"表格动态读取
3. **自动同步** — 新增/删除任务只需修改 USER.md，飞书端自动同步
4. **内容动态** — 返回内容根据 USER.md 实际内容生成，不硬编码

## Security & Privacy

- 仅读取本地 `~/.openclaw/workspace/USER.md` 文件
- 不进行任何网络请求，不发送数据到外部
- 不写入任何文件，不存储用户数据
- 无持久化操作，无后台进程
