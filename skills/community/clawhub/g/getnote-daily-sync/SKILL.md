---
name: getnote-notion-daily
version: 1.0.0
description: >
  每日自动将 Get笔记（biji.com）当天的录音笔记、会议记录、待办事项汇总后写入
  Notion 数据库，生成结构化日报页面。
  Use when user says "同步今日 Get笔记", "生成今日日报", "把今天的笔记写到 Notion",
  "getnote daily sync", or triggers a scheduled daily note summary.
capabilities:
  - env://GETNOTE_API_KEY
  - env://GETNOTE_CLIENT_ID
  - env://NOTION_TOKEN
  - env://NOTION_DATABASE_ID
  - env://MY_NAME
  - network://openapi.biji.com
  - network://api.notion.com
examples:
  - "同步今日 Get笔记到 Notion"
  - "生成今日日报"
  - "把今天的 Get笔记写到 Notion"
  - "getnote daily sync"
---

# Get笔记 → Notion 每日日报 Skill

将你今天在 **Get笔记**（biji.com）录制的录音笔记、会议记录、灵感笔记自动汇总，生成一份结构化日报写入 **Notion** 数据库。

---

## 日报结构

每次同步后，Notion 中会创建一个新页面，包含：

- 📊 **今日概览** — 今天做了什么、最需要跟进的待办（Top 3）、今日关键洞察
- 🗣️ **客户会** — 每场会议的录音信息 + 总结 + 待办
- 🎤 **技术分享 / 录音** — 非会议类录音的摘要
- 💡 **个人灵感** — 文字类笔记
- 📌 **后续建议** — 含时间关键词的待办汇总

---

## 配置（环境变量）

在 OpenClaw 配置或 `.env` 文件中设置以下变量：

| 变量名 | 必填 | 说明 |
|---|---|---|
| `GETNOTE_API_KEY` | ✅ | Get笔记 API Key（在 Get笔记设置中获取） |
| `GETNOTE_CLIENT_ID` | ✅ | Get笔记 Client ID |
| `NOTION_TOKEN` | ✅ | Notion Integration Token（[创建方法](https://developers.notion.com/docs/create-a-notion-integration)） |
| `NOTION_DATABASE_ID` | ✅ | 目标 Notion 数据库 ID（从 Database URL 中提取） |
| `MY_NAME` | ❌ | 你的名字关键词，用于过滤"我需要跟进"的待办（例如 `Alice,我`）；留空则显示全部待办 |

### 获取 Notion Database ID

打开 Notion 数据库页面，URL 格式为：
```
https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
```
取 `?v=` 前的 32 位字符串即为 `NOTION_DATABASE_ID`。

### Notion Database 字段要求

目标 Database 需要包含以下字段（类型必须匹配）：

| 字段名 | 类型 |
|---|---|
| `Name` | Title（标题） |
| `date` | Date（日期） |
| `Summary` | Text（文本） |
| `Tags` | Multi-select |
| `Source` | Select |

---

## 使用方式

### 手动触发（问 AI）

直接对话即可：
> "同步今日 Get笔记到 Notion"

### 定时自动运行（推荐）

设置 OpenClaw Cron，每天晚上自动执行：

> "每天晚上 10 点同步今日 Get笔记到 Notion"

或手动添加 Cron Job：
```json
{
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "同步今日 Get笔记到 Notion"
  },
  "sessionTarget": "isolated"
}
```

---

## 工作原理

1. 调用 Get笔记 Open API 拉取今日全部笔记
2. 按类型分类（客户会 / 技术分享 / 个人灵感），过滤测试笔记
3. 提取录音信息、总结、待办、金句等结构化字段
4. 在 Notion 创建日报页面，写入所有内容

---

## 依赖

- Python 3（标准库，无需额外安装）
- Get笔记账号（biji.com）+ API Key
- Notion Integration + 目标 Database

---

## 运行脚本（直接执行）

```bash
export GETNOTE_API_KEY="your-key"
export GETNOTE_CLIENT_ID="your-client-id"
export NOTION_TOKEN="secret_xxx"
export NOTION_DATABASE_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export MY_NAME="你的名字"  # 可选

python3 skills/getnote-notion-daily/scripts/daily_sync.py
```
