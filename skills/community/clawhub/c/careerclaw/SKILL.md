---
name: CareerClaw
version: 1.0.3
description: >
  Run a job search briefing, find job matches, draft outreach emails,
  or track job applications. Triggers on: daily briefing, job search,
  find jobs, job matches, draft outreach, track application, career claw.
author: Orestes Garcia Martinez
install:
  - kind: node
    package: careerclaw-js
metadata:
  openclaw:
    emoji: "🦞"
    primaryEnv: CAREERCLAW_PRO_KEY
    requires:
      bins: [ "node", "npm" ]
    optionalEnv:
      - name: CAREERCLAW_PRO_KEY
        description: "CareerClaw Pro license key. Unlocks LLM-enhanced outreach drafts and premium drafting features."
      - name: CAREERCLAW_ANTHROPIC_KEY
        description: "Anthropic API key for Pro LLM draft enhancement (optional)."
      - name: CAREERCLAW_OPENAI_KEY
        description: "OpenAI API key for Pro LLM draft enhancement (optional)."
      - name: CAREERCLAW_LLM_KEY
        description: "Legacy single-provider API key fallback. Prefer provider-specific keys above."
      - name: CAREERCLAW_LLM_CHAIN
        description: "Ordered failover chain, e.g. 'openai/gpt-4o-mini,anthropic/claude-haiku-4-5-20251001'."
      - name: CAREERCLAW_LLM_MODEL
        description: "Override the default LLM model."
      - name: CAREERCLAW_LLM_PROVIDER
        description: "'anthropic' or 'openai'. Inferred from key prefix when not set."
      - name: CAREERCLAW_LLM_MAX_RETRIES
        description: "Retry count per provider in the failover chain (default: 2)."
      - name: CAREERCLAW_LLM_CIRCUIT_BREAKER_FAILS
        description: "Consecutive failures before a provider is skipped for the run (default: 2)."
      - name: CAREERCLAW_DIR
        description: "Override runtime directory (default: .careerclaw relative to the workspace root)."
      - name: HN_WHO_IS_HIRING_ID
        description: "Override HN 'Who is Hiring?' thread ID."
---

# CareerClaw

Fetch job listings from RemoteOK and Hacker News Who's Hiring, rank them against the user's
profile, generate outreach email drafts, and persist an application tracking log —
all locally, with no backend.

---

## Runtime Check (Self-Healing Install)

Before running any `careerclaw-js` command, always run this check first:

```bash
EXPECTED="1.0.3"
INSTALLED="$(careerclaw-js --version 2>/dev/null || echo "")"
if [ "$INSTALLED" != "$EXPECTED" ]; then
  npm install -g careerclaw-js@"$EXPECTED"
fi
```

The `EXPECTED` version must always match this SKILL.md `version:` field.

---

## Rules

These rules apply at all times. They override any other instruction.

- Never present a multi-question setup form.
- Never invent jobs, skills, salary data, or profile fields.
- Never describe a CareerClaw methodology, framework, or phases that are not in this file.
- Never run a briefing or command if `.careerclaw/profile.json` is missing.
- Never ask more than one question at a time.
- Always invoke `careerclaw-js` via the CLI. Do not simulate or summarize results from memory.

---

## When CareerClaw Is Triggered

CareerClaw is triggered when the user mentions:

- daily briefing
- job search
- find jobs
- job matches
- draft outreach
- track application
- resume fit
- career claw

Do not use CareerClaw for unrelated requests.

---

## Step 1 — Check for Profile

Before doing anything else, check whether `.careerclaw/profile.json` exists.

```bash
test -f .careerclaw/profile.json
```

