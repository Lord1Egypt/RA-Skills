# Prompt Request

Use this file if you want to re-implement Audible Goodreads Deal Scout without using this repository's code directly.

The first sections are for humans: what the skill is trying to do and why it exists. The later sections are for a coding agent: contracts, edge cases, implementation boundaries, and acceptance criteria.

## Human Intention

Build a small, selective reading-deal workflow.

The workflow should help a reader notice the few Audible deals that are actually worth attention because they clear a public quality bar, match the reader's Goodreads library or Want-to-Read shelf, or fit the reader's stated taste.

It should not feel like a deal feed. It should feel like a careful filter: fewer notifications, better relevance, and clear reasons.

The product posture is important:
- The system reports opportunities only.
- It does not buy, reserve, check out, redeem credits, manage subscriptions, or complete purchases.
- Any purchase decision stays manual and outside the workflow.

## Human Scope

The workflow should support three related jobs:

1. Daily deal check:
   Fetch today's Audible daily promotion, compare it with Goodreads and optional personal context, then recommend, suppress, or report an error.
2. Want-to-Read discount scan:
   Use a Goodreads CSV to scan books on the user's Want-to-Read shelf against Audible US and report visible discounts or member-visible cash prices when optional Audible auth is configured.
3. Setup and diagnostics:
   Help a user create config, verify local paths, check auth readiness, inspect CSV headers, and understand what data the workflow reads or writes.

The workflow should not:
- Become a general Audible scraper.
- Build account-login browser automation.
- Auto-buy anything.
- Store mutable state inside the installed skill folder.
- Depend on private infrastructure, local machine names, tunnel names, or unpublished credentials.

## Best User Setup

The workflow works with public data only, but the best setup uses:

- The official Goodreads library CSV export.
- Short taste notes, written or dictated by the user, or drafted by an AI from favorite books, disliked books, preferred genres, pacing, tone, and themes.
- Optional Audible authentication only when the user wants member-visible cash prices in Want-to-Read scans.

If the user does not want personalization, the daily deal flow should still work from public Goodreads data only.

## Trust And Data Access

Make data access explicit and narrow.

The workflow may read:
- A config file.
- A Goodreads CSV, only when configured.
- A notes file or pasted notes, only when configured.
- Audible daily deal, search, and product pages.
- A local Audible auth file, only when the user explicitly creates and supplies one.
- Goodreads public pages for public rating resolution and optional rating enrichment.
- OpenClaw CLI state only for delivery, cron, and diagnostics.

The workflow may write:
- Config, artifacts, reports, cache, and state under a workspace storage directory.
- Optional delivery messages through a configured OpenClaw channel.
- Optional cron entries when daily automation registration is requested.

Default storage should be:

```text
<workspace>/.audible-goodreads-deal-scout/
```

Do not store mutable config, cache, auth, state, or artifacts under the installed skill directory, because skill updates may replace that folder.

## Implementation Model

Implement this as a ClawHub / OpenClaw skill-style staged workflow, not as one monolithic prompt.

The daily deal path has four stages:

1. Prepare:
   Fetch and parse Audible deterministically, load optional local inputs, apply local short-circuit rules, and write artifacts.
2. Runtime:
   Let the agent resolve Goodreads public evidence and write compact fit text. Return JSON only.
3. Finalize:
   Validate runtime JSON, apply decision rules, and render the final message.
4. Optional delivery:
   Apply delivery policy, send through OpenClaw if requested, and mark scheduled emissions safely.

The Want-to-Read scan is a separate manual command:

1. Load Goodreads CSV.
2. Select current `to-read` rows.
3. Search Audible conservatively.
4. Parse visible prices or optional authenticated prices.
5. Render compact Markdown and structured JSON.

The core design choice is deterministic first, model second. The model should not scrape Audible or decide control flow that can be handled locally.

## Required Inputs

Minimum daily deal inputs:
- Audible marketplace, default `us`.
- Goodreads score threshold, default `3.8`.

