---
name: china-im-workflow-cli
description: "Orchestrate cross-platform IM workflows using Feishu CLI, DingTalk CLI, and WeCom CLI. Teach AI agents how to combine lark-cli (200+ commands), dws (DingTalk Workspace CLI), and wecom-cli to automate reporting, task management, notifications, and marketing across China's three major enterprise IM platforms. Covers: auto-send weekly reports via Feishu, sync tasks between DingTalk and WeCom, cross-platform notification broadcasting, marketing content distribution to all three platforms simultaneously. Triggers on: 飞书CLI工作流, 钉钉CLI自动化, 企微CLI集成, 跨平台IM, IM workflow automation, Feishu DingTalk WeCom CLI orchestration, 中国企业IM自动化, agent CLI workflow, multi-platform notification, 跨平台周报, 多平台消息分发"
---

# China IM Workflow CLI - 跨平台IM工作流编排

You are an expert at orchestrating workflows across China's three major enterprise IM platforms using their official CLI tools.

## Core Principle

**You don't replace the CLIs — you orchestrate them.** Each CLI handles its own platform. Your value is knowing WHEN to use WHICH CLI, and HOW to combine them into workflows that save real time.

## CLI Reference

### 1. Feishu/Lark CLI (`lark`)
- **Install**: `npm install -g @larksuite/cli`
- **Auth**: `lark auth login`
- **Repo**: https://github.com/larksuite/cli
- **Coverage**: 200+ commands, 20+ Agent Skills
- **Domains**: Messenger, Docs, Base, Sheets, Calendar, Mail, Tasks, Meetings

**Key Commands**:
```bash
# Messaging
lark message send --chat <chat_id> --text "content"
lark message list --chat <chat_id> --limit 20

# Docs
lark doc create --title "title" --folder <folder_id>
lark doc get --token <doc_token>
lark doc content --token <doc_token>

# Base (多维表格)
lark base list
lark base record add --app <app_token> --table <table_id> --data '{"field":"value"}'
lark base record list --app <app_token> --table <table_id>

# Calendar
lark calendar list
lark calendar event create --summary "meeting" --start "2026-05-23T10:00:00" --end "2026-05-23T11:00:00"

# Mail
lark mail send --to "user@example.com" --subject "subject" --body "content"

# Tasks
lark task create --summary "task name" --due "2026-05-30"
lark task list --status open
```

### 2. DingTalk Workspace CLI (`dws`)
- **Install**: `npm install -g dingtalk-workspace-cli`
- **Auth**: `dws auth login`
- **Repo**: https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli
- **Coverage**: AI表格, 日历, 通讯录, 待办, DING消息
- **Domains**: Contacts, Calendar, Todo, AI Sheet, DING

**Key Commands**:
```bash
# Todo/Task
dws todo list
dws todo create --subject "task" --due "2026-05-30"
dws todo update --id <todo_id> --status completed

# DING (urgent notification)
dws ding send --users "user1,user2" --text "urgent message"

# Calendar
dws calendar list
dws calendar event create --summary "meeting" --start "2026-05-23T10:00:00"

# AI Sheet
dws sheet list
dws sheet record add --sheet <sheet_id> --data '{"col1":"val1"}'

# Contacts
dws contact search --name "张三"
dws contact department list
```

### 3. WeCom CLI (`wecom`)
- **Install**: `npm install -g @wecom/cli`
- **Auth**: `wecom auth login`
- **Repo**: https://github.com/WecomTeam/wecom-cli
- **Coverage**: 消息, 日程, 文档, 智能表, 会议, 待办, 通讯录
- **Domains**: Message, Calendar, Doc, SmartSheet, Meeting, Todo, Contacts

**Key Commands**:
```bash
# Messaging
wecom message send --user "userid" --text "content"
wecom message send --chat <chatid> --markdown "# Report\ncontent"

# Calendar
wecom calendar list
wecom calendar event create --summary "meeting" --start "2026-05-23T10:00:00"

# Todo
wecom todo list
wecom todo create --title "task" --deadline "2026-05-30"

# Doc
wecom doc create --title "title"
wecom doc get --id <doc_id>

# Smart Sheet
wecom sheet list
wecom sheet record add --sheet <sheet_id> --data '{"field":"value"}'

# Meeting
wecom meeting create --topic "topic" --start "2026-05-23T10:00:00"
```

## Workflow Templates

### Workflow 1: 自动周报 (Auto Weekly Report)
**Scenario**: Collect data from multiple sources, generate report, send to all platforms.

```bash
# Step 1: Get this week's tasks from DingTalk
dws todo list --completed --since "7d ago"

# Step 2: Get calendar events from Feishu
lark calendar event list --start "$(date -d '7 days ago' +%Y-%m-%d)" --end "$(date +%Y-%m-%d)"

# Step 3: Create report doc in Feishu
lark doc create --title "周报 $(date +%Y-W%V)" --folder <weekly_report_folder>

# Step 4: Write report content
lark doc content --token <doc_token> --write "# 本周工作\n## 完成事项\n- ...\n## 下周计划\n- ..."

# Step 5: Send notification to all platforms
lark message send --chat <team_chat> --text "📋 周报已生成: [链接]"
dws ding send --users "manager1,manager2" --text "周报已提交，请查阅"
wecom message send --chat <wecom_chat> --markdown "# 周报通知\n周报已生成，请查阅"
```

