---
name: coursera-progress
version: 1.0.0
description: >
  Fetch and display Coursera course enrollment, completion progress, grades,
  certificates, and upcoming deadlines using the Coursera API. Use this skill
  whenever the user wants to check their Coursera learning progress, see what
  courses they're enrolled in, review assignment deadlines, track certificate
  completions, or get a learning summary. Trigger on phrases like "my Coursera
  courses", "Coursera progress", "check my Coursera", "what's due on Coursera",
  "Coursera certificate", "online course progress", or "my enrollments".
metadata:
  clawdbot:
    requires:
      bins: ["curl", "python3"]
      env:
        - name: COURSERA_CLIENT_ID
          description: "Coursera API client ID (see setup)"
        - name: COURSERA_CLIENT_SECRET
          description: "Coursera API client secret"
        - name: COURSERA_ACCESS_TOKEN
          description: "OAuth2 access token (generated from client credentials)"
          optional: true
---

# Coursera Progress Skill

Fetch enrollment status, grades, deadlines, and certificates from Coursera via the Coursera REST API v1.

---

## Authentication setup

Coursera uses OAuth 2.0. Two paths:

### Path A — Personal access (for learners)

1. Go to [coursera.org/account/api](https://www.coursera.org/account/api) → Generate key
2. Note the **Client ID** and **Client Secret**
3. Get a token (client credentials flow):

```bash
export COURSERA_CLIENT_ID="your_client_id"
export COURSERA_CLIENT_SECRET="your_client_secret"

COURSERA_ACCESS_TOKEN=$(curl -s -X POST \
  "https://api.coursera.com/oauth2/client_credentials/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$COURSERA_CLIENT_ID&client_secret=$COURSERA_CLIENT_SECRET" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")

export COURSERA_ACCESS_TOKEN
```

### Path B — Unofficial API (no key needed)

Coursera's public endpoints don't require auth for some queries. Use when the user hasn't set up credentials.

---

## Base URL and headers

```
https://api.coursera.com/api
```

```bash
AUTH_HEADER="Authorization: Bearer $COURSERA_ACCESS_TOKEN"
```

---

## Core API calls

### Get enrollments for a user

```bash
# Get your own user ID first
curl -s "https://api.coursera.com/api/users/v1/me" \
  -H "$AUTH_HEADER"

# Then fetch enrollments
curl -s "https://api.coursera.com/api/enrollments.v1?userId=USER_ID&fields=courseId,enrolledAt,grade,completedAt,certificateCode" \
  -H "$AUTH_HEADER"
```

### Get course details by ID

```bash
curl -s "https://api.coursera.com/api/courses.v1?ids=COURSE_ID_1,COURSE_ID_2&fields=name,slug,description,specializations" \
  -H "$AUTH_HEADER"
```

### Get on-demand course progress

```bash
curl -s "https://api.coursera.com/api/onDemandCourseCompletions.v1?userId=USER_ID&courseId=COURSE_ID&fields=progressPercent,completedAt,grade" \
  -H "$AUTH_HEADER"
```

### Get assignment deadlines

```bash
curl -s "https://api.coursera.com/api/onDemandDeadlineSchedules.v1?courseId=COURSE_ID&fields=deadlineSchedule,moduleIds" \
  -H "$AUTH_HEADER"
```

### Get certificate info

```bash
curl -s "https://api.coursera.com/api/certificates.v1?userId=USER_ID&fields=courseId,issuedAt,verifyUrl,grade" \
  -H "$AUTH_HEADER"
```

### Search for courses

```bash
curl -s "https://api.coursera.com/api/courses.v1?q=search&query=SEARCH_TERM&fields=name,slug,partnerIds,primaryLanguages" \
  -H "$AUTH_HEADER" \
  | python3 -m json.tool
```

---

## Displaying results

**Active enrollments summary:**
```
Your Coursera Courses
─────────────────────────────────────────────────────
📚 Machine Learning Specialization (Stanford/DeepLearning.AI)
   Progress: 68% complete   Grade: 91.4%
   Next deadline: Mar 28 — Week 4 Programming Assignment

📚 Python for Everybody (University of Michigan)
   Progress: 100% ✅  Grade: 96.7%
   Certificate: Issued Jan 12, 2026
   Verify: https://coursera.org/verify/XXXX

📚 SQL for Data Science (UC Davis)
   Progress: 23%  Grade: —
   Next deadline: Apr 3 — Module 2 Quiz
─────────────────────────────────────────────────────
Certificates earned: 1   Active courses: 2
```

**Upcoming deadlines:**
```
Deadlines (next 14 days):
  Mar 28  Week 4 Programming Assignment  — Machine Learning
  Apr 3   Module 2 Quiz                 — SQL for Data Science
  Apr 10  Peer Review Submission        — Machine Learning
```

---

## Without API credentials (public lookup)

For course search and public course info:

```bash
# Public course info (no auth)
curl -s "https://api.coursera.com/api/courses.v1?q=search&query=python&includes=instructors&fields=name,partnerIds,instructorIds,primaryLanguages,workload" \
  | python3 -m json.tool
```

For personal data (grades, certificates), credentials are required.

---

## Python helper for parsing progress

```python
import json, subprocess, os

def get_enrollments(user_id):
    token = os.environ["COURSERA_ACCESS_TOKEN"]
    r = subprocess.run(
        ["curl", "-s",
         f"https://api.coursera.com/api/enrollments.v1?userId={user_id}"
         f"&fields=courseId,enrolledAt,grade,completedAt,certificateCode",
         "-H", f"Authorization: Bearer {token}"],
        capture_output=True, text=True)
    return json.loads(r.stdout).get("elements", [])

def upcoming_deadlines(enrollments, days=14):
    from datetime import date, timedelta
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    # Parse deadlines per course and filter by date
    ...
```

---

## Error handling

| Error | Meaning | Fix |
|---|---|---|
| `401 Unauthorized` | Token expired or missing | Re-run token generation step |
| `403 Forbidden` | Scope missing on key | Regenerate API key with correct scopes |
| Empty `elements` array | No enrollments found | Confirm correct user ID |
| Rate limit (429) | Too many requests | Back off 30s; Coursera is ~100 req/min |
