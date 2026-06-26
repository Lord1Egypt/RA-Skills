# 任务与提醒系统

Use when the user asks what to do next, wants reminders, or needs a follow-up/task operating system.

## Task Types

- customer_follow_up
- customer_birthday_or_event
- sales_review
- team_1on1
- employee_training
- weekly_review
- cash_flow_check
- content_publish
- old_customer_reactivation
- complaint_resolution

## Task Schema

```json
{
  "type": "owner_task",
  "title": "",
  "category": "",
  "owner": "",
  "target_object": "",
  "due_date": "",
  "priority": "low|medium|high",
  "action": "",
  "acceptance_standard": "",
  "metric": "",
  "status": "todo|doing|done|overdue",
  "notes": ""
}
```

## Reminder Rules

- Customer birthday/event: remind 3 days before and same day.
- Next customer follow-up: remind same morning.
- Employee 1-on-1: remind 1 day before.
- Weekly review: every week same day/time.
- Cash flow check: weekly for small teams, daily when cash is tight.
- Complaint resolution: same day response, 24-hour follow-up.

## Output Pattern

```markdown
**本周任务**
| 任务 | 对象 | 负责人 | 截止时间 | 验收标准 |
|---|---|---|---|---|

**提醒**
- ...

**逾期风险**
- ...
```

## Prioritization

High priority if:
- affects cash flow
- high-value customer
- complaint or churn risk
- key employee risk
- deadline within 48 hours

Low priority if:
- no clear business result
- no owner
- no deadline
- only "nice to have"
