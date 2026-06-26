# Service Profiles — Observed Operating Behavior

Each entry: safe pattern, known failure modes, first observed date.

---

## Yahoo Finance

- **Endpoint:** `query2.finance.yahoo.com` — preferred. `query1` rate-limits faster.
- **Auth:** None — User-Agent header required (`Mozilla/5.0 ...`)
- **Safe pattern:** Sequential requests, 0.6s sleep between tickers
- **Never:** Parallel requests — triggers 429 immediately
- **Cache:** 5 minutes minimum — serve from cache whenever possible
- **Crypto:** Use CoinGecko instead — single batch call, more reliable
- **Script:** `scripts/fetch-prices.py` wraps all of this automatically
- **First observed:** 2026-04-17

---

## CoinGecko

- **Endpoint:** `api.coingecko.com/api/v3/simple/price`
- **Auth:** None on free tier
- **Safe pattern:** Batch all coins in one call — `ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true`
- **Free tier:** Generous — rarely rate-limits on normal usage
- **Cache:** 5 minutes via `fetch-prices.py`
- **First observed:** 2026-04-17

---

## Ghost Admin API

- **Endpoint:** `https://<site>.ghost.io/ghost/api/admin/`
- **Auth:** JWT token generated fresh each call from Admin API key
- **Key location:** your credentials file → field `key` (format: `{"key": "<id>:<secret>"}`)
- **Permission wall:** Integration tokens cannot write to `/settings/` — owner-only. Browser automation required for code injection and theme uploads.
- **Image uploads:** Python `requests` only — curl multipart breaks on macOS zsh
- **First observed:** 2026-03-17

---

## ClawHub API

- **Endpoint:** `https://clawhub.ai/api/v1/skills`
- **Auth:** Bearer token from your credentials file
- **Safe pattern:** Python `requests` with multipart — `data={"payload": json.dumps(payload)}` + `files=[...]`
- **Never:** curl — JSON quoting breaks silently on zsh, returns `Invalid JSON payload` every time
- **Never:** Browser importer — intermittent server errors, unreliable
- **First observed:** 2026-03-18

---

## Telegram Bot API

- **Pattern:** Use OpenClaw `message` tool — never raw curl
- **File delivery:** `sendDocument` endpoint for PDFs and media
- **Rate limits:** 30 messages/second global, 1 message/second per chat
- **First observed:** 2026-03-14

---

## Replicate (FLUX image gen)

- **Auth:** API token via OpenClaw config
- **Error quirk:** "Less than $5.0 in credit" error message is unreliable — check dashboard for real balance
- **Cost:** FLUX 1.1 Pro ~$0.02–0.04/image — $15 balance = 350–700 images. Never needs a top-up for normal usage.
- **First observed:** 2026-03-19

---

## OpenAI API

- **Endpoint:** `api.openai.com/v1/`
- **Auth:** Bearer token — `Authorization: Bearer sk-...`
- **Rate limits:** Tier-dependent. Free tier: 3 RPM / 200 RPD. Tier 1+: 500–3,500 RPM depending on model. Check `x-ratelimit-remaining-requests` response header.
- **Token limits separate from request limits:** A single request can burn your TPM ceiling without hitting RPM. Watch both.
- **Safe pattern:** Exponential backoff on 429. Header `retry-after` tells you exactly how long to wait — use it.
- **Streaming vs. non-streaming:** Both count equally against rate limits. Streaming does NOT get preferential treatment.
- **Model-specific ceilings:** GPT-4o has lower RPM than GPT-4o-mini on the same tier. Always check the model's specific limit, not the account's general limit.
- **Never:** Parallel requests on free/tier-1 — you'll 429 immediately and waste retries
- **Cache:** Cache completions aggressively. Same prompt = same response at temperature 0. Save tokens and money.
- **First observed:** 2026-04-18

---

## Anthropic API

