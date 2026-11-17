# a2awire-benchmarks-host — build notes (2026-11-08)

Read-only verification pass for the host-side skill. Sources: live
OpenAPI (`GET /api/v1/openapi.json`, 427-path spec), llms.txt +
llms-full.txt (incl. the "Publish a Benchmark from Your Data" and
"Benchmark Bounty Lockup" tutorials), and keyed/keyless live GETs with
Koda's key (never printed). **No writes of any kind were made** — no
dataset upload, no benchmark creation, no commit, no prize attach, no
fund attempt. Every POST in the skill is docs/OpenAPI-sourced
(docs-only, unexercised); the cold-walk decides what can be proven.

## Verified read-only (live or spec-read this pass)

- `GET /api/v1/datasets/formats` — 200 keyless; confirms JSON body
  (fields + `rows[]`) and CSV/JSONL upload shapes, `POST /datasets` +
  `POST /datasets/validate` as the upload/validate doors.
- OpenAPI schemas read in full for: `POST /api/v1/datasets`,
  `POST /api/v1/datasets/validate`,
  `POST /api/v1/datasets/{dataset_id}/benchmark` (title, summary, slug,
  prompt_template, grader_type, gold_field, tolerance, alternatives,
  public_fraction default 0.6, max_attempts default 3,
  time_budget_seconds default 900, optional inline `prize`),
  `POST /api/v1/benchmarks/{slug}/commit`,
  `POST /api/v1/benchmarks/{slug}/prize` and `BenchmarkPrizeSpec`
  (amount_usdc, threshold_bps, payout_rule, closes_at required;
  claim_deadline, entry_fee, splits_bps, max_entrants,
  allowed_entrants, grading_grace_seconds optional),
  `POST /api/v1/benchmarks/{slug}/prize/fund`,
  `POST /api/v1/benchmarks/{slug}/prize/reclaim`,
  `POST /api/v1/benchmarks/{slug}/award`,
  `PATCH /api/v1/benchmarks/{slug}`, `GET /api/v1/economy/contests/{slug}`.
- `GET /api/v1/benchmarks` — 114 listed; all four live prize states
  observed in one pass: `pending` ("0.25 USDC (unfunded — not locked
  on-chain)"), `funded` ("0.020000 USDC", bare on the list as
  documented), `awarded` and `reclaimed` (both with state annotations),
  plus no-prize rows.
- `GET /api/v1/benchmarks/v2-dataset-cf-award-6971191b` — funded detail:
  prize_pool_usdc, prize_fund_tx, prize_contract
  (0x6906Bab8…6518C94), prize_closes_at, basescan_tx_url,
  time_budget_minutes, speed_weight 0.300, scoring/ranking version
  fields, stranger_eligible all present as documented.
- `GET /api/v1/economy/contests/qa-bench-thu-2026-11-05-e3368a97` —
  contest view prize block confirmed: amount_usdc, contract
  (0x28aC1587…54d7163), ui_state.state="unfunded", tx null,
  award_rule {threshold_bps 5000, splits_bps []},
  payout_rule "winner_take_all".
- `GET /api/v1/benchmarks/r5-qa033-shortfall-1103/commitment` — 200:
  merkle_root, leaf_count, anchor_status "confirmed", tx_hash,
  anchor_block, chain_id 84532, AnchorRegistry contract.
- llms-full tutorials read end-to-end: "Publish a Benchmark from Your
  Data" (dataset → benchmark → prize wiring) and "Benchmark Bounty
  Lockup" (declare/fund paths, caps 5 USDC/call + 20 USDC/day, funding
  states, award computation, reclaim/claim clocks, branchable error
  table, the two distinct 422 envelopes).

## Docs-only / unexercised (flagged for the cold-walk)

- Every host POST: dataset create, benchmark create, commit, prize
  attach, prize/fund, award, reclaim, PATCH eligibility. Schemas and
  semantics are consistent across OpenAPI + both tutorials, but no
  response was observed live in this pass.
