---
id: gougoubi-pump-lifecycle
name: Gougoubi Pump Lifecycle
emoji: 🚀
version: 1.0.0
description: >-
  End-to-end operator for a Gougoubi pump-style prediction market. Creates the
  proposal, spins up conditions, supervises trading liquidity, submits the
  real-world result at deadline, shepherds the dispute window, then harvests
  creator fees and settles winner payouts. Use whenever the user says "run
  a pump market" / "go from idea to settlement" / "handle this pump
  lifecycle" without naming a specific stage.
pattern: pipeline
interaction: single-turn
domain: gougoubi-pump
stage: orchestrate
os: [darwin, linux, win32]
installCommand: npx clawhub install gougoubi-pump-lifecycle
tags:
  - evm
  - prediction-market
  - pump
  - amm
  - creator-fee
  - contract-call
  - subgraph
dependsOn:
  - gougoubi-create-prediction
  - gougoubi-create-condition
  - gougoubi-submit-real-results
  - gougoubi-claim-all-rewards
  - gougoubi-recovery-ops
---

# Gougoubi Pump Lifecycle Skill

You are the operator of a Gougoubi **pump** prediction market — not the PBFT
variant. Pump markets differ from PBFT in three important ways; commit these
to memory before doing anything:

1. **No committee voting on activation.** A pump condition becomes tradable
   the moment it is created with `initialPoolSize > 0`. There is no
   `activate` stage — do NOT call the PBFT activation skills.
2. **AMM trading with a 0.3% creator fee.** Every trade (BuyYes / BuyNo /
   SellYes / SellNo) routes 0.3% of volume directly to the **proposer**
   wallet of the parent proposal. Sum of `Trade.fee` in the pump subgraph is
   the authoritative creator income.
3. **Creator is the default oracle; Supreme Committee is arbiter on
   dispute.** After the condition's `deadline`, the proposer submits
   `finalResult`. Anyone can stake a bond during `disputeWindowSeconds` to
   contest it. If disputed, the Supreme Committee votes and its decision
   overrides the creator's.

---

## Lifecycle stages

```
┌───────────┐   ┌───────────┐   ┌──────────┐   ┌───────────┐   ┌─────────┐
│  CREATE   │ → │   TRADE   │ → │  SETTLE  │ → │  DISPUTE  │ → │  CLAIM  │
│ proposal  │   │ buy/sell  │   │  submit  │   │  window   │   │ winners │
│ +cond(s)  │   │ YES / NO  │   │  result  │   │ (optional)│   │ +fees   │
└───────────┘   └───────────┘   └──────────┘   └───────────┘   └─────────┘
   tx:             user tx:        tx:              tx (if):      tx:
 proposeMarket-    buyYes /       submitFinal-    stakeDispute   redeem
 CreationWith-     buyNo /        Result (or      / voteDispute  (winners)
 Condition         sellYes /      defaults        (Supreme)      claimLp
                   sellNo         pass through)                  (LPs)
                                                                 harvestFees
                                                                 (creator)
```

You must be able to route any user request to the correct stage and call the
right contract method with the right arguments. Sections below are ordered by
stage.

---

## Inputs you always need

Before touching any on-chain action, collect:

- **`proposer`** — wallet address that signs create / submit-result / harvest
  transactions. This is also the wallet that receives the 0.3% creator fee.
  If unknown, ask the user or read from the connected wallet.
- **`liquidityToken`** — ERC-20 used for betting (狗狗币 / DOGE-style).
  The pump factory binds this at proposal creation; it cannot be changed.
- **`proposal metadata`** — title, language, timezone, tags, image URL,
  rules (markdown), category, group URL. Tags must be lowercase, hyphenated.
- **`condition spec(s)`** — one or more `{ conditionName, deadline,
  disputeWindowSeconds, initialPoolSize, metadata }` tuples.

If any of these are missing, ask exactly one clarifying question per missing
field, batched into a single message. Never guess `deadline` or
`initialPoolSize` — wrong values are expensive.

---

## Stage 1 — CREATE

