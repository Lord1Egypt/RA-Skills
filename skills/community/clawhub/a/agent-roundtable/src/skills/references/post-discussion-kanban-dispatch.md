# Post-Discussion: Kanban Task Dispatch

After a roundtable discussion concludes with action items, the coordinator
should create kanban tasks and dispatch to team members.

## Pattern

```
Roundtable Conclusion
  ↓
Create kanban tasks (one per person, grouped by owner)
  ↓
Subscribe notifications (company group + individual groups)
  ↓
Notify each person in their Feishu group
  ↓
Gateway Dispatcher auto-assigns to worker agents
```

## Task Creation

Group P0 action items by owner, create one comprehensive task per person:

```bash
hermes kanban create "【P0】Project Name + Brief Description" \
  --assignee mafei \
  --body "## 任务来源
圆桌讨论 rt_xxxxxxxx 结论。

## 任务内容
1. **Task 1** (0.5天)
   - Detail...
2. **Task 2** (1天)
   - Detail...

## 截止时间
5/28（周三）Code Freeze

## 验收标准
- [ ] Criterion 1
- [ ] Criterion 2

## 参考文档
docs/roundtable-open-source-readiness.md"
```

## Three-Step Dispatch (from kanban-orchestrator)

```bash
# 1. Subscribe task notifications to company group
hermes kanban notify-subscribe $TASK_ID \
  --platform feishu --chat-id oc_your_company_group_id \
  --notifier-profile default

# 2. Notify individual in their team group
python3 ~/.hermes/scripts/feishu-send.py default oc_dev_team_group_id \
  '🚀 【P0任务】Brief description\n\n📋 task_id: title\n⏰ 截止: date\n📄 详情: doc_path'

# 3. Dispatcher auto-picks up ready tasks
```

## Feishu Group Mapping (OPC Team)

| Member | Role | Group Chat ID |
|--------|------|---------------|
| 饼哥 | Product Director | oc_product_team_group_id |
| 像素姐 | Designer | oc_design_team_group_id |
| 码飞 | Developer | oc_dev_team_group_id |
| 公司群 | All | oc_your_company_group_id |

## Example: AI Relay Open-Source (2026-05-23)

Discussion `rt_xxxxxxxx` produced 4 kanban tasks:

| Task ID | Assignee | Title | Status |
|---------|----------|-------|--------|
| t_xxxxxxxx | mafei | 安全扫描+密钥清理+License合规 | done |
| t_xxxxxxxx | mafei | CI/CD流水线+本地构建脚本 | done |
| t_xxxxxxxx | bingge | README+QuickStart+Issue/PR模板 | done |
| t_xxxxxxxx | pixiel | Logo+视觉底线+截图素材 | done |

All 4 tasks completed within the same day. Gateway Dispatcher auto-assigned
to worker agents after creation.

## Key Lessons

1. **Group tasks by owner** — Don't create one task per sub-item; bundle related items into one comprehensive task per person
2. **Include context in task body** — File paths, existing code structure, API format, reference docs
3. **Subscribe BEFORE dispatch** — Notifications must be set up before the worker starts, or you miss the start event
4. **Check completion** — After tasks are done, verify deliverables before marking as accepted
