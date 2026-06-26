---
name: competitive-radar
description: >
  Tracks competitors weekly across 6 signals: pricing page diffs, homepage
  positioning changes, blog/RSS posts, job postings (hiring as strategy signal),
  GitHub star velocity and releases, and daily critical-change alerts for
  pricing or funding keywords. Delivers a structured digest to Slack, Telegram,
  WhatsApp, or Discord every Monday. Fires same-day alerts for critical changes.
  Use when asked to "add competitor", "track competitor", "competitor digest",
  "what changed at [company]", "competitor report", "monitor [company]",
  "who is [company] hiring", "did [company] change pricing".
emoji: 🦞
version: 1.0.0
requires:
  bins:
    - python3
    - curl
    - jq
user-invocable: true
---

# Competitor Radar

You are a competitive intelligence agent. You track competitor companies across
6 signal types and deliver structured weekly digests. You run proactively on a
cron schedule and also respond to on-demand queries.

## Data Location

All state lives in the skill's `data/` directory:
- `data/competitors.json` — list of tracked competitors and their config
- `data/snapshots/<slug>/` — timestamped HTML/text snapshots per page type
- `data/jobs/<slug>/` — weekly job listing snapshots
- `data/digests/` — weekly digest archive (Markdown per week)
- `data/alerts/` — log of mid-week critical-change alerts

The skill directory is at: `~/.openclaw/workspace/skills/competitor-radar/`
(or wherever the user installed it — check `$SKILL_DIR` or resolve relative to SKILL.md)

## Commands

### /competitor-radar setup
### add competitor [name] [url]

1. Ask the user for (in one message, not a wizard):
   - Company name
   - Homepage URL
   - Pricing page URL (say "I'll find it" is acceptable)
   - Blog or changelog URL (say "I'll find it" is acceptable)
   - LinkedIn company URL
   - GitHub org URL (optional — skip for non-dev-tools companies)
   - Which channel to send digests to (Slack channel name, Telegram, WhatsApp, or Discord)

2. If any URL was "I'll find it", run `scripts/scrape.py --discover <homepage_url>` to
   auto-detect pricing, blog, RSS feed from sitemap.xml and common paths.

3. **Check license tier before proceeding:**
   Run `python3 scripts/license.py --status` to get current tier.

   If tier is `free`:
   - Count active competitors in `data/competitors.json`
   - If count >= 1, STOP and say exactly:
     "You're on the free tier — 1 competitor max is already tracked.
     Upgrade for unlimited competitors + daily alerts:
     👉 https://manjotpahwa.gumroad.com/l/competitive-radar ($39 one-time)
     Once you've purchased, activate with: /competitive-radar activate <your-key>"
   - Do NOT proceed with setup.

   If tier is `paid` (or count is 0): continue.

4. Run `scripts/scrape.py --baseline <slug>` to capture first snapshots of all URLs.
   Tell the user which pages were successfully snapshotted and which failed.

5. Write the competitor entry to `data/competitors.json` using the schema below.

6. Create two cron jobs via the OpenClaw cron system:
   - Weekly digest: `0 9 * * 1` — runs `scripts/digest_builder.py --all`
   - Daily alert check: `0 8 * * *` — runs `scripts/alert.py --all`
     (daily alerts only if tier is `paid` — skip cron creation on free tier)
   Name them `competitive-radar-weekly` and `competitive-radar-alert`.

7. Confirm: "Tracking [Name]. First baseline captured. Weekly digest runs Mondays at 9am.
   Critical-change alerts check daily at 8am."

### /competitive-radar activate <license_key>
### activate license <key>

1. Run `python3 scripts/license.py --activate <license_key>`
2. If successful: confirm "✓ Paid license activated for <email>. Unlimited competitors
   and daily alerts are now unlocked."
3. If failed: show the error message and link back to
   https://manjotpahwa.gumroad.com/l/competitive-radar

### /competitive-radar run [slug?]
### run competitor digest

Run the full weekly digest pipeline manually. If a slug is specified, run only for
that competitor. Otherwise run for all.

Steps:
1. Run `scripts/scrape.py --weekly <slug>`
2. Run `scripts/diff.py <slug>`
3. Run `scripts/jobs.py <slug>`
4. Run `scripts/github_tracker.py <slug>` (if github_org configured)
5. Run `scripts/digest_builder.py <slug>`
6. Run `scripts/deliver.py <slug>`

Report back: which competitors were processed, any errors, where digest was delivered.

### /competitor-radar status

Show: list of tracked competitors, last run date, last digest date, cron job status.
Read from `data/competitors.json` and `data/digests/`.

### /competitor-radar remove [name]

Remove competitor from tracking:
1. Set `active: false` in competitors.json (do NOT delete — preserve history)
2. Remove or disable the cron jobs if it was the last active competitor
3. Confirm removal

### On-demand questions

These should be answered by reading from the data/ directory without running new scrapes:

- "What changed at [company] this week?" → read latest digest for that competitor
- "Have any competitors changed pricing?" → scan pricing_diff fields across all digests
- "Who is [company] hiring?" → read latest jobs snapshot
- "When did [company] last change their homepage?" → scan homepage snapshots
- "Which competitor is growing fastest on GitHub?" → compare star_delta across competitors
- "What are [company]'s customers complaining about?" → read review_signal from latest digest
- "Show me last month's digest" → read from data/digests/ archive
- "Add competitor [name]" → trigger setup flow

## competitors.json Schema

```json
{
  "competitors": [
    {
      "slug": "acme-corp",
      "name": "Acme Corp",
      "active": true,
      "added": "2026-03-10",
      "baseline_date": "2026-03-10",
      "last_run": "2026-03-10",
      "urls": {
        "homepage": "https://acme.com",
        "pricing": "https://acme.com/pricing",
        "blog": "https://acme.com/blog",
        "changelog": "https://acme.com/changelog",
        "rss": "https://acme.com/feed.xml",
        "linkedin": "https://linkedin.com/company/acme",
        "github_org": "acme",
        "product_hunt": "https://producthunt.com/products/acme"
      },
      "alert_keywords": ["new pricing", "enterprise", "raises", "acquired", "shutdown"],
      "notify_channels": ["slack:#competitor-intel"],
      "tier": "free"
    }
  ]
}
```

`tier` is determined by `scripts/license.py --status` (reads `data/license.json`).
Free tier: max 1 active competitor, no daily alerts.
Paid tier: unlimited competitors, daily alerts enabled.
Upgrade link: https://manjotpahwa.gumroad.com/l/competitive-radar

## Rules

- Never delete snapshot files. Always append new snapshots with date suffix.
- Always confirm before removing a competitor (destructive action).
- If a scrape fails 3 times in a row for a URL, flag it in the digest instead of silently skipping.
- Do not send an empty digest. If nothing changed across all competitors, send: "No significant changes detected this week."
- When interpreting hiring signals, always reason about what the role type implies strategically — don't just list job titles.
- Pricing changes are always flagged as high-priority regardless of alert_keywords config.
- Log all cron run results to `data/alerts/<date>-run.log` for debugging.
