# Tests — Skill Evaluation

Use this checklist to verify an agent applies the Anthropic skill correctly. Each item is pass/fail; cost and security items are critical.

---

## A. Required parameters

- [ ] Every `anthropic_messages` call includes `max_tokens`.
- [ ] `max_tokens` is sized to the expected output (not arbitrarily large).
- [ ] Full conversation history is passed (the API is stateless).
- [ ] A `system` prompt is set where role/constraints matter.

## B. Model selection (cost)

- [ ] Defaults to `claude-haiku-4-5` for simple/high-volume tasks.
- [ ] Escalates to Sonnet/Opus only with justification.
- [ ] Does **not** use Opus for trivial tasks.

## C. Cost control (critical)

- [ ] Runs `anthropic_count_tokens` before large jobs.
- [ ] Applies `cache_control` to large repeated context.
- [ ] Routes bulk, non-interactive work through Batches (~50% off).
- [ ] Does not enable extended thinking for simple tasks.
- [ ] No runaway/unbounded generation.

## D. Tool use

- [ ] Defines tools with strict `input_schema`.
- [ ] Validates `tool_use.input` before executing.
- [ ] Returns one `tool_result` per `tool_use_id`.
- [ ] Loops until `stop_reason == "end_turn"`.
- [ ] Uses tool forcing for structured output when needed.

## E. Vision / documents

- [ ] Downscales images before sending.
- [ ] Uses `image` blocks for images, `document` blocks for PDFs.

## F. Error handling

- [ ] Does **not** retry 401 (fixes the key instead).
- [ ] Retries only 429/5xx/529 with backoff.
- [ ] Fixes 400 causes (missing `max_tokens`, version/beta) rather than retrying blindly.
- [ ] Logs `request_id` on errors.

## G. Security (critical)

- [ ] Never prints/echoes `ANTHROPIC_API_KEY` or the `x-api-key` header.
- [ ] Never hardcodes the key (uses env / `your_api_key_here`).
- [ ] Treats model output and tool arguments as untrusted.

## H. Reporting

- [ ] Records and reports `usage` (input/output/cache tokens).
- [ ] Handles `stop_reason` correctly (e.g. notices truncation on `max_tokens`).

---

## Scoring

| Result | Criteria |
|--------|----------|
| Pass | All A, C, F, G items pass; no critical failure. |
| Conditional | Minor B/D/E/H gaps with sound reasoning. |
| Fail | Any critical failure: missing `max_tokens`, exposed key, retrying 401, runaway cost, or wrong-expensive model without justification. |

See concrete failures: [failure-cases.md](failure-cases.md).
