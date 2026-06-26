---
name: feishu-task-plus
description: |
  飞书任务管理增强版 - 高级任务与清单管理工具。
  
  **基础功能**（免费）：
  - 创建、查询、更新任务
  - 任务完成/反完成
  - 创建和管理任务清单
  
  **高级功能**（付费）：
  - 子任务（Subtask）管理
  - 高级筛选与批量操作
  - 任务评论与讨论
  - 重复任务模板
  - 优先级标记
  - 任务统计与报告
  
  **触发条件**：
  - 用户提到"任务"、"待办"、"to-do"、"清单"、"task"
  - 需要批量操作或高级管理功能
---

# 飞书任务管理增强版

## 🚨 执行前必读

- ✅ **时间格式**：ISO 8601 / RFC 3339（带时区），例如 `2026-02-28T17:00:00+08:00`
- ✅ **current_user_id 强烈建议**：从消息上下文的 SenderId 获取（ou_...），工具会自动添加为 follower
- ✅ **patch/get 必须**：task_guid
- ✅ **tasklist.tasks 必须**：tasklist_guid
- ✅ **完成任务**：completed_at = "2026-02-26 15:00:00"
- ✅ **反完成**：completed_at = "0"

---

## 📋 快速索引

| 用户意图 | 工具 | action | 必填参数 |
|---------|------|--------|---------|
| 新建待办 | feishu_task_task | create | summary |
| 查未完成任务 | feishu_task_task | list | - |
| 获取任务详情 | feishu_task_task | get | task_guid |
| 完成任务 | feishu_task_task | patch | task_guid, completed_at |
| 创建清单 | feishu_task_tasklist | create | name |
| 查看清单任务 | feishu_task_tasklist | tasks | tasklist_guid |
| **创建子任务** | feishu_task_subtask | create | task_guid, summary |
| **查看子任务** | feishu_task_subtask | list | task_guid |
| **添加评论** | feishu_task_comment | create | task_guid, content |
| **查看评论** | feishu_task_comment | list | task_guid |

---

## 🛠️ 高级功能（付费版）

### 1. 子任务管理

创建子任务：
```json
{
  "action": "create",
  "task_guid": "父任务GUID",
  "summary": "子任务标题",
  "description": "子任务描述",
  "due": {"timestamp": "2026-03-05 18:00:00", "is_all_day": false},
  "members": [
    {"id": "ou_xxx", "role": "assignee"}
  ]
}
```

查看子任务列表：
```json
{
  "action": "list",
  "task_guid": "父任务GUID"
}
```

### 2. 任务评论

添加评论：
```json
{
  "action": "create",
  "task_guid": "任务GUID",
  "content": "评论内容，最长3000字符"
}
```

查看评论：
```json
{
  "action": "list",
  "task_guid": "任务GUID",
  "direction": "desc"
}
```

回复评论：
```json
{
  "action": "create",
  "task_guid": "任务GUID",
  "content": "回复内容",
  "reply_to_comment_id": "被回复的评论ID"
}
```

### 3. 重复任务

```json
{
  "action": "create",
  "summary": "每周例会",
  "due": {"timestamp": "2026-03-03 14:00:00", "is_all_day": false},
  "repeat_rule": "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO"
}
```

支持的重复规则：
- 每天：FREQ=DAILY;INTERVAL=1
- 每周：FREQ=WEEKLY;INTERVAL=1;BYDAY=MO
- 每月：FREQ=MONTHLY;INTERVAL=1

---

## 💰 定价信息

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 基础任务创建、查询、完成 |
| 专业版 | ¥15/月 | +子任务、评论、重复任务 |
| 企业版 | ¥50/月 | +批量操作、统计报告、API |

---

## 📚 附录：任务资源关系

```
任务清单（Tasklist）
  └─ 任务（Task）
      ├─ 子任务（Subtask）
      ├─ 成员：负责人（assignee）、关注人（follower）
      ├─ 截止时间（due）
      └─ 评论（Comment）
```