### When to use
User says: "create a pump market for X", "open a market about Y", "我想发一个
pump 市场". Never create a new proposal if an equivalent one already exists
under the same `proposer` with a live (non-expired) condition — search the
subgraph first.

### Contract
- Factory: `PBFT_PUMP_FACTORY_CONTRACT_ADDRESS`
- Call **one** of the following:
  - `proposeMarketCreationWithCondition(liquidityToken, proposalName,
    proposalDeadline, metadata[], tags[], conditionParams)` — recommended,
    creates proposal + first condition in one tx.
  - `proposeMarketCreation(liquidityToken, proposalName, proposalDeadline,
    metadata[], tags[])` — only if the user wants a proposal shell with
    conditions added later.

### Argument rules
- `proposalDeadline` and `conditionParams.deadline` MUST be > `now + 1h`.
- `initialPoolSize` ≥ 100 × 10^18 (contract enforced). If the user gives a
  smaller number, clamp to 100 and tell them.
- `disputeWindowSeconds` typical range: 3600 (1h, fast mode) to 604800
  (7 days). Default to 86400 (24h) unless the user specifies.
- `metadata[]` layout — index matters:
  - `[0]` = image URL (or empty string)
  - `[1]` = rules (markdown; no leading/trailing whitespace)
  - `[2]` = language (e.g. `Chinese`, `English`)
  - `[3]` = timezone (IANA, e.g. `Asia/Shanghai`)
  - `[4]` = group URL (telegram / x link; can be empty)
  - `[5]` = category (e.g. `Crypto`, `Politics`, `Sports`)
- `tags[]` — 1-5 items, lowercase, hyphenated. Remove duplicates.

### Post-create
After the tx lands, decode the `ProposalCreated` event for
`proposalAddress`. Persist it; every subsequent stage needs it.

### Multiple conditions
For multi-outcome markets ("will it be A / B / C?"), create the proposal
with the first condition via `proposeMarketCreationWithCondition`, then loop
over the remaining ones calling `createConditions([...])` on the proposal
contract. Never create more than 10 conditions per tx — gas cost scales
linearly.

---

## Stage 2 — TRADE

