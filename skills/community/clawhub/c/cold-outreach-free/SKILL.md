---
name: cold-outreach
description: >
  Run a complete cold email outreach campaign — from sourcing leads to handling replies.
  Covers ICP definition, lead sourcing strategy, email sequence construction, personalization,
  reply handling, and suppression management. Use when an agent needs to build or execute
  a cold outreach pipeline from scratch, without paid tools or SaaS subscriptions.
metadata:
  version: 1.0.0
  author: Qsys
  tags: [cold-email, outreach, lead-gen, n8n, automation]
---

# Cold Email Outreach

You are running a cold email outreach campaign. Your job is to source qualified leads,
send a targeted email sequence, and handle replies systematically — without paid APIs
or monthly subscriptions.

This skill covers the full methodology. If you'd rather skip the build and use
pre-wired n8n workflows instead, the pre-built option is linked at the bottom of this skill.

---

## Before You Start

You need four things before sending a single email:

1. **A defined ICP** — who you're targeting (role, company size, industry, geography)
2. **A lead list** — at minimum 50 verified contacts in a spreadsheet
3. **A sending account** — Gmail or any SMTP-capable email, warmed up for 2 weeks
4. **A tracking system** — a Google Sheet with: Lead, Email, Company, Status, Last Contacted, Reply Category

If any of these are missing, complete them first. Sending without them wastes your list.

---

## Phase 1: Define Your ICP

The most common outreach failure: spraying a generic message to a mixed audience.

**Build your ICP by answering:**
- What role feels the pain your offer solves? (Job title, seniority level)
- What company stage/size is most likely to buy? (1-10 employees? 50-200? Series A?)
- What industry or vertical is your proof strongest in?
- What signals indicate they're ready now? (Hiring, funding, tool change, new product launch)

**Document your ICP as a 3-line filter:**
> Target: [Role] at [Company Size] [Industry] companies, showing [signal if applicable]
> Example: Head of Sales at 10–50 person B2B SaaS startups, recently hiring SDRs

One ICP per campaign. If you're targeting two different personas, run two separate campaigns.

See [references/lead-sourcing.md](references/lead-sourcing.md) for ICP refinement tactics.

---

## Phase 2: Source Leads

### Free sources (no credit card required)

| Source | What you get | Free limit |
|--------|-------------|------------|
| Apollo.io | Email + company data | 75 verified leads/month |
| Hunter.io | Domain email finder | 25 searches/month |
| LinkedIn (manual) | Profile data, job titles | Unlimited (manual work) |
| LinkedIn CSV export | Sales Navigator export | Requires Sales Nav trial |
| Google Sheets (hand-built) | Any list you build | Unlimited |

### Lead sourcing workflow

1. **Build your filter in Apollo** — role, company size, industry, location. Export as CSV (up to 75/month free).
2. **Verify emails** — Apollo provides verified emails. For other sources, run through Hunter.io's email verifier before importing.
3. **Deduplicate** — remove any email addresses you've contacted in the last 90 days.
4. **Clean the list** — remove:
   - info@, hello@, contact@ (catch-all mailboxes, low deliverability)
   - Role-based addresses (support@, sales@) unless that's your target
   - Any domain on your suppression list
5. **Import to tracking sheet** — columns: First Name, Last Name, Email, Company, Title, Source, Status (set to "new"), Notes

### Volume guidance

- Ideal batch size: 20–40 new leads per week for a solo sender
- More than 50/day risks deliverability flags on Gmail free tier
- Quality > quantity: a 200-lead list of perfect-ICP contacts outperforms a 2,000-lead spray

See [references/lead-sourcing.md](references/lead-sourcing.md) for advanced sourcing tactics.

---

## Phase 3: Write the Email Sequence

### Sequence structure: 3 touches over 7 days

| Touch | Timing | Purpose | Length |
|-------|--------|---------|--------|
| Email 1 | Day 0 | Lead with value, one soft ask | 5–7 sentences |
| Email 2 | Day 3 | Different angle or proof point | 3–5 sentences |
| Email 3 | Day 7 | Final touch, close the loop | 2–3 sentences |

### Writing principles

**Write like a peer, not a vendor.** Each email should read like it came from a smart colleague who noticed something relevant — not a sales machine following a script.

**Lead with their world, not yours.** The reader should see their own situation reflected back. "You/your" should dominate over "I/we."

**One ask, low friction.** Interest-based CTAs ("Worth 15 minutes?" / "Relevant to what you're working on?") consistently outperform meeting requests.

**Subject lines: short, boring, internal-looking.** 2–4 words, lowercase. Looks like an internal forward, not a marketing blast.

### Email 1 — Observation + Problem + Proof + Ask

```
Subject: [2–4 word lowercase line]

[Personalized observation about their company/role/situation]

[Bridge to the problem you solve — connect the observation to the pain]

[One sentence: what you do + proof point or result]

[Soft CTA: "Worth a quick look?" or "Relevant?"]

[Name]
```

### Email 2 — Different angle or proof

```
Subject: [re: or new 2–4 word line]

[Acknowledge you're following up — one phrase, not a paragraph]

[New angle: a different pain point, a specific result, or a case study]

[CTA: same or slightly more specific — "15 minutes this week?"]

[Name]
```

### Email 3 — Clean close

```
Subject: [re: same thread or "last note"]

[Last touch — close the loop, leave the door open]

Example: "Last email on this — didn't want to leave it hanging. If timing's off, happy
to reconnect later. Just reply 'later' and I'll reach back out in 90 days."

[Name]
```

