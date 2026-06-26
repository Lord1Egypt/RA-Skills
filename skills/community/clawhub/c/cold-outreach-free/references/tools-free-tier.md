# Tools — Free Tier Setup Guide

Setup notes for every tool in the cold outreach stack. All run at $0/month.

---

## Apollo.io

**Role:** Lead sourcing (email + company data)
**Free limit:** 75 verified export credits/month
**Website:** apollo.io

### Account setup

1. Go to apollo.io → Sign up with Google or email
2. Complete onboarding (select "Lead Generation" as use case)
3. Verify email — required before exports work
4. No credit card needed for free tier

### Free tier limits (as of 2026)

| Feature | Free Limit |
|---------|------------|
| Export credits | 75/month |
| Email reveals | Included in export credits |
| Saved searches | Unlimited |
| Contact records (view) | Unlimited |
| Sequences (Apollo native) | 2 active sequences |

### Filter setup tips

- **Always check "Verified Email" only** — unverified emails spike bounces and hurt deliverability
- **Company Headcount** is more reliable than "Employees" estimate — use the range filter
- **Save your best search** as a named saved search — rerun monthly to find new entries
- **Don't export your entire search** — prioritize top-scored leads using the lead scoring rubric (see lead-sourcing.md)

### Export process

1. Run your search, apply all filters
2. Select all results (or select top N manually)
3. Click Export → Export to CSV
4. Map fields: First Name, Last Name, Email, Title, Company, LinkedIn URL
5. Download CSV, open in Google Sheets, verify column structure

---

## Hunter.io

**Role:** Email verification + domain-based email finding
**Free limit:** 25 searches/month, 50 verifications/month
**Website:** hunter.io

### Account setup

1. Go to hunter.io → Sign up with Google or email
2. Free account — no credit card required
3. Confirm email

### Domain Search (finding emails for a company)

1. Go to Domain Search tab
2. Enter company domain (e.g., `stripe.com`)
3. Hunter returns all known emails + pattern used (e.g., `{first}.{last}@company.com`)
4. Filter by department to find your target role
5. Export results as CSV

### Email Verifier (checking individual emails)

1. Go to Email Verifier tab
2. Paste a single email or upload a CSV
3. Results: Valid, Risky, Invalid
   - **Valid:** use it
   - **Risky:** catch-all domain — email may exist but can't be confirmed. Skip for cold outreach.
   - **Invalid:** remove from list immediately

### Google Sheets Add-on

Install from Google Workspace Marketplace:
1. Extensions → Add-ons → Get add-ons
2. Search "Hunter for Sheets"
3. Authorize with your Hunter account
4. Use in your Leads sheet:
   - `=HUNTER_VERIFY(A2)` — verifies the email in cell A2
   - Returns "deliverable", "risky", or "undeliverable"

---

## Gmail / SMTP

**Role:** Email sending
**Free limits:** 500 emails/day (Gmail free), 2,000/day (Google Workspace)
**Requirement:** Separate sending account (not your primary inbox)

### Setting up a sending account

1. Create a new Gmail account specifically for outreach: `yourname.outreach@gmail.com`
2. **Do not send cold emails from your primary email** — reputation risk
3. Set up your email signature: Name, title, company name, link to your website

### SPF and DKIM (basic)

Gmail handles SPF/DKIM automatically for @gmail.com accounts. No setup needed.

If you're using a custom domain (e.g., `@yourcompany.com`):
- SPF: Add TXT record to your DNS: `v=spf1 include:_spf.google.com ~all`
- DKIM: Enable in Google Workspace Admin → Apps → Gmail → Authenticate email
- Without SPF/DKIM on custom domains, emails frequently land in spam

### Warm-up protocol (mandatory before cold sending)

A new Gmail account that immediately sends 40 cold emails will be flagged. Warm it up first.

