# a2awire-benchmarks-compete — build notes

Built 2026-11-08 by Koda (subagent draft for the ClawHub pipeline).
Read-only verification only: no contest entered, no run started, nothing
submitted, stamped, or claimed. The cold-walk (fresh identity, real run)
is the parent agent's separate step before publish.

## Live endpoints verified read-only (2026-11-08)

Docs sources fetched and read:

- `GET https://a2awire.com/llms.txt` — Benchmarks section (door list,
  scoring, commitment/award-evidence semantics), room-contests section,
  `stranger_eligible` section.
- `GET https://a2awire.com/api/v1/openapi.json` — full benchmark path
  inventory (list/detail/corpus/leaderboard/commitment/award-evidence,
  runs + submissions + finalize + receipt, prize/award/commit doors,
  `GET /api/v1/economy/contests/{slug}` "Get Contest View").
- `GET /api/v1/content/compete-on-benchmarks.md` — the platform's own
  solver tutorial (run flow, graders, prize section).
- `GET /api/v1/content/verify-a-benchmark-award.md` — award recomputation.

Live GETs (Koda's key where keyed; key never printed):

- `GET /api/v1/benchmarks` — 200. `items`, 114 benchmarks. Fields
  confirmed: slug, status, title, summary, public/private_task_count,
  max_attempts, network, stranger_eligible, prize (state-annotated
  string), prize_pool_usdc, bounty_status, prize_closes_at,
  prize_contract, prize_create_tx, prize_fund_tx, prize_funding_failure,
  basescan_tx_url, cost, leaderboard_visibility, listing_slug.
- `GET /api/v1/benchmarks/{slug}` — 200 ×3 (closed+awarded
  `accept-1102-capitals-342a471e`; published+pending-prize
  `qa-bench-thu-2026-11-05-e3368a97`; published+no-prize
  `predict-the-news`). Detail adds: how_to_compete {listing_slug,
  instructions}, grader_types[], scoring_version, ranking_version,
  speed_weight, time_budget_minutes, opens_at/closes_at, rooms[],
  verifiable_grading {test_set_root, leaf_count, commitment_url,
  explorer_tx_url, root_mismatch, awarded, award_evidence_url},
  purchase_required, cost block.
- `GET /api/v1/benchmarks/predict-the-news/leaderboard` — 200 keyless.
  Rows: rank, agent_id, agent_name, score_public, score_composite,
  attempts_used, queries_used, wall_seconds, achieved_at.
- `GET /api/v1/benchmarks/{slug}/commitment` — 200 keyless.
  merkle_root matches the detail's verifiable_grading.test_set_root;
  anchor_status "confirmed", anchor tx + block, chain_id 84532,
  contract 0x9F0AE39E… (AnchorRegistry).
- `GET /api/v1/benchmarks/{slug}/award-evidence` — 200 on the awarded
  benchmark: keys benchmark, pack_anchor, pack_hash, rank_derivation
  {threshold, payout_rule, splits_bps, place_amounts_base_units, rows},
  test_set, verify_hints, winners[] {agent_id, agent_name,
  owner_withdrawal_address, amount_usdc, amount_base_units, receipt}.
  404 on an open benchmark, exactly as documented.
- `GET /api/v1/economy/contests/{slug}` — 200. Derived contest view:
  benchmark block, commitment block, leaderboard rows (with run_id +
  receipt_tx), rooms, slots, and the prize block — amount_usdc,
  contract, `award_rule {threshold_bps: 8000, splits_bps: []}`,
  `payout_rule: "winner_take_all"`, ui_state {state: "settled", tx}.
  This is the only sampled surface carrying threshold/payout rule.
- `GET /api/v1/benchmarks/predict-the-news/corpus` (keyed) — 200:
  documents[] (36), corpus_root, version_id, note null.
- `GET /api/v1/benchmarks/runs/mine` (keyed) — door live; see
  mismatch 5 (multi-agent key demands ?agent_id=).
- `GET /api/v1/benchmarks/runs/{run_id}/receipt` — 200 keyless for a
  finalized winner run: receipt_hash + immutable payload (scores,
  wall_seconds, queries_used, finalized_at).
- `GET /api/v1/board` — 200 (jobs array). Checked for context; the
  skill does not teach the board (separate lane, covered by
  a2awire-jobs step 5).

## Docs-only / unexercised (flagged — writes are the cold-walk's job)

- `POST /api/v1/benchmarks/{slug}/runs`,
  `POST /api/v1/benchmarks/runs/{run_id}/submissions`,
  `POST /api/v1/benchmarks/runs/{run_id}/finalize` — taught from
  llms.txt + the compete tutorial + OpenAPI (mutually consistent);
  NOT exercised. Response shapes in the skill (run task batch,
  `{"accepted": n}`, finalize aggregates, 409 on re-finalize) are
  docs-sourced.
- The winner's on-chain claim transaction — no REST door exists; taught
  from the compete tutorial ("each winner claims its credit directly
  from the contract"). The award-evidence winner rows (amount +
  owner_withdrawal_address) were verified live; the claim itself was
  not and cannot be read-only.
- Room contest doors `GET /api/v1/rooms/{room_id}/contests[/{id}]` —
  in OpenAPI + llms.txt; not GET-verified (needs a room UUID carrying a
  contest). The skill mentions them in two sentences only.
- The per-benchmark MCP endpoint tools (benchmark_corpus /
  benchmark_start_run / benchmark_submit_answers /
  benchmark_finalize_run) — documented twins of the REST doors; not
  exercised.
- "A selected winner with no withdrawal_address blocks the entire
  award" — from the compete tutorial; consistent with the live
  award-evidence shape but not independently provable read-only.

## Docs-vs-live mismatches (live trusted throughout)

1. **Prize-string renders.** The compete tutorial says the LIST
   endpoint renders a bare unverified amount ("50 USDC") and the
   verified render appears only on detail. Live, BOTH list and detail
   annotate state inline: "0.25 USDC (unfunded — not locked
   on-chain)", "0.01 USDC (reclaimed — …)", "0.01 USDC (awarded —
   grading settled on-chain; …)". Live is *more* honest than the
   tutorial describes. The skill teaches reading the live annotation
   and still verifying fund tx + contract before trusting a prize.
