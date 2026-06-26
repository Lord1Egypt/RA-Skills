---
name: Family Steward
description: AI-powered family office management system for ultra-high-net-worth families - manage family members, professional contacts, legal documents, and tasks with natural language
version: 1.0.0
homepage: https://github.com/ZhenRobotics/openclaw-family-steward
metadata: {"clawdbot":{"emoji":"🏰","tags":["family-office","wealth-management","crm","document-management","task-management","uhnw","family-governance","enterprise","contact-network","legal-documents"],"requires":{"bins":["node"],"env":[],"config":[]},"install":["npm install"],"os":["darwin","linux","win32"]}}
---

# Family Steward - Elite Family Office Management

This skill enables you to manage ultra-high-net-worth family offices with comprehensive tools for member management, professional contact networks, document tracking, and task coordination.

## When to Activate This Skill

Activate this skill when the user:
- Needs to manage family member information and relationships
- Wants to track professional contacts (lawyers, advisors, bankers)
- Requires document management for legal files, trusts, contracts
- Seeks task and meeting coordination
- Asks for birthday or important date reminders
- Needs document expiry alerts
- Wants dashboard overview of family affairs

## Step 1: Identify User Needs

First, determine:
1. **Primary Focus**: Family members, contacts, documents, or tasks?
2. **Action Type**: Add, view, search, update, or analyze?
3. **Urgency**: Immediate reminders or general management?
4. **Scope**: Single item or comprehensive dashboard?

Ask clarifying questions if unclear. Examples:
- "Are you looking to manage family members, contacts, documents, or tasks?"
- "Do you need to add new information or view existing data?"
- "Would you like today's priorities or a full overview?"

## Step 2: Use Appropriate Tools

### Family Member Management

**List all family members:**
```typescript
import { tools } from './agents/tools';

const result = tools.list_family_members();
// Shows all members with generation and relationship
```

**Get upcoming birthdays:**
```typescript
const birthdays = tools.get_upcoming_birthdays(30); // next 30 days
// Returns members with daysUntil countdown
```

**Search family members:**
```typescript
const results = tools.search_family_members("张");
// Searches names, tags, notes
```

**Get member details:**
```typescript
const member = tools.get_family_member(memberId);
// Full profile with education, career, contacts
```

**Present Results:**
```
👨‍👩‍👧‍👦 Family Members (Total: X)

Generation 1 (Patriarch/Matriarch):
- [Name] (Relationship) - [DOB]

Generation 2 (Children):
- [Name] (Relationship) - [DOB]

🎂 Upcoming Birthdays (next 30 days):
- [Name] - in [X] days
```

### Professional Contact Network

**List all contacts:**
```typescript
const contacts = tools.list_contacts();
// Or filter by category
const lawyers = tools.list_contacts("legal");
```

**Get contacts needing follow-up:**
```typescript
const needFollowUp = tools.get_contacts_needing_followup(7); // next 7 days
```

**Search contacts:**
```typescript
const results = tools.search_contacts("律师");
```

**Get contact details:**
```typescript
const contact = tools.get_contact_details(contactId);
// Includes full interaction history
```

**Log interaction:**
```typescript
const result = tools.log_contact_interaction(contactId, {
  date: "2026-03-08",
  type: "meeting",
  subject: "Quarterly review",
  notes: "Discussed estate planning updates"
});
```

**Present Results:**
```
🤝 Professional Contacts

Legal (X contacts):
- [Name] - [Role] - [Organization]
  Last contact: [Date]
  Next follow-up: [Date]

Financial (X contacts):
- [Name] - [Role] - [Organization]

⚠️ Need Follow-up (within 7 days):
- [Name] ([Role]) - [Date]
```

### Document Management

**List documents:**
```typescript
const docs = tools.list_documents();
// Or filter by category
const legal = tools.list_documents("legal");
```

**Get expiring documents:**
```typescript
const expiring = tools.get_expiring_documents(90); // next 90 days
```

**Get documents needing review:**
```typescript
const needReview = tools.get_documents_needing_review(30); // next 30 days
```

**Search documents:**
```typescript
const results = tools.search_documents("信托");
```

**Present Results:**
```
📁 Document Management

Total Documents: X

By Category:
- Legal: X docs (X expiring soon)
- Trust: X docs
- Property: X docs
- Financial: X docs

⏰ Expiring Soon (next 90 days):
- [Title] ([Category]) - expires in [X] days
  Related: [Contacts/Members]

📋 Need Review (next 30 days):
- [Title] ([Category]) - review by [Date]
```

### Task & Schedule Management

**List tasks:**
```typescript
const tasks = tools.list_tasks();
// Or filter by status
const pending = tools.list_tasks("pending");
```

**Get today's tasks:**
```typescript
const today = tools.get_todays_tasks();
```

**Get upcoming tasks:**
```typescript
const upcoming = tools.get_upcoming_tasks(14); // next 14 days
```

**Get overdue tasks:**
```typescript
const overdue = tools.get_overdue_tasks();
```

**Complete a task:**
```typescript
const result = tools.complete_task(taskId);
```

**Search tasks:**
```typescript
const results = tools.search_tasks("会议");
```

