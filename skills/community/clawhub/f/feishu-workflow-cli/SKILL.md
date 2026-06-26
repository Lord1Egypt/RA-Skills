---
name: feishu-workflow-cli
description: "Orchestrate complex Feishu/Lark workflows using the official lark CLI (v1.0.40+, 200+ commands, 17 domains). Teach AI agents when and how to chain lark CLI commands into production-ready workflows for reporting, project management, meeting automation, document collaboration, and cross-domain orchestration. Covers: auto weekly report generation (Base→Doc→Mail→Message), project tracking dashboard (Tasks→Base→Calendar), meeting lifecycle automation (Calendar→VC→Doc→Wiki), approval-driven workflows (Approval→Message→Tasks), and data pipeline orchestration (Sheet→Base→Doc→Mail). Triggers on: 飞书CLI工作流, feishu workflow, lark CLI automation, 飞书自动化, feishu report automation, lark agent workflow, 飞书周报自动化, feishu meeting automation, lark task management, 飞书审批流程, feishu doc collaboration, lark base workflow, 飞书多维表格工作流, feishu calendar automation, lark mail automation, 飞书邮件自动化, agent feishu orchestration, AI飞书工作流"
---

# Feishu Workflow CLI - 飞书CLI工作流编排专家

You are an expert at orchestrating complex workflows within Feishu/Lark using the official `lark` CLI. You don't just run commands — you design end-to-end workflows that chain multiple domains into automated processes.

## Core Philosophy

**Single commands are tools. Chained commands are workflows. Your value is the workflow, not the command.**

The lark CLI covers 17 business domains with 200+ commands. Most users only use 2-3 domains in isolation. You teach agents how to combine domains into workflows that eliminate manual handoffs.

## CLI Quick Reference

### Installation & Auth
```bash
# Install
npm install -g @larksuite/cli

# Authenticate
lark auth login

# Verify
lark auth status

# Update to latest
npm update -g @larksuite/cli
```

### Domain Coverage (v1.0.40+)

| Domain | Key Commands | Workflow Role |
|--------|-------------|---------------|
| **Messenger** | `lark message send/list/reply` | Notification & alerts |
| **Docs** | `lark doc create/get/content` | Report generation |
| **Base** | `lark base record add/list/update` | Data storage & tracking |
| **Sheets** | `lark sheet read/write` | Data analysis |
| **Slides** | `lark slide create/add` | Presentation output |
| **Calendar** | `lark calendar event create/list` | Scheduling & triggers |
| **Mail** | `lark mail send/list` | External communication |
| **Tasks** | `lark task create/list/update` | Action tracking |
| **VC/Meetings** | `lark vc join/leave/events` | Meeting lifecycle |
| **Wiki** | `lark wiki create/list` | Knowledge management |
| **Contacts** | `lark contact search/list` | People lookup |
| **Drive** | `lark drive list/upload` | File management |
| **Approval** | `lark approval create/list` | Process governance |
| **Markdown** | `lark md convert` | Format transformation |

---

## Workflow Templates

### Workflow 1: 自动周报 (Auto Weekly Report)

**Scenario**: Pull data from Base/Sheets, generate a formatted Doc, email to stakeholders, notify team chat.

```bash
# Step 1: Collect completed tasks from Base
lark base record list --app <project_base> --table <tasks_table> \
  --filter '{"status":"completed","week":"current"}'

# Step 2: Collect calendar events for context
lark calendar event list --start "$(date -d '7 days ago' +%Y-%m-%dT00:00:00)" \
  --end "$(date +%Y-%m-%dT23:59:59)"

# Step 3: Create weekly report document
lark doc create --title "周报 $(date +%Y-W%V)" --folder <report_folder>

# Step 4: Write structured content
lark doc content --token <doc_token> --write "# 本周工作总结

## 关键成果
- [从Base数据提取]

## 会议纪要
- [从Calendar事件提取]

## 下周计划
- [从Tasks提取open tasks]

## 风险与阻塞
- [需要关注的事项]"

# Step 5: Email to stakeholders
lark mail send --to "manager@company.com" --subject "周报 $(date +%Y-W%V)" \
  --body "周报已生成，请查阅: <doc_link>"

# Step 6: Notify team chat
lark message send --chat <team_chat_id> \
  --text "📋 本周周报已生成: <doc_link>"
```

**Decision Points**:
- If Base has no completed tasks → check Tasks domain as fallback
- If manager prefers WeCom → use cross-platform workflow (see china-im-workflow-cli)
- If report needs charts → use Sheets to generate, then embed in Doc

### Workflow 2: 项目追踪看板 (Project Tracking Dashboard)

**Scenario**: Sync project data across Tasks, Base, and Calendar for a unified view.

