---
name: content-pipeline-provisioner
description: "Self-serve AI content pipeline skill for OpenClaw. Sets up and runs a fully automated social media content engine on your own OpenClaw instance using your own API keys and accounts. Automates TikTok daily posts (AI-generated slides), Twitter/X 5 posts per day in your voice, newsletter 3x per week via MailerLite, daily blog post published to your site, and morning/evening Telegram briefings. Use when setting up a content pipeline for any product or brand, or when asked to 'provision pipeline for [product]', 'set up content pipeline', 'run my content engine', 'start posting for [product]', 'go live [slug]', 'pause pipeline', or 'resume pipeline'."
---

# Content Pipeline Provisioner

Automated content engine for OpenClaw. One command sets up daily TikTok, Twitter, newsletter, blog, and briefings for any product — all on your machine, your accounts, your data.

## This Skill Is Self-Hosted
You control everything. Your APIs, your accounts, your posting schedule. Nothing goes through Xero. For a fully done-for-you version (Xero runs it for you), see xeroaiagency.com/services.

## What Gets Automated

| Channel | Frequency | Requirement |
|---|---|---|
| TikTok slideshow | 1/day | Postiz account + TikTok connected |
| Twitter/X posts | 5/day | Postiz account + Twitter connected |
| Newsletter | Mon/Wed/Fri | MailerLite API key + subscriber group |
| Blog post | 1/day | Supabase + Netlify (see setup-checklist.md) |
| Morning briefing | 7 AM daily | Telegram bot token + chat ID |
| Evening briefing | 8 PM daily | Telegram bot token + chat ID |

## Before You Start
Complete the setup checklist at `references/setup-checklist.md`. Takes ~30 minutes. You need:
- **OpenClaw** installed and running
- **Larry skill** installed (`clawhub install larry` or download from larrybrain.com) — this is the TikTok posting engine this skill runs on top of
- **Postiz** account with TikTok + Twitter connected (postiz.com — free plan works)
- **OpenAI** API key (for image + text generation)
- **MailerLite** API key + group ID (for newsletter)
- **Telegram** bot token + chat ID (for briefings)
- **Supabase + Netlify** (optional — only needed for blog auto-publishing)

## Trigger Commands

| What you say | What happens |
|---|---|
| `provision pipeline for [product]` | Start interactive setup for a new product |
| `go live [slug]` | Flip test posts to public after you've reviewed them |
| `pause pipeline [slug]` | Disable all crons for a product |
| `resume pipeline [slug]` | Re-enable crons for a product |
| `pipeline status` | Show all active pipelines and their cron health |

## Provisioning Flow

```
You: "provision pipeline for [product name]"
  → Evo asks 6 questions (2 min)
  → Generates config.json + voice guide
  → Creates system folder in your workspace
  → Registers 6 crons (SELF_ONLY — not public yet)
  → Runs one test generation
  → You review: "looks good" or "redo [feedback]"
  → You say: "go live [slug]"
  → Evo flips all crons to PUBLIC
  → Pipeline runs daily from that point
```

## Step-by-Step Execution

### Step 1 — Ask 6 questions
When triggered, ask the user in sequence (do not dump all at once):

1. "What's the product name and what does it do? (2-3 sentences)"
2. "Who is your target audience?"
3. "Describe your brand voice in 3 words (e.g. bold, educational, casual)"
4. "Any topics that are completely off-limits?"
5. "What are your TikTok and Twitter/X usernames?"
6. "What timezone should posts go out in? (e.g. America/New_York)"

### Step 2 — Generate system slug
`slug = productName.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/-+/g, '-')`
Example: "Echo Reviews" → "echo-reviews"

### Step 3 — Create system folder
```
LARRY_ROOT = ~/[workspace]/99-External-Systems/skills/larry
SYSTEMS_DIR = {LARRY_ROOT}/tiktok-marketing/systems
TEMPLATE_DIR = {SYSTEMS_DIR}/echo-system-1
NEW_DIR = {SYSTEMS_DIR}/{slug}-system-1
```
- Copy template: `cp -r {TEMPLATE_DIR} {NEW_DIR}`
- Write `{NEW_DIR}/config.json` using answers from Step 1. See `references/config-schema.md`.
- Write `{NEW_DIR}/voice.md` from brand voice + product description. See `references/voice-guide-template.md`.
- Add entry to `{LARRY_ROOT}/tiktok-marketing/systems.json`

