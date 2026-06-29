---
name: applytop
description: ApplyTop is a CLI + Node client for the ApplyTop public API — search the jobs pool and access your alerts, matches, saved jobs, and CVs, including AI ATS scoring, CV tailoring, and cover-letter generation, from the terminal or programmatically.
homepage: https://applytop.com
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":[],"env":["APPLYTOP_API_KEY"]}}}
---

# ApplyTop

Command-line interface **and** Node client for the [ApplyTop](https://applytop.com) public API. Search jobs and work with your alerts, matches, saved jobs, and CVs — including AI ATS scoring, CV tailoring, and cover-letter generation — from the terminal or your own code. Commands print JSON to stdout, so they pipe cleanly into `jq`.

## Install

The package is published on npm.

```bash
npm install -g applytop          # global install, gives you the `applytop` binary
# or run without installing:
npx applytop jobs:search -q engineer
```

Requires Node ≥ 18.

## ⚠️ Authentication Required

Every command except `auth:*` needs an API key, and **the API is an ApplyTop Pro feature**. Free accounts cannot create keys, and calls from a non-Pro account return `403 pro_required`.

1. Create a key at **https://applytop.com/dashboard/api-keys** (keys look like `at_live_…`).
2. Provide it in one of three ways — **precedence: `--api-key` flag > `APPLYTOP_API_KEY` env > saved file** (`~/.applytop/credentials.json`):

```bash
applytop auth:login                      # prompts for the key, validates it, saves it
applytop auth:login --api-key at_live_xxx
export APPLYTOP_API_KEY=at_live_xxx      # env var
applytop jobs:search -q engineer --api-key at_live_xxx   # per-command flag
```

Check / clear auth:

```bash
applytop auth:status      # key source, owner, tier
applytop auth:logout      # remove saved credentials
```

## ⚠️ Hard Rules

1. **Three commands cost 1 AI credit each:** `cvs:tailor`, `cvs:cover-letter`, `cvs:ats-score`. The credit is charged to the key owner. Everything else is free. A failed AI generation is automatically refunded. Check the balance first with `applytop account:credits`.
2. **`<jobId>` for the AI commands accepts a pool job id OR a matched-job id** — a job id from `jobs:search`, or one of your matched ids from `matches:list`. If you omit `--cv`, your default CV is used.

## Core Workflow

1. **Authenticate** — `auth:login` once (or set `APPLYTOP_API_KEY`).
2. **Discover** — `jobs:search` (public pool), `alerts:list` / `alerts:jobs`, or `matches:list` (your matched jobs).
3. **Inspect** — `jobs:get`, `matches:get`, `saved:list`, `cvs:list` / `cvs:get`.
4. **Act (costs credits)** — `cvs:ats-score`, `cvs:tailor`, `cvs:cover-letter`; download with `cvs:pdf`.
5. **Pipe** — every command emits JSON to stdout; chain with `jq`.

```bash
applytop jobs:search -q "react developer" --work-model remote --limit 5 | jq '.jobs[].title'
```

## Essential Commands

| Command | Description |
|---|---|
| `auth:login` | Save an API key (validates it). `--api-key`, `--api-url` |
| `auth:status` | Show authentication status (key source, owner, tier) |
| `auth:logout` | Remove the saved credentials |
| `account:me` | Your profile |
| `account:credits` | Your AI-credit balance and tier |
| `jobs:search` | Search the public jobs pool. `-q/--query`, `--country`, `--work-model`, `--type`, `--limit`, `--page` |
| `jobs:get` | One pool job. `--id` \| `--slug` |
| `alerts:list` | Your job alerts. `--limit`, `--offset`, `--status`, `--search` |
| `alerts:jobs <alertId>` | Matched jobs for one alert. `--limit`, `--min-score`, `--search` |
| `matches:list` | Your matched jobs across all alerts. `--min-score`, `--country`, `--work-model`, `--search`, `--sort-by`, `--limit`, `--offset` |
| `matches:get <matchId>` | One matched job, full detail |
| `saved:list` | Your saved jobs. `--limit`, `--offset`, `--country`, `--work-model`, `--search` |
| `cvs:list` | Your CVs (metadata) |
| `cvs:get <cvId>` | One CV, full detail |
| `cvs:pdf <cvId>` | Download a CV as PDF. `--template`, `-o/--output` |
| `cvs:ats-score <cvId>` | ATS score for a CV — **1 credit** |
| `cvs:tailor <jobId>` | CV tailored to a job — **1 credit**. `--cv`, `--template` |
| `cvs:cover-letter <jobId>` | Cover letter for a job — **1 credit**. `--cv`, `--hiring-manager` |

Global options: `--api-key <key>`, `--api-url <url>` (default `https://applytop.com/api/v1`), `--insecure` (dev-only, self-signed TLS), `--raw` (compact single-line JSON), `--version`, `--help`.

Run `applytop --help` or `applytop <command> --help` for full details.

## Common Patterns

**Search the pool, then tailor a CV to one result:**
```bash
JOB=$(applytop jobs:search -q "platform engineer" --work-model remote --limit 1 | jq -r '.jobs[0].id')
applytop cvs:tailor "$JOB"            # uses your default CV; costs 1 credit
```

**List strong matches and download a tailored PDF:**
```bash
applytop matches:list --min-score 70 --limit 10 | jq '.matches[] | {id, title, score}'
applytop cvs:pdf <cvId> --template modern -o resume.pdf
```

**Generate a cover letter for a matched job:**
```bash
applytop cvs:cover-letter <matchId> --hiring-manager "Jane Doe"   # 1 credit
```

**Programmatic use (the package also exports the client):**
```js
import { ApplyTop, ApplyTopError } from 'applytop';

const client = new ApplyTop({ apiKey: process.env.APPLYTOP_API_KEY });
const { jobs, total } = await client.jobsSearch({ q: 'engineer', work_model: 'remote', limit: 5 });

try {
  const result = await client.cvsTailorToJob({ jobId, cvId });   // 1 credit
  console.log(result.cvId, 'balance:', result.balance);
} catch (err) {
  if (err instanceof ApplyTopError && err.code === 'insufficient_credits') {
    console.error(`Need ${err.required}, have ${err.balance}`);
  } else throw err;
}
```
Client methods: `me()`, `credits()`, `jobsSearch()`, `jobsGet()`, `alertsList()`, `alertsJobs()`, `matchesList()`, `matchesGet()`, `savedList()`, `cvsList()`, `cvsGet()`, `cvsAtsScore()`, `cvsTailorToJob()`, `cvsCoverLetterForJob()`, `cvsDownloadPdf()` (resolves to a `Buffer`).

## Output & Errors

Success prints the response payload as JSON to **stdout** (exit `0`). Errors print `{ "error": { "code", "message", … } }` to **stderr** and exit `1`.

| Code | Meaning |
|---|---|
| `auth_required` / `invalid_api_key` | Missing / invalid key |
| `pro_required` | Account is not on ApplyTop Pro |
| `insufficient_credits` | Out of AI credits (includes `balance`, `required`, `tier`) |
| `premium_template_requires_pro` | A Pro-only PDF template on a free plan |
| `not_found` | Resource missing or not yours |
| `rate_limited` | Per-key rate limit (100/min) exceeded |

## Common Gotchas

- **Pro is mandatory.** No key can be created on a free account; live calls return `403 pro_required`.
- **Credits are charged to the key owner**, not the caller — and only for `cvs:tailor`, `cvs:cover-letter`, `cvs:ats-score`. Failed generations are auto-refunded.
- **Rate limit is 100 requests/min per key** → `rate_limited`. Back off and retry.
- **`--insecure` is for self-signed dev certs only.** Never use it against production.
- **`<jobId>` ≠ `<cvId>`.** The AI commands take a *job* id (pool or matched); pick the CV with `--cv` or fall back to your default.
- **Auth precedence** is `--api-key` > `APPLYTOP_API_KEY` > `~/.applytop/credentials.json` — a stray env var will override your saved login.

## Quick Reference

```bash
applytop auth:login                                  # save + validate key
applytop account:me                                  # profile
applytop account:credits                             # credit balance + tier
applytop jobs:search -q "react" --work-model remote  # search public pool
applytop jobs:get --slug some-job-slug               # one pool job
applytop alerts:list                                 # your alerts
applytop alerts:jobs <alertId> --min-score 60        # matched jobs for an alert
applytop matches:list --min-score 70 --limit 10      # your matches
applytop matches:get <matchId>                       # one match, full detail
applytop saved:list                                  # saved jobs
applytop cvs:list                                    # your CVs
applytop cvs:pdf <cvId> -o resume.pdf                # download CV PDF
applytop cvs:ats-score <cvId>                        # 1 credit
applytop cvs:tailor <jobId> --cv <cvId>              # 1 credit
applytop cvs:cover-letter <jobId>                    # 1 credit
```
