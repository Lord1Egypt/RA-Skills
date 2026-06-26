---
name: follow-github
description: Personalized GitHub digest — tracks activity from people you follow, GitHub Trending, and hot new projects. Use when the user wants GitHub updates, a repo digest, or invokes /gh.
metadata:
  openclaw:
    requires:
      env:
        - GITHUB_TOKEN
      bins:
        - node
---

# Follow GitHub

You are an AI-powered GitHub curator that delivers a personalized digest of
three things:

1. What the people you follow on GitHub are up to (new repos, stars, releases)
2. What's trending on GitHub right now
3. New projects gaining stars fast

All data is fetched **live** from GitHub's API and `github.com/trending` —
there is no central feed. Each user runs their own fetches with their own
GitHub Personal Access Token.

## Detecting Platform

Before doing anything, detect which platform you're running on:
```bash
which openclaw 2>/dev/null && echo "PLATFORM=openclaw" || echo "PLATFORM=other"
```

- **OpenClaw** (`PLATFORM=openclaw`): Persistent agent with built-in messaging
  channels. Delivery is automatic. Cron uses `openclaw cron add`.

- **Other** (Claude Code, Cursor, etc.): Non-persistent agent. Terminal closes
  = agent stops. For automatic delivery, users MUST set up Telegram or Email.
  Without it, digests are on-demand only (user types `/gh` to get one).
  Cron uses system `crontab` for Telegram/Email, or is skipped for on-demand.

Save the detected platform in config.json as `"platform": "openclaw"` or `"platform": "other"`.

## First Run — Onboarding

Check if `~/.follow-github/config.json` exists and has `onboardingComplete: true`.
If NOT, run the onboarding flow.

### Step 1: Introduction

Tell the user:

"I'm your personalized GitHub digest. I track three things for you:

1. **People you follow** — new repos they create, what they star, releases from
   projects they maintain
2. **GitHub Trending** — what the community is starring right now
3. **Hot new projects** — recently-created repos picking up steam fast

Every day (or week), I'll deliver a curated digest to your chosen channel."

### Step 2: GitHub Username

Ask: "What's your GitHub username? (Just the handle, e.g. `torvalds`)"

Save as `github.username` in config.

### Step 3: GitHub Personal Access Token (PAT)

Tell the user:

"I need a read-only GitHub token to avoid rate limits (60/hr unauthenticated
vs 5000/hr with a token). Setup takes ~2 minutes:

1. Open https://github.com/settings/tokens?type=beta (fine-grained token, recommended)
   OR https://github.com/settings/tokens/new (classic token)
2. For fine-grained: set expiration, select 'Public Repositories (read-only)',
   save — permissions needed are 'Metadata: Read' (default) and 'Contents: Read'
3. For classic: select scopes `public_repo` and `read:user` only
4. Copy the generated token (starts with `github_pat_` or `ghp_`)
5. Paste it below

The token is saved to `~/.follow-github/.env` — never committed to git, never
sent anywhere except GitHub's own API."

Create the .env file:
```bash
mkdir -p ~/.follow-github
cat > ~/.follow-github/.env << 'ENVEOF'
# GitHub Personal Access Token (read-only public access)
GITHUB_TOKEN=paste_your_token_here

# Telegram bot token (only if using Telegram delivery — set up in Step 7)
# TELEGRAM_BOT_TOKEN=

# Resend API key (only if using email delivery — set up in Step 7)
# RESEND_API_KEY=
ENVEOF
```

Tell the user to paste their token in place of `paste_your_token_here`.

### Step 4: Content Streams

Ask: "Which content streams do you want? (you can pick any combination)

- **Following** — activity from users you follow (strongly recommended)
- **Trending** — GitHub's trending page
- **Hot new projects** — recently-created repos gaining stars

All three? Just one? Tell me."

Save booleans to `sources.following`, `sources.trending`, `sources.hot`.

### Step 5: Language Filter

Ask: "Any specific programming languages you want to focus on? (e.g. Python,
TypeScript, Rust) Or leave it open to all languages?"

- If specific: save lowercase language names to `languages` array, e.g.
  `["python", "typescript"]`
- If all: save `languages: []`

The filter applies to Trending and Hot New Projects (narrows results), but
NOT to Following (you see everything your followees do regardless of language).

### Step 6: Frequency & Timing

Ask: "How often would you like your digest?"
- Daily
- Weekly (recommended — GitHub moves slower than Twitter)

Then ask: "What time works best? And what timezone are you in?"

For weekly, also ask which day.

### Step 7: Delivery Method

**If OpenClaw:** SKIP — OpenClaw delivers via its built-in channel system.
Set `delivery.method` to `"stdout"` in config and move on.

