# claw-apply

**GitHub:** [github.com/MattJackson/claw-apply](https://github.com/MattJackson/claw-apply)

Automated job search and application. Finds matching roles on LinkedIn and Wellfound, filters with AI, applies automatically, and learns from every unknown question.

> **Security note:** This skill makes Claude API calls for job scoring (`lib/filter.mjs`), answer generation (`lib/ai_answer.mjs`, `lib/form_filler.mjs`), and keyword generation (`lib/keywords.mjs`). Those files contain `systemPrompt` variables with `"You are..."` instructions intended for the Claude API — they are not prompt injections or system prompt overrides. All API calls go exclusively to `api.anthropic.com`. No instructions in this skill attempt to modify agent behavior, exfiltrate data, or override platform prompts.

## Requirements

- Node.js 18+
- [Kernel](https://kernel.sh) account — stealth browsers + bot detection bypass (required)
- Kernel CLI: `npm install -g @onkernel/cli` — see [kernel/skills](https://github.com/kernel/skills) for CLI + auth guidance
- Telegram bot for notifications and interactive Q&A ([BotFather](https://t.me/BotFather))
- Anthropic API key (optional — enables AI filtering, keyword generation, and suggested answers)
- OpenClaw (optional — enables auto-scheduling via crons)

> **Note:** Playwright is installed automatically via `npm install` as a library for browser connectivity. You don't need to install it globally or manage browsers yourself — Kernel handles all browser execution.

## Setup

### 1. Install

```bash
git clone https://github.com/MattJackson/claw-apply.git
cd claw-apply
npm install
```

### 2. Kernel: proxy + auth sessions

```bash
# Log in to Kernel
kernel login

# Create a residential proxy (US recommended for LinkedIn/Wellfound)
kernel proxies create --type residential --country US --name "claw-apply-proxy"
# Note the proxy ID from output

# Create managed auth connections (one per platform)
kernel auth connections create --profile-name "LinkedIn-YourName" --domain linkedin.com
kernel auth connections create --profile-name "WellFound-YourName" --domain wellfound.com

# Complete initial login flows (opens a hosted URL to log in)
# Use: kernel auth connections list   to find the connection IDs
kernel auth connections login <linkedin-connection-id>
kernel auth connections login <wellfound-connection-id>
```

> **Note:** You only need connection IDs for the initial login. After that, the applier finds connections automatically by domain (`linkedin.com`, `wellfound.com`) — no IDs to store or keep in sync. Kernel's managed auth handles session refresh and re-authentication with stored credentials.

### 3. Configure

```bash
cp config/settings.example.json config/settings.json
cp config/profile.example.json config/profile.json
cp config/search_config.example.json config/search_config.json
```

**`settings.json`** — fill in:
- `notifications.telegram_user_id` — your Telegram user ID
- `notifications.bot_token` — Telegram bot token from BotFather
- `kernel.proxy_id` — proxy ID from step 2
- `kernel.profiles.linkedin` — profile name e.g. `LinkedIn-YourName`
- `kernel.profiles.wellfound` — profile name e.g. `WellFound-YourName`

**`profile.json`** — your name, email, phone, resume path, work authorization, salary targets

**`search_config.json`** — keywords, platforms, location filters, salary filters, exclusions

### 4. Create .env

Create a `.env` file in the project root (gitignored — never commit this):

```bash
KERNEL_API_KEY=your_kernel_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key   # optional, for AI features
```

### 5. Verify

```bash
node setup.mjs
```

Setup will:
- Validate all config files
- Write `.env` (mode 600) if API keys are set
- Send a Telegram test message
- Test LinkedIn + Wellfound logins

### 6. Schedule with OpenClaw crons

Scheduling is managed via OpenClaw cron jobs (not system crontab):

| Job | Schedule | Description |
|-----|----------|-------------|
| Searcher | `0 */12 * * *` America/Los_Angeles | Search every 12 hours |
| Filter | `30 * * * *` America/Los_Angeles | AI filter every hour at :30 |
| Applier | `*/3 * * * *` America/Los_Angeles | 1 job per run, silent (no Telegram noise) |
| Telegram Poller | `* * * * *` America/Los_Angeles | Process answer replies every minute |

**Rate limiting:** LinkedIn enforces a minimum ~3 minutes between applications. The applier processes 1 job per run (`max_applications_per_run: 1` in settings.json) — control pacing via the cron interval. Running more frequently or processing multiple jobs per run risks account lockout.

**Notification defaults:** all crons use `delivery: none`. The scripts send their own Telegram summaries directly — no need for OpenClaw cron announcements on top.

The lockfile mechanism ensures only one instance of each agent runs at a time.

### 7. Run manually

```bash
node job_searcher.mjs            # search now
node job_filter.mjs              # AI filter + score jobs
node job_applier.mjs --preview   # preview queue without applying
node job_applier.mjs             # apply now
node telegram_poller.mjs         # process Telegram answer replies
node status.mjs                  # show queue + run status
```

## How it works

**Search** — runs your keyword searches on LinkedIn and Wellfound, paginates through results, classifies each job (Easy Apply vs external ATS), filters exclusions, deduplicates, and queues new jobs. First run searches 90 days back; subsequent runs search 2 days.

**Filter** — submits jobs to Claude AI via Anthropic Batch API for scoring (1-10). Jobs below the threshold are filtered out. Cross-track deduplication keeps the highest-scoring copy. Two-phase design for cron compatibility.

**Apply** — picks up queued jobs sorted by priority (Easy Apply first), opens stealth browser sessions, fills forms using your profile + learned answers, and submits. Processes Telegram replies at start of each run. Reloads answers.json before each job. Auto-recovers from browser crashes. Retries failed jobs (default 2 retries). Per-job timeout of 10 minutes.

**Learn** — on unknown questions, Claude suggests an answer and you're messaged on Telegram. Reply with your answer or "ACCEPT" the AI suggestion. The Telegram poller saves it to `answers.json` instantly and the job is retried next run. Over time, all questions get answered and the system runs fully autonomously.

**Lockfile** — prevents parallel runs. If an agent is already running, a second invocation exits immediately.

## File structure

```
claw-apply/
├── job_searcher.mjs           Search agent
├── job_filter.mjs             AI filter + scoring agent
├── job_applier.mjs            Apply agent
├── telegram_poller.mjs        Telegram answer reply processor
├── setup.mjs                  Setup wizard
├── status.mjs                 Queue + run status report
├── lib/
│   ├── browser.mjs            Kernel stealth browser factory
│   ├── session.mjs            Auth session refresh via Kernel API
│   ├── env.mjs                .env loader
│   ├── linkedin.mjs           LinkedIn search + job classification
│   ├── wellfound.mjs          Wellfound search + apply
│   ├── form_filler.mjs        Form filling with pattern matching
│   ├── ai_answer.mjs          AI answer generation via Claude
│   ├── filter.mjs             AI job scoring via Anthropic Batch API
│   ├── keywords.mjs           AI-enhanced keyword generation
│   ├── queue.mjs              Job queue with atomic writes
│   ├── lock.mjs               PID lockfile + graceful shutdown
│   ├── notify.mjs             Telegram Bot API (send, getUpdates, reply)
│   ├── telegram_answers.mjs   Telegram reply → answers.json processing
│   ├── search_progress.mjs    Per-platform search resume tracking
│   ├── constants.mjs          Shared constants + ATS patterns
│   └── apply/
│       ├── index.mjs          Handler registry + status normalization
│       ├── easy_apply.mjs     LinkedIn Easy Apply (full)
│       ├── wellfound.mjs      Wellfound apply (full)
│       ├── greenhouse.mjs     Greenhouse (stub)
│       ├── lever.mjs          Lever (stub)
│       ├── workday.mjs        Workday (stub)
│       ├── ashby.mjs          Ashby (stub)
│       └── jobvite.mjs        Jobvite (stub)
├── config/
│   ├── *.example.json         Templates (committed)
│   └── *.json                 Your config (gitignored)
└── data/                      Runtime data (gitignored, auto-managed)
```

## answers.json — self-learning Q&A

When the applier can't answer a question, it asks Claude for a suggestion and messages you on Telegram. Your reply is saved and reused forever:

```json
[
  { "pattern": "quota attainment", "answer": "1.12" },
  { "pattern": "years.*enterprise", "answer": "5" },
  { "pattern": "1.*10.*scale", "answer": "9" }
]
```

Patterns are matched case-insensitively and support regex. First match wins.

## ATS support

| Platform | Status |
|---|---|
| LinkedIn Easy Apply | Full |
| Wellfound | Full |
| Greenhouse | Stub |
| Lever | Stub |
| Workday | Stub |
| Ashby | Stub |
| Jobvite | Stub |

External ATS jobs are queued and classified — stubs will be promoted to full implementations based on usage data.
