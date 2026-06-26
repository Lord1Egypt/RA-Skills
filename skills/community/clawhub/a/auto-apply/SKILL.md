---
name: auto-apply
version: 2.0.0
description: Automate your job search and application process with Mokaru. Search thousands of jobs, tailor your resume to each role, track applications through your pipeline, and get AI-powered career coaching. Supports remote and on-site roles across all industries. Use when users ask about job hunting, career search, applying for jobs, resume optimization, interview prep, or application tracking.
requires:
  env:
    - MOKARU_API_KEY
  bins:
    - curl
    - jq
---

# Mokaru Job Search & Application Tracker

You can search for jobs, save and track job applications, and read the user's career profile through the Mokaru API.

**Important:** This skill does NOT submit job applications on behalf of the user. It helps with the preparation: finding jobs, saving them to a tracker, updating application status, and reviewing the user's profile. The user (or their browser agent) must visit the `applyLink` from search results to actually apply. When the user says "apply", save the job to their tracker and provide the apply link so they can complete the application themselves.

## Authentication

Every request requires a Bearer token. The token is stored in the `MOKARU_API_KEY` environment variable and starts with `mk_`.

Include this header on all requests:

```
Authorization: Bearer $MOKARU_API_KEY
```

## Base URL

```
https://api.mokaru.ai
```

All endpoints are under `/v1/`.

---

## Endpoints

### 1. Search Jobs

**When to use:** The user wants to find job listings. They might say "find me React jobs in New York" or "search for remote marketing roles."

**Method:** `POST /v1/jobs/search`

**Required scope:** `jobs:search`

**Rate limit:** 30 requests per minute

**Request body (JSON):**

| Field               | Type     | Required | Description                                                        |
|---------------------|----------|----------|--------------------------------------------------------------------|
| `query`             | string   | Yes      | Job search keywords (e.g. "software engineer")                     |
| `location`          | string   | No       | City, state, or country (e.g. "San Francisco, CA")                 |
| `remote`            | boolean  | No       | Filter for remote jobs only                                        |
| `workArrangement`   | string   | No       | One of: `remote`, `hybrid`, `onsite`                               |
| `employmentType`    | string   | No       | E.g. "fulltime", "parttime", "contract"                            |
| `datePosted`        | string   | No       | Recency filter (e.g. "today", "3days", "week", "month")            |
| `salaryMin`         | number   | No       | Minimum annual salary filter                                       |
| `country`           | string   | No       | Country code or name                                               |
| `benefits`          | string[] | No       | Required benefits to filter on                                     |
| `includeKeywords`   | string[] | No       | Keywords that must appear in the job                               |
| `excludeKeywords`   | string[] | No       | Keywords that must NOT appear in the job                           |
| `includeCompanies`  | string[] | No       | Limit to specific companies                                        |
| `excludeCompanies`  | string[] | No       | Exclude specific companies                                         |
| `cursor`            | string   | No       | Opaque pagination cursor from a previous response's `nextCursor`   |

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/jobs/search \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "frontend engineer",
    "location": "New York",
    "remote": true
  }' | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "title": "Frontend Engineer",
      "company": "Acme Corp",
      "companyLogo": "https://...",
      "companyWebsite": "https://...",
      "location": "New York, NY",
      "city": "New York",
      "state": "NY",
      "country": "US",
      "isRemote": true,
      "employmentType": "fulltime",
      "applyLink": "https://...",
      "applyIsDirect": false,
      "publisher": "LinkedIn",
      "description": "<p>We are looking for a Frontend Engineer...</p>",
      "highlights": { "qualifications": [...], "responsibilities": [...] },
      "benefits": ["Health insurance", "401k"],
      "salaryMin": 120000,
      "salaryMax": 160000,
      "salaryPeriod": "year",
      "postedAt": "2026-03-10T..."
    }
  ],
  "total": 142,
  "hasMore": true,
  "nextCursor": "eyJwYWdlIjoyfQ=="
}
```

**Pagination:** Pass the `nextCursor` from a response as `cursor` in the next request to fetch more results. When `hasMore` is `false`, `nextCursor` is `null`.

**How to use the results:** Present jobs in a readable list. Include the title, company, location, salary range (if available), and the apply link. If `hasMore` is true, fetch the next page with `cursor`.

---

### 2. Create Application

**When to use:** The user wants to save or track a job. They might say "save this job" or "add this to my tracker." You can also use this right after a search to save a result.

**Method:** `POST /v1/tracker/applications`

**Required scope:** `tracker:write`

**Rate limit:** 20 requests per minute

**Request body (JSON):**

| Field            | Type   | Required | Description                                                                                      |
|------------------|--------|----------|--------------------------------------------------------------------------------------------------|
| `jobTitle`       | string | Yes      | Job title (max 200 chars)                                                                        |
| `company`        | string | Yes      | Company name (max 200 chars)                                                                     |
| `location`       | string | No       | Job location (max 200 chars)                                                                     |
| `jobUrl`         | string | No       | URL of the job posting (max 2000 chars, must be a valid URL). Used for duplicate detection       |
| `jobDescription` | string | No       | Full job description text (max 50,000 chars). Required (non-empty) for `autoPrepare`.            |
| `jobListingId`   | string | No       | If saving from a Mokaru search result, pass the job's `id` to automatically pull salary/details  |
| `source`         | string | No       | One of: `LinkedIn`, `CompanyWebsite`, `JobWebsite`, `Referral`, `Agency`, `Other`. Defaults to `Other` |
| `autoPrepare`    | boolean | No      | When `true`, Mokaru duplicates the user's default resume and tailors it to the job description using AI. Requires Plus plan, a default resume, and a non-empty job description. |

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/tracker/applications \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Frontend Engineer",
    "company": "Acme Corp",
    "location": "New York, NY",
    "jobUrl": "https://acme.com/careers/frontend",
    "jobListingId": "clx...",
    "source": "JobWebsite",
    "autoPrepare": true
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "applicationId": "clx...",
  "existing": false,
  "autoPrepare": true
}
```