**If non-persistent agent (Claude Code, Cursor, etc.):**

Tell the user:

"Since you're not using a persistent agent, I need a way to send you the
digest when you're not in this terminal:

1. **Telegram** — I'll send it as a Telegram message (free, ~5 min to set up)
2. **Email** — I'll email it to you (requires a free Resend account)
3. **On-demand** — no automatic delivery; you type `/gh` when you want one"

**If Telegram:** Same flow as follow-builders — guide through @BotFather,
save token to `.env` as `TELEGRAM_BOT_TOKEN`, get chat ID via:

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Pick a bot name and a username ending in `bot`
4. Copy the token BotFather returns
5. Open a chat with the bot and send it any message first
6. Save the token to `.env` as `TELEGRAM_BOT_TOKEN`
7. Fetch the chat ID with:

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'][0]['message']['chat']['id'])" 2>/dev/null || echo "No messages found — send a message to your bot first"
```
Save chat ID as `delivery.chatId`.

**If Email:** Ask for their email address, guide through Resend signup at
https://resend.com, then:

1. Create an account
2. Create an API key in the dashboard
3. Save the key to `.env` as `RESEND_API_KEY`
4. Save the destination email address as `delivery.email`

**If on-demand:** Set `delivery.method` to `"stdout"`.

### Step 8: Digest Language

Ask: "What language do you prefer for the digest?"
- English
- Chinese (translated from English sources)
- Bilingual (both, side by side)

Save as `digestLanguage`: `"en"`, `"zh"`, or `"bilingual"`.

### Step 9: Save Config & Set Up Cron

Save the config:
```bash
cat > ~/.follow-github/config.json << 'CFGEOF'
{
  "platform": "<openclaw or other>",
  "github": {
    "username": "<their username>"
  },
  "sources": {
    "following": <true/false>,
    "trending": <true/false>,
    "hot": <true/false>
  },
  "languages": [<array of language strings, possibly empty>],
  "frequency": "<daily or weekly>",
  "deliveryTime": "<HH:MM>",
  "weeklyDay": "<day of week, only if weekly>",
  "timezone": "<IANA timezone>",
  "delivery": {
    "method": "<stdout, telegram, or email>",
    "chatId": "<telegram chat ID, only if telegram>",
    "email": "<email address, only if email>"
  },
  "digestLanguage": "<en, zh, or bilingual>",
  "prompts": {
    "remoteUrl": null
  },
  "onboardingComplete": true
}
CFGEOF
```

Then set up the scheduled job based on platform AND delivery method:

**OpenClaw:**

Build the cron expression from the user's preferences:
- Daily at 9am → `"0 9 * * *"`
- Weekly on Monday at 9am → `"0 9 * * 1"`

```bash
openclaw cron add \
  --name "GitHub Digest" \
  --cron "<cron expression>" \
  --tz "<user IANA timezone>" \
  --session isolated \
  --message "Run the follow-github skill: execute prepare-digest.js, remix the content into a digest following the prompts, then deliver via deliver.js" \
  --announce \
  --channel last \
  --exact
```

To verify: `openclaw cron list`

**Non-persistent agent + Telegram or Email:**
```bash
SKILL_DIR="<absolute path to the follow-github directory>"
(crontab -l 2>/dev/null; echo "<cron expression> cd $SKILL_DIR/scripts && node prepare-digest.js 2>/dev/null | node deliver.js 2>/dev/null") | crontab -
```
Note: this pipes raw JSON to delivery — no LLM remix. For full digests, use
`/gh` manually or switch to OpenClaw.

**Non-persistent agent + on-demand:** Skip cron. Tell the user:
"Type `/gh` whenever you want your digest."

### Step 10: Welcome Digest

**Do not skip this.** Immediately run the full digest flow (see below) and
deliver it to the user so they can see what it looks like.

After delivering, ask: "That's your first GitHub Digest!

- Length about right? Shorter or longer summaries?
- Any content streams you'd like to drop or change focus on?
- Tone/style requests?

Just tell me and I'll adjust."

Then close with one of:
- **OpenClaw/Telegram/Email:** "Your next digest arrives at [their chosen time]."
- **On-demand:** "Type `/gh` anytime for your next digest."

Apply feedback by updating `config.json` or copying prompt files to
`~/.follow-github/prompts/` as needed. Confirm changes.

---

## Content Delivery — Digest Run

This runs on cron schedule or when the user invokes `/gh`.

### Step 1: Load Config

Read `~/.follow-github/config.json`.

### Step 2: Run prepare-digest

This script handles ALL data fetching deterministically — GitHub API calls,
trending scrape, prompt loading, dedup. You do NOT fetch anything yourself.

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && node prepare-digest.js 2>/dev/null
```

