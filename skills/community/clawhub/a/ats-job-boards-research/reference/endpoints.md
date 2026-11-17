# ats-job-boards-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**30 endpoints across 1 platform group(s).**

## Jobs (30)

### `jobs_ashby_board`

- **HTTP:** `GET /jobs/ashby/board`
- **What:** List an organization's Ashby job board. Lists an organization's public Ashby board postings with inline detail (description, compensation when include_compensation=true). The org is the Ashby slug from its careers URL. An unknown org returns an empty board (Ashby does not 404).
- **Params:** `include_compensation` (boolean, optional) — Include compensation summary; `org` (string, **required**) — Ashby org slug (careers URL)

### `jobs_company_search`

- **HTTP:** `GET /jobs/company-search`
- **What:** Find which ATS a company uses by slug. Probes Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, Rippling, Teamtailor, and Pinpoint in parallel for a slug and reports the providers where it resolves to a non-empty board (with the open-role count and board URL). Workday is excluded (its board needs tenant + datacenter + site).
- **Params:** `slug` (string, **required**) — Company careers slug to probe

### `jobs_eightfold_board`

- **HTTP:** `GET /jobs/eightfold/board`
- **What:** List an Eightfold tenant's job board. Lists a company's public Eightfold AI job board, paged via limit/offset. tenant is the {tenant}.eightfold.ai subdomain from the careers URL; domain is the hiring organization's own domain (e.g. microsoft.com), also visible on the tenant's careers page.
- **Params:** `domain` (string, **required**) — Hiring organization domain; `limit` (integer, optional) — Page size, default 10, max 10 (upstream caps results per page regardless of a larger value); `location` (string, optional) — Filter: location contains; `offset` (integer, optional) — Page offset, default 0; `query` (string, optional) — Free-text search; `tenant` (string, **required**) — Eightfold tenant subdomain (careers URL)

### `jobs_eightfold_job`

- **HTTP:** `GET /jobs/eightfold/job`
- **What:** Get a single Eightfold position. Returns a single Eightfold position with its full HTML/text description. id is the position id from a board listing; tenant/domain as in the board endpoint.
- **Params:** `domain` (string, **required**) — Hiring organization domain; `id` (string, **required**) — Eightfold position id from a board listing; `tenant` (string, **required**) — Eightfold tenant subdomain

### `jobs_gem_board`

- **HTTP:** `GET /jobs/gem/board`
- **What:** List a company's Gem job board. Lists a company's public Gem (gem.com) board postings with inline detail (full HTML description, and compensation when the company publishes a pay range). The company is the Gem vanity URL slug from its careers URL.
- **Params:** `company` (string, **required**) — Gem vanity URL slug (careers URL)

### `jobs_greenhouse_board`

- **HTTP:** `GET /jobs/greenhouse/board`
- **What:** List a company's Greenhouse job board. Lists a company's public Greenhouse board postings in the shared Job shape. Set content=true to include each job's full HTML description in one call. The token is the company's Greenhouse board slug from its careers URL.
- **Params:** `content` (boolean, optional) — Include full HTML description per job; `token` (string, **required**) — Greenhouse board token (careers URL slug)

### `jobs_greenhouse_job`

- **HTTP:** `GET /jobs/greenhouse/job`
- **What:** Get a single Greenhouse job. Returns one Greenhouse job, identified by the board `token` and job `id`, both required. The response has the title, company, department, team, location and offices, workplace type, employment type, posting and apply URLs, posting date, compensation, and the description as HTML and plain text. An unknown token or id returns `404`.
- **Params:** `id` (string, **required**) — Greenhouse job id; `token` (string, **required**) — Greenhouse board token

### `jobs_hiring_signals`

