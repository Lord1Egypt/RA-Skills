---
name: claw-calendar
description: "Calendar Skills 智能日历助手：通过 REST API 与 Claw Calendar (claw-calendar.com) 交互，管理日历和事件。凭证从环境变量读取，支持创建日历、添加事件、查询日程。"
description_zh: "Claw Calendar 智能日历助手 - 管理日历、创建事件、自动同步到手机原生日历"
description_en: "Smart Calendar Assistant - Manage calendars and events via Claw Calendar API"
version: 1.0.2
allowed-tools: Read,Write,Bash
metadata:
  openclaw:
    requires:
      env:
        - CLAW_CALENDAR_API_KEY
        - CLAW_CALENDAR_API_URL
    primaryEnv: CLAW_CALENDAR_API_KEY
    security:
      expectedPatterns:
        - pattern: "env_credential_access"
          reason: "Required to authenticate with Claw Calendar API. API key is read from environment variable and sent to the official claw-calendar.com API endpoint only."
---

## 何时使用

用户需要**管理日历**、**创建事件**、**设置提醒**或**订阅日历**时使用本 skill。

# Claw Calendar 智能日历助手

面向 Claw Calendar 云服务：通过 REST API 创建日历、添加事件，支持 .ics 订阅链接同步到手机原生日历。

## 凭证（环境变量）

| 变量 | 说明 |
|------|------|
| **CLAW_CALENDAR_API_KEY** | Claw Calendar API 密钥（在用户设置中生成） |
| **CLAW_CALENDAR_API_URL** | API 地址（可选，默认为 https://claw-calendar.com） |

脚本会校验 API Key，缺失时报错并退出。

## API 端点

- **Base URL**: `https://claw-calendar.com/api`（默认）
- **认证方式**: Bearer Token（API Key）

## 脚本

| 脚本 | 作用 |
|------|------|
| `scripts/list-calendars.js` | 列出用户所有日历 |
| `scripts/create-calendar.js` | 创建新日历，返回订阅链接 |
| `scripts/list-events.js` | 列出指定日历的事件 |
| `scripts/create-event.js` | 在日历中创建新事件 |

## 日历管理

### 列出日历

```bash
node scripts/list-calendars.js
```

输出：日历 ID、名称、颜色、订阅链接。

### 创建日历

```bash
# 必填：日历名称
node scripts/create-calendar.js --name "我的日历"

# 可选：描述、颜色
node scripts/create-calendar.js --name "股票提醒" --description "持仓股票重要日期" --color "#4f46e5"
```

输出：日历 ID、订阅链接（用于添加到手机日历）。

## 事件管理

### 列出事件

```bash
# 列出所有日历的事件
node scripts/list-events.js --calendar-id <calendarId>

# 按日期范围筛选
node scripts/list-events.js --calendar-id <calendarId> --start 2026-04-01 --end 2026-04-30
```

### 创建事件

```bash
# 必填：日历ID、标题、开始日期
node scripts/create-event.js --calendar-id <calendarId> --title "会议" --start-date 2026-04-15

# 完整参数示例
node scripts/create-event.js \
  --calendar-id <calendarId> \
  --title "招商银行分红" \
  --description "分红除权日，请注意股价变动" \
  --start-date 2026-04-15 \
  --end-date 2026-04-15 \
  --start-time "09:30:00" \
  --end-time "10:30:00" \
  --alarm \
  --alarm-minutes 1440
```

**事件参数**：

| 参数 | 说明 | 必填 |
|------|------|------|
| `--calendar-id` | 日历 ID | ✅ |
| `--title` | 事件标题 | ✅ |
| `--start-date` | 开始日期 (YYYY-MM-DD) | ✅ |
| `--end-date` | 结束日期 (YYYY-MM-DD) | 否 |
| `--start-time` | 开始时间 (HH:MM:SS) | 否 |
| `--end-time` | 结束时间 (HH:MM:SS) | 否 |
| `--description` | 事件描述 | 否 |
| `--location` | 地点 | 否 |
| `--alarm` | 启用提醒 | 否 |
| `--alarm-minutes` | 提前多少分钟提醒（默认 15） | 否 |

## 订阅日历到手机

创建日历后，会返回 `.ics` 订阅链接，按以下方式添加到手机日历：

- **iOS**: 设置 → 日历 → 账户 → 添加订阅日历 → 粘贴链接
- **Android**: 日历应用 → 更多 → 设置 → 添加日历 → 订阅日历
- **macOS**: 日历 → 文件 → 新建日历订阅 → 粘贴链接

## 安全提醒

- API Key 视为密码，不要提交到仓库或日志中
- 仅通过环境变量配置：`export CLAW_CALENDAR_API_KEY=your-key`
- 建议定期轮换 API Key

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 401 Unauthorized | API Key 无效或过期 | 检查环境变量或重新生成 Key |
| 403 Forbidden | 无权访问该日历 | 检查日历 ID 是否正确 |
| 404 Not Found | 日历不存在 | 确认日历 ID 或列出日历检查 |
