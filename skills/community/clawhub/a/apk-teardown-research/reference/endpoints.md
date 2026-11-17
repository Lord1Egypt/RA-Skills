# apk-teardown-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## AppInsights (6)

### `apk_teardown_compare_ownership`

- **HTTP:** `GET /apk-teardown/compare-ownership`
- **What:** Compare two apk-teardown jobs for evidence of common ownership. Compares two DIFFERENT completed jobs (not versions of the same app) for signals of common ownership -- shared signing certificate, SDK/analytics identifiers, and more.
- **Params:** `job_id_a` (string, **required**) — First completed job ID; copy data.job_id returned by POST /apk-teardown/jobs; `job_id_b` (string, **required**) — Second completed job ID; copy data.job_id returned by another POST /apk-teardown/jobs

### `apk_teardown_delete_job`

- **HTTP:** `DELETE /apk-teardown/jobs/{job_id}`
- **What:** Delete an apk-teardown job. Purges a job's metadata/result before its normal retention window expires. The uploaded binary is already gone by the time any job reaches a terminal state, so this only ever deletes job metadata, never a binary.
- **Params:** `job_id` (string, **required**) — Caller-owned job ID from data.job_id returned by POST /apk-teardown/jobs

### `apk_teardown_diff`

- **HTTP:** `GET /apk-teardown/diff`
- **What:** Diff two completed apk-teardown jobs. Compares two already-completed jobs -- typically two versions of the same app -- and returns what changed (permissions, signing, SDKs, size, and more).
- **Params:** `job_id_a` (string, **required**) — First completed job ID; copy data.job_id returned by POST /apk-teardown/jobs; `job_id_b` (string, **required**) — Second completed job ID; copy data.job_id returned by another POST /apk-teardown/jobs

### `apk_teardown_job_status`

- **HTTP:** `GET /apk-teardown/jobs/{job_id}`
- **What:** Poll an apk-teardown job's status/result. Returns the current status (queued, processing, done, failed, or lost) of a submitted job, and its full result once done.
- **Params:** `job_id` (string, **required**) — Job ID from data.job_id returned by POST /apk-teardown/jobs; the response also supplies poll_path

### `apk_teardown_submit`

- **HTTP:** `POST /apk-teardown/jobs`
- **What:** Submit an APK for static teardown analysis. Uploads a single .apk/.xapk file (up to 400MB), or set file_url to have the server fetch it from an https:// URL instead -- exactly one of "file" or "file_url" must be given, not both. Enqueues a Tier 1 static-analysis job -- manifest, permissions, signing, SDK detection, tech stack, locales, and more. Poll the returned poll_path for the result, or set webhook_url for push delivery. Identical uploads (by sha256) within 48h return the existing job instead of re-running analysis. file_url is validated (https only, must resolve to a public address -- no loopback/private/link-local targets) and every redirect hop is re-validated the same way before being followed.
- **Params:** _none_

### `apk_teardown_timeline`

- **HTTP:** `GET /apk-teardown/timeline`
- **What:** Build a version timeline across 2+ apk-teardown jobs. Compares 2+ completed jobs the caller asserts are versions of the same app and returns the consecutive pairwise diff for each version transition, sorted by version code.
- **Params:** `job_ids` (string, **required**) — Comma-separated list of 2+ completed job IDs copied from data.job_id values returned by POST /apk-teardown/jobs