### Workflow 2: 跨平台任务同步 (Cross-Platform Task Sync)
**Scenario**: Create a task on one platform, sync to others.

```bash
# Create task on DingTalk (primary)
dws todo create --subject "完成Q2报告" --due "2026-06-15" --priority high

# Sync to Feishu
lark task create --summary "完成Q2报告" --due "2026-06-15"

# Sync to WeCom
wecom todo create --title "完成Q2报告" --deadline "2026-06-15"

# Notify stakeholders on all platforms
lark message send --chat <project_chat> --text "🆕 新任务: 完成Q2报告 (截止6/15)"
wecom message send --user "stakeholder_id" --text "新任务已创建: 完成Q2报告"
```

### Workflow 3: 紧急通知广播 (Urgent Notification Broadcast)
**Scenario**: Send urgent message across all platforms simultaneously.

```bash
# DING on DingTalk (highest priority)
dws ding send --users "all" --text "🚨 紧急: 服务器故障，请立即处理"

# Feishu message
lark message send --chat <ops_chat> --text "🚨 紧急: 服务器故障，请立即处理"

# WeCom message
wecom message send --chat <ops_chat> --markdown "# 🚨 紧急通知\n服务器故障，请立即处理"
```

### Workflow 4: 营销内容多平台分发 (Marketing Content Distribution)
**Scenario**: Create marketing content once, distribute to all IM platforms.

```bash
# Step 1: Create content doc in Feishu
lark doc create --title "营销文案 $(date +%Y%m%d)" --folder <marketing_folder>

# Step 2: Send formatted content to each platform
# Feishu - rich markdown
lark message send --chat <marketing_chat> --markdown "# 新品发布\n✨ 产品亮点\n- 亮点1\n- 亮点2\n🔗 [详情链接]"

# DingTalk - DING for important campaigns
dws ding send --users "sales_team" --text "新品发布！查看详情并跟进客户"

# WeCom - external customer groups
wecom message send --chat <customer_group> --markdown "# 🎉 新品发布\n产品介绍...\n[购买链接]"
```

### Workflow 5: 会议协调 (Meeting Coordination)
**Scenario**: Check availability across platforms and create meeting.

```bash
# Check calendars on all platforms
lark calendar free-busy --users "user1,user2" --start "2026-05-23T14:00:00" --end "2026-05-23T18:00:00"
dws calendar free-busy --users "user3,user4" --start "2026-05-23T14:00:00" --end "2026-05-23T18:00:00"

# Find common slot and create meeting on primary platform
lark calendar event create --summary "项目评审会" --start "2026-05-23T15:00:00" --end "2026-05-23T16:00:00" --attendees "user1,user2"

# Notify on other platforms
dws ding send --users "user3,user4" --text "项目评审会 5/23 15:00-16:00，已在飞书创建会议"
wecom message send --user "user5" --text "项目评审会 5/23 15:00-16:00"
```

## Decision Framework

When the user asks for an IM-related task, follow this decision tree:

1. **Single platform?** → Use that platform's CLI directly
2. **Cross-platform notification?** → Workflow 3 (broadcast)
3. **Task management?** → Workflow 2 (sync) or single platform
4. **Reporting?** → Workflow 1 (auto weekly report)
5. **Marketing?** → Workflow 4 (content distribution)
6. **Meeting?** → Workflow 5 (coordination)

## Platform Selection Guide

| Need | Best Platform | Why |
|------|--------------|-----|
| Rich document collaboration | Feishu | Best doc/base/sheet integration |
| Urgent task tracking | DingTalk | DING ensures visibility |
| External customer comms | WeCom | Native customer connection |
| Data-heavy workflows | Feishu | Base (多维表格) is most powerful |
| Approval workflows | DingTalk | Best approval flow integration |
| Meeting management | Feishu | Calendar + Meeting integration |

## Safety Rules

1. **Always preview before sending**: Use `--dry-run` or `--preview` flags when available
2. **Confirm destructive actions**: Deleting messages/docs/tasks requires explicit user confirmation
3. **Rate limiting**: Don't send more than 10 messages per minute across all platforms
4. **Auth check**: Always verify auth status before operations: `lark auth status`, `dws auth status`, `wecom auth status`
5. **Error handling**: If one platform fails, continue with others and report the failure

## Prerequisites Check

Before starting any workflow, verify:
```bash
# Check all CLIs are installed
which lark && echo "✅ Feishu CLI" || echo "❌ Install: npm install -g @larksuite/cli"
which dws && echo "✅ DingTalk CLI" || echo "❌ Install: npm install -g dingtalk-workspace-cli"
which wecom && echo "✅ WeCom CLI" || echo "❌ Install: npm install -g @wecom/cli"

# Check auth status
lark auth status
dws auth status
wecom auth status
```

## Important Notes

- These CLIs operate on behalf of the authenticated user — respect their permissions
- All CLIs support JSON output (`--format json`) for programmatic processing
- Each CLI has built-in Agent Skills — check `lark skills list`, `dws skills list` for platform-specific automation
- For complex workflows, consider writing a shell script that chains CLI commands
- Monitor CLI updates — all three are actively developed with new commands added monthly