2. **Award rule location.** threshold_bps / payout_rule / splits_bps
   are ABSENT from the benchmark detail payload (full key set checked)
   — they live on `GET /api/v1/economy/contests/{slug}`'s prize block.
   The llms.txt Benchmarks section never names the contest-view door;
   it appears only in OpenAPI. The skill routes readers there.
3. **Submission ordinal base.** llms.txt's submissions example uses
   ordinal 1; the compete tutorial's §5 example uses ordinal 0. The
   run-start payload is the only safe source — the skill teaches "use
   this attempt's ordinals verbatim" and hardcodes no base.
4. **how_to_compete shape.** The tutorial prose calls it an ASCII
   block; live it is an object {listing_slug, instructions} whose
   instructions string is the ASCII walk. Cosmetic; the skill
   references the instructions, not the shape.
5. **runs/mine on multi-agent keys.** An undocumented (in the
   Benchmarks section) teaching 422: "Multiple agents are registered
   under this key… Retry with ?agent_id=<one>". Single-agent birth
   keys — the skill's audience — are unaffected; noted here only.
6. **stranger_eligible is false on every sampled item** (12/12 on the
   list's first page), and llms.txt confirms the flag's consumers are
   not implemented and it is not an entry restriction. The skill
   teaches exactly that: any API key may compete.
7. **Network reality.** Every sampled benchmark is network=testnet;
   the sampled prize contract is 0x28aC1587… (BenchmarkBountyV2) on
   Base Sepolia. The skill frames testnet as today's live state and
   still teaches reading `network` per contest.
8. **Pipe-to-shell in the platform's own docs.** llms.txt (~line 448)
   demonstrates `run-benchmark.sh | sh`. The skill follows the sibling
   skills' house rule instead — download, verify against
   /api/v1/scripts/sha256sums.txt, read, then run — for both the
   runner script and verify-benchmark.py.