```bash
# Step 1: Get all open tasks
lark task list --status open --assignee <user_id>

# Step 2: Get project milestones from Base
lark base record list --app <project_base> --table <milestones_table>

# Step 3: Get upcoming deadlines from Calendar
lark calendar event list --start "$(date +%Y-%m-%dT00:00:00)" \
  --end "$(date -d '+14 days' +%Y-%m-%dT23:59:59)"

# Step 4: Update Base dashboard with current status
lark base record update --app <project_base> --table <dashboard_table> \
  --id <record_id> --data '{"open_tasks":<count>,"upcoming_deadlines":<count>}'

# Step 5: Send status alert if overdue items exist
if [ <overdue_count> -gt 0 ]; then
  lark message send --chat <project_chat_id> \
    --text "⚠️ 项目有 <overdue_count> 个逾期任务，请关注"
fi
```

### Workflow 3: 会议生命周期自动化 (Meeting Lifecycle)

**Scenario**: From scheduling to follow-up, automate the entire meeting process.

```bash
# Phase 1: Schedule
lark calendar event create \
  --summary "项目评审会" \
  --start "2026-05-26T15:00:00" \
  --end "2026-05-26T16:00:00" \
  --attendees "user1,user2,user3"

# Phase 2: Pre-meeting prep (1 hour before)
lark doc create --title "会议纪要模板 - 项目评审会" --folder <meeting_folder>
lark message send --chat <project_chat_id> \
  --text "📋 评审会15:00开始，议程文档: <doc_link>"

# Phase 3: Meeting join (for AI agent)
lark vc join --meeting_id <meeting_id>
lark vc events --meeting_id <meeting_id>  # Monitor events

# Phase 4: Post-meeting actions
lark vc leave --meeting_id <meeting_id>

# Create follow-up tasks from meeting notes
lark task create --summary "落实评审会决议项1" --due "2026-06-02" --assignee <owner>
lark task create --summary "落实评审会决议项2" --due "2026-06-05" --assignee <owner>

# Update meeting doc with action items
lark doc content --token <doc_token> --write "## 决议事项
1. [决议1] - 负责人: xxx - 截止: 2026-06-02
2. [决议2] - 负责人: xxx - 截止: 2026-06-05"

# Notify attendees of action items
lark mail send --to "attendees@company.com" \
  --subject "评审会决议事项" \
  --body "会议决议已记录，请查阅: <doc_link>"
```

### Workflow 4: 审批驱动工作流 (Approval-Driven Workflow)

**Scenario**: Submit approval, track status, notify on result, create follow-up tasks.

```bash
# Step 1: Submit approval
lark approval create --definition <approval_code> \
  --data '{"title":"采购申请","amount":"50000","reason":"设备更新"}'

# Step 2: Monitor approval status (poll or webhook)
lark approval list --status pending --applicant <user_id>

# Step 3: On approval - create execution tasks
# (Triggered when status changes to approved)
lark task create --summary "执行采购 - 设备更新" --due "2026-06-15"
lark base record add --app <procurement_base> --table <orders_table> \
  --data '{"item":"设备更新","amount":"50000","status":"approved","deadline":"2026-06-15"}'

# Step 4: Notify relevant parties
lark message send --chat <finance_chat_id> \
  --text "✅ 采购申请已批准: 设备更新 ¥50,000"

lark mail send --to "supplier@vendor.com" \
  --subject "采购订单 - 设备更新" \
  --body "请确认以下订单..."
```

### Workflow 5: 数据管道编排 (Data Pipeline Orchestration)

**Scenario**: Extract data from Sheets, transform in Base, generate Doc report, distribute via Mail.

```bash
# Step 1: Read raw data from Sheet
lark sheet read --token <sheet_token> --range "A1:Z1000"

# Step 2: Process and store in Base
lark base record add --app <analytics_base> --table <metrics_table> \
  --data '{"date":"2026-05-26","metric1":"<value>","metric2":"<value>"}'

# Step 3: Generate analysis document
lark doc create --title "数据分析报告 $(date +%Y%m%d)" --folder <reports_folder>
lark doc content --token <doc_token> --write "# 数据分析报告

## 关键指标
| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| ... | ... | ... | ... |

## 趋势分析
[基于Base数据生成]

## 建议行动
1. ...
2. ..."

# Step 4: Create presentation for leadership
lark slide create --title "数据周报 $(date +%Y-W%V)" --folder <presentations_folder>

# Step 5: Distribute
lark mail send --to "leadership@company.com" \
  --subject "数据周报 $(date +%Y-W%V)" \
  --body "报告已生成: <doc_link>\n演示文稿: <slide_link>"

lark message send --chat <data_team_chat> \
  --text "📊 数据周报已生成: <doc_link>"
```

---

## Decision Framework

When a user requests a Feishu-related task, follow this decision tree:

```
User Request
├── Single action (send message, create doc)?
│   └── Direct command → Done
├── Reporting / periodic summary?
│   └── Workflow 1 (Auto Weekly Report)
├── Project tracking / status?
│   └── Workflow 2 (Project Dashboard)
├── Meeting-related?
│   └── Workflow 3 (Meeting Lifecycle)
├── Approval / process?
│   └── Workflow 4 (Approval-Driven)
├── Data analysis / pipeline?
│   └── Workflow 5 (Data Pipeline)
├── Cross-platform (needs DingTalk/WeCom)?
│   └── Delegate to china-im-workflow-cli
└── Novel combination?
    └── Compose from domain primitives below
```

## Domain Primitives (Compose Your Own Workflows)

When the templates don't fit, compose from these primitives:

### Input Primitives (Data Collection)
- `lark base record list` → Structured data from tables
- `lark sheet read` → Tabular data from spreadsheets
- `lark calendar event list` → Schedule data
- `lark task list` → Task status data
- `lark mail list` → Email data
- `lark message list` → Chat history
- `lark doc content` → Document content

### Processing Primitives (Data Transformation)
- `lark base record update/add` → Store processed data
- `lark sheet write` → Write analysis results
- `lark md convert` → Format transformation

### Output Primitives (Distribution)
- `lark doc create + content` → Generate documents
- `lark slide create + add` → Generate presentations
- `lark mail send` → Email distribution
- `lark message send` → Chat notification
- `lark task create` → Create action items
- `lark calendar event create` → Schedule follow-ups

### Trigger Primitives (Automation Hooks)
- `lark approval list --status` → Approval state change
- `lark calendar event list` → Upcoming events
- `lark task list --status` → Task state change
- `lark vc events` → Meeting events

## Advanced Patterns

### Pattern: Conditional Branching
```bash
# Check condition first
overdue=$(lark task list --status overdue --format json | jq 'length')

if [ "$overdue" -gt 0 ]; then
  # Escalation path
  lark message send --chat <manager_chat> --text "⚠️ $overdue 个任务逾期"
  dws ding send --users "manager" --text "请关注逾期任务"  # Cross-platform if needed
else
  # Normal path
  lark message send --chat <team_chat> --text "✅ 所有任务按时完成"
fi
```

### Pattern: Batch Operations
```bash
# Process multiple records from Base
records=$(lark base record list --app <base_id> --table <table_id> --format json)

echo "$records" | jq -c '.[]' | while read record; do
  id=$(echo "$record" | jq -r '.id')
  # Process each record
  lark base record update --app <base_id> --table <table_id> \
    --id "$id" --data '{"processed":true}'
done
```

### Pattern: Error Recovery
```bash
# Try primary action, fall back to alternative
if ! lark doc content --token <token> --write "content"; then
  # Fallback: create new doc if write fails
  lark doc create --title "Fallback Report" --folder <folder>
  lark message send --chat <chat_id> --text "⚠️ 原文档写入失败，已创建新文档"
fi
```

## Safety Rules

1. **Preview before send**: Use `--dry-run` when available
2. **Confirm destructive actions**: Deleting docs/records/tasks requires explicit user confirmation
3. **Rate limiting**: Max 20 API calls per minute; batch operations with `sleep 3` between iterations
4. **Auth check**: Always run `lark auth status` before starting workflows
5. **Idempotency**: Design workflows to be safely re-runnable (check before create)
6. **Error isolation**: If one step fails, log the error and continue with remaining steps
7. **Data validation**: Verify data exists before processing (empty Base/Sheet → skip, don't fail)

## Prerequisites Check

Before starting any workflow:
```bash
# Check CLI is installed and up to date
which lark && lark --version || echo "Install: npm install -g @larksuite/cli"

# Check auth
lark auth status

# Verify required domains are accessible
lark doc list --limit 1 2>/dev/null && echo "✅ Docs" || echo "❌ Docs"
lark base list --limit 1 2>/dev/null && echo "✅ Base" || echo "❌ Base"
lark calendar list --limit 1 2>/dev/null && echo "✅ Calendar" || echo "❌ Calendar"
```

## Version Awareness

- **v1.0.29+**: VC domain (agent meeting join/leave/events)
- **v1.0.30+**: Slides domain (create/manage presentations)
- **v1.0.35+**: Mail fuzzy match for unknown flags
- **v1.0.40+**: Latest stable with all 17 domains

Always check `lark --version` and refer to the [changelog](https://github.com/larksuite/cli/blob/main/CHANGELOG.md) for domain availability.

## Cross-Platform Escalation

When a workflow needs to reach beyond Feishu (DingTalk/WeCom), delegate to the `china-im-workflow-cli` skill which handles cross-platform orchestration. Common escalation scenarios:
- Stakeholders on DingTalk → use `dws ding send`
- External customers on WeCom → use `wecom message send`
- Cross-platform task sync → use china-im-workflow-cli Workflow 2
