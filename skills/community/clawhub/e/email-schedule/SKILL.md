---
name: email-schedule
description: 从 macOS 邮件应用检索邮件，并根据邮件中的事件信息创建提醒事项。支持按时间范围（今天、昨天到今天、未读）检索邮件，自动提取会议、活动等时间信息，在事件发生前2小时设置提醒。Use when: (1) 用户要求查看指定范围的邮件并创建提醒, (2) 需要从邮件中提取日程并设置提醒, (3) 自动识别邮件中的会议时间并添加到提醒事项。
---

# 邮件日程 (Email Schedule)

从 macOS 邮件应用检索邮件，并根据邮件内容自动创建提醒事项。

## 功能

1. **邮件检索** - 从 macOS 邮件应用数据库读取邮件
2. **智能识别** - 从邮件主题和内容中提取会议/活动时间
3. **自动提醒** - 在事件发生前 2 小时设置提醒事项

## 支持的时间范围

- `today` - 今天收到的邮件
- `yesterday` - 昨天到今天收到的邮件
- `unread` - 所有未读邮件
- `all` - 最近 50 封邮件

## 使用流程

当用户要求处理邮件时：

### 1. 确认检索范围

询问或确认用户要查看的邮件范围：
- "今天的邮件"
- "昨天到今天的邮件"
- "未读邮件"
- "最近邮件"

### 2. 执行邮件检索

```bash
./scripts/fetch_emails.sh <范围>
```

范围参数：`today` | `yesterday` | `unread` | `all`

### 3. 创建提醒事项

将邮件 JSON 传递给创建脚本：

```bash
./scripts/fetch_emails.sh <范围> | ./scripts/create_reminders.py
```

### 4. 返回结果

格式：
```
📧 邮件检索完成

查看邮件数量: X
创建提醒数量: Y

提醒详情:
• [事件名称] - [时间]
• ...
```

## 时间识别规则

脚本会自动识别以下格式的时间：

- `2026年3月31日 14:30`
- `3月31日 下午2点`
- `明天 上午10点`
- `下周一 14:00`
- `3/31 14:30`

## 依赖

- macOS 自带邮件应用
- Python 3
- sqlite3
- remindctl (`brew install steipete/tap/remindctl`)

## 手动查询示例

直接在终端查询今日邮件：

```bash
# 查询今天的邮件（正确的 SQL）
sqlite3 ~/Library/Mail/V10/MailData/Envelope\ Index \
  "SELECT datetime(m.date_received, 'unixepoch', 'localtime') as date, 
          a.address as sender, 
          s.subject 
   FROM messages m 
   LEFT JOIN addresses a ON m.sender = a.ROWID 
   LEFT JOIN subjects s ON m.subject = s.ROWID 
   WHERE date(m.date_received, 'unixepoch') = date('now') 
   ORDER BY m.date_received DESC"
```

## 技术说明

### 时间戳处理

macOS 邮件数据库中的 `date_received` 和 `date_sent` 字段存储的是 **Unix 时间戳**（相对于1970年1月1日的秒数）。

正确的 SQL 查询方式：
```sql
-- 正确：直接使用 unixepoch 转换
SELECT datetime(date_received, 'unixepoch', 'localtime') as date
FROM messages

-- 错误：不需要添加偏移量（这是旧版 Mac CFAbsoluteTime 的方式）
-- SELECT datetime(date_received + 978307200, 'unixepoch') -- 会导致日期错误（显示为2057年）
```

### 限制说明

- 仅支持 macOS 系统自带的邮件应用
- 需要邮件应用数据库位于默认路径：`~/Library/Mail/V10/MailData/Envelope Index`
- 提醒事项会创建在默认的"提醒事项"列表中
- 仅对识别出未来时间的邮件创建提醒

## 脚本说明

### fetch_emails.sh
查询邮件数据库，关联 subjects、addresses、summaries 表获取实际文本内容，返回 JSON 格式的邮件列表。

### create_reminders.py
解析邮件内容，提取时间信息，使用 remindctl CLI 创建提醒事项。
