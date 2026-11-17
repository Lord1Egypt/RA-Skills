---
name: flashrev-ai-enrich
description: Use this skill when an AI agent needs to enrich a CSV lead list through the flashrev-ai-enrich npm CLI. Triggers on list enrichment, filling missing company or person fields, verifying or unlocking emails and phones, finding CEOs, executives, LinkedIn posts, matching companies or people to FlashRev IDs, Google search/news/maps lookups, scraping a page, or running an LLM over each row. Agents must run with `FLASHREV_ENRICH_AI_MODE=1`, call `schema --json`, use only live `funcName` values, and invoke each command with explicit `--capability FUNC_NAME --map ... --output ...`. For broad person enrich requests, run a profile + contact pipeline when supported; for contact-only requests, run only the requested contact capability. Avoid `--prompt` unless explicitly requested. Dry-run and sample preview are required before live runs unless already authorized.
---

# FlashRev AI Enrich

Use the `flashrev-ai-enrich` CLI to enrich CSV lead lists through FlashRev. The CLI does not send outreach messages. It reads CSV files, maps CSV columns to FlashRev capability inputs, validates the job with dry-run, previews enriched sample rows, then writes an enriched CSV.

## Commands

```
flashrev-ai-enrich init [--force]                              Write default config
flashrev-ai-enrich doctor [--no-api]                            Self-check Node / config / API
flashrev-ai-enrich tokens [--json]                              Show balance / total / used / plan
flashrev-ai-enrich token-history [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--limit N] [--json]
                                                                Show consumption log (auto-paginates)
flashrev-ai-enrich schema [--advanced|--all] [--json]           List production-backed capabilities (synced from backend at runtime).
                                                                Default view shows recommended product entries and category summaries;
                                                                --advanced lists all atoms by category, --all shows the raw registry
flashrev-ai-enrich plan --source X.csv [--goal contact|person|company|identity|all] [--contact-type email|phone|both] [--json] [--emit-jobs|--no-emit-jobs]
                                                                Recommend concrete follow-up capabilities from the CSV's non-empty
                                                                columns; JSON is read-only unless --emit-jobs is passed. 0 tokens
flashrev-ai-enrich dry-run  --source leads.csv (--capability ID | --job planned.job.json | --prompt "...") [--map ...] [--output ...] [--json]
                                                                Validate job and show run plan without calling backend. --json returns approvalReasons/wouldOverwrite
flashrev-ai-enrich run      --source leads.csv [--out X.csv] (--capability ID | --job F | --prompt "...") [--yes] [--concurrency N] [--sample-size N] [--sample-only] [--report-json [PATH]] [--guided] [--overwrite]
                                                                Real enrichment with sample preview. In AI mode stdout is JSON and progress is stderr
```

## Agent Execution Contract

Agent runtimes should treat this CLI as a schema-first structured tool, not a natural-language router.

Use this order for every non-trivial enrichment job:

1. Set `FLASHREV_ENRICH_AI_MODE=1`.
2. Run `flashrev-ai-enrich doctor --no-api`.
3. Run `flashrev-ai-enrich schema --json`.
4. Select one or more `funcName` values returned by the live schema. Each CLI command still runs exactly one `--capability`.
   For broad requests, prefer `flashrev-ai-enrich plan --source X.csv --json` (0 tokens): it returns
   ranked follow-up jobs with inferred `--map` values, argv, `approvalReasons[]`, output paths, and
   overwrite/high-volume boundaries — no need to parse human recommendation text. Add `--emit-jobs`
   only after file creation is acceptable.
5. Run `flashrev-ai-enrich tokens --json`.
6. Build explicit `--map` and `--output` flags from the CSV headers and the selected schema for each selected capability, or use job files emitted by `plan --emit-jobs`.
7. Run `flashrev-ai-enrich dry-run` for each selected capability before that capability's live run (`--json` is automatic in ai-mode). Read `approvalReasons[]`, `requiresApproval`, and `wouldOverwrite`.
8. Ask for approval unless the user already authorized `--yes`. Always stop for approval at the boundaries flagged by `plan --json` or `dry-run --json` (`approvalReasons[]` — contact cleartext unlock, `customer_api` egress, `--allow-internal-targets`, overwriting existing files, high-volume runs).
9. For agent-mediated approval, first run `flashrev-ai-enrich run --sample-only --sample-size 10 ... --yes` after the user approves spending sample tokens. Show the JSON `sample` to the user and continue with the full `run` only after approval.
10. Run `flashrev-ai-enrich run`, chaining each capability from the previous output CSV when multiple capabilities are needed. In AI mode, stdout is the structured result (output path, status counts, exact token spend); use `--report-json path` when a file copy is needed.
11. Report the final output path, per-capability status counts, row errors, and actual token spend from the run report / CLI summary and token history.

