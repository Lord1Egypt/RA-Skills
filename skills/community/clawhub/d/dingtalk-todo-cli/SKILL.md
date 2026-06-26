---
name: dingtalk-todo-cli
description: "Manage DingTalk tasks and todos using the official dws CLI (v1.0.32+, 10+ domains). Teach AI agents how to create, track, sync, and automate DingTalk todo workflows including personal task management, team task distribution, DING-based urgent escalation, AI sheet integration for tracking, and cross-platform task sync. Covers: daily standup automation (Todo→DING→Sheet), task delegation with tracking (Todo→Contact→DING→Sheet), overdue escalation (Todo→DING→Calendar), sprint planning (Sheet→Todo→Calendar), and meeting action item capture (Calendar→Todo→DING). Triggers on: 钉钉待办管理, dingtalk todo, dws task management, 钉钉CLI任务, dingtalk CLI todo, 钉钉DING提醒, dingtalk DING escalation, 钉钉AI表格追踪, dingtalk sheet tracking, 钉钉任务同步, dingtalk task sync, 钉钉工作流, dingtalk workflow automation, agent dingtalk orchestration, AI钉钉待办"
---

# DingTalk Todo CLI - 钉钉CLI待办管理专家

You are an expert at managing tasks and todos in DingTalk using the official `dws` CLI. You don't just create tasks — you design todo workflows that ensure visibility, accountability, and follow-through.

## Core Philosophy

**A task without follow-through is just a wish.** DingTalk's unique strength is DING — guaranteed notification delivery. Your workflows combine Todo + DING + Sheet to create tasks that actually get done.

## CLI Quick Reference

### Installation & Auth
```bash
# Install
npm install -g dingtalk-workspace-cli

# Authenticate
dws auth login

# Verify
dws auth status
```

### Domain Coverage (v1.0.32+)

| Domain | Key Commands | Workflow Role |
|--------|-------------|---------------|
| **Todo** | `dws todo create/list/update/delete` | Core task management |
| **DING** | `dws ding send` | Urgent notification & escalation |
| **Calendar** | `dws calendar list/event create` | Deadline scheduling |
| **AI Sheet** | `dws sheet list/record add/update` | Tracking & analytics |
| **Contacts** | `dws contact search/department list` | People lookup |
| **Attendance** | `dws attendance list` | Work status check |
| **Approval** | `dws approval create/list` | Process governance |
| **Bot** | `dws bot list/send` | Automated messaging |
| **Drive** | `dws drive list/upload` | File management |
| **API** | `dws api call` | Raw OpenAPI access |

---

## Workflow Templates

### Workflow 1: 每日站会自动化 (Daily Standup Automation)

**Scenario**: Collect yesterday's completed tasks, today's plan, send DING for blockers, log to Sheet.

```bash
# Step 1: Get yesterday's completed tasks
dws todo list --completed --since "1d ago"

# Step 2: Get today's open tasks
dws todo list --status open --assignee <user_id>

# Step 3: Check for overdue items
dws todo list --overdue

# Step 4: If blockers exist, send DING to manager
overdue=$(dws todo list --overdue --format json)
if [ "$(echo "$overdue" | jq 'length')" -gt 0 ]; then
  dws ding send --users "<manager_id>" \
    --text "⚠️ 有 $(echo "$overdue" | jq 'length') 个逾期任务需要关注"
fi

# Step 5: Log standup to AI Sheet
dws sheet record add --sheet <standup_sheet> \
  --data "{\"date\":\"$(date +%Y-%m-%d)\",\"completed\":\"<completed_list>\",\"planned\":\"<planned_list>\",\"blockers\":\"<blocker_list>\"}"
```

### Workflow 2: 任务分配与追踪 (Task Delegation with Tracking)

**Scenario**: Assign task, notify assignee via DING, track in Sheet, escalate on overdue.

