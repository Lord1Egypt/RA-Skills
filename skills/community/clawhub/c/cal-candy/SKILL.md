---
name: cal-candy
description: Local markdown-based calendar management. Use for: (1) Adding calendar events with date, time, title and optional description, (2) Listing upcoming or past events, (3) Viewing calendar in monthly format, (4) Checking today's events, (5) Setting reminders for events, (6) Deleting events. Triggered when user mentions calendar, events, schedule, reminders, or wants to manage time-bound tasks.
author: googcheng@qq.com
---

# Cal-Candy - Markdown Calendar

基于本地 Markdown 文件的日历系统，事件默认存储在 `~/.openclaw/workspace/calendar/` 目录, user can set the location by env MDCAL_DIR。

## 快速开始

所有命令通过 `python scripts/mdcal.py <command>` 执行：

### 添加事件
```bash
python scripts/mdcal.py add <date> <time> <title> [desc] [-r minutes]
```
- `date`: 日期 (YYYY-MM-DD) 或 `today`/`tomorrow`
- `time`: 时间 (HH:MM)
- `title`: 事件标题
- `desc`: 可选描述
- `-r`: 可选提醒（提前分钟数）

**示例:**
```bash
python scripts/mdcal.py add today 14:00 团队会议 :: 讨论项目进度 -r 15
python scripts/mdcal.py add 2026-04-01 10:00 "openclaw meeting"
```

### 查看事件
```bash
python scripts/mdcal.py list [month] [-a]
```
- `month`: 月份 (YYYY-MM 或 MM)，默认当月
- `-a`: 显示所有事件包括过去的

**示例:**
```bash
python scripts/mdcal.py list          # 当月事件
python scripts/mdcal.py list -a       # 显示所有
python scripts/mdcal.py list 2026-03  # 指定月
```

### 日历视图
```bash
python scripts/mdcal.py view [year] [month]
```
以日历格式显示本月或指定月份。

### 今日事件
```bash
python scripts/mdcal.py today
```

### 即将到来
```bash
python scripts/mdcal.py upcoming [-d days]
```
默认显示未来7天事件。

### 设置提醒
```bash
python scripts/mdcal.py remind [event_id] [minutes]
```
查看或设置事件提醒。

### 删除事件
```bash
python scripts/mdcal.py delete <event_id>
```
事件ID为5位UUID，列出会显示在事件后面。

## 数据存储

- **日历文件**: `~/.openclaw/workspace/calendar/YYYY-MM.md`
- **提醒文件**: `~/.openclaw/workspace/calendar/reminders.json`

事件格式：
```markdown
- [ ] 2026-03-22 14:00 会议标题 :: 描述 #abc12
```

## 常用场景

1. **查看今天有啥安排**: `python scripts/mdcal.py today`
2. **查看本月日程**: `python scripts/mdcal.py list`
3. **添加会议**: `python scripts/mdcal.py add tomorrow 15:00 会议 :: 讨论Q1目标 -r 10`
4. **添加提醒**: `python scripts/mdcal.py remind <event_id> 15`
