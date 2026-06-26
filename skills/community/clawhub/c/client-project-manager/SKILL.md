---
name: client-project-manager
description: Manage freelance clients, projects, invoices, and communications. Use when tracking client work, creating invoices, sending updates, managing deadlines, or organizing freelance business operations.
argument-hint: "[action] [client-or-project]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Client Project Manager

A complete freelance business management system. Track clients, projects, deadlines, deliverables, invoices, and communications from a single skill.

## How to Use

```
/client-project-manager add client "Acme Corp" --contact "jane@acme.com" --rate "$100/hr"
/client-project-manager add project "Website Redesign" --client "Acme Corp" --deadline "2026-03-15" --budget "$5000"
/client-project-manager status
/client-project-manager update "Website Redesign" --progress 60 --note "Homepage mockup approved"
/client-project-manager invoice "Acme Corp" --project "Website Redesign"
/client-project-manager weekly-update "Acme Corp"
/client-project-manager dashboard
```

## Data Storage

All data is stored in `./freelance-data/` as JSON files:

```
freelance-data/
  clients.json        # Client CRM data
  projects.json       # Active and completed projects
  time-log.json       # Time tracking entries
  invoices/           # Generated invoices
  updates/            # Client update emails
```

If the directory doesn't exist, create it on first use. If files exist, read them first and preserve all existing data.

## Commands

### `add client`

Add a new client to the CRM.

```
/client-project-manager add client "[Name]" --contact "[email]" --rate "[rate]" --notes "[notes]"
```

Store in `clients.json`:
```json
{
  "id": "client-uuid",
  "name": "Acme Corp",
  "contact_email": "jane@acme.com",
  "default_rate": "$100/hr",
  "notes": "Prefers Slack for communication",
  "projects": [],
  "total_billed": 0,
  "total_paid": 0,
  "created": "2026-02-13",
  "status": "active"
}
```

### `add project`

Add a new project under a client.

```
/client-project-manager add project "[Name]" --client "[Client]" --deadline "[date]" --budget "[amount]" --deliverables "[list]"
```

Store in `projects.json`:
```json
{
  "id": "project-uuid",
  "name": "Website Redesign",
  "client_id": "client-uuid",
  "client_name": "Acme Corp",
  "status": "active",
  "progress": 0,
  "budget": 5000,
  "billed": 0,
  "deadline": "2026-03-15",
  "created": "2026-02-13",
  "deliverables": [
    { "name": "Homepage mockup", "status": "pending", "due": "2026-02-20" },
    { "name": "Inner pages", "status": "pending", "due": "2026-03-01" },
    { "name": "Development", "status": "pending", "due": "2026-03-10" },
    { "name": "Launch", "status": "pending", "due": "2026-03-15" }
  ],
  "notes": [],
  "time_entries": []
}
```

### `log time`

Log time worked on a project.

```
/client-project-manager log time "[Project]" --hours [X] --description "[what you did]"
```

Append to `time-log.json`:
```json
{
  "id": "entry-uuid",
  "project_id": "project-uuid",
  "client_id": "client-uuid",
  "date": "2026-02-13",
  "hours": 3.5,
  "rate": 100,
  "amount": 350,
  "description": "Built responsive navigation and hero section"
}
```

### `update`

Update project progress and add notes.

```
/client-project-manager update "[Project]" --progress [0-100] --note "[update]" --deliverable "[name]" --status "[done|in-progress|pending]"
```

### `status`

Show current status of all active projects.

Output format:
```
╔══════════════════════════════════════════════════════════════╗
║                    FREELANCE DASHBOARD                       ║
╠══════════════════════════════════════════════════════════════╣

📊 Active Projects: 3
💰 Outstanding Invoices: $2,500
⏰ Hours This Week: 22.5
📅 Next Deadline: Website Redesign (Acme Corp) — Mar 15

──────────────────────────────────────────────────────────────
PROJECT: Website Redesign
CLIENT: Acme Corp | DEADLINE: Mar 15, 2026
PROGRESS: ████████████░░░░░░░░ 60%
BUDGET: $3,000 / $5,000 billed
DELIVERABLES:
  ✅ Homepage mockup (Feb 20) — DONE
  🔄 Inner pages (Mar 1) — IN PROGRESS
  ⬜ Development (Mar 10) — PENDING
  ⬜ Launch (Mar 15) — PENDING
──────────────────────────────────────────────────────────────
```

