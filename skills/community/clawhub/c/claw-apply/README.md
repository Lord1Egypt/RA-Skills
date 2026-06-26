# claw-apply

Automated job search and application engine for LinkedIn and Wellfound. Searches for matching roles, applies automatically, and learns from every unknown question it encounters.

Built for [OpenClaw](https://openclaw.dev) but runs standalone with Node.js.

## What it does

- **Searches** LinkedIn and Wellfound on a schedule with your configured keywords and filters
- **Filters** jobs using Claude AI batch scoring — only applies to roles that match your profile
- **Applies** to matching jobs automatically via LinkedIn Easy Apply and Wellfound's native flow
- **Learns** — when it hits a question it can't answer, it asks Claude for a suggestion, messages you on Telegram, and saves your reply for all future jobs
- **Deduplicates** across runs and search tracks so you never apply to the same job twice
- **Retries** failed applications up to a configurable number of times before giving up
- **Recovers** from browser crashes, session timeouts, and network errors automatically

## Quick start

```bash
git clone https://github.com/MattJackson/claw-apply.git
cd claw-apply
npm install
```

### 1. Configure

Copy the example configs and fill in your values:

```bash
cp config/settings.example.json config/settings.json
cp config/profile.example.json config/profile.json
cp config/search_config.example.json config/search_config.json
```

| File | What to fill in |
|------|----------------|
| `profile.json` | Name, email, phone, resume path, work authorization, salary |
| `search_config.json` | Job titles, keywords, platforms, filters, exclusions |
| `settings.json` | Telegram bot token + user ID, Kernel profiles, proxy ID |

### 2. Set up Kernel (stealth browsers)

claw-apply uses [Kernel](https://kernel.sh) for stealth browser sessions that bypass bot detection.

```bash
npm install -g @onkernel/cli
kernel login

# Create a residential proxy
kernel proxies create --type residential --country US --name "claw-apply-proxy"

# Create authenticated browser profiles
kernel auth connections create --profile-name "LinkedIn-YourName" --domain linkedin.com
kernel auth connections create --profile-name "WellFound-YourName" --domain wellfound.com

# Complete initial login flows (use: kernel auth connections list  to find IDs)
kernel auth connections login <linkedin-connection-id>
kernel auth connections login <wellfound-connection-id>
```

Add the profile names and proxy ID to `config/settings.json`. Connection IDs are not needed — the applier finds them automatically by domain.

### 3. Set up Telegram notifications

1. Message [@BotFather](https://t.me/BotFather) on Telegram to create a bot
2. Copy the bot token to `settings.json` -> `notifications.bot_token`
3. Message [@userinfobot](https://t.me/userinfobot) to get your user ID
4. Add it to `settings.json` -> `notifications.telegram_user_id`

### 4. Create .env

```bash
echo "KERNEL_API_KEY=your_kernel_api_key" > .env
echo "ANTHROPIC_API_KEY=your_anthropic_api_key" >> .env
```

The `.env` file is gitignored. `ANTHROPIC_API_KEY` is optional but enables AI keyword generation and AI-suggested answers.

### 5. Verify setup

```bash
node setup.mjs
```

Validates config, tests logins, and sends a test Telegram message.

### 6. Run

```bash
node job_searcher.mjs            # search now
node job_filter.mjs              # AI filter + score jobs
node job_applier.mjs --preview   # preview queue without applying
node job_applier.mjs             # apply now
node telegram_poller.mjs         # process Telegram answer replies
node status.mjs                  # show queue + run status
```

### 7. Schedule (OpenClaw crons)

Scheduling is managed via OpenClaw cron jobs:

| Job | Schedule | Description |
|-----|----------|-------------|
| Searcher | `0 */12 * * *` | Search every 12 hours |
| Filter | `30 * * * *` | AI filter every hour at :30 |
| Applier | disabled by default | Enable when ready |
| Telegram Poller | `* * * * *` | Process answer replies every minute |

The lockfile mechanism ensures only one instance of each agent runs at a time.

## How it works

### Search flow

1. Runs your configured keyword searches on LinkedIn and Wellfound
2. Paginates through results (LinkedIn) and infinite-scrolls (Wellfound)
3. Classifies each job: Easy Apply, external ATS (Greenhouse, Lever, etc.), or recruiter-only
4. Filters out excluded keywords and companies
5. Deduplicates against the existing queue by job ID and URL
6. Saves new jobs to `data/jobs_queue.json` with status `new`
7. Sends a Telegram summary

### Filter flow

1. Submits jobs to Claude AI via Anthropic Batch API (50% cost savings)
2. Scores each job 1-10 based on match to your profile and search track
3. Jobs below the minimum score (default 5) are marked `filtered`
4. Cross-track deduplication keeps the highest-scoring copy
5. Two-phase design: submit batch → collect results (designed for cron)

### Apply flow

1. Processes Telegram replies first — saves new answers, flips answered jobs back to `new`
2. Picks up all `new` and `needs_answer` jobs, sorted by priority (Easy Apply first)
3. Reloads `answers.json` before each job (picks up Telegram replies mid-run)
4. Opens a stealth browser session per platform (LinkedIn, Wellfound, external)
5. For each job:
   - **LinkedIn Easy Apply**: navigates to job, clicks Easy Apply, fills the multi-step modal (Next → Review → Submit), handles post-submit confirmation dialogs
   - **Wellfound**: navigates to job, clicks Apply, fills the form, submits
   - Detects and skips recruiter-only listings, external ATS jobs, and honeypot questions
   - Selects resume from previously uploaded resumes (radio buttons) or uploads via file input
6. On unknown required fields: asks Claude for a suggested answer, messages you on Telegram with the question + AI suggestion, moves on
7. Failed jobs are retried on the next run (up to `max_retries`, default 2)
8. Browser crash recovery: detects dead sessions and creates fresh browsers automatically
9. Sends a summary with counts: applied, failed, needs answer, skipped

### Self-learning answers

When the applier encounters a form question it doesn't know how to answer:

1. Claude generates a suggested answer based on your profile and resume
2. Telegram message sent with the question, options (if select), and AI suggestion
3. You reply with your answer, or reply "ACCEPT" to use the AI suggestion
4. The Telegram poller (cron, every minute) saves your answer to `answers.json` and flips the job back to `new`
5. Next applier run retries the job with the saved answer
6. **Every future job** with the same question is answered automatically

Over time, all common questions get answered and the applier runs fully autonomously.

Patterns support regex:

```json
[
  { "pattern": "quota attainment", "answer": "1.12" },
  { "pattern": "years.*enterprise", "answer": "5" },
  { "pattern": "1.*10.*scale", "answer": "9" }
]
```

## Configuration

### Settings

| Key | Default | Description |
|-----|---------|-------------|
| `max_applications_per_run` | no limit | Cap applications per run |
| `max_retries` | `2` | Times to retry a failed application |
| `enabled_apply_types` | `["easy_apply"]` | Which apply types to process |
| `browser.provider` | `"kernel"` | `"kernel"` for stealth browsers, `"local"` for local Playwright |

### Search filters

| Filter | Type | Description |
|--------|------|-------------|
| `remote` | boolean | Remote jobs only |
| `posted_within_days` | number | Only jobs posted within N days |
| `easy_apply_only` | boolean | LinkedIn Easy Apply only |
| `exclude_keywords` | string[] | Skip jobs with these words in title or company |
| `first_run_days` | number | On first run, look back N days (default 90) |

## Project structure

```
claw-apply/
├── job_searcher.mjs           Search agent
├── job_filter.mjs             AI filter + scoring agent
├── job_applier.mjs            Apply agent
├── telegram_poller.mjs        Telegram answer reply processor
├── setup.mjs                  Setup wizard
├── status.mjs                 Queue status report
├── lib/
│   ├── constants.mjs          Shared constants and defaults
│   ├── browser.mjs            Kernel/Playwright browser factory
│   ├── session.mjs            Kernel Managed Auth session refresh
│   ├── env.mjs                .env loader (no dotenv dependency)
│   ├── form_filler.mjs        Form filling with pattern matching
│   ├── ai_answer.mjs          AI answer generation via Claude
│   ├── filter.mjs             AI job scoring via Anthropic Batch API
│   ├── keywords.mjs           AI-generated search keywords
│   ├── linkedin.mjs           LinkedIn search + job classification
│   ├── wellfound.mjs          Wellfound search
│   ├── queue.mjs              Job queue with atomic writes
│   ├── lock.mjs               PID-based process lock
│   ├── notify.mjs             Telegram Bot API (send, getUpdates, reply)
│   ├── search_progress.mjs    Per-platform search resume tracking
│   ├── telegram_answers.mjs   Telegram reply → answers.json processing
│   └── apply/
│       ├── index.mjs          Apply handler registry + status normalization
│       ├── easy_apply.mjs     LinkedIn Easy Apply (multi-step modal)
│       ├── wellfound.mjs      Wellfound apply
│       ├── greenhouse.mjs     Greenhouse ATS (stub)
│       ├── lever.mjs          Lever ATS (stub)
│       ├── workday.mjs        Workday ATS (stub)
│       ├── ashby.mjs          Ashby ATS (stub)
│       └── jobvite.mjs        Jobvite ATS (stub)
├── config/
│   ├── *.example.json         Templates (committed)
│   ├── profile.json           Your info (gitignored)
│   ├── search_config.json     Your searches (gitignored)
│   ├── answers.json           Learned answers (gitignored)
│   └── settings.json          Your settings (gitignored)
└── data/
    ├── jobs_queue.json         Job queue (auto-managed)
    ├── applications_log.json   Application history (auto-managed)
    └── telegram_offset.json    Telegram polling offset (auto-managed)
```

## Job statuses

| Status | Meaning |
|--------|---------|
| `new` | Found, waiting to apply |
| `applied` | Successfully submitted |
| `needs_answer` | Blocked on unknown question, waiting for your reply |
| `failed` | Failed after max retries |
| `already_applied` | Duplicate detected, previously applied |
| `filtered` | Below AI score threshold |
| `duplicate` | Cross-track duplicate (lower-scoring copy) |
| `skipped_honeypot` | Honeypot question detected |
| `skipped_recruiter_only` | LinkedIn recruiter-only listing |
| `skipped_external_unsupported` | External ATS (Greenhouse, Lever, etc.) |
| `skipped_easy_apply_unsupported` | LinkedIn job without Easy Apply button |
| `skipped_no_apply` | No apply button found on page |
| `no_modal` | Easy Apply button found but modal didn't open |
| `stuck` | Modal progress stalled after repeated clicks |
| `incomplete` | Modal flow didn't reach submit |

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

## Roadmap

- [x] LinkedIn Easy Apply (multi-step modal)
- [x] Wellfound apply
- [x] Kernel stealth browsers + residential proxy
- [x] AI job filtering via Anthropic Batch API
- [x] Self-learning answer bank with Telegram Q&A loop
- [x] AI-suggested answers via Claude
- [x] Telegram answer polling (instant save + applier safety net)
- [x] Browser crash recovery
- [x] Retry logic with configurable max retries
- [x] Preview mode (`--preview`)
- [x] Configurable application caps and retry limits
- [ ] External ATS support (Greenhouse, Lever, Workday, Ashby, Jobvite)
- [ ] Per-job cover letter generation via LLM
- [ ] Indeed support

## License

[AGPL-3.0-or-later](LICENSE)