If `existing` is `true`, the application was already tracked (matched by `jobUrl`) and the existing ID is returned. No duplicate is created.

If `autoPrepare` is `true` in the response, Mokaru is tailoring the user's resume in the background (~30 seconds). The application status will be `preparing` until done.

**Auto-prep errors:** If auto-prep fails, the API returns a clear error code:
- `PLAN_REQUIRED` (403) - user needs a Plus plan
- `NO_DEFAULT_RESUME` (400) - user must set a default resume in Mokaru first
- `JOB_DESCRIPTION_TOO_SHORT` (400) - job description is missing or empty

**Workflow tip:** When saving a job from search results, pass the `id` from the search result as `jobListingId`. This auto-fills salary and description data. Add `"autoPrepare": true` to also tailor the resume automatically.

---

### 3. List Applications

**When to use:** The user wants to see their tracked applications. They might ask "show my applications" or "what jobs have I applied to?"

**Method:** `GET /v1/tracker/applications`

**Required scope:** `tracker:read`

**Rate limit:** 60 requests per minute

**Query parameters:**

| Param    | Type   | Required | Description                                                   |
|----------|--------|----------|---------------------------------------------------------------|
| `status` | string | No       | Filter by status (see status values below)                    |
| `limit`  | number | No       | Results per page, default 25, max 100                         |
| `offset` | number | No       | Number of results to skip for pagination                      |

**Valid status values:** `watchlist`, `preparing`, `applied`, `response`, `screening`, `interview_scheduled`, `interviewed`, `offer`, `negotiating`, `accepted`, `rejected`, `withdrawn`, `no_response`

**Curl example:**

```bash
curl -s -G https://api.mokaru.ai/v1/tracker/applications \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  --data-urlencode "status=applied" \
  --data-urlencode "limit=10" | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "jobTitle": "Frontend Engineer",
      "company": "Acme Corp",
      "location": "New York, NY",
      "jobUrl": "https://acme.com/careers/frontend",
      "status": "applied",
      "source": "JobWebsite",
      "priority": 3,
      "salaryMin": 120000,
      "salaryMax": 160000,
      "appliedDate": "2026-03-10T...",
      "createdAt": "2026-03-10T...",
      "updatedAt": "2026-03-12T..."
    }
  ],
  "total": 24,
  "hasMore": true,
  "limit": 10,
  "offset": 0
}
```

**How to present:** Show the list as a table or concise summary. Include status, company, job title, and any salary info. If `hasMore` is true, let the user know there are more results.

---

### 4. Get Application Detail

**When to use:** The user wants to see the full detail of a specific application, including its timeline, interviews, and notes. They might say "show me the details of my Acme application" or "what's the status of that job?"

**Method:** `GET /v1/tracker/applications/{id}`

**Required scope:** `tracker:read`

**Rate limit:** 60 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/tracker/applications/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "id": "clx_abc123",
    "jobTitle": "Frontend Engineer",
    "company": "Acme Corp",
    "location": "New York, NY",
    "jobUrl": "https://acme.com/careers/frontend",
    "jobDescription": "We are looking for...",
    "status": "interviewed",
    "source": "JobWebsite",
    "priority": 5,
    "notes": "Great conversation with hiring manager",
    "salaryMin": 120000,
    "salaryMax": 160000,
    "salaryPeriod": "year",
    "cvId": "clx_cv456",
    "appliedDate": "2026-03-10T...",
    "createdAt": "2026-03-10T...",
    "updatedAt": "2026-03-15T...",
    "timeline": [
      {
        "id": "tl1",
        "status": "interviewed",
        "description": "status_changed",
        "createdAt": "2026-03-15T..."
      }
    ],
    "interviews": [
      {
        "id": "int1",
        "round": 1,
        "type": "video",
        "date": "2026-03-14T10:00:00.000Z",
        "notes": "Technical interview",
        "contact": {
          "id": "ct1",
          "firstName": "Sarah",
          "lastName": "Jones",
          "jobTitle": "Engineering Manager"
        }
      }
    ]
  }
}
```

**How to use:** Present the application details clearly. Highlight the current status, upcoming interviews (with dates and contacts), and any notes. If the user has interviews coming up, suggest they prepare.

---

### 5. Update Application

**When to use:** The user wants to change the status, priority, notes, or details of a tracked application. They might say "mark that application as interviewed" or "set priority to high."

**Method:** `PATCH /v1/tracker/applications/{id}`

**Required scope:** `tracker:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field      | Type   | Description                                           |
|------------|--------|-------------------------------------------------------|
| `status`   | string | New status (see valid status values above)            |
| `priority` | number | 1 (lowest) to 5 (highest)                            |
| `notes`    | string | Free-text notes (max 5,000 chars)                     |
| `jobTitle` | string | Updated job title (max 200 chars)                     |
| `company`  | string | Updated company name (max 200 chars)                  |
| `location` | string | Updated location (max 200 chars)                      |

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/tracker/applications/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "interviewed",
    "priority": 5,
    "notes": "Great conversation with the hiring manager"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "application": {
    "id": "clx_abc123",
    "jobTitle": "Frontend Engineer",
    "company": "Acme Corp",
    "location": "New York, NY",
    "status": "interviewed",
    "priority": 5,
    "notes": "Great conversation with the hiring manager",
    "updatedAt": "2026-03-15T..."
  }
}
```

Status changes are automatically recorded in the application's timeline.

---

### 6. List Contacts

**When to use:** The user wants to see their networking contacts. They might say "show my contacts" or "who do I know at Acme Corp?"

**Method:** `GET /v1/contacts`

**Required scope:** `contacts:read`

**Rate limit:** 60 requests per minute

**Query parameters:**

| Param          | Type   | Required | Description                                              |
|----------------|--------|----------|----------------------------------------------------------|
| `limit`        | number | No       | Results per page, default 25, max 100                    |
| `offset`       | number | No       | Number of results to skip                                |
| `relationship` | string | No       | Filter by type (see relationship values below)           |
| `search`       | string | No       | Search by name, company, or email (case-insensitive)     |

**Valid relationship values:** `RECRUITER`, `HIRING_MANAGER`, `HR_MANAGER`, `TEAM_LEAD`, `DEPARTMENT_HEAD`, `CEO_FOUNDER`, `COLLEAGUE`, `FRIEND`, `REFERRAL`, `OTHER`

**Curl example:**

```bash
curl -s -G https://api.mokaru.ai/v1/contacts \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  --data-urlencode "search=Acme" \
  --data-urlencode "limit=10" | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "firstName": "Sarah",
      "lastName": "Jones",
      "jobTitle": "Engineering Manager",
      "company": "Acme Corp",
      "relationship": "HIRING_MANAGER",
      "email": "sarah@acme.com",
      "phone": "+1 555-0200",
      "linkedIn": "https://linkedin.com/in/sarahjones",
      "createdAt": "2026-03-10T...",
      "updatedAt": "2026-03-15T..."
    }
  ],
  "total": 12,
  "hasMore": true,
  "limit": 10,
  "offset": 0
}
```

---

### 7. Get Contact Detail

**When to use:** The user wants to see full details of a specific contact. They might say "show me Sarah's info" or "what's the recruiter's email?"

**Method:** `GET /v1/contacts/{id}`

**Required scope:** `contacts:read`

**Rate limit:** 30 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/contacts/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "id": "clx_abc123",
    "firstName": "Sarah",
    "lastName": "Jones",
    "jobTitle": "Engineering Manager",
    "company": "Acme Corp",
    "relationship": "HIRING_MANAGER",
    "email": "sarah@acme.com",
    "phone": "+1 555-0200",
    "linkedIn": "https://linkedin.com/in/sarahjones",
    "createdAt": "2026-03-10T...",
    "updatedAt": "2026-03-15T..."
  }
}
```

