---
name: cross-platform-im-cli
description: "Orchestrate cross-platform IM workflows across Feishu, DingTalk, and WeCom using their official CLIs. Teach AI agents how to combine lark CLI (v1.0.40+, 17 domains, 200+ commands), dws CLI (v1.0.32+, 10 domains), and wecom CLI (v0.1.8+, 7 domains) for unified messaging, task sync, notification broadcasting, and workflow automation across China's three major enterprise IM platforms. Covers: unified inbox triage, cross-platform task synchronization, multi-channel notification broadcast, platform-aware routing, and emergency communication. Triggers on: 跨平台IM, cross-platform IM, 飞书钉钉企微, Feishu DingTalk WeCom, 多平台消息, multi-platform messaging, IM工作流编排, IM workflow orchestration, 跨平台通知, cross-platform notification, 跨平台任务同步, cross-platform task sync, 企业IM自动化, enterprise IM automation, agent IM orchestration, AI跨平台工作流"
---

# Cross-Platform IM CLI - 跨平台IM工作流编排专家

You are an expert at orchestrating workflows across China's three major enterprise IM platforms — Feishu, DingTalk, and WeCom — using their official CLI tools.

## Core Philosophy

**Each platform has unique strengths. Your job is knowing WHEN to use WHICH platform, and HOW to make them work together.**

- **Feishu** → Best for: documents, data (Base/Sheet), collaboration
- **DingTalk** → Best for: task accountability (DING), approvals, attendance
- **WeCom** → Best for: external customer communication, meeting management

## CLI Reference

### Feishu/Lark CLI (`lark`) — v1.0.40+
```bash
npm install -g @larksuite/cli && lark auth login
# 17 domains: Messenger, Docs, Base, Sheets, Slides, Calendar, Mail, Tasks, VC, Wiki, Contacts, Drive, Approval, Markdown
```

### DingTalk CLI (`dws`) — v1.0.32+
```bash
npm install -g dingtalk-workspace-cli && dws auth login
# 10 domains: Todo, DING, Calendar, AI Sheet, Contacts, Attendance, Approval, Bot, Drive, API
```

### WeCom CLI (`wecom`) — v0.1.8+
```bash
npm install -g @wecom/cli && wecom auth login
# 7 domains: Message, Calendar, Doc, SmartSheet, Meeting, Todo, Contacts
```

---

## Workflow Templates

### Workflow 1: 统一收件箱分拣 (Unified Inbox Triage)

**Scenario**: Check messages across all platforms, categorize by urgency, route to appropriate handler.

```bash
# Step 1: Collect unread messages from all platforms
feishu_msgs=$(lark message list --unread --format json)
dingtalk_msgs=$(dws todo list --status open --format json)
wecom_msgs=$(wecom message list --unread --format json)

# Step 2: Categorize by urgency
# - DING messages = urgent
# - @mentions = high
# - Group messages = normal
# - Broadcasts = low

# Step 3: Route urgent items
# Urgent DingTalk → DING already ensures visibility
# Urgent Feishu → escalate to DING
# Urgent WeCom → send DING to DingTalk for visibility

# Step 4: Create summary
lark doc create --title "消息摘要 $(date +%Y%m%d)" --folder <inbox_folder>
lark doc content --token <doc_token> --write "# 今日消息摘要

## 🔴 紧急
- [DING] 服务器告警 - 需立即处理
- [@提及] 客户投诉 - 需今日回复

## 🟡 重要
- [飞书] 项目进度更新
- [企微] 客户会议邀请

## 🟢 一般
- [钉钉] 团队周报
- [飞书] 知识库更新"

# Step 5: Notify on critical items
dws ding send --users "<self_id>" --text "📋 今日有2条紧急消息，请查看摘要文档"
```

### Workflow 2: 跨平台任务同步 (Cross-Platform Task Sync)

**Scenario**: Create task on primary platform, sync to others, ensure visibility everywhere.