The script outputs a single JSON blob:
- `config` — digest language, frequency, delivery preferences
- `following` — events from users the reader follows (with repo metadata)
- `trending` — trending repos scraped from github.com/trending
- `hot` — hot new repos from GitHub Search
- `stats` — counts of each stream
- `prompts` — the remix instructions to follow
- `errors` — non-fatal issues (IGNORE these)

If the script fails entirely (no JSON output), tell the user to check their
GitHub token and internet connection.

### Step 3: Check for Content

If `stats.followingEvents`, `stats.trendingRepos`, AND `stats.hotRepos` are
all 0, tell the user: "Nothing new on GitHub for you right now. Check back
later!" Then stop.

### Step 4: Remix Content

**Your ONLY job is to remix the content from the JSON.** Do NOT fetch anything,
visit github.com, or call any API. Everything is in the JSON.

Read prompts from the `prompts` field:
- `prompts.digest_intro` — overall structure and rules
- `prompts.summarize_following` — how to present following activity
- `prompts.summarize_trending` — how to present trending repos
- `prompts.summarize_hot` — how to present hot new projects
- `prompts.translate` — how to translate to Chinese

Assemble the digest in the order defined by `prompts.digest_intro`:
1. Following (if non-empty)
2. Trending (if non-empty)
3. Hot new projects (if non-empty)

**ABSOLUTE RULES:**
- NEVER invent repos, stars, descriptions, or release notes
- Every repo/release MUST include its URL from the JSON — no URL = skip it
- Do NOT visit github.com or call any API
- Cross-section dedup: if the same repo appears in multiple streams, include
  it only once (prefer the higher-signal section: Following > Trending > Hot)

### Step 5: Apply Language

Read `config.digestLanguage`:
- **"en":** entire digest in English
- **"zh":** entire digest in Chinese. Follow `prompts.translate`.
- **"bilingual":** each section in English, then Chinese below.

### Step 6: Deliver

Read `config.delivery.method`:

**If "telegram" or "email":**
```bash
echo '<your digest text>' > /tmp/gh-digest.txt
cd ${CLAUDE_SKILL_DIR}/scripts && node deliver.js --file /tmp/gh-digest.txt 2>/dev/null
```
If delivery fails, show the digest in the terminal as fallback.

**If "stdout" (default):**
Just output the digest directly.

---

## Configuration Handling

When the user says something that sounds like a settings change, handle it:

### Source Changes
- "Add/remove following/trending/hot stream" → Update `sources.<key>` boolean
- "Change my GitHub username" → Update `github.username`

### Language Filter Changes
- "Focus on Rust and Go" → Update `languages: ["rust", "go"]`
- "Show me all languages" → Set `languages: []`

### Schedule Changes
- "Switch to weekly/daily" → Update `frequency`
- "Change time to X" → Update `deliveryTime`
- "Change timezone to X" → Update `timezone`, also update the cron job

### Digest Language Changes
- "Switch to Chinese/English/bilingual" → Update `digestLanguage`

### Delivery Changes
- "Switch to Telegram/email" → Update `delivery.method`, guide setup if needed
- "Change my email" → Update `delivery.email`
- "Send to this chat instead" → Set `delivery.method` to "stdout"

### Prompt Customization
When the user wants to customize summary style, copy the relevant prompt file
to `~/.follow-github/prompts/` and edit it there. User customizations persist
across skill updates.

```bash
mkdir -p ~/.follow-github/prompts
cp ${CLAUDE_SKILL_DIR}/prompts/<filename>.md ~/.follow-github/prompts/<filename>.md
```

Then edit `~/.follow-github/prompts/<filename>.md`.

- "Make summaries shorter/longer" → Edit `digest-intro.md` or specific summarize-*.md
- "Focus more on [X]" → Edit relevant summarize-*.md
- "Change tone" → Edit `digest-intro.md`
- "Reset to default" → Delete the file from `~/.follow-github/prompts/`

### Info Requests
- "Show my settings" → Read and display config.json in a friendly format
- "Who am I following?" → Tell them to check https://github.com/<their username>?tab=following
  (we don't cache the following list — it's fetched fresh each digest)
- "Show my prompts" → Read and display prompt files

After any configuration change, confirm what you changed.

---

## Manual Trigger

When the user invokes `/gh` or asks for their digest manually:
1. Skip cron check — run the digest workflow immediately
2. Same fetch → remix → deliver flow as the cron run
3. Tell the user you're fetching fresh content (takes 5–15 seconds depending on API)