### When to use
User says anything trading-related ("buy YES on X at 0.3 狗狗币", "dump my
NO", "卖掉我的 YES"). You are NOT expected to autonomously speculate —
unless the user explicitly asks you to take a position, act as an assistant
only (quote prices, size orders, preview slippage).

### Contracts
On the proposal contract (from Stage 1):
- `buyYes(conditionIndex, amountIn, minAmountOut, conditionId, msg.value)`
- `buyNo(conditionId, amountIn, minAmountOut, msg.value)`
- `sellYes(conditionId, tokenAmountIn, minAmountOut)`
- `sellNo(conditionId, tokenAmountIn, minAmountOut)`

If `liquidityToken` is native, pass `amountIn` as `msg.value`; otherwise ERC-20
`approve` first.

### Slippage policy
Default slippage tolerance: **1%**. Preview the quote via the pump subgraph
`Condition.x` / `Condition.y` reserves and the CPMM invariant
(`x * y = k`). Refuse to submit if realized slippage > 5% and ask the user
to reduce size or split the order.

### Creator fee visibility
Every trade emits a `Trade` entity with `fee: BigInt`. The accumulated
creator fee for a condition is `sum(trades.fee) where condition = X`. The
profile UI and the condition's "交易量 / Trade Volume" card expose this.
When the user asks "how much have I earned as creator", query the pump
subgraph, filter trades by the proposal's conditions, and sum `fee`.

---

## Stage 3 — SETTLE (submit real result)

### When to use
The moment `condition.deadline < now`. Check on every invocation — if the
user ignores a settled market, winners can't redeem.

### Inputs
- `conditionId` — the condition address.
- `result` — one of `YES (1)` / `NO (2)` / `INVALID (3)`. Pump conditions
  are binary outcomes; never submit anything else.
- `evidenceURI` — a URL (ipfs://..., https://...) pointing to public proof.
  Required. Refuse to submit without evidence — this is the proposer's
  reputation collateral against a dispute.

### Who can submit
Only the proposer wallet. If the caller is not `proposal.proposer`,
reject the request — do NOT attempt to submit from another wallet.

### Call
On the proposal contract: `submitFinalResult(conditionId, result,
evidenceURI)`.

---

## Stage 4 — DISPUTE (optional)

### Fired when
Anyone (not the proposer) calls `stakeDispute(conditionId)` with ≥ bond
amount during `disputeWindowSeconds` after the result was submitted. If
no one disputes, the submitted result becomes final when the window closes.

### If the user is the disputer
- Explain: disputing stakes bond on reverse outcome; if Supreme Committee
  agrees, disputer wins bond + penalty; if not, bond is forfeit.
- Call `stakeDispute(conditionId)` with exactly the required bond —
  pull the current required bond from the condition's
  `disputerBondRequired` (do not assume a fixed number).

### If the user is a Supreme Committee member
- Use `usePumpVoteConditionDisputeSupreme` / `voteConditionDisputeSupreme`
  (YES = uphold proposer's result, NO = flip to disputer's claim).
- Evidence is public on the condition detail page; read both sides before
  voting. Never vote without reading both evidence URIs.

### State machine
```
SUBMITTED ─(no dispute, timer elapses)→ SETTLED
SUBMITTED ─(stakeDispute)→ DISPUTED
DISPUTED  ─(Supreme votes YES)→ SETTLED (proposer's result stands)
DISPUTED  ─(Supreme votes NO)→ SETTLED (disputer's result)
```

At SETTLED, redemption opens.

---

## Stage 5 — CLAIM

Three parties, three calls, all on the proposal contract.

### Winners (holders of the winning YES/NO token)
`redeem(conditionId)` — burns the winning tokens and sends the settlement
token back at 1:1 proportional to pool-at-settlement. Losing tokens are
worthless — do not tell the user to hold onto them.

### LPs (anyone who seeded `initialPoolSize` at creation)
`claimLp(conditionId)` — returns proportional share of residual liquidity
plus accumulated fee dust. Only the proposer has LP by default on a pump
market, unless other wallets were explicitly added.

### Creator (proposer)
The 0.3% fee is transferred **at trade time**, not accumulated on-chain.
So the creator does NOT need a `harvestFees` call — the wallet already has
the funds. What the creator DOES do here: confirm the on-chain balance
matches the subgraph's `sum(trades.fee)` and flag any drift.

If the proposer also bought YES/NO for themselves, they redeem via
`redeem()` like any other winner.

---

## Recovery / safety rails

### Before any write tx
1. Verify `walletAddress` is the expected signer for this stage
   (proposer for create/submit/claimLp, any for trade, Supreme member for
   dispute vote).
2. Simulate via `publicClient.simulateContract(...)` first. If it reverts,
   parse the custom error, translate to user-friendly text (use the existing
   `parseContractError` util), and surface that instead of raw bytes.
3. If gas estimate > 2× the wallet's typical spend, pause and ask the user
   to confirm — this is usually a stuck condition or wrong param.

### Partial failures
If the CREATE tx lands but follow-up `createConditions` reverts, do NOT
retry the whole create. Delegate to the `gougoubi-recovery-ops` skill with
the proposalAddress; it will scan state and build a minimal repair plan.

### Idempotency
Every stage is idempotent on the *target state*, not on the call. Re-calling
`submitFinalResult` on an already-submitted condition reverts. Always read
`condition.status` from the pump subgraph before writing.

### Status values (pump subgraph)
- `CREATED` — tradable (conditions fresh off create).
- `TRADING` — same, with volume > 0.
- `SETTLING` — deadline passed, awaiting result submission.
- `DISPUTED_PROCESSING` — dispute active, Supreme voting.
- `SETTLED` — final, redemption open.

Treat `SETTLING` as a hint to run Stage 3; treat `SETTLED` as a hint to run
Stage 5.

---

## Subgraph queries (copy-paste ready)

All queries go to the pump subgraph (`NEXT_PUBLIC_PBFT_PUMP_GRAPH_API_URL`).
Use the `/api/pbft-pump-graph` proxy when running in the browser.

### Load a proposal with its conditions and creator income

```graphql
query PumpProposalState($address: Bytes!) {
  proposal(id: $address) {
    id
    name
    proposer
    liquidityToken
    deadline
    conditions {
      id
      name
      status
      deadline
      disputeWindowSeconds
      tradeCount
      x
      y
      finalResult
      winner
    }
  }
  trades(where: { condition_in: $conditionIds }, first: 1000) {
    id
    condition { id }
    fee
    tokenIn
    timestamp
  }
}
```

Sum `trades.fee` per `condition.id` for creator income. Do this once per
session; cache for 30 seconds.

### Quote YES buy before submitting
Compute expected out from current `x` (YES reserve) and `y` (NO reserve):
```
amountOutBeforeFee = y - (x * y) / (x + amountIn)
fee = amountIn * 3 / 1000
amountOutAfterFee = amountOutBeforeFee * 997 / 1000
```
Show the user `amountOut ± slippageTolerance` before any contract write.

---

## Conversational recipes

Pick the recipe that matches the user's first message, then follow the
numbered steps in order. Do NOT skip steps; do NOT reorder.

### Recipe A — "Open a pump market about X"
1. Gather proposal metadata (1 clarifying message, batched).
2. Gather the first condition spec.
3. Preview the full tx payload to the user (title, deadline, pool, fee note).
4. Require explicit user confirm ("ok" / "yes" / "发").
5. Call `proposeMarketCreationWithCondition`.
6. On receipt, reply with the new proposal URL and remind them that the
   0.3% creator fee will auto-flow to their wallet on every trade.

### Recipe B — "How much have I earned?"
1. Resolve `proposer` wallet (or ask).
2. Query pump subgraph for proposals where `proposer = wallet`.
3. For each proposal, sum `trades.fee` across all its conditions.
4. Group by `liquidityToken.symbol`, report per-token totals.
5. Link to the "交易量 / Trade Volume" card on the most active condition
   so the user can drill in.

### Recipe C — "Settle my market / the deadline just passed"
1. Fetch condition by id, check `status`.
2. If not `SETTLING`, explain current state and stop.
3. Ask for `result` (YES/NO/INVALID) and `evidenceURI`.
4. Require evidence; refuse without it.
5. Simulate, then call `submitFinalResult`.
6. On receipt, tell the user the dispute window length and when it closes.

### Recipe D — "Claim everything I can"
1. Fetch wallet's token holdings across this proposal's conditions.
2. For each SETTLED condition where the user holds the winning token,
   batch `redeem` calls (one tx per condition — no batch primitive
   exists in pump yet).
3. If the user is also the proposer, also call `claimLp` on any condition
   with residual LP.
4. Report totals in the liquidity token + a link to the tx hashes.

---

## Output format

Always respond in the language of the user's message. Default to Chinese
when the user wrote Chinese, English otherwise. Structure every
multi-stage operation as:

```
📍 Stage: <stage name>
🎯 Action: <concise verb phrase>
📊 Inputs: <table of resolved params>
⚠️ Checks: <simulation / state / evidence results>
▶️ Tx: <hash or "awaiting signature">
✅ Next: <what happens when this tx lands>
```

Never claim success before the receipt lands. Poll `waitForTransactionReceipt`
with timeout 90s; on timeout, return the hash and tell the user to verify
on BSCScan.

---

## What this skill must NEVER do

- Submit a result without evidence.
- Create a duplicate proposal when a live one already exists.
- Dispute without explaining bond-forfeit risk.
- Quote slippage-adjusted trades using stale (>60s old) reserves.
- Call any PBFT-mode skill (`gougoubi-activate-created-conditions`,
  `gougoubi-submit-real-results` in committee mode). Pump is not PBFT.
- Touch the user's wallet for self-trading without an explicit request.

---

## Version notes

- 1.0.0 — Initial release. Covers create / trade / settle / dispute /
  claim for single-liquidity-token pump markets on BNB Chain.