```bash
# Step 1: Create task on primary platform (DingTalk for accountability)
dws todo create --subject "完成客户方案" --due "2026-06-10" --priority high

# Step 2: Sync to Feishu (for collaboration)
lark task create --summary "完成客户方案" --due "2026-06-10"

# Step 3: Sync to WeCom (for external-facing teams)
wecom todo create --title "完成客户方案" --deadline "2026-06-10"

# Step 4: Add to tracking base
lark base record add --app <task_base> --table <sync_table> \
  --data '{"task":"完成客户方案","due":"2026-06-10","dingtalk_id":"<id>","feishu_id":"<id>","wecom_id":"<id>","status":"open"}'

# Step 5: Notify stakeholders on their preferred platform
# Manager on DingTalk
dws ding send --users "<manager_id>" --text "📋 新任务: 完成客户方案 (截止6/10)"

# Team on Feishu
lark message send --chat <team_chat> --text "🆕 新任务: 完成客户方案 (截止6/10)"

# Sales on WeCom
wecom message send --chat <sales_chat> --text "新任务: 完成客户方案 (截止6/10)"
```

### Workflow 3: 多渠道通知广播 (Multi-Channel Notification Broadcast)

**Scenario**: Send notification across all platforms with platform-appropriate formatting.

```bash
# Define the notification
NOTIFICATION="系统维护通知：6月1日 02:00-06:00 系统升级，届时服务不可用"
URGENCY="high"  # low, normal, high, critical

# Route based on urgency
case $URGENCY in
  critical)
    # All platforms, all channels, maximum visibility
    dws ding send --users "all" --text "🚨 $NOTIFICATION"
    lark message send --chat <all_staff> --text "🚨 $NOTIFICATION"
    wecom message send --chat <all_staff> --markdown "# 🚨 紧急通知\n\n$NOTIFICATION"
    ;;
  high)
    # All platforms, targeted channels
    dws ding send --users "<affected_users>" --text "⚠️ $NOTIFICATION"
    lark message send --chat <ops_chat> --text "⚠️ $NOTIFICATION"
    wecom message send --chat <ops_chat> --text "⚠️ $NOTIFICATION"
    ;;
  normal)
    # Primary platform + secondary notification
    lark message send --chat <team_chat> --text "📢 $NOTIFICATION"
    wecom message send --chat <team_chat> --text "📢 $NOTIFICATION"
    ;;
  low)
    # Primary platform only
    lark message send --chat <team_chat> --text "ℹ️ $NOTIFICATION"
    ;;
esac
```

### Workflow 4: 平台感知路由 (Platform-Aware Routing)

**Scenario**: Automatically route messages to the right platform based on content type and recipient.

```bash
# Routing rules:
# 1. External customers → WeCom (native customer connection)
# 2. Internal approvals → DingTalk (best approval flow)
# 3. Document collaboration → Feishu (best doc integration)
# 4. Urgent items → DingTalk DING (guaranteed delivery)
# 5. Data/reporting → Feishu (Base/Sheet)
# 6. Meeting coordination → Primary platform of attendees

route_message() {
  local type=$1
  local recipient=$2
  local content=$3

  case $type in
    customer)
      wecom message send --user "$recipient" --text "$content"
      ;;
    approval)
      dws approval create --data "$content"
      dws ding send --users "$recipient" --text "您有新的审批待处理"
      ;;
    document)
      lark doc create --title "$content" --folder <shared_folder>
      lark message send --chat <team_chat> --text "📄 新文档: $content"
      ;;
    urgent)
      dws ding send --users "$recipient" --text "🚨 $content"
      lark message send --chat <ops_chat> --text "🚨 $content"
      ;;
    report)
      lark base record add --app <report_base> --table <data_table> --data "$content"
      lark message send --chat <team_chat> --text "📊 数据已更新"
      ;;
    meeting)
      # Check which platform attendees use
      lark calendar event create --summary "$content" --start "<time>" --end "<time>"
      dws ding send --users "$recipient" --text "📅 新会议: $content"
      ;;
  esac
}
```

### Workflow 5: 应急通信 (Emergency Communication)

**Scenario**: System outage or critical incident — ensure all stakeholders are reached immediately.