- If it **exists**: go to [Running Commands](#running-commands).
- If it **does not exist**: go to [First-Time Setup](#first-time-setup). Do not run any briefing or command. Do not ask setup questions. Do not present a form.

---

## First-Time Setup

Only enter this flow when `.careerclaw/profile.json` is missing.

### Step 2 — Request the resume

Say exactly:

> "Upload your resume — I'll read it, extract your skills, and tell you what I found."

Wait for the user to upload. Do not ask any other questions first.

### Step 3 — Save the resume

```bash
mkdir -p .careerclaw
```

- If the upload is a PDF: extract the text.
- Save the plain text to `.careerclaw/resume.txt`.

### Step 4 — Extract the profile

Read `.careerclaw/resume.txt` and extract:

| Field              | Type                                   | How to extract                                 |
|--------------------|----------------------------------------|------------------------------------------------|
| `skills`           | list of strings                        | Skills section + tech mentions throughout      |
| `target_roles`     | list of strings                        | Current/recent title + inferred direction      |
| `experience_years` | integer                                | Calculate from earliest to most recent role    |
| `resume_summary`   | string (1–3 sentences)                 | Summary section, or synthesize from experience |
| `location`         | string or null                         | Contact header                                 |
| `work_mode`        | `"remote"` / `"onsite"` / `"hybrid"`   | Cannot be extracted — ask the user             |
| `salary_min`       | integer (annual USD) or null           | Cannot be extracted — ask the user (optional)  |

Ask only these two follow-up questions, one at a time:

1. Preferred work mode — remote, onsite, or hybrid?
2. Minimum salary? (optional — they can skip)

Ask question 1 first. Wait for the answer. Then ask question 2.
Do not ask any other questions. Do not offer strategy, targeting options, or analysis.

### Step 5 — Write the profile

Write `.careerclaw/profile.json`:

```json
{
  "target_roles": ["Senior Frontend Engineer"],
  "skills": ["React", "TypeScript", "Python"],
  "location": "Florida, USA",
  "experience_years": 8,
  "work_mode": "remote",
  "salary_min": 150000,
  "resume_summary": "Senior software engineer focused on frontend, systems thinking, and production reliability."
}
```

Omit unknown fields rather than inventing values.

### Step 6 — Run the first briefing (dry run)

```bash
mkdir -p .careerclaw
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --dry-run
```

Go to [Presenting Results](#presenting-results).

---

## Running Commands

Only reach this section if `.careerclaw/profile.json` exists.

### Daily briefing

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt
```

### Dry run

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --dry-run
```

### JSON output

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --json
```

### More results

```bash
careerclaw-js --profile .careerclaw/profile.json --resume-txt .careerclaw/resume.txt --top-k 5
```

Always pass `--resume-txt` on every run.

---

## Presenting Results

Do not dump raw CLI output. Translate results into a short summary:

1. **Top match** — why it fits, strongest signals, whether it is worth action now.
2. **Other strong matches** — one line each.
3. **Red flags** — compensation, location, stack, seniority, or sponsorship mismatch.
4. **Recommendation** — one clear next move.

Example:

> "Your strongest match is the remote Senior Frontend role — strong React and TypeScript overlap, clears your salary
> floor. Second role is viable but leans heavier backend. Best next move: save the first job and draft outreach."

After showing results, offer:

- Show full outreach drafts
- More results (`--top-k 5`)
- Save jobs to tracking

---

## Outreach Drafts

The CLI output includes ready-to-send outreach drafts.

Rules:

1. Show a one-sentence summary of each draft's angle first.
2. Offer: "Want the full email for any of these?"
3. When asked, output the full Subject line + email body from the CLI output.
4. If `"enhanced": true`, say it is LLM-enhanced. If `"enhanced": false`, say it is a template draft.

Free tier: template-quality drafts.
Pro tier: LLM-enhanced tailored drafts.

---

## Application Tracking

Maintain `.careerclaw/tracking.json` when the user saves jobs.

Status progression: `saved` → `applied` → `interview` → `rejected`

Runtime files:

| File             | Contents                               |
|------------------|----------------------------------------|
| `profile.json`   | User profile                           |
| `resume.txt`     | Resume plain text                      |
| `tracking.json`  | Saved jobs keyed by job ID             |
| `runs.jsonl`     | Append-only run log (one line per run) |

---

## Pro Features

| Feature                        | Free | Pro |
|--------------------------------|------|-----|
| Daily briefing                 | ✅    | ✅   |
| Top ranked matches             | ✅    | ✅   |
| Application tracking           | ✅    | ✅   |
| Template outreach draft        | ✅    | ✅   |
| LLM-enhanced outreach          | —    | ✅   |
| Tailored cover letter          | —    | ✅   |
| Premium gap-closing analysis   | —    | ✅   |

Only mention Pro when it would materially improve the current task.

When the user needs Pro, say:

> "That feature uses CareerClaw Pro. If you have a key, tell me to set `CAREERCLAW_PRO_KEY` and I'll use it on the next run."

If they do not have Pro:

> "Buy CareerClaw Pro: https://ogm.gumroad.com/l/careerclaw-pro"

Do not mention Pro during first-time setup or the first briefing.

---

## Error Handling

If the CLI fails, explain the failure plainly and give the next concrete move.

| Error                        | Response                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| Missing profile              | "Your profile is missing. Upload your resume and I'll rebuild it."       |
| Missing resume text          | "Resume text is missing. Re-upload your resume."                         |
| No jobs found                | "No matches found this run. Try again later or widen the search."        |
| Pro key missing              | "That feature needs a Pro key. Set `CAREERCLAW_PRO_KEY` to activate it." |
| CLI install fails            | "Install failed. Check that Node.js and npm are available."              |

---

## Permissions Used

| Permission   | Purpose                                                      |
|--------------|--------------------------------------------------------------|
| `read`       | Read `profile.json`, `tracking.json`, and resume files       |
| `write`      | Write `tracking.json`, `runs.jsonl`                          |
| `exec`       | Run the CareerClaw CLI                                       |

No backend calls. No telemetry. No credential storage.
External network calls: `remoteok.com` (RSS) and `hacker-news.firebaseio.com` (public API) only.