---

### 8. Create Contact

**When to use:** The user wants to save a new networking contact. They might say "add Sarah Jones as a contact" or "save the recruiter's info."

**Method:** `POST /v1/contacts`

**Required scope:** `contacts:write`

**Rate limit:** 20 requests per minute

**Request body (JSON):**

| Field          | Type   | Required | Description                              |
|----------------|--------|----------|------------------------------------------|
| `firstName`    | string | Yes      | First name (max 100 chars)               |
| `lastName`     | string | Yes      | Last name (max 100 chars)                |
| `jobTitle`     | string | No       | Contact's job title (max 200 chars)      |
| `company`      | string | No       | Company name (max 200 chars)             |
| `relationship` | string | No       | Relationship type (see values above)     |
| `email`        | string | No       | Email address (max 200 chars)            |
| `phone`        | string | No       | Phone number (max 50 chars)              |
| `linkedIn`     | string | No       | LinkedIn profile URL (max 500 chars)     |

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/contacts \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Sarah",
    "lastName": "Jones",
    "jobTitle": "Engineering Manager",
    "company": "Acme Corp",
    "relationship": "HIRING_MANAGER",
    "email": "sarah@acme.com"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx..."
}
```

---

### 9. Update Contact

**When to use:** The user wants to update a contact's details. They might say "update Sarah's phone number" or "change the recruiter's company."

**Method:** `PATCH /v1/contacts/{id}`

**Required scope:** `contacts:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field          | Type        | Description                              |
|----------------|-------------|------------------------------------------|
| `firstName`    | string      | First name (max 100 chars)               |
| `lastName`     | string      | Last name (max 100 chars)                |
| `jobTitle`     | string/null | Job title (max 200 chars, null to clear) |
| `company`      | string/null | Company name (max 200 chars)             |
| `relationship` | string/null | Relationship type (see values above)     |
| `email`        | string/null | Email address (max 200 chars)            |
| `phone`        | string/null | Phone number (max 50 chars)              |
| `linkedIn`     | string/null | LinkedIn URL (max 500 chars)             |

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/contacts/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+1 555-0201",
    "relationship": "TEAM_LEAD"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx_abc123"
}
```

Pass `null` for optional fields to clear them (e.g. `"phone": null`).

---

### 10. Delete Contact

**When to use:** The user wants to remove a contact. They might say "delete that contact" or "remove Sarah from my contacts."

**Method:** `DELETE /v1/contacts/{id}`

**Required scope:** `contacts:write`

**Rate limit:** 10 requests per minute

**Curl example:**

```bash
curl -s -X DELETE https://api.mokaru.ai/v1/contacts/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

---

### 11. Get Profile

**When to use:** The user wants to see their career profile, or you need context about their background to tailor a job search. For example, "what skills do I have on file?" or before searching, to understand their experience level.

**Method:** `GET /v1/profile`

**Required scope:** `profile:read`