Rules for agents:

- Do not use `--prompt` by default. Use it only when the user explicitly requests prompt routing or does not want to choose a capability.
- Never invent capability IDs, input fields, or output fields. Use only the live `schema --json` response.
- Prefer explicit `--capability ID` even when the user's request is written in natural language.
- If a requested capability is missing from the live schema, say it is unavailable in the connected environment instead of guessing a hidden backend route.
- For a broad request such as "enrich this CSV" or "complete these people", enrich both person profile fields and contact fields when the CSV has a person identifier.
- For contact-only planning, use `plan --contact-type email|phone|both` when the user asks for one contact channel or both.
- If the request needs `customer_api`, confirm the destination domain before live `run`.
- If the request needs `--allow-internal-targets`, get separate explicit approval before using that flag.

## Supported starting signals

Use this section to decide whether the user's CSV has enough information to start enrichment. Treat it as product-level guidance; the live `schema --json` response remains authoritative for exact capability inputs, rules, and output fields.

Person enrich can start from:

| Signal strength | Accepted inputs |
|---|---|
| Best | `flashrev_person_id`, `person_linkedin_url`, `linkedin_url` |
| Strong | `email`, `phone` |
| Common | `full_name + company_name`, `first_name + last_name + company_name` |
| Better common | Name plus company plus `job_title` |
| Company context | Name plus `company_website`, `company_domain`, or `company_linkedin` |
| Lowest confidence | `company_name + job_title`; use top-one selection only after the user accepts ambiguity, then pass `--param allow_low_confidence_match=true` |

Company enrich can start from:

| Signal strength | Accepted inputs |
|---|---|
| Best | `flashrev_company_id`, `company_website`, `company_domain`, `company_linkedin` |
| Common | `company_name`, preferably with `company_country`, `company_city`, or `industry` when available |

Contact enrich can start from:

| Signal strength | Accepted inputs |
|---|---|
| Best | `flashrev_person_id`, `person_linkedin_url`, `linkedin_url` |
| Strong | `email`, `phone` |
| Common | `full_name + company_name`, `first_name + last_name + company_name`, or name plus company website/domain/LinkedIn |
| Role search | `company_name + job_title`; use only after the user accepts top-one selection, then pass `--param allow_low_confidence_match=true` |

Rules:

- Do not require normal users to provide FlashRev IDs; prefer LinkedIn, email, phone, or name plus company when IDs are absent.
- Treat email, phone, LinkedIn, and name plus company as identity signals for broad person enrichment, not as proof that the user only wants contact fields.
- If the user explicitly asks for contact-only output, route to the contact capabilities instead of profile enrichment.
- If no supported starting signal is present, ask for LinkedIn URL, email, phone, name plus company, or company plus job title before running enrichment.

## Required confirmations before real `run`

