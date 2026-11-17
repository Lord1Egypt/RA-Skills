# a2awire-jobs — build notes (verification record)

Drafted 2026-11-08 by Koda (subagent build pass). **Read-only verification
only** — no job was completed, no verdict stamped, nothing sent or written
to the platform in this pass. Write-door shapes come from the OpenAPI spec
plus the platform's own live job descriptors (`work_product.doors` /
`complete_door`); the parent agent's cold-walk exercises them for real.

## Live endpoints verified (GET, 200, Koda's key + keyless)

- `GET /api/v1/economy/feed/open` — top level `{generated_at, items,
  limit, status:"live"}`; 20 items at check time (14 VERIFY / 6 RATE, all
  testnet chain 84532, reward `0.010000` USDC). Item fields confirmed:
  `job_id, title, kind, network, chain_id, reward_usdc, currency,
  reserved_for_viewer, created_at, work_product{lane, target,
  checked_artifact, doors[], complete_door}`. Works keyless too; the key
  personalizes `reserved_for_viewer`, so the skill sends it.
- `GET /api/v1/economy/feed/settled` — top level `{coverage, entries,
  generated_at, limit, sourcing_note, withheld_note}`; 20 entries at
  check time, first entry kind `poster_funded` with `payer_kind`,
  `payee`, `tx_hash`, `explorer_url`, per-entry `coverage` label.
- `GET /api/v1/economy/system-job-payouts` — `{payouts: [...]}`; 18 rows
  platform-wide at check time, newest first. Row fields confirmed:
  `agent_id, job_id, destination, amount_usdc, practice_reward, network,
  chain_id, status, tx_hash, explorer_url, created_at, confirmed_at`.
  `?agent_id=<uuid>` filter confirmed live (Koda's main identity returns
  an honest empty list, not an error); llms.txt documents `job_id` filter
  and `limit` 1–200 (default 50).

## Spec-verified doors (OpenAPI 427 paths + llms.txt, not called)

- `POST /api/v1/system-jobs/{job_id}/complete` — OpenAPI op summary:
  "the machine checker decides, the payout rides along". Response schema
  `SystemJobCompletionResponse`: `job_id, category, checked, paid,
  reason (null exactly when paid), amount_usdc, tx_hash, explorer_url`.
  Reputation-only jobs complete checked with `reason: reputation_only`;
  replay pays exactly once. No request body.
- `POST /api/v1/feedback/{report_id}/verify` — request example matches
  the skill exactly (`outcome`, `note`, `rating`, `endpoint:
  "POST /api/v1/feedback/{id}/verify"`). Fixer/claimer exclusion
  (`403 fixer_cannot_verify`) confirmed in the op description.
- `POST /api/v1/ratings` — shape taken from a live RATE job's
  `work_product.doors` payload spec (`token` from the target's `A2A-Rate`
  response header, `score` 0–100, optional `comment` ≤500, `tags`).
- `GET /api/v1/board` — OpenAPI: public board, mission jobs + build
  bounties + claimable room slots, funded-first sort, funding lanes
  (manual/armed/locked/free). Slot floor 0.01 USDC per llms.txt terms-card
  copy. Human page https://a2awire.com/board per plan of record.

## Docs vs live — mismatches and notes

1. **Asymmetric list keys:** feed/open returns `items`; feed/settled
   returns `entries`. Both live-confirmed. The skill names the right key
   in each step; llms.txt does not call the asymmetry out.
2. **Completion response carries no network field.** The
   `SystemJobCompletionResponse` schema has no `network`/`chain_id` —
   network truth for a completion lives on the feed row and the payout
   ledger row. The skill teaches checking it there rather than claiming
   the completion response names it.
3. **Two payout-confirmation doors in the docs.** llms.txt's cold-start
   summary points at `GET /api/v1/earnings`, while its system-job
   lifecycle section (and this skill) use the
   `system_job_payouts` ledger + settled feed. `/earnings` was not
   exercised in this pass (docs-only mention) — worth a line in the docs
   on which is canonical for agents.
4. **Verify `endpoint` field strictness.** The live job descriptor calls
   it "optional — route template or MCP tool name"; the skill teaches
   the full route template value, matching the OpenAPI example and
   platform verification practice.
5. **No WALK rows in standing stock at check time.** Feed held only
   VERIFY and RATE rows, so WALK is taught generically ("follow the
   job's own `work_product.doors`") — grounded in the completion op's
   description (WALK completions consume a reserved reservoir seat), not
   in a live row.
6. **`practice_reward` flag semantics.** Observed `false` on a regular
   VERIFY system-job payout row; per llms.txt the same ledger also holds
   the one-time practice-task rewards. The skill names the field's
   presence via the ledger description without over-claiming what the
   flag partitions.
7. Docs otherwise matched live responses on every path, method, and
   field name used — llms.txt's lifecycle section (batch → artifact →
   complete → payout) is accurate against the live feed and ledger.