```bash
# Phase 1: Immediate broadcast (within 1 minute)
INCIDENT="生产环境数据库故障，影响范围：订单系统"
dws ding send --users "all" --text "🚨 紧急: $INCIDENT"
lark message send --chat <incident_chat> --text "🚨 紧急: $INCIDENT"
wecom message send --chat <incident_chat> --markdown "# 🚨 紧急事件\n\n$INCIDENT\n\n处理中，请关注更新"

# Phase 2: Create incident tracking
lark doc create --title "故障报告 $(date +%Y%m%d-%H%M)" --folder <incident_folder>
dws sheet record add --sheet <incident_sheet> \
  --data "{\"time\":\"$(date +%Y-%m-%dT%H:%M)\",\"incident\":\"$INCIDENT\",\"status\":\"investigating\"}"

# Phase 3: Status updates (every 15 minutes)
update_status() {
  local status=$1
  local detail=$2
  dws ding send --users "all" --text "🔄 更新: $INCIDENT - $status"
  lark message send --chat <incident_chat> --text "🔄 状态: $status\n$detail"
  wecom message send --chat <incident_chat> --text "🔄 状态: $status\n$detail"
}

# Phase 4: Resolution notification
dws ding send --users "all" --text "✅ 已恢复: $INCIDENT - 服务已正常"
lark message send --chat <incident_chat> --text "✅ 服务已恢复，故障报告将稍后发出"
wecom message send --chat <incident_chat> --text "✅ 服务已恢复"

# Phase 5: Post-incident report
lark doc content --token <doc_token> --write "# 故障报告

## 时间线
- $(date +%H:%M) 故障发生
- $(date +%H:%M) 开始排查
- $(date +%H:%M) 服务恢复

## 影响范围
- 订单系统不可用约XX分钟

## 根因分析
- [待补充]

## 改进措施
1. [待补充]
2. [待补充]"
```

---

## Platform Selection Guide

| Need | Best Platform | CLI Command | Why |
|------|--------------|-------------|-----|
| Rich document collaboration | Feishu | `lark doc create` | Best doc/base/sheet integration |
| Urgent task accountability | DingTalk | `dws ding send` | DING guarantees visibility |
| External customer comms | WeCom | `wecom message send` | Native customer connection |
| Data-heavy workflows | Feishu | `lark base record add` | Base is most powerful |
| Approval workflows | DingTalk | `dws approval create` | Best approval flow |
| Meeting management | Feishu | `lark vc join` | VC + Calendar integration |
| Smart sheet tracking | WeCom | `wecom sheet record add` | SmartSheet for tracking |
| AI-powered analysis | DingTalk | `dws sheet` | AI Sheet with built-in AI |
| Email communication | Feishu | `lark mail send` | Only platform with email |
| Presentation output | Feishu | `lark slide create` | Only platform with slides |

## Cross-Platform Data Flow Patterns

### Pattern: Fan-Out (One → Many)
```
Source → Feishu Base
       → DingTalk DING
       → WeCom Message
```
Use when: Broadcasting same information to all platforms

### Pattern: Fan-In (Many → One)
```
DingTalk Todo ─┐
Feishu Tasks ──┼→ Feishu Base (unified view)
WeCom Todo ────┘
```
Use when: Aggregating data from multiple platforms

### Pattern: Chain (Sequential)
```
DingTalk Approval → Feishu Doc → WeCom Customer Notification
```
Use when: Process flows across platforms sequentially

### Pattern: Escalation (Conditional)
```
Feishu Message → (if urgent) → DingTalk DING → (if critical) → WeCom + DingTalk
```
Use when: Need to escalate based on urgency

## Safety Rules

1. **Preview before broadcast**: Always show the user what will be sent before multi-platform broadcast
2. **Confirm DING usage**: DING is intrusive — confirm before sending to non-assignees
3. **Rate limiting**: Max 10 messages per minute per platform; 30 total across all platforms
4. **Auth check all platforms**: Verify auth on all relevant CLIs before starting
5. **Error isolation**: If one platform fails, continue with others and report the failure
6. **No duplicate notifications**: Don't send the same content to the same person on multiple platforms unless urgency requires it
7. **Respect platform norms**: Use markdown on Feishu, plain text on DingTalk DING, markdown on WeCom

## Prerequisites Check

```bash
# Check all CLIs
which lark && echo "✅ Feishu CLI v$(lark --version)" || echo "❌ Install: npm install -g @larksuite/cli"
which dws && echo "✅ DingTalk CLI v$(dws --version)" || echo "❌ Install: npm install -g dingtalk-workspace-cli"
which wecom && echo "✅ WeCom CLI v$(wecom --version)" || echo "❌ Install: npm install -g @wecom/cli"

# Check auth
lark auth status
dws auth status
wecom auth status
```

## Integration with Single-Platform Skills

For deep single-platform workflows, delegate to specialized skills:
- **Feishu deep workflows** → `feishu-workflow-cli` skill
- **DingTalk todo management** → `dingtalk-todo-cli` skill
- **This skill** → Cross-platform orchestration only

Don't duplicate single-platform logic. Compose and delegate.
