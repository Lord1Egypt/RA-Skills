---
name: auto-job-applier
description: >
  Automatically find and apply to jobs that match the user's resume using the resumex.dev API,
  web search, and browser automation. Use this skill whenever the user asks to: search for jobs,
  find job matches, auto-apply to jobs, apply for jobs automatically, find jobs based on my resume,
  or any variant of job hunting, job searching, or job application automation. Fetches the user's
  full resume data from resumex.dev, extracts skills/experience/preferences, searches for matching
  jobs on the web, presents an approval list, then automatically fills and submits applications
  using browser control. Logs all applications to the user's resumex.dev job tracker.
  Always use this skill when the user mentions "apply to jobs", "job search", "find jobs for me",
  "auto apply", or "job hunting" — even if they haven't explicitly mentioned resumex.
requires:
  bins: [python3, curl]
  pip: [requests>=2.28.0]
  env:
    required:
      - RESUMEX_API_KEY       # Required. Get from resumex.dev → Dashboard → Resumex API
    optional:
      - JOB_SEARCH_LOCATION   # Default city/country for job search (e.g. "Pune, India")
      - JOB_TYPE              # full-time | part-time | contract | internship (default: full-time)
      - REMOTE_ONLY           # true | false (default: false)
      - MAX_APPLICATIONS      # Max jobs to auto-apply per session (default: 5)
---

# Auto Job Applier Skill

This skill connects to the user's **resumex.dev** account, reads their resume data, matches them
to relevant jobs via web search, presents an approval list, then **automatically applies** to
approved jobs using browser automation — filling forms, answering screening questions, and
submitting applications. All applications are logged to the resumex.dev job tracker.

> **Architecture:** ResumeX stores resume data and the job tracker. **OpenClaw's built-in AI**
> does all the thinking and text generation (cover letters, screening answers, scoring).
> Web search finds jobs. Browser tool fills and submits applications.
> `user_preferences.json` remembers extra info between sessions.

> **No third-party AI API keys required.** This skill uses only OpenClaw's built-in LLM
> for all AI tasks (cover letter drafting, screening question answers, job scoring).
> The only external API key needed is `RESUMEX_API_KEY`.

---

## Required Environment Variable

| Variable | Required | Description |
|---|---|---|
| `RESUMEX_API_KEY` | ✅ **Required** | API key from resumex.dev → Dashboard → Resumex API |
| `JOB_SEARCH_LOCATION` | Optional | Override city/country for job search |
| `JOB_TYPE` | Optional | `full-time` \| `part-time` \| `contract` \| `internship` |
| `REMOTE_ONLY` | Optional | `true` \| `false` (default: `false`) |
| `MAX_APPLICATIONS` | Optional | Max jobs to apply per session (default: `5`) |

**How to set `RESUMEX_API_KEY` in OpenClaw:**
1. Go to **resumex.dev → Dashboard → Resumex API**
2. Click **Generate API Key**
3. In OpenClaw, go to **Settings → Environment Variables**
4. Add `RESUMEX_API_KEY` with the copied key value

**No other keys are needed.** There is no Anthropic key, no OpenAI key, no other third-party service.

---

## Privacy & Data Handling

> **Read this before using the skill.**

### What data leaves your device

| Data | Sent To | Why |
|---|---|---|
| Resume data (API read) | resumex.dev | To fetch your resume for job matching |
| Application logs (company, role, URL, status) | resumex.dev | To track your job applications |
| Your name, email, phone, LinkedIn | Job application websites | To fill application forms |
| Cover letter (generated text) | Job application websites | Submitted as part of each application |