Optional daily deal inputs:
- Goodreads CSV path.
- Notes file or inline notes.
- Privacy mode: `normal` or `minimal`.
- Invocation mode: `manual` or `scheduled`.
- State file for duplicate scheduled suppression.
- Artifact directory.
- Delivery policy.
- Delivery channel and target.

Minimum Want-to-Read scan inputs:
- Goodreads CSV path with `to-read` shelf data.
- Audible marketplace `us` for v1.

Optional Want-to-Read scan inputs:
- `--limit N`
- `--offset N`
- `--scan-order newest|csv|oldest|random`
- `--seed TEXT`
- `--max-requests N`
- `--request-delay SECONDS`
- `--min-discount-percent N`
- `--output-json PATH`
- `--output-md PATH`
- `--include-non-deals`
- `--verbose`
- `--progress plain|json|none`
- `--progress-interval SECONDS`
- `--refresh-cache`
- `--no-cache`
- `--offline-fixtures PATH`
- `--title TEXT --author TEXT` for a single-book debug scan
- `--audible-auth-path PATH` for optional authenticated price lookup

## Daily Deal Prepare Rules

Apply these rules in order:

1. Resolve config and storage paths.
2. Validate the Audible marketplace.
3. Resolve notes text. If a configured notes file is missing, return `error_missing_notes_file`.
4. Validate the configured Goodreads CSV path. If explicitly configured and missing, return `error_missing_csv`.
5. Fetch the current Audible daily promotion with browser-like headers:
   - a normal browser User-Agent
   - `Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8`
   - `Accept-Encoding: gzip, deflate`
   - `Accept-Language: en-US,en;q=0.9`
6. Guard unauthenticated Audible fetches before network access: allow only HTTPS Audible daily-deal, search, and product URLs on known Audible marketplace hosts unless a deliberate debug override is used.
7. Use an `auto` fetch backend by default: try the Python fetch path first, then fall back to browser-like `curl` for recoverable Audible HTTP failures such as Python-client `503`, `403`, `429`, or gateway errors. Preserve diagnostics including backend, HTTP status, final URL, attempts, and fallback reason in prepare metadata.
8. Retry transient daily-promotion failures and temporary no-active-promotion parses before returning a suppression or error.
9. Parse title, author, product id, URL, summary, genres, runtime, year, sale price, list price, and hidden/member-price signals where visible.
10. Compute a deal key from marketplace, store-local date, and product id.
11. In scheduled mode, suppress a duplicate if the same deal key was already emitted.
12. Load Goodreads CSV if configured.
13. Validate CSV column overrides against actual detected headers before parsing.
14. Classify exact shelf matches locally.
15. If matching is ambiguous for the same title, return `error_ambiguous_personal_match`.
16. If exact shelf is `read`, return `suppress_already_read`.
17. If exact shelf is `currently-reading`, return `suppress_currently_reading`.
18. If exact shelf is `to-read`, keep the run active. This is positive evidence and can override the public Goodreads threshold later.
19. Build compact personal artifacts only when privacy allows it.
20. Always write a fresh `prepare-result.json`, including `ready`, `suppress`, and `error` outcomes.

The last rule is critical. A failed current-day prepare must never leave a stale previous-day `artifacts/current/prepare-result.json` behind. A fresh prepare must also remove stale downstream current artifacts, including `runtime-output.json`, `run-and-deliver-result.json`, and `mark-emitted-result.json`, so old delivery results are not visible as current.

## Daily Deal Runtime Contract

The runtime step must read prepared artifacts and return JSON only:

```json
{
  "schemaVersion": 1,
  "goodreads": {
    "status": "resolved | no_match | lookup_failed",
    "url": "string | null",
    "title": "string | null",
    "author": "string | null",
    "averageRating": "number | null",
    "ratingsCount": "integer | null",
    "evidence": "string | null"
  },
  "fit": {
    "status": "written | not_applicable | unavailable",
    "sentence": "string | null"
  }
}
```

