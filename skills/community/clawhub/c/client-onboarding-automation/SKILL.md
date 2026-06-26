# Client Onboarding Automation Skill

Automate client onboarding workflows: intake forms, document collection, welcome sequences, and CRM setup.

## What This Skill Does

Streamlines new client onboarding by automating:
1. **Intake form processing** — Parse form submissions, extract key data
2. **Document collection** — Auto-request and track required documents
3. **Welcome email sequences** — Send personalized onboarding emails via Resend/SendGrid
4. **CRM record creation** — Auto-create client records with all collected data
5. **Task assignment** — Create onboarding checklists and assign team tasks
6. **Follow-up reminders** — Auto-nudge clients who haven't submitted docs

## Configuration

```json
{
  "email_provider": "resend",
  "crm": "google_sheets",
  "intake_fields": ["name", "email", "phone", "company", "service_needed"],
  "required_docs": ["ID", "contract", "payment_info"],
  "welcome_sequence": [
    { "delay_hours": 0, "template": "welcome" },
    { "delay_hours": 24, "template": "getting_started" },
    { "delay_hours": 72, "template": "check_in" }
  ]
}
```

## Email Templates

### Welcome Email
```
Subject: Welcome to {company_name}! Here's what's next

Hi {client_name},

Welcome aboard! We're excited to work with you.

Here's your onboarding checklist:
1. ✅ Sign up (done!)
2. 📋 Upload required documents: {doc_list}
3. 📞 Schedule your kickoff call: {calendar_link}

Questions? Reply to this email anytime.

Best,
{team_name}
```

### Document Reminder
```
Subject: Quick reminder: We still need {missing_docs}

Hi {client_name},

Just a friendly nudge — we're still waiting on:
{missing_doc_list}

Upload here: {upload_link}

This helps us get started faster on your {service_type}.

Thanks!
{team_name}
```

## Workflow

```
New Client Signs Up
    ↓
Parse Intake Data → Create CRM Record
    ↓
Send Welcome Email (immediate)
    ↓
Check for Required Documents (daily)
    ├── All docs received → Send "All set!" email → Assign to team
    └── Missing docs → Send reminder (day 1, 3, 7)
    ↓
Schedule Kickoff Call
    ↓
Onboarding Complete → Move to Active Client status
```

## Use Cases
- **Service businesses** — Law firms, accounting, consulting
- **SaaS companies** — New user activation flows
- **Agencies** — Client intake and project kickoff
- **Healthcare** — Patient intake and insurance verification
- **Real estate** — Buyer/seller onboarding with doc collection

## Requirements
- Email provider API key (Resend recommended)
- Google Sheets or CRM access for record keeping
- Calendar link for scheduling (Calendly, Cal.com, etc.)