**Rate limit:** 30 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/profile \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "firstName": "Jane",
    "lastName": "Doe",
    "email": "jane@example.com",
    "phone": "+1 555-0100",
    "address": "New York, NY",
    "country": "US",
    "province": "NY",
    "jobTitle": "Frontend Engineer",
    "summary": "5 years of experience in...",
    "sector": "Technology",
    "linkedIn": "https://linkedin.com/in/janedoe",
    "website": "https://janedoe.dev",
    "portfolio": null,
    "jobTitles": [
      { "title": "Frontend Engineer", "displayOrder": 0 },
      { "title": "React Developer", "displayOrder": 1 }
    ],
    "skills": [
      { "name": "React", "category": "TECHNICAL", "level": "expert" },
      { "name": "TypeScript", "category": "TECHNICAL", "level": "advanced" }
    ],
    "workExperiences": [
      {
        "jobTitle": "Frontend Engineer",
        "company": "TechCo",
        "location": "New York, NY",
        "startDate": "2022-01-15T00:00:00.000Z",
        "endDate": null,
        "isCurrent": true,
        "description": "Building the design system...",
        "responsibilities": ["Led frontend architecture"],
        "achievements": ["Reduced bundle size by 40%"]
      }
    ],
    "educations": [
      {
        "school": "MIT",
        "degree": "Bachelor of Science",
        "field": "Computer Science",
        "startDate": "2016-09-01T00:00:00.000Z",
        "endDate": "2020-06-15T00:00:00.000Z",
        "isCurrent": false
      }
    ]
  }
}
```

**Note:** The profile response uses friendly aliases `school` / `field` for education (derived from the DB fields `institution` / `fieldOfStudy`). When calling the dedicated `/v1/education` endpoints, use `institution` and `fieldOfStudy` instead (see section 24-28). Skill `category` values are the enum `TECHNICAL`, `SOFT`, or `LANGUAGE`.

**How to use:** Pull the user's job titles, skills, and current role to craft better search queries. Mention their background when recommending jobs.

---

### 12. Update Profile

**When to use:** The user wants to update their career profile. They might say "change my job title" or "update my LinkedIn" or "add my new employer."

**Method:** `PATCH /v1/profile`

**Required scope:** `profile:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field          | Type        | Description                              |
|----------------|-------------|------------------------------------------|
| `firstName`    | string      | First name (max 100 chars)               |
| `lastName`     | string      | Last name (max 100 chars)                |
| `email`        | string      | Email address (max 254 chars)            |
| `phone`        | string/null | Phone number (max 50 chars)              |
| `address`      | string/null | Address (max 200 chars)                  |
| `country`      | string/null | Country (max 100 chars)                  |
| `province`     | string/null | Province or state (max 100 chars)        |
| `birthDate`    | string/null | ISO date string (e.g. "1990-01-15")      |
| `driverLicense`| string/null | Driver license type (max 50 chars)       |
| `gender`       | string/null | Gender (max 50 chars)                    |
| `jobTitle`     | string/null | Current job title (max 200 chars)        |
| `summary`      | string/null | Professional summary (max 2000 chars)    |
| `sector`       | string/null | Industry sector (max 100 chars)          |
| `employer`     | string/null | Current employer (max 200 chars)         |
| `linkedIn`     | string/null | LinkedIn username or URL (auto-normalized)|
| `website`      | string/null | Website URL (https:// added if missing)  |
| `portfolio`    | string/null | Portfolio URL (https:// added if missing)|

Pass `null` for optional fields to clear them.

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/profile \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Senior Software Engineer",
    "employer": "Acme Corp",
    "linkedIn": "jane-smith"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

LinkedIn usernames are automatically converted to full URLs. For example, `"jane-smith"` becomes `"https://linkedin.com/in/jane-smith"`. Website and portfolio URLs have `https://` prepended if missing.

**Important:** Profile changes propagate to all resumes that use profile data. This is different from updating a resume's `cvData` which only affects that specific resume.

---

### 13. List Resumes

**When to use:** The user wants to see their resumes, or you need to know which resume to export or update. They might say "show my resumes" or "which CVs do I have?"

**Method:** `GET /v1/resume`

**Required scope:** `resume:read`

**Rate limit:** 60 requests per minute

**Query parameters:**

| Param    | Type   | Required | Description                           |
|----------|--------|----------|---------------------------------------|
| `limit`  | number | No       | Results per page, default 25, max 100 |
| `offset` | number | No       | Number of results to skip             |

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/resume \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "name": "Software Engineer Resume",
      "template": "classic",
      "isDefault": true,
      "createdAt": "2026-01-15T...",
      "updatedAt": "2026-03-20T..."
    }
  ],
  "total": 3,
  "hasMore": false,
  "limit": 25,
  "offset": 0
}
```

---

### 14. Get Resume Detail

**When to use:** The user wants to see the full content of a specific resume, or you need the data to provide career advice. They might say "show me my default resume" or "what's on my Software Engineer CV?"

**Method:** `GET /v1/resume/{id}`

**Required scope:** `resume:read`

**Rate limit:** 30 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/resume/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "id": "clx...",
    "name": "Software Engineer Resume",
    "template": "classic",
    "isDefault": true,
    "cvData": {
      "firstName": "Jane",
      "lastName": "Doe",
      "email": "jane@example.com",
      "jobTitle": "Software Engineer",
      "experiences": [...],
      "education": [...],
      "skills": [...]
    },
    "designSettings": { ... },
    "optionalFields": { ... },
    "sectionOrder": ["personal", "experience", "education", "skills"],
    "hiddenItems": { ... },
    "createdAt": "2026-01-15T...",
    "updatedAt": "2026-03-20T..."
  }
}
```

The `cvData` field contains the full resume content: personal info, work experiences, education, skills, languages, certificates, projects, and more. The `hiddenItems` field tracks which individual entries (experiences, education, etc.) are hidden from the rendered resume.

---

### 15. Create Resume

**When to use:** The user wants to create a new resume. They might say "create a new resume for backend roles" or "make a copy of my CV with a different name."

**Method:** `POST /v1/resume`

**Required scope:** `resume:write`

**Rate limit:** 10 requests per minute

**Request body (JSON):**

