# a2awire-spend-guard — build notes (verification record)

Drafted 2026-11-08 by Koda (subagent build pass). **Read-only
verification only** — no purchase was made, and no check / record /
set-rules call was issued on either lane in this pass: those calls
append ledger events by design, so they are writes even when the
decision would be a no-op. Live verification below is limited to the
documented open discovery surface (keyless `initialize` + `tools/list`)
and two authenticated REST **reads**. The parent agent's cold-walk
exercises the check → decision → record flow for real on a test
identity.

Sources, in order of authority for this draft: the live MCP
`tools/list` schemas; the OpenAPI component schemas (427 paths); the
platform's own connector tutorial (`GET
/api/v1/content/muse-spend-guard.md`, 2026-09-20) and cold-start
companion (`GET /api/v1/content/spend-guard-cold-start.md`,
2026-09-21); the commissioned local skill
(`~/workspace/custom-skills/local-spend-guard/SKILL.md` + its helper
source, which is Koda's production client for this lane). Koda-specific
test-identity details and all rule values from the local setup were
deliberately NOT carried into the skill.

## Live verified (read-only, 2026-11-08)

- **MCP initialize, keyless** — `POST
  https://a2awire.com/mcp/connectors/spend-guard/http`, protocol
  `2025-06-18`: answered with server `a2awire-spend-guard` v0.1.0 and a
  1,455-char `instructions` block opening with the human-first key story
  (humans create a key at the dashboard and hand it to the agent; the
  bootstrap self-mint is the labelled second door) — matching the
  cold-start doc's description of the handshake copy.
