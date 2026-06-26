# 🤖 Auto Job Applier — OpenClaw Skill

> Automatically find jobs matching your resume and apply to them with a single command —
> powered by your **resumex.dev** resume data and **OpenClaw's built-in AI**.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-6366f1?style=flat-square)](https://openclaw.dev)
[![ResumeX API](https://img.shields.io/badge/ResumeX-API-10b981?style=flat-square)](https://resumex.dev)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776ab?style=flat-square)](https://python.org)
[![No Third-Party AI](https://img.shields.io/badge/AI-OpenClaw%20Built--in%20Only-f59e0b?style=flat-square)](#no-third-party-ai-apis)

---

## What This Skill Does

| Step | What Happens |
|---|---|
| 1️⃣ | Fetches your full resume from **resumex.dev** via API |
| 2️⃣ | Loads your saved preferences (salary, visa, notice period) |
| 3️⃣ | Builds a job-match profile from your skills, experience, and location |
| 4️⃣ | Runs targeted web searches across LinkedIn, Naukri, Indeed, Wellfound, and more |
| 5️⃣ | Scores and ranks each job 0–100 against your profile |
| 6️⃣ | **⛔ Presents an approval list — waits for you to select which jobs to apply to** |
| 7️⃣ | Auto-fills application forms, generates cover letters, handles screening questions |
| 8️⃣ | Logs every application to your resumex.dev job tracker |

> **You are always in control.** The agent never submits a single application without your
> explicit approval in Step 6. This is enforced in the workflow and cannot be bypassed.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **OpenClaw account** | Install this skill from the OpenClaw skill registry |
| **resumex.dev account** | Free account at [resumex.dev](https://resumex.dev) |
| **Resume published** | At least one resume must be saved and active in resumex.dev |
| **`RESUMEX_API_KEY`** | Generated from resumex.dev → Dashboard → Resumex API |
| **Python 3.8+** | Already available on most systems (`python3 --version`) |
| **`requests` library** | `pip3 install -r requirements.txt` or `pip3 install requests` |
| **`curl`** | Used for direct API calls (`curl --version`) |

---

## Setup (3 Steps)

### Step 1 — Get Your ResumeX API Key

1. Go to **[resumex.dev](https://resumex.dev)** and log in
2. Navigate to **Dashboard → Resumex API**
3. Click **Generate API Key**
4. Copy the key (it starts with `rx_...`)

### Step 2 — Add the Key to OpenClaw

1. In OpenClaw, open **Settings → Environment Variables**
2. Click **Add Variable**
3. Name: `RESUMEX_API_KEY`
4. Value: paste your key from Step 1
5. Save

> ⚠️ **Do not share this key.** It grants read access to your resume data and write access
> to your job tracker. Generate a new key from resumex.dev if you believe it was exposed.

### Step 3 — Install This Skill

Install from the OpenClaw skill registry and you're ready to go.

---

## Usage

Just tell OpenClaw in natural language:

```
"Find me software engineer jobs in Pune and apply to the best matches"
"Search for remote Python developer jobs and auto-apply to the top 5"
"Find backend developer jobs and help me apply"
"Auto-apply to jobs matching my resume"
```

The skill activates automatically when you use words like:
`apply to jobs`, `job search`, `find jobs for me`, `auto apply`, `job hunting`, `find matching jobs`

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `RESUMEX_API_KEY` | ✅ **Required** | — | API key from resumex.dev → Dashboard → Resumex API |
| `JOB_SEARCH_LOCATION` | Optional | From resume | Override city/country, e.g. `"Pune, India"` |
| `JOB_TYPE` | Optional | `full-time` | `full-time` \| `part-time` \| `contract` \| `internship` |
| `REMOTE_ONLY` | Optional | `false` | Set `true` to only search remote jobs |
| `MAX_APPLICATIONS` | Optional | `5` | Maximum jobs to apply to per session |

> **No other API keys are needed.** There is no Anthropic key, no OpenAI key, no third-party
> AI service. All AI tasks (cover letters, screening answers) use OpenClaw's built-in LLM.

---

## No Third-Party AI APIs

This skill is designed to work **exclusively with OpenClaw's built-in AI**. Specifically:

| Task | How It's Done |
|---|---|
| Cover letter generation | `draft_cover_letter.py` builds a prompt → OpenClaw's LLM generates the letter |
| Screening question answers | OpenClaw's LLM generates answers from your resume context |
| Job scoring and ranking | Deterministic algorithm in `search_jobs.py` (no AI needed) |
| Form field mapping | Rule-based matching in `fill_application.py` (no AI needed) |

**Previous versions of this skill incorrectly called Anthropic's API** (`claude-sonnet-4-20250514`).
This has been completely removed. You do not need an Anthropic API key.

---

## Privacy & Data Policy

### Data sent to external services

| What | Where | Why |
|---|---|---|
| Resume read (name, email, skills, experience) | resumex.dev | To fetch your resume for matching |
| Application logs (company, role, URL, status) | resumex.dev | To track your applications |
| Name, email, phone, LinkedIn, cover letter | Job application websites | To fill and submit applications |

Data sent to resumex.dev is governed by the **[resumex.dev Privacy Policy](https://resumex.dev/privacy)**.

### Data stored locally only

| File | Location | Contents |
|---|---|---|
| `data/user_preferences.json` | Local skill directory | Salary expectation, visa status, notice period, address, and optionally: gender, DOB, ethnicity, veteran/disability status, screening answers |

> ⚠️ **`data/user_preferences.json` stays on your machine.** It is never uploaded to resumex.dev
> or any other server. It may contain sensitive fields if you choose to save them.

### Sensitive fields in preferences

These fields are **only saved** if a job application form explicitly requires them and you choose
to provide the value. You can always decline or skip:

| Field | When Asked | Can Decline? |
|---|---|---|
| `gender` | Diversity/EEO forms only | ✅ Yes — leave blank |
| `ethnicity` | Diversity/EEO forms only | ✅ Yes — leave blank |
| `veteran_status` | U.S. compliance forms only | ✅ Yes |
| `disability_status` | Compliance forms only | ✅ Yes |
| `date_of_birth` | Forms that legally require it | ✅ Yes |

The agent will always tell you **which company's form** is asking before prompting you.

### Securing the preferences file

```bash
# Restrict file permissions so only you can read it
chmod 600 data/user_preferences.json

# View all saved preferences
python3 scripts/manage_preferences.py list

# Delete a specific preference
python3 scripts/manage_preferences.py delete gender

# Clear everything and start fresh
python3 scripts/manage_preferences.py reset
```

---

## Scripts Reference

All scripts are located in the `scripts/` directory and require `python3`.

### `fetch_resume.py` — Fetch Resume Data

```bash
# Print full resume JSON
python3 scripts/fetch_resume.py

# Extract a specific field
python3 scripts/fetch_resume.py --field email
python3 scripts/fetch_resume.py --field phone
python3 scripts/fetch_resume.py --field current_company

# Extract by JSON path
python3 scripts/fetch_resume.py --json-path profile.fullName
python3 scripts/fetch_resume.py --json-path experience[0].role

# Save resume to a file
python3 scripts/fetch_resume.py --save /tmp/resume.json
```

**Requires:** `RESUMEX_API_KEY` env var

---

### `search_jobs.py` — Job Search Utilities

```bash
# Generate search queries from a profile
python3 scripts/search_jobs.py generate-queries \
  --roles "Software Engineer,Backend Developer" \
  --skills "Python,Django,React,PostgreSQL" \
  --location "Pune, India" \
  --seniority "mid" \
  --job-type "full-time"

# Parse a raw job posting into structured JSON
python3 scripts/search_jobs.py parse-job \
  --url "https://example.com/job/123" \
  --title "Software Engineer" \
  --company "Acme Corp" \
  --raw-text "We are looking for a Software Engineer..."

# Score a job against a profile
python3 scripts/search_jobs.py score \
  --profile '{"roles":["Software Engineer"],"skills":["Python","Django"],"seniority":"mid-level","location":"Pune, India"}' \
  --job '{"title":"Software Engineer","required_skills":["Python"],"location":"Pune"}'
```

---

### `fill_application.py` — Form Field Mapping

```bash
# Map form fields to resume values
python3 scripts/fill_application.py map-fields \
  --resume /tmp/resume.json \
  --prefs data/user_preferences.json \
  --fields '[{"label":"First Name","type":"text"},{"label":"Email","type":"email"},{"label":"Salary Expectation","type":"text"}]'

# Get value for a single field
python3 scripts/fill_application.py get-value \
  --resume /tmp/resume.json \
  --field-label "Email Address"

# Check what percentage of form fields can be auto-filled
python3 scripts/fill_application.py check-coverage \
  --resume /tmp/resume.json \
  --prefs data/user_preferences.json \
  --fields '[{"label":"First Name"},{"label":"Email"},{"label":"Gender"},{"label":"Salary"}]'
```

---

### `draft_cover_letter.py` — Cover Letter Prompt Generator

> **No Anthropic or third-party AI key needed.** This script generates a prompt.
> OpenClaw's built-in LLM produces the actual cover letter.

```bash
python3 scripts/draft_cover_letter.py \
  --resume /tmp/resume.json \
  --job_title "Software Engineer" \
  --company "Acme Corp" \
  --job_description "We are looking for a skilled engineer..." \
  --output /tmp/cover_letter_acme.txt
```

The script prints a structured prompt to stdout. The OpenClaw agent feeds this to its
built-in LLM and saves the result to `--output` if specified.

---

### `manage_preferences.py` — User Preferences

```bash
# List all saved preferences
python3 scripts/manage_preferences.py list

# Get a specific value
python3 scripts/manage_preferences.py get salary_expectation

# Set preferences
python3 scripts/manage_preferences.py set salary_expectation "8-12 LPA"
python3 scripts/manage_preferences.py set notice_period "30 days"
python3 scripts/manage_preferences.py set willing_to_relocate true
python3 scripts/manage_preferences.py set visa_status "Indian citizen, no sponsorship needed"

# Save screening question answers
python3 scripts/manage_preferences.py set-screening "authorized_to_work_india" "Yes"
python3 scripts/manage_preferences.py set-screening "require_sponsorship" "No"

# Find a screening answer by fuzzy question text
python3 scripts/manage_preferences.py find-screening "Are you authorized to work"

# Delete a preference
python3 scripts/manage_preferences.py delete gender

# View all known preference keys
python3 scripts/manage_preferences.py known-keys

# Clear everything
python3 scripts/manage_preferences.py reset
```

---

### `log_application.py` — Log to ResumeX Tracker

```bash
python3 scripts/log_application.py \
  --company "Acme Corp" \
  --role "Software Engineer" \
  --url "https://careers.acme.com/apply/12345" \
  --status "applied" \
  --method "auto-applied" \
  --score 92 \
  --notes "Applied via auto-job-applier skill"

# Test without calling the API
python3 scripts/log_application.py \
  --company "Test" --role "Test" --url "https://example.com" --dry-run
```

Valid `--status` values: `wishlist` | `applied` | `interview` | `offer` | `rejected`
Valid `--method` values: `auto-applied` | `manual` | `easy-apply` | `email`

The script automatically retries on transient errors and tries fallback endpoints
if the primary job logging endpoint returns 404.

**Requires:** `RESUMEX_API_KEY` env var

---

## Job Boards Supported

| Board | Search Method | Auto-Apply? | Notes |
|---|---|---|---|
| LinkedIn | Web search | 🔗 Manual only | ToS concerns; agent opens page, you submit |
| Naukri | Web search + form | ✅ Auto | Standard form fill |
| Indeed | Web search + form | ✅ Auto | Standard form fill |
| Wellfound | Web search + form | ✅ Auto | Standard form fill |
| Internshala | Web search + form | ✅ Auto | Good for Indian market |
| Glassdoor | Web search | 🔗 Manual (redirect) | Redirects to company ATS |
| Company career pages | Web search + form | ✅ Auto | Direct application forms |

See `references/job_boards.md` for detailed search query patterns.

---

## Safety Defaults

| Safety Feature | Default Behavior |
|---|---|
| Approval gate | **Always shown** before any application is submitted |
| LinkedIn Easy Apply | **Disabled by default** (ToS risk) — enable explicitly if desired |
| File uploads | **Never automated** — flagged for manual upload |
| CAPTCHA | **Skips automatically** — marks job as "manual apply" |
| Max applications | Default `5` per session — configurable via `MAX_APPLICATIONS` |
| Resume fetch | **Once per session** — not cached across sessions |

---

## Testing Safely

Before using for real applications, test with dummy data:

```bash
# 1. Check that your API key works
python3 scripts/fetch_resume.py 2>&1 | head -5

# 2. Generate search queries (no network calls)
python3 scripts/search_jobs.py generate-queries \
  --roles "Software Engineer" \
  --skills "Python,React" \
  --location "Pune, India"

# 3. Test field mapping with a sample resume
python3 scripts/fetch_resume.py --save /tmp/my_resume.json
python3 scripts/fill_application.py check-coverage \
  --resume /tmp/my_resume.json \
  --fields '[{"label":"First Name"},{"label":"Email"},{"label":"Salary Expectation"}]'

# 4. Set MAX_APPLICATIONS=1 for your first real run
# In OpenClaw environment variables: MAX_APPLICATIONS = 1
```

---

## Troubleshooting

### `RESUMEX_API_KEY` errors

```
ERROR: RESUMEX_API_KEY environment variable is not set.
```
→ Go to OpenClaw **Settings → Environment Variables** and add `RESUMEX_API_KEY`.

```
ERROR: 401 Unauthorized. Your RESUMEX_API_KEY is invalid or expired.
```
→ Regenerate your key at **resumex.dev → Dashboard → Resumex API** and update OpenClaw.

### No jobs found

- Try removing the location filter (`JOB_SEARCH_LOCATION=""`)
- Set `REMOTE_ONLY=true` for remote-only search
- Broaden role titles in your resume (e.g. add "Backend Developer" alongside "Software Engineer")

### Application form issues

| Issue | Resolution |
|---|---|
| CAPTCHA detected | Skill marks job as "manual apply" and skips — open the link yourself |
| Login required | Log into the job board in the browser first, then retry |
| Multi-step form fails | Skill saves a screenshot of the last completed step |
| Submit button not found | Skill takes a screenshot and asks you to review |

---

## File Structure

```
auto-job-applier/
├── SKILL.md                          # Agent instructions (OpenClaw reads this)
├── README.md                         # This file
├── requirements.txt                  # Python dependencies (requests>=2.28.0)
├── scripts/
│   ├── http_client.py               # Shared HTTP client (retry, backoff, errors)
│   ├── fetch_resume.py               # Fetch resume from resumex.dev API
│   ├── search_jobs.py                # Generate queries, parse and score jobs
│   ├── fill_application.py          # Map form fields to resume data
│   ├── manage_preferences.py        # CRUD for user_preferences.json
│   ├── draft_cover_letter.py        # Build cover letter prompt for OpenClaw LLM
│   └── log_application.py           # Log application to resumex.dev tracker
├── references/
│   ├── job_boards.md                 # Job board patterns and selectors
│   ├── form_field_mappings.md        # Form label → resume JSON path mappings
│   └── screening_questions.md        # Common screening questions and strategies
└── data/
    └── user_preferences.json         # Auto-created; local only; never uploaded
```

---

## Changelog

### v2.1.0 (2026-04-14)
- ✅ **Fixed resume fetch endpoint** — corrected from `/api/v1/agent/resume` (deprecated) to `/api/v1/agent`
- ✅ **Fixed job logging 404** — added endpoint fallback (`/jobs` → `/logs`) with clear error messages
- ✅ **Migrated to `requests` library** — replaced all `urllib` with modern session-based HTTP client
- ✅ **Added shared HTTP client** — `scripts/http_client.py` with retry, exponential backoff, `Retry-After` support
- ✅ **Added custom error hierarchy** — `AuthenticationError`, `RateLimitError`, `NotFoundError`, `ServerError`, `NetworkError`
- ✅ **Added `--dry-run` flag** — test `log_application.py` without calling the API
- ✅ **Added `requirements.txt`** — declares `requests>=2.28.0` dependency
- ✅ **Cleaned up dead imports** — removed unused `urllib` imports from `fill_application.py`

### v2.0.0 (2026-04-14)
- ✅ **Removed Anthropic API dependency** — cover letters now generated via OpenClaw's built-in LLM
- ✅ **Fixed metadata** — `RESUMEX_API_KEY` now correctly listed as `required` in skill front-matter
- ✅ **Added Privacy section** — full disclosure of what data goes where
- ✅ **Added sensitive field handling** — agent warns before saving DOB, gender, ethnicity etc.
- ✅ **Strengthened approval gate** — Step 6 explicitly documented as mandatory and non-bypassable
- ✅ **Added README** — this file

### v1.0.0 (2026-04-14)
- Initial release

---

## License

MIT License. See repository root for details.

---

## Links

- **ResumeX:** [resumex.dev](https://resumex.dev)
- **ResumeX API Docs:** [resumex.dev/api-docs](https://resumex.dev/api-docs)
- **OpenClaw:** [openclaw.dev](https://openclaw.dev)
- **ResumeX Privacy Policy:** [resumex.dev/privacy](https://resumex.dev/privacy)
