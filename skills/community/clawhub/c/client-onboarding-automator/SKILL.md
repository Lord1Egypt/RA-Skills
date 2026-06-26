# Client Onboarding Automator Skill

Automate the entire client onboarding workflow — from initial inquiry to project kickoff. Handles intake forms, contract generation, payment collection, welcome sequences, and project setup.

## What This Skill Does

1. **Intake Processing** — Captures new client info from email/form submissions
2. **Contract Generation** — Creates service agreements from templates
3. **Payment Collection** — Sends Stripe payment links automatically
4. **Welcome Sequence** — Sends onboarding email series (day 0, 1, 3, 7)
5. **Project Setup** — Creates folders, tasks, and checklists for new clients
6. **CRM Update** — Logs client details in your tracking system

## Trigger

When a new inquiry arrives (email matching pattern, form webhook, or manual trigger):

```
New client: [name] | [email] | [service] | [budget]
```

## Workflow

### Step 1: Intake
Parse the incoming inquiry and extract:
- Client name and email
- Service requested
- Budget/package selected
- Timeline expectations
- Special requirements

### Step 2: Auto-Response (Immediate)
Send a personalized acknowledgment email:
```
Subject: Thanks for reaching out, [Name]! Here's what happens next

Hi [Name],

Thanks for your interest in [service]. I've received your inquiry and here's what to expect:

1. I'll review your requirements (within 2 hours)
2. You'll receive a proposal with pricing
3. Once approved, we kick off immediately

In the meantime, here's a quick questionnaire to help me prepare:
[Link to intake form]

Best,
[Your name]
```

### Step 3: Proposal Generation
Create a proposal document with:
- Scope of work (based on service selected)
- Pricing (from your rate card)
- Timeline
- Terms

### Step 4: Contract + Payment
Once proposal is accepted:
- Generate contract from template
- Create Stripe payment link for the agreed amount
- Send contract + payment link to client

### Step 5: Welcome Sequence
After payment:
- **Day 0:** Welcome email + access credentials + kickoff questionnaire
- **Day 1:** "Getting started" guide + calendar link for kickoff call
- **Day 3:** Check-in + first deliverable preview
- **Day 7:** Progress update + feedback request

### Step 6: Project Setup
- Create project folder in workspace
- Generate task checklist from service template
- Set up recurring check-in reminders

## Configuration

```json
{
  "business_name": "Your Business Name",
  "from_email": "hello@yourdomain.com",
  "reply_to": "you@yourdomain.com",
  "stripe_key": "sk_live_...",
  "services": {
    "basic": { "name": "Basic Package", "price": 497, "description": "..." },
    "pro": { "name": "Pro Package", "price": 997, "description": "..." },
    "enterprise": { "name": "Enterprise", "price": 2497, "description": "..." }
  },
  "welcome_sequence_delays": [0, 1, 3, 7]
}
```

## Requirements
- Resend, SendGrid, or SMTP for email
- Stripe for payments
- OpenClaw with email/webhook channel configured
