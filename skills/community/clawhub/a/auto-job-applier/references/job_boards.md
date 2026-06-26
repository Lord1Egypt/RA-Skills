# Job Boards Reference

Search URL patterns, form selectors, and browser automation tips for each major job board.
Use these to construct targeted web search queries, direct job search links, and to automate
form filling via the browser tool.

---

## India-Focused Boards

### Naukri.com
- **Search URL:** `https://www.naukri.com/{role}-jobs-in-{city}`
- **Example:** `https://www.naukri.com/python-developer-jobs-in-pune`
- **Web search query:** `site:naukri.com "{role}" "{skill}" jobs Pune`
- **Best for:** Mid/senior IT roles, large Indian companies
- **Apply method:** Form (redirect to company page or Naukri quick apply)
- **Browser notes:**
  - Quick Apply requires Naukri login
  - Most postings redirect to external ATS
  - Form selectors vary by company ATS
- **Common form selectors:**
  ```
  input[name="name"], input[placeholder*="name"]
  input[name="email"], input[type="email"]
  input[name="mobile"], input[type="tel"]
  textarea[name="coverLetter"]
  input[type="file"] (resume upload)
  ```

### LinkedIn India
- **Search URL:** `https://www.linkedin.com/jobs/search/?keywords={role}&location={city}`
- **Easy Apply filter:** Add `&f_AL=true`
- **Best for:** MNCs, startups, remote roles
- **Apply method:** Easy Apply (LinkedIn form) or External redirect
- **Browser notes:**
  - ⚠️ **Easy Apply requires active LinkedIn login session**
  - ⚠️ **Automated submission may violate LinkedIn ToS — default to manual**
  - External apply jobs redirect to company career pages (auto-fill works)
  - Easy Apply forms use React components — standard CSS selectors may not work
- **Recommendation:** List as "🔗 Manual (LinkedIn)" — navigate but don't submit