- **Endpoint:** `api.anthropic.com/v1/messages`
- **Auth:** `x-api-key` header — not Bearer format
- **Rate limits:** Two separate ceilings: RPM (requests per minute) AND TPM (tokens per minute). Hitting either triggers 429.
- **TPM is usually the binding constraint** — a single large context window can eat your TPM budget before RPM becomes relevant
- **Model-specific limits:** Haiku has higher RPM/TPM ceilings than Sonnet, which has higher than Opus. Route cheap tasks to Haiku.
- **Prompt caching:** Prefix caching cuts token cost 90% on cached portions. Cache prefix must be identical to the character — a single token difference breaks the cache.
- **Safe pattern:** Check `x-ratelimit-remaining-tokens` and `x-ratelimit-remaining-requests` headers on every response
- **Streaming:** Use streaming for long responses — avoids gateway timeouts on responses > 30s
- **Never:** Assume Haiku limits apply to Sonnet or vice versa — they're tracked independently
- **First observed:** 2026-04-18

---

## GitHub API

- **Endpoint:** `api.github.com`
- **Auth:** `Authorization: Bearer <PAT>` — classic or fine-grained PAT
- **Primary rate limit:** 5,000 req/hr authenticated. 60 req/hr unauthenticated. Check `x-ratelimit-remaining` header.
- **Secondary rate limits (the real gotcha):** Separate from the primary limit. Triggered by: too many write operations in a short window, too many concurrent requests, too many requests to a single endpoint. Returns 403, not 429.
- **Safe pattern:** Sequential writes with 1s sleep between. Never fire parallel POST/PATCH/DELETE calls.
- **Search API:** Separate limit — 30 req/min authenticated, 10 unauthenticated. Completely independent of the main 5,000/hr.
- **GraphQL:** Single endpoint `api.github.com/graphql` — counts as one request regardless of query complexity, but has its own point budget
- **Pagination:** Always paginate — default page size is 30, max 100. Never assume you got all results on page 1.
- **Never:** Use unauthenticated requests for anything beyond occasional public repo reads
- **First observed:** 2026-04-18

---

## Brave Search API

- **Endpoint:** `api.search.brave.com/res/v1/web/search`
- **Auth:** `X-Subscription-Token` header
- **Model:** Credit-based, NOT rate-based. Each query costs credits regardless of response size.
- **Free tier:** 2,000 queries/month. Does not reset on 429 — it hard-stops when credits are exhausted.
- **Failure mode:** Returns 429 when monthly credits are gone. This is a budget wall, not a speed wall — waiting does not help. Credits reset on billing date.
- **Safe pattern:** Cache results aggressively. Same query within a session = serve from cache, don't re-query.
- **No retry value on 429:** Unlike most APIs, retrying a Brave 429 immediately is useless — you're out of credits, not over a speed limit.
- **Results freshness:** `freshness` param accepts `day`, `week`, `month`, `year` — use it to filter stale results on time-sensitive queries
- **First observed:** 2026-04-18

---

## Serper (Google Search API)

- **Endpoint:** `google.serper.dev/search`
- **Auth:** `X-API-KEY` header
- **Model:** Credit-based. Free tier: 2,500 credits. Each search = 1 credit.
- **Failure mode:** Returns 403 when credits exhausted. Credits don't reset — must purchase more.
- **Safe pattern:** Batch intent before querying. One well-crafted query beats three exploratory ones.
- **Result types:** `/search` (web), `/images`, `/news`, `/places`, `/scholar` — each costs 1 credit regardless of type
- **Never:** Fire exploratory parallel queries — each one costs a credit whether useful or not
- **vs. Brave:** Serper returns Google results (higher coverage), Brave returns Brave index (more privacy-friendly, often enough for research). Use Brave first, Serper when Google coverage matters.
- **First observed:** 2026-04-18

---

## Notion API

- **Endpoint:** `api.notion.com/v1/`
- **Auth:** Bearer integration token + `Notion-Version: 2022-06-28` header (required)
- **Rate limit:** 3 requests/second per integration. Hard wall — 429 with no retry-after header.
- **Safe pattern:** 350ms sleep between requests. Never parallel.
- **Pagination:** All list endpoints are paginated — `has_more` + `next_cursor` pattern. Max page size: 100. Always loop until `has_more: false`.
- **Block vs. page:** Fetching a page gives you metadata only, not content. Content lives in blocks — separate `GET /blocks/{id}/children` call required.
- **Write quirk:** Appending blocks is additive — there's no replace operation. To update content you must delete existing blocks first, then append.
- **Never:** Assume a page fetch includes body content — it never does
- **First observed:** 2026-04-18