### Step 3b — Generate Twitter config
Write `{LARRY_ROOT}/social/twitter/config.json` using the buyer's brand details.
This file MUST be generated fresh — never copy Xero's version. Use this structure:
```json
{
  "brand": {
    "company": "{productName}",
    "products": ["{productName}"],
    "mission": "{one-line mission derived from product description}"
  },
  "timezone": "{user timezone from Step 1}",
  "leadMinutes": 10,
  "schedule": ["09:00", "12:00", "15:00", "18:00", "20:00"],
  "postiz": {
    "integrationId": "{POSTIZ_TWITTER_ID from .env}",
    "secretFile": "config/secrets/postiz_keys.json"
  },
  "openai": {
    "secretFile": "config/secrets/openai_keys.json"
  },
  "voiceFile": "{NEW_DIR}/voice.md",
  "outputDir": "99-External-Systems/skills/larry/social/twitter/posts",
  "mixTargets": {
    "build": 0.35,
    "ai_news": 0.20,
    "ops_lesson": 0.20,
    "engage": 0.15,
    "cta": 0.10
  }
}
```

### Step 4 — Load user credentials
Read from `~/.openclaw/.env`:
- `OPENAI_API_KEY` — required for image generation
- `POSTIZ_API_KEY` — required for scheduling
- `POSTIZ_TIKTOK_ID` — Postiz integration ID for TikTok
- `POSTIZ_TWITTER_ID` — Postiz integration ID for Twitter
- `MAILERLITE_API_KEY` + `MAILERLITE_GROUP_ID` — required for newsletter
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` — required for briefings

If any required key is missing, tell the user exactly which one and link to `references/setup-checklist.md` for how to get it.

### Step 5 — Register crons (SELF_ONLY — test mode)
Register 6 crons using the cron tool. All start as SELF_ONLY / dry-run until user confirms:

**TikTok** — daily at 7:30 AM user timezone:
`"Run the TikTok daily post for {slug} system at {NEW_DIR} in SELF_ONLY mode"`

**Twitter** (×5) — spread across day, user timezone:
`"Run Twitter posts for {slug} using voice guide at {NEW_DIR}/voice.md — post to Postiz SELF_ONLY"`

**Newsletter** — Mon/Wed/Fri 9 PM:
`"Draft and send {productName} newsletter using voice at {NEW_DIR}/voice.md and MailerLite config"`

**Blog** — daily 2 PM:
`"Write and publish one SEO blog post for {productName} using voice at {NEW_DIR}/voice.md"`

**Morning briefing** — 7 AM:
`"Send morning pipeline briefing for {productName} to Telegram TELEGRAM_CHAT_ID"`

**Evening briefing** — 8 PM:
`"Send evening pipeline briefing for {productName} to Telegram TELEGRAM_CHAT_ID"`

Store cron IDs in `{NEW_DIR}/cron-ids.json`.

### Step 6 — Run test generation
Generate one TikTok hook pack and one sample tweet. Show output to user. Ask: "Does this look right? Say 'go live [slug]' when ready, or 'redo [feedback]' to adjust."

### Step 7 — Go live
When user says "go live [slug]":
- Update `{NEW_DIR}/config.json`: set `posting.privacyLevel` to `"PUBLIC"`
- Update all crons to remove SELF_ONLY restriction
- Confirm to user: "Pipeline is live. First public post goes out tomorrow at 7:30 AM [timezone]."

## Pause / Resume

**Pause:** Disable all crons in `{NEW_DIR}/cron-ids.json` using cron tool. Update config: `"active": false`.
**Resume:** Re-enable all crons. Update config: `"active": true`. Confirm to user.

## Error Handling
- Missing API key → tell user exactly which key, link to setup-checklist.md
- Postiz error → check integration IDs, suggest reconnecting channel in Postiz
- MailerLite error → verify API key and group ID are correct
- Image generation failure → retry once, then fall back to text-only post with note to user

## Reference Files
- `references/setup-checklist.md` — step-by-step account setup (start here)
- `references/config-schema.md` — how to map product answers to config.json fields
- `references/voice-guide-template.md` — format for generating voice.md
- `references/blog-schema.md` — Supabase table schema for blog publishing