Runtime rules:
- Prefer Goodreads book pages over author, list, review, or discussion pages.
- Verify title and author before trusting a Goodreads score.
- Use `lookup_failed` when Goodreads could not be checked.
- Use `no_match` when Goodreads was checked but no confident matching book page was found.
- If `privacyMode` is `minimal`, do not use raw CSV, detailed taste artifacts, review-source artifacts, or notes.
- If fit text is written, make it compact: roughly 2 or 3 short sentences, about 45 to 90 words.
- Mention one likely appeal and one credible limitation when useful.
- Do not invent taste evidence.

## Daily Deal Finalize Rules

Finalize maps prepare/runtime data into one user-facing decision.

Final statuses:
- `recommend`
- `suppress`
- `error`

Core final reason codes:
- `recommend_to_read_override`
- `recommend_public_threshold`
- `suppress_below_goodreads_threshold`
- `suppress_no_goodreads_match`
- `error_goodreads_lookup_failed`

Rules:
1. If prepare returned `suppress` or `error`, finalize that result directly.
2. If Goodreads status is `lookup_failed`, return an error.
3. If Goodreads status is `no_match`, suppress.
4. If exact shelf is `to-read`, recommend even if the public threshold is not met.
5. Otherwise recommend only when Goodreads average rating is greater than the configured threshold.
6. Suppress when Goodreads average rating is less than or equal to the threshold.
7. If fit writing is unavailable, use a fallback fit line and keep the decision.

Keep the final message concise and structured:
- marketplace and store date
- title, author, and year when known
- price and discount when known
- Goodreads rating and rating count when resolved
- runtime and genre when known
- short Audible description
- fit paragraph or fallback fit line
- Audible link
- Goodreads link when available

## Scheduled Delivery Safety

Scheduled runs need stricter safety than manual runs.

Rules:
- `run-and-deliver` must refuse scheduled prepare results whose status is `error`.
- `run-and-deliver` must refuse stale scheduled artifacts when `metadata.storeLocalDate` does not equal the current Audible marketplace date.
- `mark-emitted` must mark only the deal key from the same current scheduled prepare artifact that was actually delivered.
- Do not mark emitted from an arbitrary loose deal key unless it matches the current artifact.
- Manual runs should not be blocked by duplicate scheduled state.

These rules prevent a failed current-day prepare from sending a stale previous-day recommendation.

## Delivery Policies

Delivery policy should be explicit:

- `positive_only`: send only recommendations.
- `always_full`: send the full message for recommend, suppress, and error results.
- `summary_on_non_match`: send full recommendations and short summaries for suppress or error results.

Delivery should use the user's configured OpenClaw channel and target. Do not assume Telegram, WhatsApp, or any specific target unless configured.

## Privacy Modes

`normal`:
- The runtime may receive compact fit context, review-source context, and notes artifacts when configured.
- Personal context should be used only for the fit paragraph and local shelf rules.

`minimal`:
- The prepare layer may use local shelf data for deterministic decisions.
- Do not write or expose detailed personal fit artifacts to the runtime.
- Do not expose raw notes or raw Goodreads review text to the runtime.
- Runtime output should use public Goodreads evidence and summary metadata only.

Privacy must be enforced by data minimization, not just by prompt instructions.

## Want-To-Read Scan Scope

The Want-to-Read scan is a manual audit, not continuous monitoring.

It should answer:

```text
Among the Want-to-Read books I scan right now, which ones visibly look discounted on Audible?
```

V1 constraints:
- US Audible marketplace only unless explicitly extended later.
- No cron.
- No delivery.
- No long-lived "already scanned forever" state.
- No account browser automation.
- No hidden-price chasing through secondary buying-choice UI.
- No product-page fetch unless a search card already shows plausible numeric discount evidence or visible current/list prices that need confirmation.
- Use offset and limit for large backlogs instead of persistent scan progress state.