| Field            | Type    | Required | Description                              |
|------------------|---------|----------|------------------------------------------|
| `name`           | string  | Yes      | Resume name (max 200 chars)              |
| `template`       | string  | No       | Template ID (default: "classic")         |
| `isDefault`      | boolean | No       | Set as default resume                    |
| `cvData`         | object  | No       | Resume content (experiences, skills, etc)|
| `designSettings` | object  | No       | Visual styling (colors, fonts, spacing)  |
| `optionalFields` | object  | No       | Show/hide optional fields                |
| `sectionOrder`   | array   | No       | Order of resume sections                 |

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/resume \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend Engineer Resume",
    "template": "classic",
    "isDefault": false
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx..."
}
```

---

### 16. Update Resume

**When to use:** The user wants to change their resume name, template, content, or settings. They might say "rename my resume" or "update my skills on the default CV."

**Method:** `PATCH /v1/resume/{id}`

**Required scope:** `resume:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field            | Type    | Description                              |
|------------------|---------|------------------------------------------|
| `name`           | string  | Resume name (max 200 chars)              |
| `template`       | string  | Template ID                              |
| `isDefault`      | boolean | Set as default resume                    |
| `cvData`         | object  | Resume content                           |
| `designSettings` | object  | Visual styling                           |
| `optionalFields` | object  | Show/hide optional fields                |
| `sectionOrder`   | array   | Order of resume sections                 |

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/resume/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Resume",
    "isDefault": true
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx..."
}
```

---

### 17. Delete Resume

**When to use:** The user wants to remove a resume. They might say "delete that old resume" or "remove my Backend CV."

**Method:** `DELETE /v1/resume/{id}`

**Required scope:** `resume:write`

**Rate limit:** 10 requests per minute

**Curl example:**

```bash
curl -s -X DELETE https://api.mokaru.ai/v1/resume/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

If the deleted resume was the default, another resume is automatically promoted. Applications linked to this resume are unlinked (`cvId` set to null, the application itself is not deleted). Any Autopilot searches that reference this resume are also deleted.

---

### 18. Export Resume as PDF

**When to use:** The user wants to download their resume as a PDF. They might say "export my resume" or "give me a PDF of my CV."

**Method:** `POST /v1/resume/{id}/export/pdf`

**Required scope:** `resume:export`

**Rate limit:** 5 requests per minute

**Request body (JSON, optional):**

| Field    | Type   | Required | Description                   |
|----------|--------|----------|-------------------------------|
| `locale` | string | No       | Language for date formatting (default: "en") |

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/resume/clx_abc123/export/pdf \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  -o resume.pdf
```

**Response:** Binary PDF file with `Content-Type: application/pdf`. Save it to disk or send it to the user.

**Important:** This endpoint returns a binary file, not JSON. The PDF is rendered server-side with the user's chosen template and design settings.

**Export errors:**
- `RESUME_PROCESSING` (409) - resume is being tailored by auto-prep. Wait 5-10 seconds and retry.
- `EMPTY_RESUME` (400) - the resume has no `cvData` yet. Ask the user to fill in their resume first.

---

### 19. List Experiences

**When to use:** The user wants to see their work history. They might say "show my work experience" or "what jobs have I had?"

**Method:** `GET /v1/experiences`

**Required scope:** `experiences:read`

**Rate limit:** 60 requests per minute

**Query parameters:**

| Param    | Type   | Required | Description                           |
|----------|--------|----------|---------------------------------------|
| `limit`  | number | No       | Results per page, default 25, max 100 |
| `offset` | number | No       | Number of results to skip             |

**Curl example:**

```bash
curl -s -G https://api.mokaru.ai/v1/experiences \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  --data-urlencode "limit=10" | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "jobTitle": "Senior Software Engineer",
      "company": "Acme Corp",
      "location": "San Francisco, CA",
      "startDate": "2022-07-01T00:00:00.000Z",
      "endDate": null,
      "isCurrent": true,
      "description": "Building and maintaining the core platform",
      "createdAt": "2026-01-10T...",
      "updatedAt": "2026-03-15T..."
    }
  ],
  "total": 4,
  "hasMore": false,
  "limit": 10,
  "offset": 0
}
```

**Note:** The list response does not include `responsibilities` or `achievements` - use `GET /v1/experiences/{id}` to fetch those.

---

### 20. Create Experience

**When to use:** The user wants to add a new work experience. They might say "add my new job at Acme" or "save this work experience."

**Method:** `POST /v1/experiences`

**Required scope:** `experiences:write`

**Rate limit:** 20 requests per minute

**Request body (JSON):**

| Field              | Type    | Required | Description                                    |
|--------------------|---------|----------|------------------------------------------------|
| `jobTitle`         | string  | Yes      | Job title (max 200 chars)                      |
| `company`          | string  | Yes      | Company name (max 200 chars)                   |
| `location`         | string  | No       | Work location (max 200 chars)                  |
| `startDate`        | string  | No       | Full ISO-8601 datetime (e.g. "2022-07-01T00:00:00.000Z") |
| `endDate`          | string  | No       | Full ISO-8601 datetime (omit for current position)        |
| `isCurrent`        | boolean | No       | Whether this is the current position            |
| `description`      | string  | No       | Role description                                |
| `responsibilities` | array   | No       | List of responsibilities (array of strings)    |
| `achievements`     | array   | No       | List of achievements (array of strings)        |

**Date format:** `startDate` and `endDate` must be full ISO-8601 datetimes (`YYYY-MM-DDTHH:mm:ss.sssZ`). A date-only string like `"2022-07-01"` will be rejected.

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/experiences \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Senior Software Engineer",
    "company": "Acme Corp",
    "location": "San Francisco, CA",
    "startDate": "2022-07-01T00:00:00.000Z",
    "isCurrent": true,
    "description": "Building the core platform",
    "responsibilities": ["Led frontend architecture"],
    "achievements": ["Reduced bundle size by 40%"]
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx..."
}
```

---

### 21. Get Experience Detail

**When to use:** The user wants to see full details of a specific work experience.