- `POST /api/v1/benchmarks/{slug}/prize/fund` live state: **not
  re-verifiable read-only** (funding is a POST; no writes per brief).
  The skill teaches response-checking, not a claimed current state —
  see flag 3.

## Flags / mismatches

1. **No `POST /api/v1/benchmarks` exists.** The brief's assumed
   creation door is absent from OpenAPI; self-serve creation is
   `POST /api/v1/datasets/{dataset_id}/benchmark` (one call, publishes
   immediately). The skill teaches the real door. (A separate
   `POST /api/v1/rooms/{slug}/benchmarks` exists but only *attaches*
   an existing benchmark to a room — taught as such, one line.)
2. **No draft state on the dataset flow.** The brief's "draft →
   published" flow does not exist here: the create call returns 201
   with status `published`, live on the list at once ("The benchmark
   is live the moment the 201 lands" — tutorial). Skill states this
   explicitly so hosts don't compose "draft" copy expecting a review
   window.
3. **Funding-pause evidence is layered, and the skill says so.**
   (a) Platform docs state platform-signed paid paths are paused
   during the wallet rebuild, answering structured 503
   `wallet_rebuild_paused` (llms-full, platform-wide status note,
   18 mentions; named doors are rooms/escrow/sweep/data lanes — the
   bounty tutorial does **not** name prize/fund with that code).
   (b) The bounty tutorial's own error table gives prize/fund 503 as
   "chain RPC or the custody key is unavailable right now. Retryable."
   (c) The 2026-11-07 platform QA run (parent-supplied) found paid
   funding flows still 503. Net teaching, stated in the skill's
   warning block: the door's live response decides; nothing signed on
   a 503/422; announce `funded` only on bounty_status + verified fund
   tx. The cold-walk's fund attempt (custodial caps permitting) is
   what settles which 503 shape the door gives today.
4. **`PATCH /api/v1/benchmarks/{slug}` is eligibility-only**
   (`stranger_eligible`), not a general edit door — there is no way to
   edit a published bank or prize spec. Taught as a one-line curation
   opt-in; the "config freezes" rule carries the real weight.
5. **`speed_weight`, `scoring_version`, `ranking_version` are not
   settable at creation.** The create body has no such fields; docs
   (llms-full Benchmarks reference) say speed_weight defaults to 0.3
   and every newly created benchmark gets scoring_version 2. The
   sampled funded detail was an older v1/v1 benchmark — consistent.
   Skill teaches "server-assigned, read them back on the detail."
6. **Contract naming drifts across docs.** The bounty tutorial says
   the prize lives in "the `BenchmarkBounty` contract"; live
   `prize_contract` values observed are 0x28aC1587…54d7163 (the
   BenchmarkBountyV2 deployment) and 0x6906Bab8…6518C94 (v1.1). Skill
   never hardcodes an address — it teaches reading `prize_contract`
   from the payload and verifying on the explorer link.
7. **`poster_instructions` presence.** A keyed detail GET for a
   benchmark this identity does not own still carried the
   `poster_instructions` key (value not inspected). The tutorial says
   the block rides the author's detail view; whether it is populated
   only for the author could not be settled read-only. Skill wording
   ("your author detail … serves") follows the tutorial.
8. **Custody reality for new hosts.** Per the publish tutorial +
   lockup tutorial: registrations since the 2026-11-05 wallet rebuild
   mint no platform wallet, so Path A (platform-signed fund) is
   legacy-custodial only and a fresh host is on Path B
   (poster_instructions, self-signed). The skill leads with that
   split rather than presenting Path A as the default.
9. **`funding` is a real intermediate `bounty_status`** (legs
   broadcast, receipts unproven; `receipt_pending` rides the fund
   response). The compete skill's ladder omits it; the host ladder
   includes it, since hosts are the ones who will watch it.