### `invoice`

Generate a professional invoice for a client.

```
/client-project-manager invoice "[Client]" --project "[Project]" --period "[start] to [end]"
```

Generate the invoice as both Markdown and HTML in `freelance-data/invoices/`:

**Invoice content**:
```
INVOICE #[INV-YYYY-NNN]
Date: [today]
Due: [today + 14 days]

FROM:
[Your name/business — read from freelance-data/config.json if exists]

TO:
[Client name]
[Client contact]

PROJECT: [Project name]
PERIOD: [Date range]

| Date | Description | Hours | Rate | Amount |
|------|-------------|-------|------|--------|
| ... time entries from period ... |

                              Subtotal: $X,XXX.XX
                              Tax (0%): $0.00
                              TOTAL DUE: $X,XXX.XX

Payment Terms: Net 14
Payment Methods: [from config.json or "Bank Transfer / PayPal"]

Thank you for your business.
```

Save as `freelance-data/invoices/INV-2026-001-acme-corp.md` and `.html`.

### `weekly-update`

Generate a professional weekly client update email.

```
/client-project-manager weekly-update "[Client]"
```

Read the client's projects, recent time entries, and notes. Generate:

```
Subject: Weekly Update — [Project Name] — Week of [date]

Hi [Contact first name],

Here's your weekly update on [Project Name]:

**This Week:**
- [Completed deliverables and progress]
- [Key decisions made]
- [Hours worked: X.X]

**Next Week:**
- [Planned deliverables]
- [Any blockers or decisions needed from client]

**Project Status:**
- Progress: XX%
- Budget used: $X,XXX / $X,XXX
- On track for [deadline]: ✅ Yes / ⚠️ At risk / ❌ Behind

[Any questions or items needing client input]

Best,
[Your name]
```

Save to `freelance-data/updates/` and display for copy-paste.

### `payment-reminder`

Generate a polite payment reminder for overdue invoices.

```
/client-project-manager payment-reminder "[Client]"
```

Check for unpaid invoices past due date. Generate appropriate reminder:
- 1-7 days overdue: Gentle reminder
- 8-14 days overdue: Firm but professional follow-up
- 15+ days overdue: Final notice with late fee mention

### `dashboard`

Show a comprehensive business overview:

```
╔══════════════════════════════════════════════════════════════╗
║                  MONTHLY BUSINESS REPORT                     ║
╠══════════════════════════════════════════════════════════════╣

💰 Revenue This Month:     $4,250
💰 Revenue Last Month:     $3,800  (↑ 12%)
📊 Active Projects:        3
✅ Completed This Month:   1
⏰ Hours Billed:           42.5
💵 Effective Hourly Rate:  $100/hr
📋 Outstanding Invoices:   $2,500 (2 invoices)
⚠️  Overdue Invoices:      $0

TOP CLIENTS (by revenue):
  1. Acme Corp        $2,500  (59%)
  2. StartupXYZ       $1,250  (29%)
  3. LocalBiz         $500    (12%)

UPCOMING DEADLINES:
  Feb 20 — Homepage mockup (Acme Corp)
  Mar 01 — Content strategy (StartupXYZ)
  Mar 15 — Website launch (Acme Corp)
```

### `config`

Set your business details for invoices and communications.

```
/client-project-manager config --name "Your Name" --business "Your Business LLC" --email "you@email.com" --payment "PayPal: you@email.com / Bank: routing XXX"
```

Save to `freelance-data/config.json`.

## Data Integrity Rules

1. **Never overwrite** — always read existing data first, modify, then write back
2. **Always backup** — before any write operation, check data exists and is valid JSON
3. **UUID generation** — use timestamp-based IDs: `client-[timestamp]`, `project-[timestamp]`
4. **Date format** — always use ISO 8601: `YYYY-MM-DD`
5. **Currency** — store as numbers, display with `$` formatting