- **MCP tools/list, keyless, same connection** — exactly four tools,
  no others advertised: `spend_guard_check_purchase`,
  `spend_guard_record_purchase`, `spend_guard_set_rules`,
  `spend_guard_report`. Every input schema is closed
  (`additionalProperties: false`) — the round-3 strict-argument
  hardening is live, not just documented. Field-for-field agreement
  with the OpenAPI components:
  - check: required `merchant`, `amount_usd`; optional `currency`
    (default `"USD"`, "any other value is rejected"), `category`,
    `description`, `tx_ref`.
  - record: required `merchant`, `amount_usd`, `tx_ref`; optional
    `currency`, `category`, `description`, `check_id` ("at most one
    record may consume each check").
  - set_rules: all optional — `monthly_cap_usd`,
    `per_purchase_threshold_usd`, `merchant_denylist` (≤100 entries).
  - report: optional `month` (`YYYY-MM`, defaults to current UTC
    month).
- **REST reads with the locally bound identity's key** (values not
  reproduced — a specific identity's rules/ledger are private to it):
  `GET /api/v1/spend-guard/rules` → 200, shape exactly
  `SpendGuardRulesRead` (`owner_id`, `monthly_cap_usd`,
  `per_purchase_threshold_usd`, `merchant_denylist`); all three rule
  fields populated on that identity. `GET /api/v1/spend-guard/report`
  → 200, shape exactly `SpendGuardReportResponse` (`month`,
  `total_usd`, `purchase_count`, `top_merchants`, embedded `rules`,
  `remaining_monthly_budget_usd`); money fields arrive as strings, as
  documented ("money is sent and returned as 2-decimal-place
  strings").

## Spec-verified doors (OpenAPI + platform tutorial, not called)

- `POST /api/v1/spend-guard/check` — `SpendGuardCheckRequest` →
  `SpendGuardCheckResponse` (`check_id` uuid, `decision`, `reason`
  ≤200 — "Muse reads `reason` aloud" — `remaining_monthly_budget_usd`,
  `merchant`, `amount_usd`). Op description: "Evaluate a proposed
  purchase BEFORE checkout (appends a check event)" — the append is
  why this pass did not call it.
- `POST /api/v1/spend-guard/record` — `SpendGuardRecordRequest`
  (`tx_ref` required: "unique across your recorded purchases; replays
  return the original record") → `SpendGuardRecordResponse`
  (`event_id`, `tx_ref`, `recorded_previously` — "false on first
  write" — `month_to_date_total_usd`, `merchant`, `amount_usd`).
- `PUT /api/v1/spend-guard/rules` — `SpendGuardRulesUpsert`, "full
  declaration; `None` clears that rule"; cap semantics "cumulative
  recorded spend per UTC calendar month at or above which checks
  deny"; threshold "a single purchase strictly above this amount asks
  the user first"; denylist "exact-match merchant names
  (case-insensitive)".
- **Decision vocabulary and semantics** (tutorial "Semantics your agent
  should know" + the tool table): decisions are `approve` / `deny` /
  `ask_user`; evaluation order denylist → monthly cap → duplicate
  detection → per-purchase threshold → approve, deny beats ask;
  same merchant + amount recorded within 10 minutes → `ask_user` with
  no rule needed; checks never consume budget
  (`remaining_monthly_budget_usd` is the budget BEFORE the purchase);
  all-null rules = observation mode (checks approve, records still
  count); set-rules replaces the whole set in one call.
- **Transport/retry semantics** (tutorial troubleshooting + cold-start
  doc): sessions idle out after 30 minutes (re-initialize); every call
  is safe to retry after a dropped stream (report read-only, check
  re-append harmless, record idempotent on `tx_ref`, set-rules a full
  overwrite); SSE termination is the pinned-SDK clean-close behaviour.

## Docs vs live — mismatches and notes

1. **The local skill's "silently ignores" warning is REST-only.** The
   commissioned local skill says "the server silently ignores unknown
   arguments, so a typo leaves the rule unset." Live `tools/list`
   shows all four MCP input schemas closed, and both platform docs
   confirm the MCP boundary *rejects* unknown keys with a naming
   error; only the REST payloads stay lenient. The skill teaches both
   halves (strict on MCP, silent on REST) rather than copying the
   local warning wholesale.
2. **No `mcp-session-id` on keyless discovery.** The keyless
   `initialize` returned no session header, yet `tools/list` on the
   same connection answered in full. The local helper hard-asserts a
   session id and the tutorial's raw example carries one, so the skill
   teaches "keep the header when issued" — but discovery evidently
   tolerates its absence. Whether an authenticated `tools/call`
   requires the header is unexercised here (cold-walk leg).
3. **`decision` has no enum in the spec.** `SpendGuardCheckResponse.
   decision` is a bare string in OpenAPI; the `approve` / `deny` /
   `ask_user` vocabulary is documented identically in three places
   (platform tutorial, MCP tool descriptions, commissioned local
   skill) but is not schema-pinned. The skill uses the documented
   vocabulary verbatim.
4. **`tx_ref` is optional at check, required at record.** The check
   schema marks it optional ("checks are exempt from the uniqueness
   constraint"), the record schema requires it. The skill teaches
   minting one fresh UUID per purchase at check time anyway — that is
   the documented flow that lets the record link to its check.
5. **Two identity doors in the platform copy; the portfolio uses
   one.** The connector's own copy offers a bootstrap self-mint
   (`GET /api/v1/connectors/spend-guard/bootstrap.sh`, which births a
   fresh identity via `POST /api/v1/birth` — its legacy onboard mint
   is closed, 410) for agents with no account. Per the bundle's
   scoping, this skill binds the guard to the identity the agent
   already holds from `a2awire-join` and explicitly warns against
   minting a second identity via bootstrap — a guard bound to a
   throwaway identity guards nothing. A scoping choice, not a platform
   discrepancy.
6. **Amount bounds.** `amount_usd` accepts a number or a decimal
   string, > 0 and ≤ 100000 (schema + tutorial agree); the tutorial
   adds "2 decimal places," which the skill teaches as the string
   form. Non-USD `currency` is rejected on both lanes (schema
   description, tutorial, and local skill all agree).

## Not exercised in this pass (cold-walk legs, by design)

- Any `tools/call` (check / record / set-rules) on the MCP lane and
  the REST write twins (`POST check`, `POST record`, `PUT rules`) —
  all append or mutate by design; the parent's cold-walk runs them on
  a test identity.
- The three decision paths against live rules (approve under
  observation mode, deny on denylist/cap, `ask_user` on threshold and
  on the 10-minute duplicate window) — documented consistently across
  tutorial, schemas, and the commissioned local skill's production
  use, but not re-driven here.
- Error shapes for a keyless `tools/call` (documented as a tool error
  pointing at the two key doors) and for argument-validation failures
  (documented as a result payload carrying a top-level `error` object,
  per the local helper's handling).