**Data sent to resumex.dev is governed by the [resumex.dev Privacy Policy](https://resumex.dev/privacy).**

### What stays local on your device

| Data | Location | What It Contains |
|---|---|---|
| `data/user_preferences.json` | Skill directory only | Salary expectation, visa status, notice period, address, gender, date of birth, ethnicity, veteran status, disability status, screening question answers |

> ⚠️ **`user_preferences.json` may contain sensitive personal data** including date of birth,
> gender, ethnicity, veteran status, and disability status (only if you choose to save these
> when prompted during a form fill). This file is stored **locally only** and is **never sent
> to resumex.dev or any other server**. Review and restrict its filesystem permissions if needed:
> ```bash
> chmod 600 data/user_preferences.json
> ```
> To clear all saved preferences at any time:
> ```bash
> python3 scripts/manage_preferences.py reset
> ```

### Sensitive fields in preferences

The following fields are only saved if you explicitly provide them when the agent encounters a
form field that requires them. You can decline to answer, skip the field, or delete a saved
value at any time:

- `gender` — only for diversity/EEO forms
- `ethnicity` — only for diversity/EEO forms (optional, you may leave blank)
- `veteran_status` — only for U.S. government/contractor compliance forms
- `disability_status` — only for compliance forms (optional)
- `date_of_birth` — only for forms that legally require it

The agent will always tell you **which form** requires a sensitive field before asking for the value.

### Auto-submit safeguard

**The agent NEVER submits an application without your explicit approval.** Step 6 of the workflow
always presents a formatted approval list and waits for your response before any browser
interaction begins. If you are testing, set `MAX_APPLICATIONS=1` in your environment.

---

## Workflow Overview

```
1. Fetch resume data from resumex.dev API
2. Load saved user preferences (salary, visa, screening answers)
3. Build a job-match profile (skills, roles, seniority, preferences)
4. Search the web for matching jobs (3–5 query permutations)
5. Score & rank each job against the resume (0–100)
6. ⛔ APPROVAL GATE — Present formatted list → wait for user selection
7. For each approved job:
   a. Generate a tailored cover letter (via OpenClaw's built-in AI)
   b. Navigate to application page via browser
   c. Fill form fields using resume data + preferences
   d. If a required field is unknown → ask the user → save to preferences
   e. Submit the application
   f. Log to resumex.dev job tracker
8. Present final summary with statuses
```

---

## Step 1 — Fetch Resume from resumex.dev

Use the agent endpoint. All calls require `Authorization: Bearer $RESUMEX_API_KEY`.

```bash
# Fetch full resume data (GET /api/v1/agent — the correct endpoint)
curl -s -X GET "https://resumex.dev/api/v1/agent" \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json"
```

> **Note:** The endpoint is `/api/v1/agent` (NOT `/api/v1/agent/resume`, which is deprecated).
> The helper scripts handle retries with exponential backoff automatically.
> Install dependencies first: `pip3 install -r requirements.txt`

Or via the helper script:

```bash
# Full resume JSON
python3 scripts/fetch_resume.py

# Extract a specific field for form filling
python3 scripts/fetch_resume.py --field email
python3 scripts/fetch_resume.py --json-path profile.phone
```

**Expected response shape:**
```json
{
  "success": true,
  "data": {
    "activeResumeId": "...",
    "resumes": [{
      "id": "...",
      "data": {
        "profile": {
          "fullName": "...", "email": "...", "phone": "...",
          "location": "...", "summary": "...",
          "linkedin": "...", "github": "...", "website": "..."
        },
        "skills": [{"category": "...", "skills": ["...", "..."]}],
        "experience": [
          {
            "role": "...", "company": "...", "location": "...",
            "startDate": "...", "endDate": "...", "description": "..."
          }
        ],
        "education": [{"degree": "...", "institution": "...", "endDate": "...", "score": "..."}],
        "projects": [{"name": "...", "description": "...", "tags": ["..."]}],
        "achievements": [{"title": "...", "year": "..."}]
      }
    }]
  }
}
```

Parse the active resume:
```
workspace = response.data
activeResume = workspace.resumes.find(r => r.id === workspace.activeResumeId)
resumeData = activeResume.data
```

**Error handling:**

| HTTP Code | Cause | Fix |
|---|---|---|
| `401` | `RESUMEX_API_KEY` is missing or invalid | Go to resumex.dev → Dashboard → Resumex API → generate a new key |
| `404` | Resume not created yet | Go to resumex.dev → create and publish your resume |
| `429` | Rate limited | Wait 10 seconds, retry once |

---

## Step 2 — Load Saved User Preferences

Check for previously saved preferences that supplement the resume data:

```bash
python3 scripts/manage_preferences.py list
```

This returns any saved answers like salary expectation, visa status, notice period, etc.
If `user_preferences.json` doesn't exist yet, that's fine — it will be created when the
user is first asked for missing information.

**Preference fields to look for:**
- `salary_expectation` — e.g. "8-12 LPA" or "$80,000-$100,000"
- `currency` — e.g. "INR" or "USD"
- `notice_period` — e.g. "30 days" or "Immediate"
- `visa_status` — e.g. "No visa required (Indian citizen)"
- `work_authorization` — e.g. "Authorized to work in India"
- `willing_to_relocate` — true/false
- `preferred_work_type` — "remote" | "hybrid" | "onsite"
- `screening_answers` — dict of previously answered screening questions

---

## Step 3 — Build Job-Match Profile

From the resume JSON and user preferences, extract and infer:

| Field | How to Derive |
|---|---|
| Target roles | Latest `experience[0].role` + adjacent titles (e.g. "Software Engineer" → "Backend Developer", "Full Stack Developer") |
| Key skills | Top 5–8 from flattened `skills[].skills` arrays + tech stack from `experience[].description` |
| Seniority | Years of experience calculated from earliest `startDate` to today |
| Location | `profile.location` (override with `JOB_SEARCH_LOCATION` env var if set) |
| Job type | `JOB_TYPE` env var or `preferred_work_type` from preferences (default: full-time) |
| Remote | `REMOTE_ONLY` env var (default: false) |
| Industry | Infer from company names / job descriptions in experience |

**Example derived profile:**
```
Roles: Software Engineer, Backend Developer, Full Stack Developer
Skills: Python, Django, React, PostgreSQL, Docker, AWS
Seniority: Mid-level (3 years)
Location: Pune, India
Type: Full-time
Remote: No preference
Salary: 8-12 LPA (from preferences)
```

---

## Step 4 — Search for Matching Jobs

Use **web_search** to find real, current job postings. Run 3–5 targeted searches using different
query permutations to maximize coverage.

**Query templates:**
```
"{role}" "{top_skill}" jobs "{location}" site:linkedin.com OR site:naukri.com OR site:indeed.com
"{role}" "{top_skill}" "{second_skill}" hiring 2026
"{role}" remote jobs "{top_skill}" "{seniority}"
"{role}" "{top_skill}" jobs "{location}" "apply now" site:wellfound.com OR site:internshala.com
```

See `references/job_boards.md` for complete query patterns per board.

**For each search result URL, use web_fetch to extract:**
- Job title
- Company name
- Location (or Remote)
- Job URL (apply link)
- Required skills (from description)
- Nice-to-have skills
- Experience required
- Salary range (if visible)
- Application method: `form` | `easy-apply` | `email` | `redirect`

Aim to collect **10–20 raw job postings** before scoring.

---

## Step 5 — Score & Rank Jobs

Score each job 0–100 against the resume profile:

| Factor | Max Points |
|---|---|
| Skill overlap (required skills matched) | 40 |
| Role title match | 20 |
| Seniority match | 15 |
| Location / remote match | 15 |
| Industry familiarity | 10 |

**Formula:**
```
score = (skills_matched / skills_required) * 40
      + role_title_match * 20    # 20 if exact, 10 if adjacent, 0 if unrelated
      + seniority_match * 15     # 15 if exact, 8 if ±1 level, 0 if 2+ off
      + location_match * 15      # 15 if match, 8 if remote, 0 if mismatch
      + industry_match * 10      # 10 if same industry, 5 if adjacent
```

---

## Step 6 — Present Approval List to User ⛔

Present the **top 10 matches** in a formatted table. **The user MUST approve before any
applications are submitted.** Never auto-apply without explicit approval. Never skip this step.

**Format:**
```
🎯 Job Match Results for [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#   Score  Company          Role                     Location        Apply Method
──  ─────  ───────          ────                     ────────        ────────────
1   92     Acme Corp        Software Engineer        Pune (On-site)  🤖 Auto-apply
2   87     TechStartup      Backend Developer        Remote          🤖 Auto-apply
3   81     MegaCorp India   Full Stack Engineer      Mumbai          🤖 Auto-apply
4   76     DevShop          Python Developer         Pune (Hybrid)   🤖 Auto-apply
5   73     CloudCo          API Engineer             Remote          🤖 Auto-apply
6   70     DataInc          Backend Engineer         Bangalore       🔗 Manual (LinkedIn)
7   68     StartupXYZ       Software Developer       Remote          🤖 Auto-apply
8   65     BigTech          Junior SWE               Hyderabad       🤖 Auto-apply
9   62     ConsultFirm      Technical Consultant     Pune            📧 Email apply
10  58     SmallCo          Full Stack Developer     Remote          🤖 Auto-apply

🤖 = Agent will fill and submit the application automatically
🔗 = LinkedIn — agent will open the page, you submit manually
📧 = Email — agent will draft the email, you review and send

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Which jobs would you like to apply to?
Options: "all", "1,3,5", "1-5", "none", or "1-5 except 3"
```

**Apply method classification:**
- `🤖 Auto-apply` — Standard form-based application. Agent fills and submits.
- `🔗 Manual (LinkedIn)` — LinkedIn Easy Apply. Agent navigates to the page but user must submit.
  *(LinkedIn automated submission is disabled by default due to ToS concerns.)*
- `📧 Email apply` — Agent drafts the application email for user review.
- `🔗 Manual (redirect)` — Redirects to external ATS. Agent navigates, user may need to complete.

**Wait for the user to respond with their selection before proceeding.**

---

## Step 7 — Auto-Apply to Approved Jobs

For each job the user approved, execute the following sub-steps:

### 7a. Generate Cover Letter (via OpenClaw's built-in AI)

> **No external AI API is used.** Cover letters are generated by OpenClaw's own LLM.

The `draft_cover_letter.py` script reads resume data and job details, then outputs a structured
prompt. OpenClaw's agent uses that prompt with its built-in AI to generate the cover letter.

```bash
python3 scripts/draft_cover_letter.py \
  --resume /tmp/resume.json \
  --job_title "Software Engineer" \
  --company "Acme Corp" \
  --job_description "We are looking for..." \
  --output /tmp/cover_letter_acme.txt
```

The script outputs the generation prompt to stdout. The agent then:
1. Reads the prompt
2. Uses its built-in LLM to generate the cover letter text
3. Saves the result to the `--output` path if specified

**Cover letter structure:**
1. **Hook** (1 sentence): why this specific company/role excites the candidate
2. **Match** (2–3 sentences): specific skills/experiences that directly map to job requirements
3. **Value add** (1–2 sentences): a concrete result from their past work
4. **Close** (1 sentence): call to action

Keep it under 200 words. Professional but human tone.

### 7b. Navigate to Application Page

Use the **browser** tool to navigate to the job's application URL:

```
browser: navigate to "{job_url}"
```

Wait for the page to load. Take a screenshot to confirm you're on the right page.

### 7c. Identify Form Fields

Analyze the page to identify the application form. Look for:
- Input fields (`<input>`, `<textarea>`, `<select>`)
- Required indicators (`*`, `required` attribute)
- Submit buttons
- Multi-step form indicators (next/continue buttons)

See `references/form_field_mappings.md` for mapping form labels to resume data.

### 7d. Fill Form Fields

For each form field, use this priority order to find the value:

```
1. Resume data (from ResumeX API)           → profile.email, profile.phone, etc.
2. User preferences (from preferences.json) → salary_expectation, visa_status, etc.
3. Derived data (calculated by agent)       → years of experience, full name split, etc.
4. Ask the user (last resort)               → save answer to preferences for reuse
```

**Common field mappings (see `references/form_field_mappings.md` for full list):**

| Form Label | Source | JSON Path |
|---|---|---|
| First Name | Resume | `profile.fullName` (split, take first) |
| Last Name | Resume | `profile.fullName` (split, take last) |
| Email | Resume | `profile.email` |
| Phone | Resume | `profile.phone` |
| LinkedIn URL | Resume | `profile.linkedin` |
| GitHub URL | Resume | `profile.github` |
| Website | Resume | `profile.website` |
| Current Location | Resume | `profile.location` |
| Current Company | Resume | `experience[0].company` |
| Current Title | Resume | `experience[0].role` |
| Years of Experience | Derived | Calculate from earliest `startDate` |
| Salary Expectation | Preferences | `salary_expectation` |
| Notice Period | Preferences | `notice_period` |
| Cover Letter | Generated | From Step 7a |

**Browser fill commands:**
```
browser: click on the "First Name" input field
browser: type "{first_name}"
browser: click on the "Email" input field
browser: type "{email}"
...
browser: click on the "Cover Letter" textarea
browser: type "{cover_letter_text}"
```

### 7e. Handle File Upload Fields

If the form has a resume/CV upload field:
- **Do NOT attempt to upload a file automatically.**
- Note it in the summary: "⚠️ Resume upload required — please upload manually"
- Fill all other fields and leave the upload for the user.

### 7f. Handle Unknown Fields — Ask & Remember

If a form field requires information not in the resume or saved preferences:

1. **Pause the application** (do not skip the field)
2. **Ask the user:** "The application for [Company] - [Role] requires: **[field name]**. What should I enter?"
3. **Save the answer** for future use:
```bash
python3 scripts/manage_preferences.py set "[field_key]" "[user_answer]"
```
4. **Fill the field** with the user's answer and continue

> When asking for **sensitive fields** (gender, ethnicity, DOB, veteran/disability status),
> always mention which company's form requires it and that the answer will be saved locally.
> The user may decline — if so, skip the field or leave it blank if optional.

**Don't ask again for the same field type.** Once "salary expectation" is saved, use it for all
future applications unless the user explicitly changes it.

### 7g. Handle Screening Questions

Many application forms include screening questions. For each question:

1. Check `user_preferences.screening_answers` for a saved answer (fuzzy match on question text)
2. If found → use saved answer
3. If not → present the question to the user with the options available
4. Save the answer to preferences:
```bash
python3 scripts/manage_preferences.py set-screening "authorized_to_work" "Yes"
```

**Common screening questions and strategies:**
- "Are you authorized to work in [country]?" → check `visa_status` / `work_authorization`
- "Do you require sponsorship?" → derive from `visa_status`
- "What is your expected salary?" → use `salary_expectation`
- "What is your notice period?" → use `notice_period`
- "Are you willing to relocate?" → use `willing_to_relocate`
- "Why are you interested in this role?" → generate using OpenClaw's built-in LLM from resume + job description
- "Describe your experience with [X]" → generate using OpenClaw's built-in LLM from resume data

See `references/screening_questions.md` for the full list.

### 7h. Submit the Application

After all fields are filled:

1. **Take a screenshot** of the completed form for the user's records
2. **Click the submit button**
3. **Wait for confirmation** (success page, confirmation message, or redirect)
4. **Take a screenshot** of the confirmation
5. If submission fails, note the error and move to the next job

### 7i. Log to resumex.dev Job Tracker

After submission (or attempted submission), log the application:

```bash
python3 scripts/log_application.py \
  --company "Acme Corp" \
  --role "Software Engineer" \
  --url "https://careers.acme.com/apply/12345" \
  --status "applied" \
  --method "auto-applied" \
  --score 92 \
  --notes "Auto-applied via job applier skill."
```

Use `--dry-run` to test without calling the API:
```bash
python3 scripts/log_application.py \
  --company "Test" --role "Test" --url "https://example.com" --dry-run
```

The script automatically tries multiple endpoints (`/api/v1/agent/jobs`, then `/api/v1/agent/logs`)
with retry logic and exponential backoff.

Or via curl:
```bash
curl -s -X POST "https://resumex.dev/api/v1/agent/jobs" \
  -H "Authorization: Bearer $RESUMEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Acme Corp",
    "position": "Software Engineer",
    "url": "https://careers.acme.com/apply/12345",
    "status": "applied",
    "appliedDate": "2026-04-14",
    "notes": "Auto-applied via Auto Job Applier skill. Match score: 92/100. Method: auto-applied."
  }'
```

---

## Step 8 — Present Final Summary

After all approved applications are processed, show a clean summary:

```
✅ Application Summary for [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#  Company          Role                    Score   Status
1  Acme Corp        Software Engineer       92/100  ✅ Applied (auto)
3  MegaCorp India   Full Stack Engineer     81/100  ✅ Applied (auto)
5  CloudCo          API Engineer            73/100  ✅ Applied (auto)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Results: 3 applied ✅ | 0 failed ❌ | 0 manual 🔗

📝 Notes:
  • All applications logged to your resumex.dev tracker
  • Cover letters generated using OpenClaw's built-in AI
  • Saved preferences: salary_expectation, notice_period (for future use)

💡 Tip: Re-run this skill weekly for fresh job listings!
```

If any applications had issues:
```
⚠️ Issues:
  • CloudCo (API Engineer) — Resume upload required. Open the application and upload manually:
    https://careers.cloudco.com/apply/67890
```

---

## Error Handling

All HTTP scripts use the shared `http_client.py` module which provides automatic retry
with exponential backoff. Transient errors (429, 5xx, network timeouts) are retried up
to 3 times before failing. The `Retry-After` header is respected for rate limits.

| Error | Category | Response |
|---|---|---|
| `401 Unauthorized` | Auth | Ask user to check `RESUMEX_API_KEY` in OpenClaw environment |
| `403 Forbidden` | Auth | API key lacks permission — regenerate at resumex.dev |
| `404 Not Found` | Not Found | Resume may not be set up, or endpoint has changed |
| `429 Rate Limited` | Rate Limit | **Auto-retried** up to 3×, respects `Retry-After` header |
| `5xx Server Error` | Server | **Auto-retried** with exponential backoff (1s, 2s, 4s) |
| Network timeout | Network | **Auto-retried** once, then fails with clear message |
| No jobs found | Search | Broaden search: remove location filter, try adjacent roles |
| Web search blocked | Search | Try alternate job boards (Naukri, Internshala, Wellfound, etc.) |
| Browser can't load page | Browser | Note the job as "manual apply" and provide the link |
| Form field type unknown | Form | Ask the user what to enter, save to preferences |
| Submit button not found | Form | Take screenshot, ask user to review the page |
| Application page requires login | Browser | Inform user to log in first, then retry |
| CAPTCHA detected | Browser | Skip this application, mark as "manual", provide link |
| Multi-step form timeout | Browser | Save progress screenshot, note which step failed |

---

## Important Rules

1. **NEVER auto-apply without user approval.** Always present the approval list (Step 6) first.
2. **Always fetch fresh resume data** at the start of each session. Don't cache across sessions.
3. **Cache within a session** — fetch the resume once when the skill starts, reuse for all applications.
4. **Save every unknown field to preferences** — the user should never be asked the same question twice.
5. **LinkedIn jobs are manual-only by default.** Don't attempt LinkedIn Easy Apply unless the user explicitly requests it (ToS risk).
6. **Skip file upload fields** — note them for the user to complete manually.
7. **Take screenshots** before and after form submission for the user's records.
8. **Handle CAPTCHAs gracefully** — if detected, mark the job as "manual apply" and move on.
9. **Rate limits** — resumex.dev API has rate limits. Don't call the resume endpoint more than once per session.
10. **No external AI APIs** — cover letters and text generation use OpenClaw's built-in LLM only.
11. **Privacy** — resume data is fetched live from resumex.dev. Saved preferences are stored locally only in `data/user_preferences.json` and never transmitted to any server.
12. **Sensitive fields** — always inform the user before saving sensitive data (gender, DOB, ethnicity, etc.) and allow them to decline.

---

## Files in This Skill

| File | Purpose |
|---|---|
| `SKILL.md` | This file — main instructions for the agent |
| `scripts/http_client.py` | Shared HTTP client with retries, backoff, and error classification |
| `scripts/fetch_resume.py` | Fetches and parses resume from resumex.dev (supports `--field` extraction) |
| `scripts/search_jobs.py` | Constructs search queries and parses job posting results |
| `scripts/fill_application.py` | Maps form fields to resume data, outputs browser instructions |
| `scripts/manage_preferences.py` | CRUD for `user_preferences.json` (salary, visa, screening answers) |
| `scripts/draft_cover_letter.py` | Builds cover letter prompt for OpenClaw's built-in AI (no external API) |
| `scripts/log_application.py` | Logs a job application to resumex.dev tracker (with `--dry-run` support) |
| `requirements.txt` | Python dependencies (`requests>=2.28.0`) |
| `references/job_boards.md` | Job board search patterns, form selectors, browser notes |
| `references/form_field_mappings.md` | Maps form field labels → resume JSON paths |
| `references/screening_questions.md` | Common screening questions and handling strategies |
| `data/user_preferences.json` | Persistent local storage for user answers (auto-created at runtime) |