```bash
# Step 1: Create task with full context
dws todo create \
  --subject "完成Q2产品需求文档" \
  --due "2026-06-15" \
  --priority high \
  --assignee "<assignee_id>" \
  --description "包含用户调研数据、竞品分析、功能优先级排序"

# Step 2: DING the assignee to ensure visibility
dws ding send --users "<assignee_id>" \
  --text "📋 新任务: 完成Q2产品需求文档，截止6/15，优先级高"

# Step 3: Add to tracking sheet
dws sheet record add --sheet <task_tracker> \
  --data "{\"task\":\"Q2产品需求文档\",\"assignee\":\"<name>\",\"due\":\"2026-06-15\",\"status\":\"assigned\",\"created\":\"$(date +%Y-%m-%d)\"}"

# Step 4: Schedule check-in (3 days before due)
dws calendar event create \
  --summary "检查: Q2需求文档进度" \
  --start "2026-06-12T10:00:00" \
  --end "2026-06-12T10:15:00"

# Step 5: On due date - check and escalate if needed
status=$(dws todo list --id <todo_id> --format json | jq -r '.[0].status')
if [ "$status" != "completed" ]; then
  dws ding send --users "<assignee_id>,<manager_id>" \
    --text "🚨 任务逾期: Q2产品需求文档，请立即处理"
fi
```

### Workflow 3: 逾期任务升级 (Overdue Task Escalation)

**Scenario**: Automatically detect overdue tasks, escalate through DING levels.

```bash
# Step 1: Get all overdue tasks
overdue_tasks=$(dws todo list --overdue --format json)

# Step 2: Categorize by overdue duration
echo "$overdue_tasks" | jq -c '.[]' | while read task; do
  due_date=$(echo "$task" | jq -r '.due')
  days_overdue=$(( ($(date +%s) - $(date -d "$due_date" +%s)) / 86400 ))

  if [ "$days_overdue" -le 1 ]; then
    # Level 1: Gentle reminder to assignee
    dws ding send --users "$(echo "$task" | jq -r '.assignee')" \
      --text "⏰ 提醒: $(echo "$task" | jq -r '.subject') 已逾期1天"
  elif [ "$days_overdue" -le 3 ]; then
    # Level 2: Manager notification
    dws ding send --users "$(echo "$task" | jq -r '.assignee'),<manager_id>" \
      --text "⚠️ 任务逾期$(echo "$days_overdue")天: $(echo "$task" | jq -r '.subject')"
  else
    # Level 3: Director notification + daily DING
    dws ding send --users "<director_id>" \
      --text "🚨 严重逾期$(echo "$days_overdue")天: $(echo "$task" | jq -r '.subject') - 负责人: $(echo "$task" | jq -r '.assignee')"
  fi
done

# Step 3: Update tracking sheet
dws sheet record update --sheet <task_tracker> \
  --filter '{"status":"overdue"}' \
  --data '{"escalated":true}'
```

### Workflow 4: Sprint计划 (Sprint Planning)

**Scenario**: Plan sprint from backlog sheet, create todos, schedule milestones.

```bash
# Step 1: Read sprint backlog from AI Sheet
backlog=$(dws sheet record list --sheet <backlog_sheet> \
  --filter '{"sprint":"next","priority":"high"}' --format json)

# Step 2: Create todos for each backlog item
echo "$backlog" | jq -c '.[]' | while read item; do
  dws todo create \
    --subject "$(echo "$item" | jq -r '.title')" \
    --due "$(echo "$item" | jq -r '.due_date')" \
    --priority "$(echo "$item" | jq -r '.priority')" \
    --assignee "$(echo "$item" | jq -r '.assignee')"
done

# Step 3: Create sprint milestone events
dws calendar event create \
  --summary "Sprint Review" \
  --start "2026-06-13T15:00:00" \
  --end "2026-06-13T16:30:00"

dws calendar event create \
  --summary "Sprint Retrospective" \
  --start "2026-06-13T16:30:00" \
  --end "2026-06-13T17:30:00"

# Step 4: Notify team
dws ding send --users "<team_list>" \
  --text "🏃 新Sprint已启动，请查看待办列表"

# Step 5: Update sheet with sprint status
dws sheet record update --sheet <backlog_sheet> \
  --filter '{"sprint":"next"}' \
  --data '{"status":"in_progress"}'
```

### Workflow 5: 会议决议追踪 (Meeting Action Item Capture)

**Scenario**: After a meeting, create todos from action items, DING owners, track in Sheet.

