# 🦞 competitor-radar

An OpenClaw skill that tracks your competitors weekly — pricing changes, new
blog posts, hiring signals, GitHub momentum, and customer voice. Delivers a
structured digest to Slack, Telegram, WhatsApp, or Discord every Monday.
Fires same-day alerts for critical changes like pricing updates or funding
announcements.

## What it tracks

| Signal | Source | Frequency |
|---|---|---|
| Pricing page changes | Playwright scrape + semantic diff | Daily alert + weekly digest |
| Homepage positioning | curl scrape + text diff | Daily alert + weekly digest |
| Blog / changelog posts | RSS feed or scrape | Weekly digest |
| Job postings | LinkedIn + Indeed | Weekly digest |
| GitHub stars + releases | GitHub API | Weekly digest |

## Install

### 1. Clone into your OpenClaw skills directory

```bash
git clone https://github.com/manjotpahwa/competitor-radar \
  ~/.openclaw/workspace/skills/competitor-radar
```

### 2. Install Python dependencies

```bash
cd ~/.openclaw/workspace/skills/competitor-radar
pip install -r requirements.txt
playwright install chromium
```

### 3. Set environment variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) for whichever
channels you want to deliver to:

```bash
# Slack (pick one)
export SLACK_BOT_TOKEN="xoxb-..."       # bot token (preferred)
export SLACK_WEBHOOK_URL="https://..."   # or incoming webhook

# Telegram
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."

# Discord
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# WhatsApp (via Twilio)
export TWILIO_ACCOUNT_SID="..."
export TWILIO_AUTH_TOKEN="..."
export TWILIO_FROM_WHATSAPP="+14155238886"
export TWILIO_TO_WHATSAPP="+1..."

# GitHub (optional — raises rate limit from 60 to 5000 req/hr)
export GITHUB_TOKEN="ghp_..."
```

### 4. Restart OpenClaw

The skill auto-loads when OpenClaw starts.

## Usage

### Add your first competitor

In your OpenClaw chat (WhatsApp, Telegram, Slack, Discord):

```
/competitor-radar setup
```

or just:

```
add competitor Notion https://notion.so
```

OpenClaw will ask for the details, capture a baseline snapshot,
and set up weekly + daily cron jobs automatically.

### Run a manual digest

```
/competitor-radar run
```

### Ask questions

```
What changed at Notion this week?
Which competitors changed pricing recently?
Who is Figma hiring?
Show me last month's digest
```

### Check status

```
/competitor-radar status
```

## Free vs Paid

| | Free | Paid |
|---|---|---|
| Competitors tracked | 1 | Unlimited |
| Weekly digest | ✓ | ✓ |
| Daily critical alerts | — | ✓ |
| Historical digest archive | 4 weeks | Unlimited |

**Upgrade**: https://competitor-radar.gumroad.com

## File structure

```
competitor-radar/
  SKILL.md                  ← OpenClaw skill definition
  requirements.txt          ← Python dependencies
  scripts/
    scrape.py               ← Playwright + curl scraper
    diff.py                 ← Semantic diff engine
    jobs.py                 ← LinkedIn/Indeed job tracker
    github_tracker.py       ← GitHub API tracker
    digest_builder.py       ← Weekly digest assembler
    deliver.py              ← Multi-channel delivery
    alert.py                ← Daily critical-change detector
  data/
    competitors.json        ← Your competitor config
    snapshots/              ← Page snapshots (never deleted)
    jobs/                   ← Job listing snapshots
    digests/                ← Weekly digest archive
    alerts/                 ← Alert history log
```

## Troubleshooting

**Playwright not found**: Run `playwright install chromium`. If that fails,
the scraper automatically falls back to curl (works for most pages).

**No GitHub data**: Set `GITHUB_TOKEN` env var. Public API works without
it but is rate-limited to 60 requests/hour.

**Slack not delivering**: Check that your bot has `chat:write` scope and
is invited to the channel.

**Skills not loading in OpenClaw**: Ensure the directory is at
`~/.openclaw/workspace/skills/competitor-radar/` and contains `SKILL.md`.
Restart OpenClaw after adding.
