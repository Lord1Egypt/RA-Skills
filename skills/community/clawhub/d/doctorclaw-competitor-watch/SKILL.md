---
name: doctorclaw-competitor-watch
description: "Competitor watch — monitor competitor websites and social for changes, new offers, and moves. Weekly cron or on-demand."
version: 1.0.0
tags: [competitive-intelligence, monitoring, strategy, research, automation]
metadata:
  clawdbot:
    emoji: "🔍"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Competitor Watch

Know what your competitors are doing before your customers tell you. This skill monitors competitor websites, social profiles, and online presence for changes — new pricing, product launches, messaging shifts, and hiring signals — so you can react strategically instead of being caught off guard.

Run it weekly on a cron, or trigger it when you want a competitive landscape check.

## What You Get

- Website change detection (pricing, features, messaging, new pages)
- Social media activity summary (recent posts, engagement trends)
- New job postings that signal strategic moves
- Product or feature announcements
- Competitive comparison snapshot

## Setup

### Required
- **Competitor list** — Names and URLs of competitors to monitor (minimum: website URL)

### Optional (but recommended)
- **Social profiles** — LinkedIn company pages, X handles, Instagram accounts for each competitor
- **Your own positioning** — your pricing, features, and messaging for comparison
- **Alert channel** — Telegram/Discord for real-time alerts on major changes
- **Watch history** — folder to archive previous snapshots for trend tracking

### Configuration

Tell your agent:

1. **Competitors** — list of companies to watch (name + website URL minimum)
2. **Watch frequency** — how often to check (default: weekly on Monday)
3. **Focus areas** — what to watch for (pricing, features, hiring, content, all)
4. **Alert triggers** — what warrants an immediate alert (pricing change, new product launch)
5. **Comparison format** — side-by-side vs. individual reports
6. **Delivery** — where to send reports (Telegram, Discord, file)

## How It Works

### Step 1: Define Watch Targets
For each competitor, track:
- **Website:** homepage, pricing page, features page, blog
- **Social:** LinkedIn, X/Twitter, Instagram (if provided)
- **Careers:** job postings page (signals growth areas)
- **Blog/news:** recent content and announcements

### Step 2: Scan Websites
For each competitor's website:
- Fetch key pages (homepage, pricing, features, about)
- Compare against last snapshot (if available)
- Flag changes: new copy, pricing updates, new features listed, removed features
- Note new pages or sections added

### Step 3: Scan Social Media
For each competitor's social profiles:
- Pull recent posts (last 7 days)
- Summarize themes and messaging
- Note engagement levels (high-performing posts)
- Flag announcements, launches, or promotions

### Step 4: Scan Job Postings
- Check careers page or LinkedIn jobs
- Identify new roles posted
- Analyze what roles signal: engineering = building, sales = growing, marketing = pushing

### Step 5: Compile Watch Report

```
🔍 Competitor Watch — Week of [Date]

━━ [COMPETITOR 1] ━━━━━━━━━━━━━━━━━━━━
🌐 WEBSITE
• [Change detected / No changes]
• [Pricing updated: was $X, now $Y]
• [New feature page: "AI Assistant"]

📱 SOCIAL ACTIVITY
• [X] posts this week (LinkedIn: [X], X: [X])
• Top post: "[summary]" — [engagement level]
• Themes: [product launch / thought leadership / hiring push]

💼 HIRING
• [X] new job postings
• Notable: [Senior AI Engineer, Head of Sales]
• Signal: [investing in AI capabilities / scaling sales team]

💡 TAKEAWAY: [1-sentence strategic implication]

━━ [COMPETITOR 2] ━━━━━━━━━━━━━━━━━━━━
[Same format]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 COMPETITIVE SNAPSHOT
| Area       | You        | Comp 1     | Comp 2     |
|---|---|---|---|
| Pricing    | $X/mo      | $Y/mo      | $Z/mo      |
| Key Feature| [feature]  | [feature]  | [feature]  |
| Hiring     | [X] roles  | [X] roles  | [X] roles  |

⚡ ACTION ITEMS
• [Consider matching Comp 1's price drop]
• [Comp 2 launched feature X — evaluate if we need it]
• [Comp 1 hiring aggressively in sales — expect more outreach]
```

### Step 6: Deliver & Archive
- Send report via configured channel
- Save snapshot to `memory/competitor-watch/YYYY-MM-DD.md`
- If alert triggers are hit (pricing change, major launch), send immediate notification
- Keep historical data for trend analysis

## Examples

**User:** "Watch these competitors: Acme AI (acmeai.com), BotForge (botforge.io), AutoPilot Pro (autopilotpro.com)"

**Agent:** Adds to watch list, runs initial scan, delivers first report with baseline data.

**User:** "What are my competitors up to?"

**Agent runs the scan and delivers the full watch report.**

**User:** "Did anyone change their pricing this week?"

**Agent:** Checks pricing pages specifically, reports any changes detected since last scan.

## Customization Ideas

- **Real-time alerts** — get notified immediately when a competitor changes pricing or launches something new
- **Review monitoring** — track competitor reviews on G2, Capterra, Trustpilot
- **Ad monitoring** — watch for competitor ads on Google, Facebook, LinkedIn
- **Content gap analysis** — compare competitor blog topics to yours, find gaps
- **Win/loss analysis** — track deals lost to specific competitors and why

## Want More?

This skill handles competitive monitoring and reporting. But if you want:

- **Custom integrations** — connect to SEMrush, SimilarWeb, or social listening tools for deeper insights
- **Advanced automations** — real-time price monitoring, automated competitive battle cards, deal intelligence
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
