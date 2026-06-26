---
name: doctorclaw-invoice-tracker
description: "Invoice tracker — track sent invoices, flag overdue payments, draft follow-up reminders. Weekly cron or on-demand."
version: 1.0.0
tags: [invoicing, finance, payments, follow-up, automation]
metadata:
  clawdbot:
    emoji: "💰"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Invoice Tracker

Stop chasing payments manually. This skill tracks your sent invoices, flags overdue ones, and drafts polite-but-firm payment reminders — so you get paid faster without the awkward follow-ups.

Run it weekly on a cron, or trigger it whenever you need to check who owes you money.

## What You Get

- All outstanding invoices organized by status (paid, pending, overdue, severely overdue)
- Automatic overdue detection based on payment terms
- Drafted payment reminder emails for each overdue invoice
- Aging report showing how long invoices have been outstanding
- Revenue summary (total billed, total collected, total outstanding)

## Setup

### Required
- **Invoice list** — A CSV file, Google Sheet, or any structured list your agent can read. Minimum columns: client name, invoice number, amount, date sent, due date, status (paid/unpaid). More columns = better context.

### Optional (but recommended)
- **Send access** — Gmail or email provider if you want the agent to send reminders after your approval
- **Accounting integration** — QuickBooks, FreshBooks, Wave, or Stripe for automatic invoice data
- **Delivery channel** — Telegram/Discord for overdue alerts

### Configuration

Tell your agent:

1. **Invoice list location** — file path, Google Sheet URL, or accounting tool connection
2. **Payment terms** — your standard terms (default: Net 30)
3. **Reminder style** — your tone for follow-ups (professional, friendly, firm, casual)
4. **Overdue thresholds** — when to escalate (default: 7 days past due = reminder, 30 days = urgent, 60 days = escalation)
5. **Check schedule** — when to run (default: every Monday at 9:00 AM local)
6. **Delivery** — where to send the invoice digest (Telegram, Discord, file)
7. **Currency** — your billing currency (default: USD)

## How It Works

### Step 1: Load Invoice Data
- Read your invoice list from the configured source
- For each invoice, extract: client name, invoice number, amount, date sent, due date, payment status, notes
- Calculate days outstanding for each unpaid invoice

### Step 2: Categorize Invoices
Sort all unpaid invoices into categories:

**🟢 CURRENT — Not yet due**
- Due date is in the future
- No action needed

**🟡 DUE SOON — Due within 7 days**
- Approaching due date
- Optional: send a friendly pre-due reminder

**🔴 OVERDUE — Past due date (1-30 days)**
- Payment is late
- Draft a polite reminder email

**⚫ SEVERELY OVERDUE — 30+ days past due**
- Payment is significantly late
- Draft a firmer follow-up with escalation language

### Step 3: Draft Reminders
For each overdue invoice, draft a payment reminder:

- **First reminder (1-7 days overdue):** Friendly, assume they forgot. "Just a quick reminder that Invoice #X is now past due."
- **Second reminder (8-14 days overdue):** Professional but direct. "Following up on Invoice #X — please let me know if there are any questions about this balance."
- **Third reminder (15-30 days overdue):** Firm. "Invoice #X is now [X] days past due. Please arrange payment at your earliest convenience."
- **Escalation (30+ days):** Serious. "This is a final notice regarding Invoice #X. If we don't receive payment by [date], we may need to discuss next steps."

Match the configured reminder style. Mark all as DRAFT — never send without approval.

### Step 4: Compile Invoice Digest
Format the digest:

```
💰 Invoice Digest — [Date]

📊 REVENUE STATUS
Total billed (all time): $[X]
Total collected: $[X] | Outstanding: $[X]
Overdue amount: $[X] across [X] invoices

⚫ SEVERELY OVERDUE ([X] invoices — $[X] total)
1. [Client] — Invoice #[X] — $[amount]
   Sent: [date] | Due: [date] | [X] days overdue
   📝 Reminder draft ready

🔴 OVERDUE ([X] invoices — $[X] total)
2. [Client] — Invoice #[X] — $[amount]
   Sent: [date] | Due: [date] | [X] days overdue
   📝 Reminder draft ready

🟡 DUE SOON ([X] invoices — $[X] total)
3. [Client] — Invoice #[X] — $[amount]
   Due: [date] ([X] days)

🟢 CURRENT ([X] invoices — $[X] total)
All on track — no action needed

💡 INSIGHTS
• Oldest overdue: [Client] — [X] days ($[amount])
• Largest outstanding: [Client] — $[amount]
• Collection rate this month: [X]%
```

### Step 5: Deliver & Track
- Send digest via configured channel
- Show full reminder drafts below the digest for review
- When user approves ("send reminder 1" or "send all"), send the emails
- After sending, log the reminder in the invoice notes with today's date
- Update invoice status if payment is confirmed

## Examples

**User:** "Check my invoices"

**Agent runs the workflow and responds:**

> 💰 Invoice Digest — Monday, March 10
>
> 📊 REVENUE STATUS
> Total billed: $47,200 | Collected: $38,500 | Outstanding: $8,700
> Overdue: $4,200 across 3 invoices
>
> ⚫ SEVERELY OVERDUE (1 invoice — $2,400)
> 1. **Greenfield Properties** — Invoice #1047 — $2,400
>    Sent: Jan 15 | Due: Feb 14 | 24 days overdue
>    📝 Draft: "Hi Lisa, this is a follow-up regarding Invoice #1047 for $2,400, now 24 days past due. Could you please provide an update on the payment timeline?"
>
> 🔴 OVERDUE (2 invoices — $1,800)
> 2. **TechStart Inc** — Invoice #1052 — $1,200
>    Sent: Feb 10 | Due: Mar 2 | 8 days overdue
>    📝 Draft: "Hey James, just a friendly reminder that Invoice #1052 is a bit past due. Let me know if you have any questions about it."
>
> 3. **Bloom Studio** — Invoice #1054 — $600
>    Sent: Feb 20 | Due: Mar 7 | 3 days overdue
>    📝 Draft: "Hi Maria, quick heads up — Invoice #1054 was due on March 7th. Just wanted to make sure it didn't slip through the cracks!"
>
> 🟢 CURRENT (4 invoices — $4,500)
> All on track

**User:** "Send reminders 2 and 3. Mark Greenfield as payment received."

**Agent:** Sends reminders to TechStart and Bloom. Updates Greenfield to "paid" with today's date.

---

**User:** "Set up weekly invoice checks"

**Agent:** Configures cron for Monday 9:00 AM, confirms:
> "Invoice tracker scheduled for every Monday at 9:00 AM. I'll flag overdue invoices and draft reminders for your review."

## Customization Ideas

- **Auto-generate invoices** — create invoices from completed project milestones
- **Late fee calculator** — automatically calculate and include late fees per your terms
- **Payment link inclusion** — add Stripe/PayPal payment links to reminder emails
- **Client payment history** — track which clients consistently pay late
- **Monthly revenue report** — summarize billings, collections, and trends each month
- **Tax prep export** — export annual invoice data formatted for your accountant

## Want More?

This skill handles invoice tracking and payment reminders. But if you want:

- **Custom integrations** — connect to QuickBooks, Stripe, FreshBooks, or your specific invoicing tool
- **Advanced automations** — auto-generate invoices, calculate late fees, sync with your accounting system
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