### Internshala
- **Search URL:** `https://internshala.com/jobs/{role}-jobs`
- **Best for:** Internships, entry-level, freshers
- **Apply method:** Form (Internshala's own)
- **Browser notes:**
  - Requires Internshala login
  - Application forms are standardized
  - Usually has: Why interested?, Availability, Cover letter

### Wellfound (AngelList)
- **Search URL:** `https://wellfound.com/role/l/{role}/{city}`
- **Best for:** Startups, equity roles
- **Apply method:** Form (standardized Wellfound form)
- **Browser notes:**
  - Clean, standardized application form
  - Usually: Name, Email, LinkedIn, Resume, Cover letter
  - Good candidate for auto-apply
- **Common form selectors:**
  ```
  input[name="name"]
  input[name="email"]
  input[name="linkedin"]
  textarea[name="coverLetter"]
  button[type="submit"]
  ```

### Instahyre
- **Best for:** Senior engineers, product managers in India
- **Apply method:** Profile-based (auto-apply via Instahyre profile)
- **Browser notes:** Requires login + profile setup

### Indeed India
- **Search URL:** `https://in.indeed.com/jobs?q={role}&l={city}`
- **Best for:** Broad coverage across all levels
- **Apply method:** Indeed Apply or External redirect
- **Browser notes:**
  - Indeed Apply is well-structured, good for automation
  - Multi-step wizard: Contact → Resume → Questions → Review
  - External jobs redirect to company ATS
- **Common form selectors (Indeed Apply):**
  ```
  input[id="input-firstName"]
  input[id="input-lastName"]
  input[id="input-email"]
  input[id="input-phone"]
  input[id="input-location"]
  textarea[id="input-coverLetter"]
  button[id="form-action-submit"]
  ```

---

## Global Boards

### LinkedIn (Global)
- **Search URL:** `https://www.linkedin.com/jobs/search/?keywords={role}&location={location}`
- **Best for:** International roles, networking
- **Browser notes:** Same as LinkedIn India — manual only by default

### Indeed (Global)
- **Search URL:** `https://www.indeed.com/jobs?q={role}&l={location}`
- **Browser notes:** Same structure as Indeed India

### Glassdoor
- **Search URL:** `https://www.glassdoor.com/Job/{role}-jobs-SRCH_KO0,{len}.htm`
- **Best for:** Salary info + job listings combined
- **Apply method:** External redirect (Glassdoor doesn't host applications)
- **Browser notes:** Always redirects to company page

### RemoteOK
- **Search URL:** `https://remoteok.com/remote-{role}-jobs`
- **Best for:** Remote-only roles globally
- **Apply method:** External redirect
- **Browser notes:** Links to company apply pages

### We Work Remotely
- **URL:** `https://weworkremotely.com/categories/remote-programming-jobs`
- **Best for:** Remote dev jobs
- **Apply method:** External redirect

---

## Effective Web Search Queries

Use these query templates with the `web_search` tool:

```
# General match
"{role}" "{top_skill}" jobs "{location}" 2026

# India-specific
"{role}" jobs Pune OR Mumbai OR Bangalore "{skill}" "apply now"

# Remote
"{role}" remote job "{skill1}" OR "{skill2}" hiring 2026

# Startup-focused
"{role}" startup job India "{skill}" equity

# With experience filter
"2-4 years" "{role}" "{skill}" jobs India

# LinkedIn targeted
site:linkedin.com/jobs "{role}" "{skill}" "{location}"

# Naukri targeted
site:naukri.com "{role}" "{skill}" jobs

# Indeed targeted
site:indeed.com "{role}" "{skill}" "{location}" "apply now"

# Company career pages
"{role}" "{skill}" careers "apply" "{location}" 2026

# Wellfound / startup boards
site:wellfound.com "{role}" "{skill}" OR site:instahyre.com "{role}"
```

---

## Apply Method Detection Heuristics

When the agent visits a job posting URL, classify the application method:

| URL Pattern | Method | Agent Behavior |
|---|---|---|
| `linkedin.com/jobs` | `manual-linkedin` | Navigate, don't submit |
| `*.indeed.com/viewjob` + "Apply Now" button | `auto-apply` | Fill Indeed Apply form |
| `naukri.com` + "Apply" button | `auto-apply` | Fill Naukri form |
| `wellfound.com` + "Apply" button | `auto-apply` | Fill Wellfound form |
| `careers.*` or `jobs.*` (company domain) | `auto-apply` | Fill company ATS form |
| `greenhouse.io`, `lever.co`, `workday.com` | `auto-apply` | Fill ATS form |
| `mailto:` link | `email` | Draft email for user |
| Any other external redirect | `manual-redirect` | Navigate, user completes |

---

## Common ATS Platforms and Their Form Patterns

### Greenhouse
- **URL pattern:** `boards.greenhouse.io/{company}/jobs/{id}`
- **Form selectors:**
  ```
  input[id="first_name"]
  input[id="last_name"]
  input[id="email"]
  input[id="phone"]
  textarea[id="cover_letter"]
  input[type="file"]  (resume upload)
  button[type="submit"]
  ```
- **Multi-step:** No, single page

### Lever
- **URL pattern:** `jobs.lever.co/{company}/{id}`
- **Form selectors:**
  ```
  input[name="name"]
  input[name="email"]
  input[name="phone"]
  input[name="urls[LinkedIn]"]
  input[name="urls[GitHub]"]
  textarea[name="comments"]
  input[type="file"]
  button[type="submit"]
  ```

### Workday
- **URL pattern:** `*.wd*.myworkdayjobs.com`
- **Browser notes:** Complex multi-step wizard, may require login
- **Recommendation:** Mark as manual — Workday forms are difficult to automate

### BambooHR
- **URL pattern:** `*.bamboohr.com/careers/{id}`
- **Form selectors:**
  ```
  input[id="firstName"]
  input[id="lastName"]
  input[id="email"]
  input[id="phone"]
  textarea[id="coverLetter"]
  ```

---

## Application Tracking Status Values (resumex.dev)

| Status | When to use |
|---|---|
| `wishlist` | Found job, not yet applied |
| `applied` | Application submitted |
| `interview` | Got a response / scheduled interview |
| `offer` | Received offer |
| `rejected` | Application rejected / no response after 4 weeks |