**Method:** `GET /v1/experiences/{id}`

**Required scope:** `experiences:read`

**Rate limit:** 30 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/experiences/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "id": "clx_abc123",
    "jobTitle": "Senior Software Engineer",
    "company": "Acme Corp",
    "location": "San Francisco, CA",
    "startDate": "2022-07-01T00:00:00.000Z",
    "endDate": null,
    "isCurrent": true,
    "description": "Building and maintaining the core platform",
    "responsibilities": ["Led frontend architecture"],
    "achievements": ["Reduced bundle size by 40%"],
    "createdAt": "2026-01-10T...",
    "updatedAt": "2026-03-15T..."
  }
}
```

---

### 22. Update Experience

**When to use:** The user wants to change details of a work experience. They might say "update my Acme job" or "I left that position, mark it as ended."

**Method:** `PATCH /v1/experiences/{id}`

**Required scope:** `experiences:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field              | Type         | Description                                    |
|--------------------|--------------|------------------------------------------------|
| `jobTitle`         | string       | Job title (max 200 chars)                                      |
| `company`          | string       | Company name (max 200 chars)                                   |
| `location`         | string/null  | Work location (max 200 chars, null to clear)                   |
| `startDate`        | string/null  | Full ISO-8601 datetime (null to clear)                         |
| `endDate`          | string/null  | Full ISO-8601 datetime (null to clear)                         |
| `isCurrent`        | boolean/null | Whether this is the current position (null to clear)            |
| `description`      | string/null  | Role description (null to clear)                               |
| `responsibilities` | array/null   | List of responsibilities (null to clear)                       |
| `achievements`     | array/null   | List of achievements (null to clear)                           |

**Date format:** `startDate` and `endDate` must be full ISO-8601 datetimes (`YYYY-MM-DDTHH:mm:ss.sssZ`). A date-only string will be rejected.

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/experiences/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "isCurrent": false,
    "endDate": "2026-03-15T00:00:00.000Z"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx_abc123"
}
```

Pass `null` for optional fields to clear them.

---

### 23. Delete Experience

**When to use:** The user wants to remove a work experience. They might say "delete that old job" or "remove the internship from my profile."

**Method:** `DELETE /v1/experiences/{id}`

**Required scope:** `experiences:write`

**Rate limit:** 10 requests per minute

**Curl example:**

```bash
curl -s -X DELETE https://api.mokaru.ai/v1/experiences/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

---

### 24. List Education

**When to use:** The user wants to see their education history. They might say "show my education" or "what schools do I have listed?"

**Method:** `GET /v1/education`

**Required scope:** `education:read`

**Rate limit:** 60 requests per minute

**Query parameters:**

| Param    | Type   | Required | Description                           |
|----------|--------|----------|---------------------------------------|
| `limit`  | number | No       | Results per page, default 25, max 100 |
| `offset` | number | No       | Number of results to skip             |

**Curl example:**

```bash
curl -s -G https://api.mokaru.ai/v1/education \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  --data-urlencode "limit=10" | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "institution": "Stanford University",
      "degree": "Bachelor of Science",
      "fieldOfStudy": "Computer Science",
      "location": "Stanford, CA",
      "startDate": "2018-09-01T00:00:00.000Z",
      "endDate": "2022-06-15T00:00:00.000Z",
      "isCurrent": false,
      "grade": "Magna Cum Laude",
      "createdAt": "2026-01-10T...",
      "updatedAt": "2026-03-15T..."
    }
  ],
  "total": 2,
  "hasMore": false,
  "limit": 10,
  "offset": 0
}
```

**Note:** The list response does not include `description` or `gpa` - use `GET /v1/education/{id}` to fetch those.

---

### 25. Create Education

**When to use:** The user wants to add education. They might say "add my Stanford degree" or "save this school to my profile."

**Method:** `POST /v1/education`

**Required scope:** `education:write`

**Rate limit:** 20 requests per minute

**Request body (JSON):**

| Field         | Type    | Required | Description                                    |
|---------------|---------|----------|------------------------------------------------|
| `institution`  | string  | Yes      | School or institution name (max 200 chars)                    |
| `degree`       | string  | Yes      | Degree type (max 200 chars)                                   |
| `fieldOfStudy` | string  | No       | Field of study (max 200 chars)                                |
| `location`     | string  | No       | Location of the school (max 200 chars)                        |
| `startDate`    | string  | No       | Full ISO-8601 datetime (e.g. "2018-09-01T00:00:00.000Z")      |
| `endDate`      | string  | No       | Full ISO-8601 datetime (omit if currently enrolled)           |
| `isCurrent`    | boolean | No       | Whether currently enrolled                                     |
| `description`  | string  | No       | Additional details                                             |
| `grade`        | string  | No       | Grade or honors (max 50 chars, e.g. "Magna Cum Laude")        |
| `gpa`          | number  | No       | GPA value                                                      |

**Date format:** `startDate` and `endDate` must be full ISO-8601 datetimes (`YYYY-MM-DDTHH:mm:ss.sssZ`). A date-only string will be rejected.

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/education \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "institution": "Stanford University",
    "degree": "Bachelor of Science",
    "fieldOfStudy": "Computer Science",
    "startDate": "2018-09-01T00:00:00.000Z",
    "endDate": "2022-06-15T00:00:00.000Z"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx..."
}
```

---

### 26. Get Education Detail

**When to use:** The user wants to see full details of a specific education entry.

**Method:** `GET /v1/education/{id}`

**Required scope:** `education:read`

**Rate limit:** 30 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/education/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "id": "clx_abc123",
    "institution": "Stanford University",
    "degree": "Bachelor of Science",
    "fieldOfStudy": "Computer Science",
    "location": "Stanford, CA",
    "startDate": "2018-09-01T00:00:00.000Z",
    "endDate": "2022-06-15T00:00:00.000Z",
    "isCurrent": false,
    "description": "Graduated with honors",
    "grade": "Magna Cum Laude",
    "gpa": 3.8,
    "createdAt": "2026-01-10T...",
    "updatedAt": "2026-03-15T..."
  }
}
```

