# Storage Schema

## alarms.json

```json
[
  {
    "id": "alarm_20260311_001",
    "title": "起床",
    "time": "2026-03-12T07:30:00+09:00",
    "timezone": "Asia/Tokyo",
    "repeat": "none",
    "priority": "high",
    "note": "工作日早起",
    "delivery": "main-session",
    "status": "active",
    "createdAt": "2026-03-11T21:00:00+09:00"
  }
]
```

## todos.json

```json
[
  {
    "id": "todo_20260311_001",
    "title": "交报表",
    "category": "工作",
    "priority": "high",
    "status": "todo",
    "dueAt": "2026-03-14T18:00:00+09:00",
    "tags": ["报表", "财务"],
    "note": "发给财务和主管",
    "createdAt": "2026-03-11T21:10:00+09:00",
    "updatedAt": "2026-03-11T21:10:00+09:00"
  }
]
```

## memos.md

```md
# Memos

## 2026-03-11 21:15
- 标题：客户偏好
- 分类：工作
- 内容：客户更喜欢极简、浅灰、留白多的页面风格。
- 标签：客户 / 设计 / 偏好
```

## daily_digest.md

建议结构：

```md
# 今日任务摘要

## 今天到期
- 交报表（18:00）

## 高优先级
- 回客户消息

## 逾期未完成
- 跟进付款

## 一句话建议
先处理 18:00 前必须完成的事项，再做低优先级整理类任务。
```