Recommended backlog usage:

```bash
scan-want-to-read --scan-order newest --limit 40 --offset 0
scan-want-to-read --scan-order newest --limit 40 --offset 40
scan-want-to-read --scan-order newest --limit 40 --offset 80
```

## Want-To-Read Selection

Selection rules:

1. Load the Goodreads CSV.
2. Resolve relevant headers with tolerant defaults and validated overrides.
3. Filter rows whose effective shelf is `to-read`.
4. Deduplicate within the current report by Goodreads book id when present, otherwise normalized title plus author.
5. Sort by requested scan order:
   - `newest`
   - `oldest`
   - `csv`
   - `random`
6. For random ordering, use a deterministic seed for the current invocation only.
7. Apply offset.
8. Scan up to limit.

If the CSV changes, simply re-read it on the next invocation. Do not require a strict CSV fingerprint for resume.

## Want-To-Read Matching

Keep matching conservative and deterministic.

Search:
- One Audible search request per Goodreads book.
- Search URL shape for US: `https://www.audible.com/search?keywords=<title author>`.
- Parse only the first search page.
- Inspect the first three result cards.
- Try card 2 and card 3 if card 1 is unrelated.

Candidate acceptance:
- Accept exact normalized title match, or exact after subtitle/series stripping.
- Require exact or strong partial visible author agreement.
- Use Goodreads primary author as the main author.
- Additional Goodreads authors may improve confidence but should not hide a primary author mismatch.
- Missing search-card author should usually be `needs_review`, not an excuse for identity-only product fetch.

Do not overbuild v1:
- Do not solve all translated editions.
- Do not auto-accept abridged, dramatized, omnibus, podcast, course, or adaptation variants without warnings.
- Do not use narrator names as positive author evidence.
- Do not treat ISBN as a guaranteed audiobook match; it is rare supporting evidence at most.

## Want-To-Read Pricing

Statuses:
- `discounted`
- `available_no_discount`
- `price_hidden`
- `price_unknown`
- `needs_review`
- `not_found`
- `lookup_failed`

Pricing fields should include:
- `currencyCode`
- `currentPrice`
- `listPrice`
- `discountPercent`
- `pricingStatus`
- `priceBasis`
- `dealType`

Distinguish:
- `dealType: limited_time_sale` or similar when there is a visible sale/promotion signal.
- `dealType: member_cash_below_list` when authenticated member cash price is below list but not clearly a limited-time sale.
- `priceBasis: audible_public_cash` for anonymous visible cash prices.
- `priceBasis: audible_member_cash` for authenticated member-visible cash prices.
- `priceBasis: unknown` when pricing cannot be trusted.

Do not classify credit prices as cash discounts. Ignore Kindle, print, Amazon cross-sell, subscription, and membership prices when parsing Audible prices.

Classify hidden prices honestly:
- credit-only UI
- member-only cash UI
- buy-with-credit UI
- included-with-membership language
- cash price hidden behind "More Buying Choices"

Those should become `price_hidden` or `price_unknown`, not fake discounts.

## Optional Audible Authentication

Audible authentication is optional and separate from normal daily deal usage.

Rules:
- Do not ask for the user's Audible or Amazon password.
- Use an external-browser auth flow with `audible-auth-start` and `audible-auth-finish`.
- In `audible-auth-start`, tell the user to open the login URL in a browser.
- In `audible-auth-finish`, accept the final redirect URL from the browser address bar, even if the browser shows an error or not-found page.
- Store auth under the workspace storage directory, for example `.audible-goodreads-deal-scout/audible-auth.json`.
- Treat the auth file as sensitive local state because it persists bearer access/refresh token fields. The auth flow may request cookie-style Audible/Amazon credential types for compatibility, but status output must not expose token contents.
- Never print token contents.
- Use `audible-auth-status` to check expiry, allowed-use metadata, and file permissions.
- Restrict authenticated use in code to token refresh, validated Audible product ids, and allowlisted Audible/Amazon API domains.