---

### 27. Update Education

**When to use:** The user wants to change education details. They might say "update my degree" or "change the field of study."

**Method:** `PATCH /v1/education/{id}`

**Required scope:** `education:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field         | Type        | Description                                    |
|---------------|-------------|------------------------------------------------|
| `institution`  | string       | School name (max 200 chars)                                   |
| `degree`       | string       | Degree type (max 200 chars)                                   |
| `fieldOfStudy` | string/null  | Field of study (max 200 chars, null to clear)                 |
| `location`     | string/null  | Location of the school (max 200 chars, null to clear)         |
| `startDate`    | string/null  | Full ISO-8601 datetime (null to clear)                        |
| `endDate`      | string/null  | Full ISO-8601 datetime (null to clear)                        |
| `isCurrent`    | boolean/null | Whether currently enrolled (null to clear)                     |
| `description`  | string/null  | Additional details (null to clear)                            |
| `grade`        | string/null  | Grade or honors (max 50 chars, null to clear)                 |
| `gpa`          | number/null  | GPA value (null to clear)                                     |

**Date format:** `startDate` and `endDate` must be full ISO-8601 datetimes (`YYYY-MM-DDTHH:mm:ss.sssZ`).

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/education/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "degree": "Master of Science",
    "fieldOfStudy": "Machine Learning"
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx_abc123"
}
```

---

### 28. Delete Education

**When to use:** The user wants to remove an education entry. They might say "delete that school" or "remove my old degree."

**Method:** `DELETE /v1/education/{id}`

**Required scope:** `education:write`

**Rate limit:** 10 requests per minute

**Curl example:**

```bash
curl -s -X DELETE https://api.mokaru.ai/v1/education/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

---

### 29. List Skills

**When to use:** The user wants to see their skills. They might say "show my skills" or "what skills do I have?"

**Method:** `GET /v1/skills`

**Required scope:** `skills:read`

**Rate limit:** 60 requests per minute

**Query parameters:**

| Param      | Type   | Required | Description                                            |
|------------|--------|----------|--------------------------------------------------------|
| `limit`    | number | No       | Results per page, default 25, max 100                  |
| `offset`   | number | No       | Number of results to skip                              |
| `category` | string | No       | Filter by category: `TECHNICAL`, `SOFT`, or `LANGUAGE` |

**Curl example:**

```bash
curl -s -G https://api.mokaru.ai/v1/skills \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  --data-urlencode "limit=50" \
  --data-urlencode "category=TECHNICAL" | jq .
```

**Response shape:**

```json
{
  "data": [
    {
      "id": "clx...",
      "name": "TypeScript",
      "category": "TECHNICAL",
      "level": "expert",
      "score": 5,
      "displayOrder": 0,
      "isVisible": true,
      "categoryRelation": { "name": "programming", "labelEn": "Programming Languages" },
      "createdAt": "2026-01-10T...",
      "updatedAt": "2026-03-15T..."
    }
  ],
  "total": 12,
  "hasMore": false,
  "limit": 50,
  "offset": 0
}
```

The `category` field is the legacy enum (`TECHNICAL` / `SOFT` / `LANGUAGE`). The optional `categoryRelation` object holds an extended category definition (system-defined or user-defined) when the skill is linked to one.

---

### 30. Create Skill

**When to use:** The user wants to add a skill. They might say "add TypeScript to my skills" or "save this skill."

**Method:** `POST /v1/skills`

**Required scope:** `skills:write`

**Rate limit:** 20 requests per minute

**Request body (JSON):**

| Field      | Type   | Required | Description                                    |
|------------|--------|----------|------------------------------------------------|
| `name`     | string | Yes      | Skill name (max 200 chars)                                        |
| `category` | string | No       | One of: `TECHNICAL`, `SOFT`, `LANGUAGE`. Defaults to `TECHNICAL`. |
| `level`    | string | No       | Free-form proficiency label (max 50 chars, e.g. "expert")         |
| `score`    | number | No       | Integer 1-5 (higher means more proficient)                        |

**Curl example:**

```bash
curl -s -X POST https://api.mokaru.ai/v1/skills \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TypeScript",
    "category": "TECHNICAL",
    "level": "expert",
    "score": 5
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx..."
}
```

---

### 31. Get Skill Detail

**When to use:** The user wants to see details of a specific skill.

**Method:** `GET /v1/skills/{id}`

**Required scope:** `skills:read`

**Rate limit:** 30 requests per minute

**Curl example:**

```bash
curl -s https://api.mokaru.ai/v1/skills/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "data": {
    "id": "clx_abc123",
    "name": "TypeScript",
    "categoryLegacy": "TECHNICAL",
    "categoryId": null,
    "level": "expert",
    "score": 5,
    "displayOrder": 0,
    "isVisible": true,
    "createdAt": "2026-01-10T...",
    "updatedAt": "2026-03-15T..."
  }
}
```

**Note:** Unlike the list endpoint, the detail endpoint returns the raw database row. The enum category is on `categoryLegacy` (not remapped to `category`), and the optional extended category link is on `categoryId`.

---

### 32. Update Skill

**When to use:** The user wants to change a skill's details. They might say "change my TypeScript level to expert" or "update that skill's category."

**Method:** `PATCH /v1/skills/{id}`

**Required scope:** `skills:write`

**Rate limit:** 20 requests per minute

**Request body (JSON) - all fields optional, at least one required:**

| Field      | Type        | Description                                    |
|------------|-------------|------------------------------------------------|
| `name`         | string      | Skill name (max 200 chars)                                        |
| `category`     | string      | One of: `TECHNICAL`, `SOFT`, `LANGUAGE`                           |
| `level`        | string/null | Free-form proficiency label (max 50 chars, null to clear)         |
| `score`        | number/null | Integer 1-5 (null to clear)                                       |
| `isVisible`    | boolean     | Whether this skill shows on rendered resumes                       |
| `displayOrder` | number      | Integer position used for sorting skills                           |

**Curl example:**

```bash
curl -s -X PATCH https://api.mokaru.ai/v1/skills/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "level": "expert",
    "score": 5
  }' | jq .
