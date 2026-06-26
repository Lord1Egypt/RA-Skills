---
name: ai-job-hunter-pro
description: AI-powered job search assistant with RAG-based resume-JD matching, automated application pipeline, and status tracking. Use when the user wants to search for jobs matching their resume, auto-apply to positions, track application status, generate tailored cover letters, or analyze their job search funnel. Trigger phrases include "find jobs for me", "match my resume to jobs", "auto-apply", "track my applications", "job search report", "optimize my resume for this job".
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["python3"]
---

# AI Job Hunter Pro

Intelligent job search assistant with RAG-based semantic matching, automated applications, and data-driven tracking.

## Setup (first-time only)

Run the setup script to install dependencies and initialize the vector database:

```bash
cd {SKILL_DIR}
pip install -r scripts/requirements.txt
python3 scripts/setup_rag.py --init
```

Then create your profile:

```bash
cp assets/profile_template.json ~/job_profile.json
# Edit ~/job_profile.json with your info
```

Import your resume (PDF or DOCX):

```bash
python3 scripts/rag_engine.py --import-resume ~/path/to/resume.pdf
```

## Core Workflows

### Workflow 1: Smart Job Search (RAG Matching)

When user says "find jobs for me" or "match my resume":

1. Load user profile from `~/job_profile.json`
2. Run RAG matching engine:
   ```bash
   python3 {SKILL_DIR}/scripts/rag_engine.py \
     --mode search \
     --platforms linkedin,boss \
     --min-score 0.75 \
     --max-results 20
   ```
3. Present results sorted by match score
4. For each job, show: title, company, match score, top matching skills, missing skills
5. Ask user which jobs to apply to, or auto-apply if configured

### Workflow 2: Auto-Apply Pipeline

When user says "apply to these jobs" or "auto-apply":

1. For each selected job:
   ```bash
   python3 {SKILL_DIR}/scripts/apply_pipeline.py \
     --job-id <id> \
     --mode dry-run \
     --generate-cover-letter \
     --optimize-ats
   ```
2. In dry-run mode: show generated cover letter and ATS-optimized resume highlights for review
3. After user confirms, switch to `--mode submit`
4. Log result to tracker database

### Workflow 3: Application Tracking

When user says "track my applications" or "job search report":

```bash
python3 {SKILL_DIR}/scripts/tracker.py --report daily
```

Status flow: Discovered → Applied → Screening → Interview → Offer / Rejected

### Workflow 4: Feedback Loop

When user says "I like this job" or "not interested":

```bash
python3 {SKILL_DIR}/scripts/rag_engine.py \
  --mode feedback \
  --job-id <id> \
  --signal like|dislike
```

This adjusts the RAG query vectors to improve future recommendations.

## Rules

- Always start in dry-run mode. Never submit applications without explicit user confirmation.
- Respect platform rate limits: max 20 applications per day across all platforms.
- Never misrepresent the user's qualifications in cover letters or applications.
- Store all data locally. Never send resume data to external services other than the job platforms themselves.
- When a platform returns an error or blocks access, report it clearly and suggest manual fallback.
- Always show the match score and reasoning before applying.

## Configuration

User config lives at `~/job_profile.json`. Skill config in OpenClaw:

```json
{
  "skills": {
    "ai-job-hunter-pro": {
      "enabled": true,
      "profile_path": "~/job_profile.json",
      "default_platforms": ["linkedin", "boss"],
      "max_daily_applications": 20,
      "min_match_score": 0.75,
      "require_confirmation": true,
      "dry_run": true
    }
  }
}
```