Authenticated Want-to-Read scans should:
- Use authenticated price lookup only when `--audible-auth-path` is supplied.
- Usually spend one search request plus one authenticated price request for each matched title.
- Treat authenticated discounted results as member-visible cash prices below list, not proof of a limited-time sale unless the data also says that.

## Want-To-Read Request Budget And Cache

Request accounting:
- `--max-requests` counts live network requests, not rows.
- Search request = 1.
- Product page request = 1.
- Authenticated price request = 1.
- Cache hit = 0.
- Check the remaining budget before each live request.
- If the budget is exhausted, stop cleanly and render a partial report.

Cache:
- Use a parsed HTTP/result cache under `.audible-goodreads-deal-scout/cache/audible/`.
- Cache search results, product pricing, authenticated pricing, and failures.
- Use short TTLs for failures and prices; longer TTLs for search results.
- `--refresh-cache` ignores cache reads but still writes fresh cache entries.
- `--no-cache` disables cache reads and writes.
- Cached block-like failures should not trigger the live circuit breaker.

Circuit breaker:
- Treat HTTP 403, HTTP 429, CAPTCHA markers, robot-check markers, and automated-access markers as block-like.
- Abort after repeated live block-like failures.
- Abort after too many ordinary live network failures.
- Render partial results when possible.

Exit codes:
- `0`: completed selected rows, or ordinary per-row failures with a completed report.
- `1`: config, input, or output error.
- `2`: request budget exhausted before selected rows were completed.
- `3`: Audible block-like circuit breaker opened.

## Want-To-Read Progress And Reports

Progress:
- Emit progress to stderr, not stdout.
- Support human-readable progress.
- Support JSONL progress for agents.
- Support silence with `--progress none`.
- Include selected rows, completed rows, request budget, discounted count, needs-review count, hidden/unknown counts, not-found count, failed count, and current title when useful.

JSON report should include:
- `schemaVersion`
- `status`
- `reasonCode`
- `generatedAt`
- `marketplace`
- `csvPath`
- `selection`
- `requestBudget`
- `counts`
- `warnings`
- `results`

Each result should include:
- Goodreads: row key, book id, title, author, average rating, date added, ISBN, ISBN13.
- Audible: title, author, URL, product id.
- Pricing: currency code, current price, list price, discount percent, pricing status, price basis, deal type.
- Decision: status, match status, match reason, warnings, search URL.

Markdown default:
- Print compact Markdown to stdout.
- Show only discounted Want-to-Read titles, capped at 20.
- Include summary counts for hidden, unknown, needs review, not found, and failed.
- Do not flood the report with non-deals by default.

With `--include-non-deals`:
- Include compact Needs Review, Price Hidden, and Not Found sections, each capped.

With `--verbose`:
- Include search URLs and candidate notes.

Ranking:
- Discount percent descending.
- Goodreads average rating descending.
- Newest date added.

Goodreads rating enrichment:
- CSV average ratings should be used when present.
- If missing, optionally enrich a small number of discounted rows from public Goodreads book pages by Goodreads book id.
- This should be bounded by a configurable limit.
- Allow users to disable this page fetch when they want no Goodreads enrichment.

## Diagnostics And Setup Helpers

Implement user-facing helper commands equivalent to:
- `setup`
- `doctor`, including optional live `--check-audible-fetch` host probe
- `show-csv-headers`
- `measure-context`
- `prepare`
- `finalize`
- `run-and-deliver`
- `mark-emitted`
- `scan-want-to-read`
- `audible-auth-start`
- `audible-auth-finish`
- `audible-auth-status`
- `audible-auth-test-price`
- `publish-audit`

Setup should return `nextSteps` with concrete commands for:
- doctor
- checking the daily deal
- scanning Want-to-Read if a CSV is configured
- optional Audible auth