1. User has a FlashRev account with available tokens (`flashrev-ai-enrich tokens` → `remaining > 0`).
2. `FLASHREV_API_KEY` env var is set (generated from https://info.flashlabs.ai/settings/privateApps).
3. Source CSV path and output CSV path are confirmed.
4. `--capability ID` from live `flashrev-ai-enrich schema --json` is confirmed. Use `--prompt "<intent>"` only when the user explicitly asks for prompt routing.
5. Input mappings (`--map flashrev_field=csv_column`) cover at least one capability rule. Skipped only when `--prompt` is explicitly used and the LLM returns valid mappings (still subject to rule validation afterwards).
6. Output mappings (`--output csv_col=response_field`) or `--output-fields` are confirmed. Skipped only when `--prompt` is explicitly used and the LLM returned mappings, but always required for dynamic-output capabilities (e.g., `run_llm`, `scrape_and_extract`).
7. `dry-run --json` first to validate mappings, row count, planned API calls, effective concurrency, `approvalReasons[]`, and `wouldOverwrite`.
8. For agent workflows, prefer `run --sample-only --json --yes` after the user approves sample-token spend; show the returned `sample` JSON and continue to the full run only after approval.
9. Do not proceed past the sample preview (default 10 rows, configurable via `--sample-size N`) unless the user approves or `--yes` is set.
10. Existing output files require explicit approval and `--overwrite`.
11. `customer_api` and `--allow-internal-targets` each require separate explicit approval.

## Input modes

### A. CSV mode (typical batch)

```bash
flashrev-ai-enrich run \
  --source leads.csv --out leads.enriched.csv \
  --capability enrich_email \
  --map first_name=first_name --map last_name=last_name --map company_name=company \
  --output verified_email=verified_business_email \
  --yes
```

`--map` connects CSV column → capability input field; `--output` connects CSV output column → backend response field.

### B. Inline mode (single row test, no CSV)

```bash
flashrev-ai-enrich run \
  --capability verify_email \
  --input email=ada@example.com \
  --output ok=deliverable_email \
  --out out.csv --yes
```

In inline mode the `--input key=value` pairs are auto-mapped (no need for `--map`).

### C. Job file (for repeatable presets)

```bash
flashrev-ai-enrich run --source leads.csv --out out.csv --job enrich.job.json --yes
```

Job file shape:
```json
{
  "capability": "enrich_email",
  "inputMapping": {
    "first_name":  "first_name",
    "last_name":   "last_name",
    "company_name": "company"
  },
  "outputs": {
    "verified_business_email":  "verified_business_email",
    "all_verified_business_emails": "all_verified_business_emails"
  }
}
```

## Default person enrichment routing

When the user asks broadly to "enrich" a people CSV, do not stop at contact lookup. Treat the default outcome as person profile plus contact data when the CSV has a usable person identifier.

Preferred broad-person flow (plan-driven):

1. If the live schema exposes `enrich_person`, run it first — it resolves identity from any supported signal (phone, email, LinkedIn, name + company) and returns a People-detail-aligned full profile: stable anchors (`person_id`, `person_linkedin_url`), current role and company, location, skills, work/education history, plus contact data (`business_emails` / `personal_emails` / `phones`, `unlock_status` / `unlock_types`, `contact_billing_status`). **`enrich_person` unlocks email/phone contacts BY DEFAULT and this can spend contact credits (Credit orgs) or tokens (Token orgs)** — always dry-run and sample-preview before a live batch. Treat phone/email/LinkedIn as identity signals for this step, not as contact-only requests. If only `enrich_person_basic` is exposed, use that instead; if neither exists yet, run the fallback pipeline from the table below.
2. Run `flashrev-ai-enrich plan --source <previous out>.csv --json` and execute the planned jobs the user approves (`dry-run --job` then `run --sample-only --job`, then full `run --job`). Stop for approval on every `requiresApproval: true` entry and inspect `approvalReasons[]`.

Contact-only requests can use `plan --contact-type email|phone|both --json` or route directly to `enrich_email` / `enrich_phone` / `enrich_contact_waterfall`.

`enrich_person` contact-unlock rules:

- Contacts are ON by default. There is no agent-facing `include_contacts` input — do not invent one. Profile-only mode is controlled by backend Nacos configuration (`flashrev.open-enrich.person.include-contacts-default` / `-company-overrides`); if the user insists on "profile only, no contacts", explain that this is an ops-side backend switch and only run if the environment is already configured profile-only (rows then report `contact_billing_status=disabled`).
- To narrow contact types while contacts are enabled, pass a static param instead of a fake CSV column: `--param requested_types=email` or `--param requested_types=phone` (blank/omitted = both).
- `company_name`/`company_website`/`company_linkedin` + `job_title` is low-confidence top-candidate matching. Do not run it automatically. First ask the user to confirm they accept top1 person selection and possible contact unlock cost; only then pass `--param allow_low_confidence_match=true`.
- `contact_billing_status` per row: `ok` (all requested types billed or cached), `partial_billing_blocked` / `billing_blocked` (insufficient credits/tokens — cleartext is never returned for a blocked type), `disabled` (Nacos profile-only mode).

Fallback decision table (also used when the user names the outcome explicitly):

| User intent | Default capabilities |
|---|---|
| Broad person enrich, complete people, enrich this CSV | `enrich_person` when live schema exposes it; otherwise `enrich_contact_waterfall` + `get_person_job_title` + `get_person_current_company` + `get_person_location` |
| Contact info, emails and phones | `enrich_contact_waterfall` only |
| Emails only (contact-only) | `enrich_email` only |
| Phones or mobiles only (contact-only) | `enrich_phone` only |
| Full profile plus one contact type | `enrich_person` with `--param requested_types=email` (or `phone`) |
| Profile only, no contacts requested | `enrich_person` — but profile-only mode is a backend Nacos switch, not a request flag; see the contact-unlock rules above |

Apply these rules:

- Use only capabilities exposed by the live `schema --json` response. If one capability in the default pipeline is missing, skip that step and report it.
- Prefer `person_linkedin_url` / `linkedin_url` inputs when the CSV has a LinkedIn column. Otherwise use the strongest identity group available from the live schema.
- Chain outputs through intermediate CSV files and make the final file the last step's `--out`.
- Preserve earlier run results by giving each follow-up run distinct status and error columns, for example `job_title_enrich_status`, `current_company_enrich_status`, and `location_enrich_status`.
- Keep `flashrev_enrich_status` for the first/main contact run unless the user asks for custom status columns.

## Contact enrichment routing

Use explicit contact capabilities from the live schema:

| User intent | Capability |
|---|---|
| Emails only | `enrich_email` |
| Phones or mobiles only | `enrich_phone` |
| Emails and phones | `enrich_contact_waterfall`, only when live schema exposes it |
| Emails and phones, no waterfall in schema | Ask before running `enrich_email` and `enrich_phone` sequentially |

`enrich_email` and `enrich_phone` are still valid single-type contact capabilities. They use the backend contact lookup path for the requested contact type, so agents should keep using them for single-type requests instead of forcing `enrich_contact_waterfall`.

Do not require users to provide `flashrev_person_id`; normal users usually do not have it. Use the strongest available identity input:

| Input strength | Accepted inputs |
|---|---|
| Best | `person_linkedin_url` |
| Strong | `email`, `phone`, `flashrev_person_id` |
| Common | `full_name + company_name`, `first_name + last_name + company_name` |
| Better common | Name plus company plus `job_title` |
| Company role search | `company_name + job_title`, optionally with `company_website` or `company_linkedin`; requires user confirmation and `--param allow_low_confidence_match=true` |
| Explicit opt-in only | `job_title` only; use only if the live schema exposes an explicit low-confidence opt-in field and the user accepts top-one selection |

If none of those identity inputs are available, ask the user for a LinkedIn URL, email, phone, name plus company, or company plus job title before running contact enrichment.

### D. Prompt routing mode (ad-hoc human use; costs 1 extra token)

Skip `--capability` and describe the intent in natural language. The CLI sends the prompt + CSV columns + capability registry to `run_llm`, which returns JSON `{ funcName, inputMapping, outputMapping, reasoning }`; the CLI prints a Routing-decision block and then runs the resulting job through the normal dry-run / sample / run pipeline.

```bash
flashrev-ai-enrich run --source leads.csv --out leads.enriched.csv \
  --prompt "for each row, take the email column and verify it is a deliverable business email" \
  --yes
```

Rules of thumb when writing prompts:

- Name the CSV column explicitly ("take the **email** column"); vague prompts make the LLM return empty mappings.
- Describe the business outcome, not the capability name ("find the CEO" beats "use get_company_ceo").
- One capability per prompt — the LLM picks exactly one funcName.
- `--map` / `--output` on the command line override the LLM's choices; use them to lock specific columns while letting the LLM pick the capability.
- `--capability X --prompt "..."` together: `--capability` wins, `--prompt` is ignored with a stderr warning (no routing token charged).
- Unroutable prompts (e.g., "make me a sandwich") exit non-zero with the LLM's reasoning printed; zero rows run.

Agents must skip prompt routing unless the user explicitly requests it. `schema --json` plus explicit `--capability ID` is cheaper, faster, and deterministic.

For contact lookup, agents should use the contact routing table above and pass explicit `--capability`, never prompt routing.

## Status semantics (output CSV columns)

Every output CSV gets `flashrev_enrich_status` and `flashrev_enrich_error` columns:

| status | meaning |
|---|---|
| `success` | Got business data; charged per capability `unitPriceToken`. |
| `cached` | Hit contact-unlock dedup (same person/contact type already unlocked). 0 tokens. |
| `no_data` | Backend returned 200 but the requested output fields are empty / null. 0 tokens. |
| `failed` | HTTP error from backend, retries exhausted. 0 tokens. |

`Failed` count > 0 with `Tokens used` > 0 means some rows got SOMETHING from backend (charged) but not the specific output fields the user asked for.

## Cost reporting

`Summary` line in `run` output prints `(balance before → balance after)` — that delta is the **authoritative** amount charged for the row enrichments. Each row's individual `cost.tokens` reported by backend may be slightly off under high concurrency (known limitation; `token-history` is always exact).

Credit-based organizations: `enrich_person` / contact waterfall unlocks charge email/phone **credits** instead of tokens. The run summary prints a `Credits used` line (and `--report-json` includes `creditsUsed`) whenever credits were spent; per-row details come back in `cost.credits` / `cost.emailCredits` / `cost.phoneCredits`.

When `--prompt` is used, the Routing-decision block prints its own `routing cost: 1 token(s)` line. That 1 token is **not** included in the `Summary` `balance before → after` delta, since routing happens before the balance snapshot. Use `token-history` for the authoritative total after the run.

## Special capability: `customer_api`

`customer_api` does NOT call FlashRev backend — the CLI fetches the user-provided URL locally and parses the response. 0 tokens.

Inputs (via `--map <field>=<csv_col>` or `--input <field>=<value>`):

| field | required | default | notes |
|---|---|---|---|
| `url` | yes | — | target URL (alias: `endpoint`) |
| `method` | no | `GET` | HTTP method |
| `headers` | no | `{}` | JSON object of HTTP headers |
| `body` | no | — | string (sent as-is) or object (JSON-serialized; Content-Type defaults to application/json) |
| `params` | no | — | object of query-string params; appended to `url` |
| `timeout` | no | `30000` | milliseconds before AbortError |

The response JSON (or `{ text }` wrapper for non-JSON) becomes the row's enrichment data; map output columns via `--output csv_col=response_field` as usual. Useful for mixing 3rd-party APIs into the same enrichment workflow.

### Security warnings (read before using `customer_api` in an agent context)

`customer_api` lets the CLI send arbitrary HTTP requests with row-derived URL / headers / body. The target URL is **not** owned by FlashRev — it is whatever the user, prompt, or CSV column supplied. This creates two real risk surfaces an agent must mitigate:

1. **SSRF / internal-network probing.** A URL such as `http://127.0.0.1:8500/`, `http://169.254.169.254/latest/meta-data/iam/security-credentials/` (AWS/GCP/Azure cloud-metadata), or any RFC1918 address (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) can be used to reach internal services or exfiltrate cloud IAM credentials. The CLI **rejects these targets by default** (HTTP 403 `customer_api refuses internal / private target host`) along with `localhost`, IPv6 loopback `::1`, link-local `fe80::/10`, ULA `fc00::/7`, and non-`http(s)` schemes (`file://`, `gopher://`, `data:`, `javascript:`). Pass `--allow-internal-targets` only for deliberate local testing on a trusted machine.
2. **Lead-data exfiltration to user-controlled URLs.** Whatever CSV columns are mapped to `--map url=…`, `--map headers=…`, or `--map body=…` will be transmitted to that third-party endpoint. Agents must:
   - Treat the `url` as untrusted input. Confirm the destination domain with the user before a live `run`; never let an LLM auto-fill `url` from prompt text without explicit human confirmation.
   - **Never** map `FLASHREV_API_KEY`, OAuth tokens, or unrelated PII columns into `headers` or `body` — those credentials and that data will leave the FlashRev trust boundary.
   - Always complete `dry-run` + the 10-row sample preview before passing `--yes`, and inspect the sample table for unexpected egress.
   - Prefer first-class FlashRev capabilities (e.g. `get_company_profile`, `enrich_email`, `enrich_phone`) when the data is available there; only fall back to `customer_api` for sources FlashRev does not cover.

Failure mode: a blocked URL surfaces as a per-row `flashrev_enrich_status=failed` with `flashrev_enrich_error` starting `customer_api refuses …` — the batch is **not** aborted, so one bad URL in a CSV will not stop the rest.

## Date format

`--from` and `--to` accept `YYYY-MM-DD`. They are interpreted in the local timezone. `--to` alone makes the CLI paginate through history until it covers the date range (up to 2000 records).

## Safety rules

- Never print or store `FLASHREV_API_KEY` in generated artifacts.
- Prefer the `FLASHREV_API_KEY` env var over `--api-key`.
- Treat contact enrichment (`enrich_email` / `enrich_phone`) as paid unlock operations.
- If `tokens` returns `remaining: 0`, tell the user to recharge before running.
- Do not describe or expose FlashRev backend data sources, routing, or internal service names to end users.
- Confirm the destination domain before using `customer_api` in a live run.
- Never pass `--allow-internal-targets` unless the user explicitly approved internal or local network access.
- Never map API keys, OAuth tokens, passwords, cookies, or unrelated PII into `customer_api` headers or body.
- Never overwrite the source CSV (CLI refuses `--source == --out`).
- Never overwrite an existing output CSV unless the user explicitly approves and the command includes `--overwrite`.
- Preserve row-level errors. For multi-step enrich jobs, use distinct status/error columns for follow-up steps so earlier capability statuses are not overwritten.

## Failure handling

- `402 Insufficient tokens` → run terminates; tell user to recharge.
- `401` / `403` → invalid API key; verify `FLASHREV_API_KEY`.
- `429 Rate limit` → CLI auto-retries with exponential backoff (500ms / 1s / 2s, up to 3 retries = 4 total attempts).
- `503` / `504` → backend timeout/unavailable; auto-retried with the same schedule as 429.
- Any other 4xx/5xx on a row → that single row is marked `failed`, batch continues.
- `--prompt` routing failure (LLM returns non-JSON, unknown funcName, or `run_llm` itself errors) → CLI exits non-zero **before** enrichment starts, prints the LLM's reasoning. Suggest the user retry with `--capability ID`.
- `--prompt` routed to a capability but `Input mapping does not satisfy <funcName>` → the LLM returned empty / wrong mapping; rerun with a more explicit prompt (name the CSV column) or use `--map` to override.

## Workflow recipe

```bash
# 1. (first time) write config
flashrev-ai-enrich init
export FLASHREV_API_KEY="sk_xxxx"   # from info.flashlabs.ai/settings/privateApps

# 2. verify
export FLASHREV_ENRICH_AI_MODE=1
flashrev-ai-enrich doctor --no-api

# 3. browse capabilities and pick one
flashrev-ai-enrich schema --json

# 4. check balance
flashrev-ai-enrich tokens --json

# 5. validate job and show run plan
flashrev-ai-enrich dry-run --source leads.csv \
  --capability enrich_email \
  --map first_name=first_name --map last_name=last_name --map company_name=company

# 6. real run with sample preview
flashrev-ai-enrich run --source leads.csv --out out.csv \
  --capability enrich_email \
  --map first_name=first_name --map last_name=last_name --map company_name=company \
  --output verified_email=verified_business_email
# (preview shown, type 'y' to continue, or pass --yes to auto-confirm)

# 7. audit spend
flashrev-ai-enrich token-history --from 2026-05-01
```

### Shortcut for ad-hoc human use (prompt routing)

When the user does not know the capability name and is willing to spend 1 extra token to let the LLM pick:

```bash
# dry-run only routes (1 token) — no enrichment
flashrev-ai-enrich dry-run --source leads.csv \
  --prompt "find the CEO of each company"

# real run: 1 routing token + N rows
flashrev-ai-enrich run --source leads.csv --out out.csv \
  --prompt "find the CEO of each company" --yes
```

Agents should skip this and pass `--capability` directly.