---

## Airtable API

- **Endpoint:** `api.airtable.com/v0/<base_id>/<table_name>`
- **Auth:** `Authorization: Bearer <personal-access-token>`
- **Rate limit:** 5 requests/second per base. Across all tables in that base combined.
- **Safe pattern:** 200ms sleep between requests. Batch reads using `filterByFormula` instead of fetching all and filtering client-side.
- **Pagination:** `offset` token in response — keep fetching until no offset returned. Default page size: 100 records.
- **Bulk writes:** No true bulk insert. Create up to 10 records per request via array in `records` field. 10 at a time, sleep between batches.
- **Formula quirk:** `filterByFormula` uses Airtable formula syntax, not SQL. Strings need curly braces: `{Field Name} = 'value'`
- **Never:** Fetch all records then filter in code — use `filterByFormula` to push filtering server-side
- **First observed:** 2026-04-18

---

## Stripe API

- **Endpoint:** `api.stripe.com/v1/`
- **Auth:** Bearer token (secret key) — separate test and live keys, never mix environments
- **Rate limit:** 100 read requests/second, 100 write requests/second. Rarely hit in normal agent workflows.
- **Idempotency keys (critical):** Always pass `Idempotency-Key` header on POST requests. Same key = same result, safe to retry. Without it, a network timeout can trigger duplicate operations.
- **Test vs. live:** Test keys hit a completely separate environment. Test mode objects don't exist in live mode. Never assume an ID from test works in live.
- **Pagination:** Cursor-based — `starting_after` and `ending_before` params. Default 10 objects, max 100.
- **Webhooks:** Verify `Stripe-Signature` header on every incoming webhook — do not trust unverified events.
- **Safe pattern:** Always use idempotency keys on writes. Log the key with the request so you can retry safely.
- **Never:** Mix test and live keys, or skip idempotency keys on sensitive operations
- **First observed:** 2026-04-18

---

## HuggingFace Inference API

- **Endpoint:** `api-inference.huggingface.co/models/<model-id>`
- **Auth:** `Authorization: Bearer hf_...`
- **Free tier:** Rate-limited, no hard quota published — in practice ~10-30 req/min before throttling
- **Cold start (the real issue):** Models on free tier spin down when idle. First request after idle returns 503 with `{"error": "Model ... is currently loading"}` and an `estimated_time` field in seconds. This is NOT a failure — wait and retry.
- **Safe pattern:** On 503 with `estimated_time`, sleep that many seconds + 5s buffer, then retry once. If still 503, wait another 30s.
- **Never:** Treat a loading 503 as a hard failure — it's a cold start, not an error
- **Dedicated endpoints:** If you need reliable latency, use Inference Endpoints (paid) — no cold starts, dedicated hardware
- **Model-specific behavior:** Some models require specific input formats. Always check the model card before querying a new model.
- **First observed:** 2026-04-18

---

## Firecrawl

- **Endpoint:** `api.firecrawl.dev/v1/scrape` (single URL) or `/v1/crawl` (multi-page)
- **Auth:** `Authorization: Bearer fc-...`
- **Model:** Credit-based. Free tier: 500 credits/month. Single scrape = 1 credit. Crawl = 1 credit per page crawled.
- **JS rendering:** Enabled by default — adds 3-8s latency per page vs. static fetch. Use `formats: ["markdown"]` to get clean LLM-ready output.
- **vs. web_fetch:** Firecrawl handles JS-rendered pages, paywalls, and complex layouts. Use web_fetch for simple static pages — faster and free. Escalate to Firecrawl when web_fetch returns garbled or incomplete content.
- **Crawl vs. scrape:** `/scrape` is one URL, instant response. `/crawl` is async — returns a job ID, poll `/v1/crawl/<id>` until `status: completed`.
- **Safe pattern:** Scrape first. Only crawl if you need multiple pages from the same domain.
- **Never:** Use `/crawl` when `/scrape` is sufficient — crawl burns credits per page
- **First observed:** 2026-04-18