- **HTTP:** `GET /jobs/hiring-signals`
- **What:** Aggregate hiring signals for a company's board. Aggregates a company's ATS board into a hiring snapshot: total open roles, breakdowns by department/location/title, remote share, and how many roles are new in the last 7/30 days — a leading indicator of company growth. Supply provider plus that provider's slug params (token / company / org / tenant+datacenter+site / domain). Breakdowns are computed over the fetched postings.
- **Params:** `board` (string, optional) — ukg job-board UUID; `company` (string, optional) — lever / smartrecruiters / workable / recruitee / rippling / personio / teamtailor / gem / pinpoint company slug; `datacenter` (string, optional) — workday datacenter shard; `domain` (string, optional) — icims careers domain / eightfold organization domain; `host` (string, optional) — oracle cloud host (*.oraclecloud.com); `org` (string, optional) — ashby org slug; `provider` (string, **required**) — ATS provider; `site` (string, optional) — workday / oracle career site; `tenant` (string, optional) — workday / eightfold tenant; `token` (string, optional) — greenhouse board token

### `jobs_icims_board`

- **HTTP:** `GET /jobs/icims/board`
- **What:** List an iCIMS tenant's job board. Lists a company's public iCIMS job board (served through the tenant's white-labeled careers domain, e.g. careers.costco.com — not the bare {company}.icims.com subdomain, which is an OAuth-gated employee portal), paged via page/limit, with the full description inline per job. domain is the tenant's careers domain from its careers URL.
- **Params:** `domain` (string, **required**) — iCIMS tenant careers domain (careers URL); `keywords` (string, optional) — Free-text keyword search; `limit` (integer, optional) — Page size, default 20, max 50; `location` (string, optional) — Filter: location contains; `page` (integer, optional) — Page number, default 1

### `jobs_icims_job`

- **HTTP:** `GET /jobs/icims/job`
- **What:** Get a single iCIMS job. Returns a single iCIMS job with its full HTML/text description, department, and benefits. id is the req_id/slug from a board listing; lang defaults to en-us.
- **Params:** `domain` (string, **required**) — iCIMS tenant careers domain; `id` (string, **required**) — iCIMS job req_id/slug from a board listing; `lang` (string, optional) — Language code, default en-us

### `jobs_lever_posting`

- **HTTP:** `GET /jobs/lever/posting`
- **What:** Get a single Lever posting. Returns one Lever posting, identified by the `company` slug and posting `id`, both required. The response has the title, department, team, location, workplace type, employment type, posting and apply URLs, posting date, compensation, and the description as HTML and plain text. An unknown company or id returns `404`.
- **Params:** `company` (string, **required**) — Lever company slug; `id` (string, **required**) — Lever posting id

### `jobs_lever_postings`

- **HTTP:** `GET /jobs/lever/postings`
- **What:** List a company's Lever postings. Lists a company's public Lever postings (detail is inline), optionally filtered by department, location, or remote. The company is the Lever slug from its careers URL.
- **Params:** `company` (string, **required**) — Lever company slug (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_oracle_board`

- **HTTP:** `GET /jobs/oracle/board`
- **What:** List an Oracle Recruiting (ORC) tenant's job board. Lists an Oracle Recruiting Cloud tenant's public requisitions, paged via limit/offset. host and site both come from the careers URL https://{host}/hcmUI/CandidateExperience/en/sites/{site}/ (host must be an *.oraclecloud.com hostname; site looks like CX_1). The listing carries a short description; use the single-job endpoint for full detail.
- **Params:** `host` (string, **required**) — Oracle Cloud host (careers URL, *.oraclecloud.com); `limit` (integer, optional) — Page size, default 25, max 50; `offset` (integer, optional) — Page offset, default 0; `search` (string, optional) — Free-text keyword search; `site` (string, **required**) — Oracle career site number

### `jobs_oracle_job`

- **HTTP:** `GET /jobs/oracle/job`
- **What:** Get a single Oracle Recruiting (ORC) requisition. Returns a single Oracle Recruiting requisition with its full HTML/text description (description, responsibilities, qualifications). id is the requisition Id from a board listing; host/site as in the board endpoint.
- **Params:** `host` (string, **required**) — Oracle Cloud host (*.oraclecloud.com); `id` (string, **required**) — Oracle requisition Id from a board listing; `site` (string, **required**) — Oracle career site number

### `jobs_personio_feed`

- **HTTP:** `GET /jobs/personio/feed`
- **What:** List a company's Personio job board. Lists a company's public Personio board feed in the shared Job shape with detail inline, optionally filtered by department, location, or remote. The company is the Personio subdomain from its careers URL https://{company}.jobs.personio.de/.
- **Params:** `company` (string, **required**) — Personio subdomain (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_phenom_board`

- **HTTP:** `GET /jobs/phenom/board`
- **What:** Search a Phenom People tenant's job board. Searches a company's public Phenom People career site (a white-labeled domain such as careers.whataburger.com or jobs.cvshealth.com). domain is the tenant's careers domain from its careers URL. Paged via offset/limit; limit is a best-effort page-size hint some tenants ignore, so count always reflects what actually came back.
- **Params:** `category` (string, optional) — Filter: category contains; `domain` (string, **required**) — Phenom tenant careers domain (careers URL); `keywords` (string, optional) — Free-text keyword search; `limit` (integer, optional) — Page size hint, default 10, max 100 (some tenants ignore this and return their own configured page size regardless); `location` (string, optional) — Filter: location contains; `offset` (integer, optional) — Page offset, default 0; `sort` (string, optional) — Sort order, default relevant

### `jobs_phenom_job`

- **HTTP:** `GET /jobs/phenom/job`
- **What:** Get a single Phenom People job. Returns a single Phenom People job with its full HTML/text description, category, and apply URL. domain is the tenant's careers domain (as in the board endpoint); id is the jobId/reqId from a board listing (e.g. JR10002958).
- **Params:** `domain` (string, **required**) — Phenom tenant careers domain; `id` (string, **required**) — Phenom job id from a board listing

### `jobs_pinpoint_board`

- **HTTP:** `GET /jobs/pinpoint/board`
- **What:** List a tenant's Pinpoint job board. Lists a tenant's public Pinpoint (pinpointhq.com) board postings with inline detail (full HTML description, key responsibilities, skills, and benefits, plus structured compensation when the tenant publishes a pay range). The company is the tenant subdomain from its careers URL https://{company}.pinpointhq.com/.
- **Params:** `company` (string, **required**) — Pinpoint tenant subdomain (careers URL)

### `jobs_recruitee_offer`

- **HTTP:** `GET /jobs/recruitee/offer`
- **What:** Get a single Recruitee offer. Returns a single Recruitee offer with its full HTML/text description and structured compensation when the board exposes it.
- **Params:** `company` (string, **required**) — Recruitee subdomain; `id` (string, **required**) — Recruitee offer id

### `jobs_recruitee_offers`

- **HTTP:** `GET /jobs/recruitee/offers`
- **What:** List a company's Recruitee offers. Lists a company's public Recruitee offers (detail is inline), optionally filtered by department, location, or remote. The company is the Recruitee subdomain from its careers URL https://{company}.recruitee.com/.
- **Params:** `company` (string, **required**) — Recruitee subdomain (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_rippling_board`

- **HTTP:** `GET /jobs/rippling/board`
- **What:** List a company's Rippling job board. Lists a company's public Rippling board postings (thin listing — title, department, work location). The company is the Rippling board slug from its careers URL https://ats.rippling.com/{company}/jobs. Detail (full description, employment type) is fetched per job via the single-job endpoint.
- **Params:** `company` (string, **required**) — Rippling board slug (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_rippling_job`

- **HTTP:** `GET /jobs/rippling/job`
- **What:** Get a single Rippling job. Returns a single Rippling job with its full HTML/text description, employment type, and work locations. The id is the job uuid from a listing.
- **Params:** `company` (string, **required**) — Rippling board slug; `id` (string, **required**) — Rippling job uuid

### `jobs_smartrecruiters_posting`

- **HTTP:** `GET /jobs/smartrecruiters/posting`
- **What:** Get a single SmartRecruiters posting. Returns one SmartRecruiters posting, identified by the `company` id and posting `id`, both required. The response has the title, department, location, employment type, posting and apply URLs, posting date, compensation, and the job ad description as HTML and text. Recruiter personal data is left out. An unknown company or id returns `404`.
- **Params:** `company` (string, **required**) — SmartRecruiters company id; `id` (string, **required**) — SmartRecruiters posting id

### `jobs_smartrecruiters_postings`

- **HTTP:** `GET /jobs/smartrecruiters/postings`
- **What:** List a company's SmartRecruiters postings. Lists a company's public SmartRecruiters postings, paged via limit/offset. The company is the SmartRecruiters identifier from its careers URL.
- **Params:** `company` (string, **required**) — SmartRecruiters company id (careers URL); `limit` (integer, optional) — Page size, default 100, max 100; `offset` (integer, optional) — Page offset, default 0

### `jobs_teamtailor_jobs`

- **HTTP:** `GET /jobs/teamtailor/jobs`
- **What:** List a company's Teamtailor job board. Lists a company's public Teamtailor board feed in the shared Job shape with detail inline, optionally filtered by department, location, or remote. The company is the Teamtailor subdomain from its careers URL https://{company}.teamtailor.com/.
- **Params:** `company` (string, **required**) — Teamtailor subdomain (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false)

### `jobs_ukg_board`

- **HTTP:** `GET /jobs/ukg/board`
- **What:** List a UKG Pro Recruiting tenant's job board. Lists a UKG Pro Recruiting (formerly UltiPro) tenant's public opportunities, paged via limit/offset. tenant and board both come from the careers URL https://recruiting.ultipro.com/{tenant}/JobBoard/{board}. Each posting carries a brief description inline.
- **Params:** `board` (string, **required**) — UKG job-board UUID (careers URL); `limit` (integer, optional) — Page size, default 25, max 50; `offset` (integer, optional) — Page offset, default 0; `search` (string, optional) — Free-text keyword search; `tenant` (string, **required**) — UKG tenant code (careers URL)

### `jobs_workable_posting`

- **HTTP:** `GET /jobs/workable/posting`
- **What:** Get a single Workable posting. Returns a single Workable posting with its full HTML/text description. The id is the posting shortcode from a listing.
- **Params:** `company` (string, **required**) — Workable account slug; `id` (string, **required**) — Workable posting shortcode

### `jobs_workable_postings`

- **HTTP:** `GET /jobs/workable/postings`
- **What:** List a company's Workable postings. Lists a company's public Workable postings in the shared Job shape, optionally filtered by department, location, or remote. The company is the Workable account slug from its careers URL https://apply.workable.com/{company}/. Detail (full description) is fetched per job via the single-posting endpoint.
- **Params:** `company` (string, **required**) — Workable account slug (careers URL); `department` (string, optional) — Filter: department contains; `location` (string, optional) — Filter: location contains; `remote` (boolean, optional) — Filter by remote (true or false); `search` (string, optional) — Free-text search

### `jobs_workday_board`

- **HTTP:** `GET /jobs/workday/board`
- **What:** List a Workday tenant's job board. Lists a company's public Workday (CXS) postings, paged via limit/offset. tenant, datacenter (wd1/wd3/wd5/...), and site all come from the careers URL https://{tenant}.wd5.myworkdayjobs.com/{site}.
- **Params:** `datacenter` (string, **required**) — Workday datacenter shard (wd1, wd3, wd5, ...); `limit` (integer, optional) — Page size, default 20, max 20; `offset` (integer, optional) — Page offset, default 0; `search` (string, optional) — Free-text search; `site` (string, **required**) — Workday career site; `tenant` (string, **required**) — Workday tenant

### `jobs_workday_job`

- **HTTP:** `GET /jobs/workday/job`
- **What:** Get a single Workday job. Returns a single Workday posting's full detail (description, location, req id). path is the externalPath from a board listing. tenant/datacenter/site as in the board endpoint.
- **Params:** `datacenter` (string, **required**) — Workday datacenter shard; `path` (string, **required**) — Job externalPath from a board listing; `site` (string, **required**) — Workday career site; `tenant` (string, **required**) — Workday tenant