```bash
# Step 1: Get recent meeting from calendar
dws calendar list --type meeting --since "1h ago"

# Step 2: Create todos for each action item
# (Agent parses meeting notes to extract action items)
dws todo create --subject "落实产品方案调整" --due "2026-06-05" --assignee "<owner1>"
dws todo create --subject "完成技术评估报告" --due "2026-06-08" --assignee "<owner2>"
dws todo create --subject "更新项目排期表" --due "2026-06-03" --assignee "<owner3>"

# Step 3: DING all action item owners
dws ding send --users "<owner1>,<owner2>,<owner3>" \
  --text "📋 会议决议已分配，请查看待办列表并确认"

# Step 4: Log to tracking sheet
dws sheet record add --sheet <meeting_actions> \
  --data "{\"meeting\":\"项目周会\",\"date\":\"$(date +%Y-%m-%d)\",\"actions\":\"3项\",\"status\":\"assigned\"}"

# Step 5: Schedule follow-up check
dws calendar event create \
  --summary "检查会议决议执行情况" \
  --start "2026-06-04T10:00:00" \
  --end "2026-06-04T10:30:00"
```

---

## Decision Framework

```
User Request
├── Create a single task?
│   └── dws todo create → Done
├── Daily standup / status check?
│   └── Workflow 1 (Daily Standup)
├── Assign task to someone?
│   └── Workflow 2 (Task Delegation)
├── Overdue / escalation?
│   └── Workflow 3 (Overdue Escalation)
├── Sprint / batch planning?
│   └── Workflow 4 (Sprint Planning)
├── Meeting follow-up?
│   └── Workflow 5 (Meeting Action Items)
├── Need to reach Feishu/WeCom?
│   └── Delegate to china-im-workflow-cli
└── Custom tracking?
    └── Compose from primitives below
```

## Domain Primitives

### Task Operations
- `dws todo create --subject --due --priority --assignee` → Create task
- `dws todo list --status open/completed/overdue` → Query tasks
- `dws todo update --id --status completed` → Complete task
- `dws todo delete --id` → Remove task (confirm first!)

### Notification Operations
- `dws ding send --users --text` → DING notification (guaranteed delivery)
- `dws bot send --chat --text` → Bot message to group

### Tracking Operations
- `dws sheet record add --sheet --data` → Log to sheet
- `dws sheet record list --sheet --filter` → Query sheet
- `dws sheet record update --sheet --filter --data` → Update sheet

### Scheduling Operations
- `dws calendar event create --summary --start --end` → Schedule event
- `dws calendar list --type meeting` → Find meetings

### People Operations
- `dws contact search --name` → Find person
- `dws contact department list` → List departments

### Advanced: Raw API Access
- `dws api call --endpoint <path> --method GET/POST` → Direct OpenAPI access
- Use for features not yet wrapped in dws commands

## DING Escalation Levels

| Level | Overdue | Recipients | Tone |
|-------|---------|------------|------|
| 1 | 1 day | Assignee only | ⏰ Gentle reminder |
| 2 | 2-3 days | Assignee + Manager | ⚠️ Warning |
| 3 | 4-7 days | Manager + Director | 🚨 Urgent |
| 4 | 7+ days | Director + HR | 🔴 Critical |

## Safety Rules

1. **DING is intrusive**: Only use DING for genuinely important/urgent items, not routine updates
2. **Confirm before DING escalation**: Level 3+ escalations require user confirmation
3. **Rate limiting**: Max 10 DINGs per hour; batch notifications when possible
4. **Auth check**: Always run `dws auth status` before workflows
5. **No delete without confirmation**: `dws todo delete` requires explicit user approval
6. **Respect working hours**: Avoid DING outside 9:00-21:00 unless marked urgent
7. **Batch over individual**: When notifying a team, prefer one DING to multiple

## Prerequisites Check

```bash
# Check CLI
which dws && dws --version || echo "Install: npm install -g dingtalk-workspace-cli"

# Check auth
dws auth status

# Verify domains
dws todo list --limit 1 2>/dev/null && echo "✅ Todo" || echo "❌ Todo"
dws sheet list --limit 1 2>/dev/null && echo "✅ Sheet" || echo "❌ Sheet"
dws calendar list --limit 1 2>/dev/null && echo "✅ Calendar" || echo "❌ Calendar"
```

## Cross-Platform Integration

When tasks need to reach Feishu or WeCom:
- **Feishu task sync**: `lark task create --summary --due` (after creating in DingTalk)
- **WeCom notification**: `wecom message send --user --text` (for WeCom-based stakeholders)
- **Full cross-platform**: Use `china-im-workflow-cli` skill for orchestrated sync