Doctor should check:
- config path
- CSV path
- notes path
- auth file path and permissions
- cache directory
- delivery channel and target
- cron settings
- OpenClaw binary
- bundled shell wrapper

Publish audit should check:
- required public files
- ClawHub skill metadata
- `.clawhubignore`
- generated/private artifact exclusions
- obvious private marker leaks
- required trust and license files

## Artifact Expectations

The prepare step should persist machine-readable artifacts so runtime and finalize can be run separately.

Always persist:
- `prepare-result.json`

For ready outcomes, also persist:
- `audible.json`
- `personal-data.json`
- `runtime-input.json`
- `runtime-prompt.md`
- `runtime-output-schema.json`

When personalization is allowed, also persist:
- compact `fit-context.json`
- `review-source.json` when reviews exist
- `preferences.md` when notes exist

When `privacyMode` is `minimal`, omit detailed personal fit artifacts.

## Stable Contracts

Prepare statuses:
- `ready`
- `suppress`
- `error`

Common prepare reason codes:
- `ready_public`
- `ready_notes`
- `ready_full`
- `suppress_no_active_promotion`
- `suppress_duplicate_scheduled_run`
- `suppress_already_read`
- `suppress_currently_reading`
- `error_missing_notes_file`
- `error_missing_csv`
- `error_csv_unreadable`
- `error_ambiguous_personal_match`
- `error_audible_blocked`
- `error_audible_fetch_failed`
- `error_audible_parse_failed`
- `error_unsupported_marketplace`

Final statuses:
- `recommend`
- `suppress`
- `error`

Core final reason codes:
- `recommend_to_read_override`
- `recommend_public_threshold`
- `suppress_below_goodreads_threshold`
- `suppress_no_goodreads_match`
- `error_goodreads_lookup_failed`

Scheduled-delivery safety reason codes:
- `error_scheduled_prepare_failed`
- `error_stale_scheduled_prepare_result`
- `error_scheduled_prepare_date_unavailable`

The exact string set may grow, but do not erase these distinctions.

## Guardrails

- Prefer deterministic parsers and local validation over model guessing.
- Do not hide uncertainty. Use `lookup_failed`, `no_match`, `price_hidden`, `price_unknown`, or `needs_review` when appropriate.
- Do not silently ignore missing explicitly configured files.
- Do not silently accept invalid CSV override headers.
- Do not expose raw personal artifacts in minimal privacy mode.
- Do not rely on prompt obedience alone for privacy.
- Do not use personal data for anything unrelated to the user's configured book-deal workflow.
- Do not include local paths, auth tokens, cache files, generated artifacts, or machine names in published examples.
- Do not ship test suites, generated artifacts, caches, auth files, or private/internal docs in public ClawHub bundles.
- Keep output short and useful. This is not a review blog.
- Keep examples generic and public-safe.

## Tests And Acceptance Criteria

Daily deal tests:
- Prepare succeeds from fixture Audible HTML.
- Prepare retries transient no-active-promotion/fetch failures.
- Browser-like Audible headers are used.
- Every prepare outcome writes a fresh `prepare-result.json`.
- Missing notes file errors explicitly.
- Missing CSV errors explicitly.
- Invalid CSV header override errors explicitly.
- Minimal privacy mode omits personal fit artifacts.
- Read/currently-reading suppress before runtime.
- To-read exact match can override public threshold.
- Scheduled duplicate suppression does not affect manual runs.
- Scheduled `run-and-deliver` refuses error prep results.
- Scheduled `run-and-deliver` refuses stale store-local dates.
- `mark-emitted` validates the delivered prepare artifact.

