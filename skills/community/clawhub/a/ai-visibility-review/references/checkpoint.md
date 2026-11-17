# Checkpoint contract

Save one private JSON object. The renderer validates it without calling any API.
Keep unresolved run IDs and idempotency keys in a separate private recovery
file; the report accepts only terminal observations and receipts. Never omit
their reserved spend from your execution budget.
Only the fields described here are allowed, including nested objects. Unknown
metadata is rejected before any portable files are written. Keep raw supplier
responses, routing, credentials and billing envelopes in separate private files.

Top-level fields:

- `schema_version`: `1`; `method`: `"aeo-v4"`.
- `brand`: `{name, domains, aliases}`; `rivals`: a list of the same objects.
  Use bare public domain names, exact names and confirmed aliases.
- `market`: `{country, language}`.
- `questions`: five `{id, text}` objects. IDs remain stable on recheck.
- `by_name_question`: one agreed exact question naming the business.
- `engines`: three `{id, tool_id, surface, settings, rounds}` objects.
  `id` is `chatgpt`, `gemini` or `google_ai_mode`; `rounds` defaults to 3.
  `surface` is `logged_out_web`; `settings` records all exact request settings
  except prompt, including country and language representation and whether web
  search is forced. A deliberately reduced approved plan can use fewer engines
  or questions but must be labelled in `scope_note`. The renderer also flags
  missing core engines, fewer than five questions or fewer than three rounds
  independently of that note. Comparisons then describe only the reduced plan.
  Supported settings are `location_name`, `language_name`, `force_web_search`
  for ChatGPT; `country` for Gemini; and `gl`, `hl` for Google AI Mode.
- `approved_max_usd`: decimal string for the whole core plan's approved
  customer-wallet ceiling. For a retrospective import where no aggregate wallet
  ceiling was recorded, use null and explain the original authority in a
  nonempty `budget_note`. Do not substitute a wholesale test allowance.
  This reporting exception never authorizes a new call; a new execution still
  requires the bounded estimate and approvals in the runtime instructions.
- `scope_note`: human-readable scope and any omissions.
- `observations`: terminal records below; absent planned slots remain missing.
- `receipts`: one `{run_id, tool_id, cost_usd}` per paid research/observation run,
  including zero-cost failures. `cost_usd: null` means still unknown; never
  infer zero. Copy the actual settled customer charge, not wholesale or quote.
- `opportunities`: checked page/action records below.
- `by_name_findings`: optional list of `{engine, quote, fact, source_url}`.
- `changes`: optional list of `{date, description, url}` since the prior check.

Observation:

```json
{
  "run_id": "00000000-0000-4000-8000-000000000001",
  "engine": "gemini",
  "phase": "buyer",
  "question_id": "q1",
  "round": 1,
  "requested_prompt": "Which tools help a small team research prospects?",
  "requested_settings": {"country": "US"},
  "status": "ok",
  "reason": "",
  "retrieved_at": "2026-10-20T12:00:00Z",
  "model": null,
  "answer": "Example Co is an option for small teams.",
  "sources": [],
  "reviewed": true,
  "verdicts": [
    {
      "brand": "Example Co",
      "mention_quote": "Example Co",
      "recommendation_quote": "Example Co is an option for small teams.",
      "first": false
    }
  ]
}
```

This is a synthetic format illustration, not run evidence.

`phase` is `buyer`, `by_name` or `source`. Buyer and source records use an
approved question ID and that exact text. By-name uses `question_id: "by-name"`
and the exact `by_name_question`. Source records are only ChatGPT, round 1,
with forced web search; all other phases retain the engine's saved settings.
No duplicate engine/phase/question/round slots or run IDs are allowed.

Copy `requested_settings` from the actual dispatched request, excluding prompt.
It must match the engine's saved settings; the separate ChatGPT source pass
changes only `force_web_search` to true. Check the result's echoed settings when
available. Do not copy the plan over a mismatched actual request to make it pass.

Status is `ok`, `failed`, `refused` or `unusable`. Non-ok records require
`reason` and still retain a receipt, with unknown cost explicitly null.
Ok requires human/agent adjudication (`reviewed: true`), nonempty exact answer,
and an explicit `sources` list or null. Sources are citations only:
`[{url, title}]`. Combine duplicate source/citation-pill URLs once; keep
retrieved search results out. Null means unavailable, [] means known empty.

For DataForSEO, retain the returned answer/Markdown as `answer`; only copy
actual citations into `sources`. For Cloro use `data.text`, combine
`data.sources` and `data.citation_pills`. If both are null, keep null.
Store the original result privately alongside the checkpoint if needed for
review; the condensed checkpoint is not a substitute for supplier receipts.

Each positive verdict is manually adjudicated against the exact answer.
Quotes must be literal substrings; first requires a recommendation and explicit
ordering. Omitted brand verdict means no mention/recommendation after review.
Citations are computed independently by owned-domain match. The helper checks
quote grounding and logical consistency, not semantic truth or brand identity.

Opportunity:

```json
{
  "url": "https://example.com/buyers-guide",
  "kind": "third_party",
  "opened_at": "2026-10-20T12:00:00Z",
  "excerpt": "A short exact excerpt supporting the gap.",
  "gap": "What is missing or inaccurate and why it matters.",
  "action": "The specific correction, contribution or owned-page edit to try.",
  "effort": "About one hour",
  "owner": "Marketing",
  "recheck": "Whether the sampled answers cite the revised page.",
  "observation_ids": ["00000000-0000-4000-8000-000000000001"],
  "contact": {"label": "Editorial contact page", "source_url": "https://example.com/contact"},
  "draft": "Optional unsent editorial draft."
}
```

Kinds: `owned` or `third_party`. An owned page must match an owned domain.
A third-party opportunity must be cited by every listed observation; the
renderer computes recurrence from all observations, separately by phase/engine.
Do not attach an unrelated citation to make a page look supported. Save author
details only when publicly verified and include the source.

The report displays all observations, failures and model disclosures. A recheck
compares exact method, market, brand/rivals, question text/order, by-name prompt,
engine/tool/settings/round count. Known model changes and insufficient coverage
make it inconclusive. Unknown versions are always disclosed.