```

**Response shape:**

```json
{
  "success": true,
  "id": "clx_abc123"
}
```

---

### 33. Delete Skill

**When to use:** The user wants to remove a skill. They might say "delete that skill" or "remove TypeScript from my profile."

**Method:** `DELETE /v1/skills/{id}`

**Required scope:** `skills:write`

**Rate limit:** 10 requests per minute

**Curl example:**

```bash
curl -s -X DELETE https://api.mokaru.ai/v1/skills/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

---

### 34. Delete Application

**When to use:** The user wants to remove an application from their tracker. They might say "delete that application" or "remove the Acme job from my tracker."

**Method:** `DELETE /v1/tracker/applications/{id}`

**Required scope:** `tracker:write`

**Rate limit:** 10 requests per minute

**Curl example:**

```bash
curl -s -X DELETE https://api.mokaru.ai/v1/tracker/applications/clx_abc123 \
  -H "Authorization: Bearer $MOKARU_API_KEY" | jq .
```

**Response shape:**

```json
{
  "success": true
}
```

The application is soft-deleted (marked as deleted but retained in the database). Timeline entries are preserved. Any linked resume is not modified.

---

## Workflows

### Finding, saving, and preparing for jobs

1. Optionally call `GET /v1/profile` to understand the user's background.
2. Call `POST /v1/jobs/search` with a query based on what the user asked for (or derived from their profile).
3. Present the results with the `applyLink` for each job.
4. If the user wants to save one, call `POST /v1/tracker/applications` with the job details and pass the job `id` as `jobListingId`. Add `"autoPrepare": true` to tailor their resume automatically.
5. To actually apply, the user must visit the `applyLink` themselves. Provide it clearly.

### Reviewing application pipeline

1. Call `GET /v1/tracker/applications` to get all applications, or filter by status.
2. Summarize the pipeline: how many in each status, which are highest priority.
3. If the user wants to update one, call `PATCH /v1/tracker/applications/{id}`.

### Managing contacts

1. Call `GET /v1/contacts` to list all contacts, or use `search` to find by name/company.
2. Call `GET /v1/contacts/{id}` for full contact details.
3. To add a new contact, call `POST /v1/contacts` with at least `firstName` and `lastName`.
4. To update contact info, call `PATCH /v1/contacts/{id}` with the fields to change. Pass `null` to clear optional fields.
5. To delete, call `DELETE /v1/contacts/{id}`.

### Managing work experiences

1. Call `GET /v1/experiences` to list all work experiences.
2. Call `GET /v1/experiences/{id}` to see full details of a specific experience.
3. To add a new experience, call `POST /v1/experiences` with at least `jobTitle` and `company`.
4. To update, call `PATCH /v1/experiences/{id}` with the fields to change. Pass `null` to clear optional fields.
5. To delete, call `DELETE /v1/experiences/{id}`.

### Managing education

1. Call `GET /v1/education` to list all education entries.
2. Call `GET /v1/education/{id}` to see full details of a specific education entry.
3. To add, call `POST /v1/education` with at least `institution` and `degree`.
4. To update, call `PATCH /v1/education/{id}` with the fields to change. Pass `null` to clear optional fields.
5. To delete, call `DELETE /v1/education/{id}`.

### Managing skills

1. Call `GET /v1/skills` to list all skills.
2. Call `GET /v1/skills/{id}` to see details of a specific skill.
3. To add a skill, call `POST /v1/skills` with at least `name`.
4. To update, call `PATCH /v1/skills/{id}` with the fields to change. Pass `null` to clear optional fields.
5. To delete, call `DELETE /v1/skills/{id}`.

### Managing resumes

1. Call `GET /v1/resume` to see all resumes and find the right one.
2. Call `GET /v1/resume/{id}` to read the full content of a resume.
3. To create a new resume, call `POST /v1/resume` with a name and optional content.
4. To update resume content (add skills, experiences, etc.), call `PATCH /v1/resume/{id}` with the fields to change.
5. To export as PDF, call `POST /v1/resume/{id}/export/pdf` and save the binary response to a file.
6. To delete, call `DELETE /v1/resume/{id}`. Linked applications are unlinked, not deleted.

---

## Error Handling

| Status | Meaning                  | What to do                                                        |
|--------|--------------------------|-------------------------------------------------------------------|
| 400    | Bad request / validation | Check the `details` field for which fields failed. Fix and retry. |
| 401    | Invalid or missing token | Tell the user their API key is invalid or expired.                |
| 403    | Insufficient permissions | The API key does not have the required scope for this endpoint.   |
| 404    | Not found                | The application or profile does not exist.                        |
| 409    | Processing               | Resume is being tailored by auto-prep. Wait and retry.            |
| 429    | Rate limited             | Wait before retrying. Do not hammer the endpoint.                 |
| 500    | Server error             | Retry once. If it persists, tell the user something went wrong.   |
| 503    | Service unavailable      | Rate limiter or export service is temporarily down. Retry after a short wait. |

Always check the HTTP status before parsing the response body. On errors, the body contains an `error` field with a human-readable message.

---

## Documentation

Full API documentation is available at [docs.mokaru.ai](https://docs.mokaru.ai).