Want-to-Read tests:
- CSV `to-read` extraction and dedupe.
- Scan order, offset, limit, and seed behavior.
- Extra irrelevant CSV columns do not break parsing.
- Request budget counts live requests, not rows.
- Product pages are fetched only for discount-like cards or needed price confirmation.
- Missing search-card author does not trigger identity-only product fetch.
- Hidden prices become `price_hidden`.
- Cached block failures do not trip the circuit breaker.
- Top-three card inspection works when the first result is unrelated.
- Markdown default stays compact.
- JSON includes all relevant statuses and warnings.
- Progress output is separated from final report output.
- Offline fixture mode performs no live network calls.
- Authenticated pricing distinguishes member cash below list from limited-time promotions.

Acceptance:
- A fixture CSV with 5 Want-to-Read books produces deterministic JSON and Markdown.
- One numeric discount ranks first.
- Non-deals do not flood default Markdown.
- Offset and limit let a large backlog be scanned predictably.
- All tests run offline.

## Reimplementation Prompt

Use this as a compact prompt if handing the project to a coding agent:

```text
Implement a ClawHub / OpenClaw skill-style workflow called Audible Goodreads Deal Scout.

The skill checks Audible deals against Goodreads and optional personal reading context. It reports opportunities only and must never buy, reserve, check out, redeem credits, manage subscriptions, or submit payment.

Build a staged daily-deal flow:
1. prepare: deterministic Audible fetch/parse, local config/CSV/notes validation, local shelf short-circuits, duplicate scheduled suppression, artifact writing
2. runtime: Goodreads public lookup plus compact fit writing, JSON only
3. finalize: strict runtime JSON validation, decision mapping, concise message rendering
4. delivery: optional OpenClaw delivery with explicit delivery policies

Prepare must always write a fresh prepare-result.json for ready, suppress, and error outcomes and clear stale downstream current artifacts from previous runs. The default Audible fetch backend should reject unsafe non-Audible URLs before network access, try Python first for allowed URLs, and recover with browser-like curl when Audible rejects Python-client traffic but curl succeeds. Scheduled run-and-deliver must refuse error prep results and stale scheduled artifacts whose metadata.storeLocalDate is not today's date in the Audible marketplace timezone. mark-emitted must mark only the deal key from the same current prepare artifact that was actually delivered.

Support optional Goodreads CSV and notes. Validate missing explicit paths and invalid CSV header overrides. Suppress exact read/currently-reading matches before Goodreads lookup. Treat exact to-read match as positive evidence that can override the public threshold later. Enforce minimal privacy mode by omitting detailed personal artifacts, not just by telling the model not to use them.

Add a manual scan-want-to-read command for Goodreads to-read rows. It should scan Audible US conservatively, inspect the first search page and first three cards, identify visible numeric discounts or optional authenticated member cash prices, and render compact Markdown plus structured JSON. Use offset/limit instead of persistent scan progress. Count live requests, respect max-requests, cache parsed results, emit progress to stderr, and use clear statuses: discounted, available_no_discount, price_hidden, price_unknown, needs_review, not_found, lookup_failed.

Add optional Audible auth helpers for member-visible prices without asking for passwords. Store auth locally, never print tokens, and distinguish member cash price below list from true limited-time promotions with priceBasis and dealType.

Add setup, doctor, show-csv-headers, measure-context, publish-audit, and release hygiene. Store mutable data under <workspace>/.audible-goodreads-deal-scout/, not inside the installed skill folder. Keep public docs human-readable, generic, and free of private paths or generated artifacts.

Write offline tests for the daily deal flow, privacy behavior, stale-artifact protection, Want-to-Read scan selection/matching/pricing/reporting, progress output, request budgets, auth price semantics, and publish hygiene.
```

## Known Limitations

- Audible page structure can drift.
- Anonymous Audible pages often hide cash prices.
- Goodreads public lookup can fail or expose incomplete metadata.
- Goodreads CSV exports are manual and can be stale.
- Matching editions, translations, narrators, dramatizations, courses, and omnibuses is inherently imperfect.
- Public rating thresholds are useful heuristics, not truth.
- Taste notes improve fit quality only when they are specific.
- Authenticated price lookup adds useful data but increases local security responsibility.