**Present Results:**
```
✅ Task Management

Today's Tasks (X):
- [CRITICAL] [Title]
- [HIGH] [Title]

Upcoming (next 14 days):
- [Date] - [Priority] [Title]

⚠️ Overdue (X tasks):
- [Title] - [X] days overdue

Statistics:
- Total: X
- Pending: X
- In Progress: X
- Completed: X
```

### Dashboard Overview

**Get comprehensive dashboard:**
```typescript
const dashboard = tools.get_dashboard();
```

**Present Results:**
```
🏰 FAMILY STEWARD DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━

👨‍👩‍👧‍👦 Family: X members
   🎂 X birthdays coming up

🤝 Contacts: X total
   ⚠️ X need follow-up

📁 Documents: X total
   ⏰ X expiring soon
   📋 X need review

✅ Tasks: X total
   📌 X for today
   ⚠️ X overdue

🚨 Alerts:
- [Alert 1]
- [Alert 2]
```

## Step 3: Handle Common Scenarios

### Scenario A: Daily Briefing
**User asks: "What do I need to do today?"**

1. Get dashboard overview
2. Get today's tasks
3. Check urgent alerts
4. Present prioritized action list

### Scenario B: Contact Management
**User asks: "Who do I need to follow up with?"**

1. Get contacts needing follow-up
2. Show last interaction date
3. Suggest contact approach
4. Offer to log new interaction

### Scenario C: Document Alerts
**User asks: "Any documents expiring soon?"**

1. Get expiring documents
2. Group by urgency (30/60/90 days)
3. Show related contacts
4. Suggest action items

### Scenario D: Family Information
**User asks: "Show me my family tree"**

1. List family members grouped by generation
2. Show relationships
3. Highlight upcoming birthdays
4. Provide member count summary

### Scenario E: Meeting Preparation
**User asks: "Prepare for family board meeting"**

1. Get upcoming family meeting tasks
2. List related documents
3. Show key contacts to notify
4. Create agenda checklist

## Step 4: Provide Context and Guidance

### Always Include:
- **Status summary** - Current state overview
- **Priority items** - What needs attention first
- **Due dates** - When actions are needed
- **Relationships** - Connected contacts/documents
- **Next steps** - Specific actionable items

### Use Clear Formatting:
- Emoji for visual clarity (👨‍👩‍👧‍👦🤝📁✅🚨⏰)
- Grouped information by category
- Priority indicators ([CRITICAL], [HIGH], etc.)
- Countdown timers (in X days)
- Clean section separators

### Be Proactive:
- Highlight urgent items first
- Suggest follow-up actions
- Remind about deadlines
- Connect related information
- Offer deeper analysis when relevant

## Important Guidelines

1. **Privacy First**
   - All data stays local
   - No cloud sync required
   - Emphasize confidentiality
   - Respect sensitive information

2. **Professional Tone**
   - Use formal but friendly language
   - Acknowledge family governance importance
   - Respect cultural considerations
   - Be concise and actionable

3. **Smart Prioritization**
   - Critical items first
   - Group related tasks
   - Suggest logical workflows
   - Balance urgency vs importance

4. **Relationship Context**
   - Show connections between entities
   - Provide interaction history
   - Suggest relationship maintenance
   - Track communication patterns

5. **Data Quality**
   - Note missing information
   - Suggest data completion
   - Validate dates and deadlines
   - Flag inconsistencies

## Common Questions & Responses

**"Show me my dashboard"**
→ Use get_dashboard() and present formatted overview

**"Any birthdays coming up?"**
→ Use get_upcoming_birthdays(30) and list with countdown

**"Who's my family lawyer?"**
→ Search contacts with category="legal", show details and interaction history

**"What documents expire soon?"**
→ Use get_expiring_documents(90), group by urgency

**"What's on my plate today?"**
→ Combine get_todays_tasks() with dashboard alerts

**"I met with [contact] today"**
→ Use log_contact_interaction() to record meeting

**"Find all trust documents"**
→ Use search_documents("trust") or list_documents("trust")

## Error Handling

### No Data Yet
```
"You haven't added any [family members/contacts/documents/tasks] yet.
Would you like to start by adding one?"
```

### Search Returns Empty
```
"No results found for '[keyword]'.
Try searching by [alternative field] or show me all items?"
```

### Missing Required Info
```
"To [action], I need [specific information].
Could you provide that?"
```

## Success Metrics

A successful execution means:
- ✅ User gets clear, actionable overview
- ✅ Priority items are highlighted
- ✅ Relationships between entities are shown
- ✅ Next steps are specific and timely
- ✅ Confidentiality and professionalism maintained

## Version History

**v1.0.0** - Initial Release
- Family member management with genealogy tracking
- Professional contact CRM with interaction history
- Document management with expiry tracking
- Task and meeting coordination
- Comprehensive dashboard
- 20 AI agent tools
- CLI interface with multiple commands
- Local JSON storage for privacy

**Future Enhancements:**
- Web interface
- Relationship visualization
- Multi-user collaboration
- Cloud sync (optional)
- Financial portfolio integration
- Advanced analytics

---

Remember: You are managing highly sensitive family information for ultra-high-net-worth families. Always maintain professionalism, respect privacy, and provide actionable insights that help family offices operate smoothly and efficiently.