**Week 1–2:**
- Send 5–10 real emails per day to people who will reply (friends, colleagues, newsletters you're subscribed to)
- Reply to emails in the account inbox
- Goal: establish a sending/receiving pattern that looks human

**Week 3:**
- Start cold sends at 10–15/day
- Increase by 5/day each week
- Target max: 40–50/day for free Gmail

**Signs your account is warm enough:**
- Emails you send to your own other accounts land in Primary (not Promotions or Spam)
- No "suspicious activity" warnings from Google

### Gmail sending limits

| Account type | Daily limit |
|-------------|-------------|
| Gmail free (@gmail.com) | 500/day |
| Google Workspace (paid) | 2,000/day |
| Gmail via SMTP (programmatic) | 100/day (free), 2,000/day (Workspace) |

**For n8n automation:** Use Gmail OAuth2 credentials or SMTP with App Password.

**App Password setup (for SMTP):**
1. Enable 2FA on your Google account
2. Go to myaccount.google.com → Security → App Passwords
3. Create App Password for "Mail" + "Other device" → name it "n8n"
4. Use this password in n8n Gmail credentials (not your regular password)

---

## Google Sheets

**Role:** Lead tracking, hot leads routing, suppression management
**Free limits:** Unlimited rows, unlimited sheets
**Requirement:** Google account (free)

### Recommended sheet structure

Create one spreadsheet with four tabs:

**Tab 1: Leads**
| Column | Notes |
|--------|-------|
| First Name | |
| Last Name | |
| Email | |
| Company | |
| Title | |
| LinkedIn URL | Optional |
| Source | Apollo, Hunter, LinkedIn, Manual |
| Status | new / emailed-d0 / emailed-d3 / emailed-d7 / replied / not-now / unsubscribed / stalled |
| Last Contacted | Date of most recent email sent |
| Reply Category | interested / not-now / not-interested / objection / ooo |
| Notes | Anything relevant: "follow up Q3", "wants deck", etc. |

**Tab 2: Hot Leads**
Leads who replied with interest. Columns: same as Leads + "Call Scheduled," "Call Outcome," "Next Step"

Auto-populate from Leads tab when Status = "interested" (manual or via n8n Workflow 3).

**Tab 3: Suppression**
| Column | Notes |
|--------|-------|
| Email | The suppressed address |
| Company | Optional |
| Date Added | When they unsubscribed |
| Reason | unsubscribe / bounced / do-not-contact |

**Before every import:** cross-reference new leads against this tab. If a match exists, delete the row.

**Tab 4: Stats**
Track weekly:
- Total leads in list
- Emails sent this week
- Open rate (estimate from replies/opens if not using tracking)
- Replies received
- Positive replies
- Unsubscribes

Review every Friday. One number that matters: positive reply rate. If it drops below 1%, something is wrong.

---

## n8n (Optional Automation)

**Role:** Workflow automation for lead sourcing, email sequencing, and reply handling
**Free limits:** Free cloud tier (limited executions), free self-hosted (unlimited)
**Website:** n8n.io

### Free vs self-hosted

| Option | Cost | Executions | Setup |
|--------|------|-----------|-------|
| n8n Cloud free tier | $0 | ~20 executions/mo | Hosted, no setup |
| n8n self-hosted | $0 | Unlimited | Requires a server or local machine |
| n8n Cloud paid | $20/mo | Unlimited | Hosted |

**Recommendation:** Self-host on a VPS ($5–6/month on Hetzner, DigitalOcean, or Vultr) or run locally on your machine. The cloud free tier is too limited for real outreach volumes.

### Self-hosted setup (quick)

```bash
# Requires Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Access at `http://localhost:5678`. For persistent hosting, use Docker Compose or install on VPS.

### Pre-built workflow option

Rather than building the workflows from scratch, the **Cold Outreach System** ($19) includes three pre-built n8n workflow JSON files:
- Workflow 1: Lead Sourcing (CSV → filter → dedupe → Google Sheets)
- Workflow 2: Email Sequencer (reads Sheets → sends on schedule → updates status)
- Workflow 3: Reply Handler (IMAP monitor → categorizes → routes hot leads → updates Sheets)

**→ [Cold Outreach System — $19](https://qssys.gumroad.com/l/cold-outreach-system)**

Import, configure 3–5 variables, launch. Skips the 10–15 hours of building and debugging the integration from scratch.

### If building your own

Key nodes you'll need:
- **Schedule Trigger** — run daily at 9 AM
- **Google Sheets** — read/write lead data
- **Gmail** (or SMTP) — send emails
- **IMAP Email** — poll inbox for replies
- **IF** — conditional logic (send only to Status = "new", etc.)
- **Set** — update field values in Sheets rows

Start with Workflow 2 (email sequencer) — it's the highest leverage automation. Workflows 1 and 3 can be done manually until you're sending enough volume to justify automating them.