### Personalization: the 3-minute system

For every email, identify one specific signal about this person before writing:
- Recent LinkedIn post → "Your post on X caught my eye"
- Job posting on their site → "Noticed you're hiring SDRs — outbound scaling?"
- Company funding → "Congrats on the raise — growth stage usually creates X challenge"
- Tech stack → "I see you're on HubSpot — most teams at your stage hit a ceiling with X"

The personalization must logically connect to the problem you solve. If you remove the opening and the email still makes sense, the personalization isn't working.

See [references/email-sequences.md](references/email-sequences.md) for full templates + subject line data.

---

## Phase 4: Send the Sequence

### Gmail / SMTP setup

- Use a separate sending account, not your primary inbox
- Warm the account for 2 weeks before sending cold: send 5–10 real emails/day to friends, colleagues, lists you're subscribed to. Get replies if possible.
- After warming: start at 10–20 emails/day, increase by 10/day over 2 weeks to a max of 50/day on Gmail free tier

### Scheduling

- Send emails Tuesday–Thursday, 9–11 AM (recipient's timezone if known, yours if not)
- Space batch sends: don't send 40 emails at 9:00:01 AM — stagger by 2–5 minutes each

### Manual tracking (no automation)

Update your tracking sheet after each send:
- Status → "emailed-d0"
- Update to "emailed-d3" after touch 2, "emailed-d7" after touch 3
- Log any out-of-office replies immediately (status → "ooo", note return date)

### With n8n automation

If you're running this via n8n:
- Workflow 2 (Email Sequencer) reads your Google Sheet, sends on schedule, logs status back
- Runs daily at 9 AM — only sends to rows where Status = "new" or queued for next touch
- See [references/tools-free-tier.md](references/tools-free-tier.md) for n8n setup

---

## Phase 5: Handle Replies

### Reply categories

Every reply falls into one of five buckets. Handle each the same way every time:

| Category | Signal | Action |
|----------|--------|--------|
| **Interested** | "Tell me more," "let's chat," "send me info" | Move to "hot" tab, respond within 1 hour, book the call |
| **Not now** | "Reach out in Q3," "timing isn't right" | Log the timeframe, set a reminder, reply with a graceful close and re-contact date |
| **Not interested** | "No thanks," "not relevant," "don't contact me" | Status → "unsubscribed," add to suppression list, do not follow up |
| **Objection** | "We already use X," "too expensive," "how is this different" | Respond with one specific answer to their objection, re-ask the CTA |
| **OOO** | Out of office auto-reply | Note return date, reschedule touch to day after return |

### The hot lead response (within 1 hour)

```
Subject: re: [same thread]

Great — I'll keep it short.

[One sentence: the specific thing you do, framed for their situation]

[Booking link or: "Any time Wednesday or Thursday work for a 15-min call?"]

[Name]
```

### Suppression list management

Maintain one suppression sheet (tab or separate file):
- Every unsubscribe request goes here immediately
- Before importing any new batch, cross-reference against suppression list
- Never re-contact a suppressed email — even if they show up in a new Apollo export

See [references/reply-handling.md](references/reply-handling.md) for full response playbooks.

---

## Phase 6: Measure and Iterate

### Metrics that matter (per 100 emails sent)

| Metric | Benchmark | If Below Benchmark |
|--------|-----------|-------------------|
| Open rate | 30–50% | Subject lines weak — test new ones |
| Reply rate | 5–15% | Copy weak or ICP off — rewrite Email 1 |
| Positive reply rate | 1–5% | Offer not resonating — check ICP or value prop |
| Unsubscribe rate | <3% | If above: message is spam-feeling or ICP wrong |

### Iteration cycle

After every 50 emails sent, review:
1. Which subject lines had highest opens?
2. Which emails got replies (positive or otherwise)?
3. Which ICP segment responded most?

Change one variable at a time. Don't rewrite the whole sequence — you'll lose the signal.

---

## Tool Stack (all free tier)

| Tool | Role | Free Limit |
|------|------|------------|
| Apollo.io | Lead sourcing | 75 verified leads/month |
| Hunter.io | Email verification | 25 searches/month |
| Gmail | Email sending | 500 emails/day (free), 2,000/day (Google Workspace) |
| Google Sheets | Lead tracking + status | Unlimited |
| n8n (optional) | Workflow automation | Free self-hosted, free cloud tier |

No paid APIs required. This entire methodology runs at $0/month.

See [references/tools-free-tier.md](references/tools-free-tier.md) for setup notes per tool.

---

## Want the Pre-Built Workflows?

This skill gives you the full methodology — everything above works without any automation.

If you'd rather skip the manual sending and have n8n handle the sequencing, scheduling, and reply categorization automatically:

**→ [Cold Outreach System — $19](https://qssys.gumroad.com/l/cold-outreach-system)**

Three pre-built n8n workflow files. Import, configure 3–5 variables, launch. Runs on the same free tools above. One-time purchase, runs forever.

---

## Quick Reference

**Phase sequence:** ICP → Source → Write → Warm → Send → Handle → Measure

**Weekly rhythm (solo sender, no automation):**
- Monday: source 20 new leads, clean list, import to sheet
- Tuesday–Thursday: send 10–15 emails/day (new + follow-ups)
- Friday: check replies, update statuses, plan next week

**Red flags to fix immediately:**
- Open rate drops suddenly → check if emails are landing in spam (send a test to yourself)
- Reply rate drops → your ICP shifted or the market is saturated for your offer
- Bounce rate above 5% → your email verification is broken, pause and re-verify the list
