---
name: flashrev-ai-enrich
description: Use this skill when an AI agent needs to enrich a CSV lead list through the flashrev-ai-enrich npm CLI (v1.0+). Triggers on requests involving list enrichment, filling missing company/person fields, verifying emails or phones, unlocking contact emails or phone numbers, finding company CEOs / executives / industry / employees / LinkedIn posts, matching companies or people to FlashRev IDs, Google search / news / maps lookups, scraping a single page, or running an LLM over each row. The CLI is a structured tool — agents should call `flashrev-ai-enrich schema` to discover the 34 capabilities, then invoke `run` with `--capability <funcName> --map ...` directly; `--prompt "..."` exists for ad-hoc human users and costs 1 extra token per invocation. All enrichment decisions and token deductions are owned by the FlashRev backend; the CLI never calls external data providers directly except for the special `customer_api` capability. Dry-run estimates and the 10-row sample preview must be completed before live runs unless the user passed `--yes`. Agents should invoke with `FLASHREV_ENRICH_AI_MODE=1` (or `--ai-mode`) so list outputs (`tokens` / `schema` / `token-history`) and error envelopes are JSON-structured.
---

# FlashRev AI Enrich

Use the `flashrev-ai-enrich` CLI to enrich CSV lead lists through FlashRev. The CLI does not send outreach messages. It reads CSV files, maps CSV columns to FlashRev capability inputs, estimates token cost via dry-run, previews enriched sample rows, then writes an enriched CSV.

## Commands

```
flashrev-ai-enrich init [--force]                              Write default config
flashrev-ai-enrich doctor [--no-api]                            Self-check Node / config / API
flashrev-ai-enrich tokens [--json]                              Show balance / total / used / plan
flashrev-ai-enrich token-history [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--limit N] [--json]
                                                                Show consumption log (auto-paginates)
flashrev-ai-enrich schema [--json]                              List 34 capabilities (synced from backend at runtime)
flashrev-ai-enrich dry-run  --source leads.csv (--capability ID | --prompt "...") [--map ...] [--output ...]
                                                                Estimate without calling backend
flashrev-ai-enrich run      --source leads.csv --out X.csv (--capability ID | --prompt "...") [--yes] [--concurrency N] [--sample-size N]
                                                                Real enrichment with sample preview. --prompt routes to a funcName via run_llm (1 extra token)
```

## Required confirmations before real `run`

1. User has a FlashRev account with available tokens (`flashrev-ai-enrich tokens` → `remaining > 0`).
2. `FLASHREV_API_KEY` env var is set (generated from https://info.flashlabs.ai/settings/privateApps).
3. Source CSV path and output CSV path are confirmed.
4. Either `--capability ID` (from `flashrev-ai-enrich schema`) or `--prompt "<intent>"` is confirmed. Agents should prefer `--capability ID` directly; `--prompt` is for ad-hoc human use because it costs 1 extra token to route through `run_llm`.
5. Input mappings (`--map flashrev_field=csv_column`) cover at least one capability rule. Skipped only when `--prompt` is used and the LLM returns valid mappings (still subject to rule validation afterwards).
6. Output mappings (`--output csv_col=response_field`) or `--output-fields` are confirmed. Skipped under `--prompt` if the LLM returned mappings, but always required for dynamic-output capabilities (e.g., `run_llm`, `scrape_and_extract`).
7. `dry-run` first to see estimated token cost and effective concurrency.
8. Do not proceed past the sample preview (default 10 rows, configurable via `--sample-size N`) unless the user approves or `--yes` is set.

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

Agents calling this CLI should usually skip prompt routing entirely — `schema` + explicit `--capability ID` is cheaper, faster, and deterministic. Prompt routing is for humans at a terminal.

## Status semantics (output CSV columns)

Every output CSV gets `flashrev_enrich_status` and `flashrev_enrich_error` columns:

| status | meaning |
|---|---|
| `success` | Got business data; charged per capability `unitPriceToken`. |
| `cached` | Hit `unlock_contact` dedup (same `person_id` already unlocked). 0 tokens. |
| `no_data` | Backend returned 200 but the requested output fields are empty / null. 0 tokens. |
| `failed` | HTTP error from backend, retries exhausted. 0 tokens. |

`Failed` count > 0 with `Tokens used` > 0 means some rows got SOMETHING from backend (charged) but not the specific output fields the user asked for.

## Cost reporting

`Summary` line in `run` output prints `(balance before → balance after)` — that delta is the **authoritative** amount charged for the row enrichments. Each row's individual `cost.tokens` reported by backend may be slightly off under high concurrency (known limitation; `token-history` is always exact).

When `--prompt` is used, the Routing-decision block prints its own `routing cost: 1 token(s)` line. That 1 token is **not** included in the `Summary` `balance before → after` delta, since routing happens before the balance snapshot. Total user cost per `--prompt` run = 1 routing token + (rows × capability unitPriceToken).

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
   - Prefer first-class FlashRev capabilities (e.g. `get_company_profile`, `enrich_email`) when the data is available there; only fall back to `customer_api` for sources FlashRev does not cover.

Failure mode: a blocked URL surfaces as a per-row `flashrev_enrich_status=failed` with `flashrev_enrich_error` starting `customer_api refuses …` — the batch is **not** aborted, so one bad URL in a CSV will not stop the rest.

## Date format

`--from` and `--to` accept `YYYY-MM-DD`. They are interpreted in the local timezone. `--to` alone makes the CLI paginate through history until it covers the date range (up to 2000 records).

## Safety rules

- Never print or store `FLASHREV_API_KEY` in generated artifacts.
- Prefer the `FLASHREV_API_KEY` env var over `--api-key`.
- Treat email / phone enrichment (`enrich_email` / `enrich_phone`) as paid unlock operations.
- If `tokens` returns `remaining: 0`, tell the user to recharge before running.
- Do not describe or expose FlashRev backend data sources, routing, or internal service names to end users.
- Never overwrite the source CSV (CLI refuses `--source == --out`).
- Preserve row-level errors in `flashrev_enrich_status` and `flashrev_enrich_error` columns.

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
flashrev-ai-enrich doctor

# 3. browse capabilities and pick one
flashrev-ai-enrich schema | less

# 4. (optional) check balance
flashrev-ai-enrich tokens

# 5. estimate cost
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
