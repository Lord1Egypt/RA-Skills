---
name: feishu-batch-task
description: |
  Feishu Batch Task Creator - Create multiple tasks at once with templates.
  
  **Features**:
  - Batch create tasks from template
  - Quick task creation for common patterns
  - Import tasks from CSV format
  - Support task templates with default values
  
  **Trigger**:
  - User mentions "batch task", "create multiple tasks", "批量创建任务"
  - User wants to create many tasks at once
---

# Feishu Batch Task Creator

## ⚠️ Pre-requisites

- ✅ **Time format**: ISO 8601 / RFC 3339 (with timezone), e.g. `2026-02-28T17:00:00+08:00`
- ✅ **current_user_id required**: Get from message context SenderId (ou_...)
- ✅ **Use batch_create for multiple tasks**: Up to 500 records at once

---

## 📋 Quick Reference

| Intent | Tool | action | Required Params |
|--------|------|--------|-----------------|
| Create single task | feishu_task_task | create | summary |
| Batch create tasks | feishu_bitable_app_table_record | batch_create | app_token, table_id, records |
| Query tasks | feishu_task_task | list | - |
| Complete task | feishu_task_task | patch | task_guid, completed_at |

---

## 🛠️ Usage

### 1. Batch Create Tasks via Bitable

Create a bitable template first, then batch import:

```json
{
  "action": "batch_create",
  "app_token": "Mxxx",
  "table_id": "Txxx",
  "records": [
    {"fields": {"任务名称": "任务1", "截止日期": 1740441600000, "负责人": [{"id": "ou_xxx"}]}},
    {"fields": {"任务名称": "任务2", "截止日期": 1740528000000, "负责人": [{"id": "ou_yyy"}]}},
    {"fields": {"任务名称": "任务3", "截止日期": 1740614400000, "负责人": [{"id": "ou_zzz"}]}}
  ]
}
```

### 2. Common Task Templates

**Daily Standup Template**:
```json
{
  "action": "create",
  "summary": "每日站会",
  "description": "同步昨日完成事项、今日计划、阻塞问题",
  "due": {"timestamp": "2026-03-31T18:00:00+08:00", "is_all_day": false},
  "repeat_rule": "FREQ=DAILY"
}
```

**Weekly Review Template**:
```json
{
  "action": "create",
  "summary": "周报提交",
  "description": "提交本周工作总结",
  "due": {"timestamp": "2026-04-04T17:00:00+08:00", "is_all_day": false},
  "repeat_rule": "FREQ=WEEKLY;INTERVAL=1;BYDAY=FR"
}
```

### 3. Task Template Bitable

Create a bitable for templates:
- Field: 任务名称 (Text)
- Field: 任务描述 (Text)  
- Field: 截止日期 (Date)
- Field: 负责人 (Person)
- Field: 优先级 (Single Select: 高/中/低)
- Field: 所属清单 (Text)

---

## 💰 Pricing

| Version | Price | Features |
|---------|-------|----------|
| Free | ¥0 | Single task creation |
| Pro | ¥10/month | Batch create, templates |
| Team | ¥30/month | CSV import, API access |

---

## 📝 Example

**User says**: "帮我批量创建5个任务，分别是需求评审、设计评审、开发评审、测试评审、上线评审，截止日期分别是下周一到周五"

**Execute**:
1. Calculate dates for each day
2. Batch create 5 tasks with proper dates and descriptions
3. Return created task list

---

## 🔧 Tips

- Use bitable for large batch operations (up to 500 at once)
- Date fields: use millisecond timestamp (e.g., 1740441600000)
- Person fields: use `{"id": "ou_xxx"}` format
- For repeating tasks, use `repeat_rule` RFC5545 format
