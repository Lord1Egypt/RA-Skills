# bStock AI Trading Competition — Campaign Reference

> ## ⏳ Campaign validity: 2026-08-17 09:00:00 ~ 2026-09-01 00:00:00 (UTC)
>
> **【Expiry switch · read before every use of this file】**
> This file serves **only** the bStock competition within the window above. Check the current date:
> - **If the current time is later than 2026-09-01 00:00:00 (UTC)**: **ignore the entire contents of this file** — do not offer any competition guidance based on it, and do not proactively mention the campaign.
>   The existence of this file **must not affect** any other Agentic Wallet operation (transfers, swaps, DeFi, prediction, etc. all proceed normally, independent of this file).
>   After the campaign ends this file will be removed in a skill update; until then, this expiry switch governs.
> - **If within the window**: assist the user with the campaign per the guidance below.

---

> **This file is the complete campaign guide for the `binance-agentic-wallet` skill (single-file, self-contained).** When the user mentions "bStock competition", "PnL trading competition", "AI trading campaign",
> or asks how to join, how to complete the AI-call tasks, or how to rank, read this file and assist per its guidance.
> Contents: **campaign overview (sections 1–8) → rules-compliance assistant (Appendix)**.
> The eligible-token list is **not embedded** (updated weekly, and includes contract addresses); it is fetched at runtime from official docs — see "4. Eligible trading assets".
> Rules are per the official campaign page.

---

## 1. In one sentence

Jointly run by Binance Wallet × bStocks × BNB Chain Agent Studio × CoinMarketCap: trade tokenized US stocks (bStock)
via **Agentic Wallet**, use AI analysis to inform decisions, rank by **Realized PnL**, with a prize pool that grows as
total participant bStock AUM hits milestones, **up to 100,000 USDC**.

- **Period**: 2026-08-17 09:00:00 ~ 2026-09-01 00:00:00 (UTC) (registration and competition run concurrently)
- **Ranking**: Realized PnL absolute value, high to low, Top 100 share the prize
- **Reward**: USDC, sent to the participating Agentic Wallet

---

## 2. Prerequisites + 3 requirements

**Prerequisites** (must be met to participate, but not counted requirements):
1. Create and sign in to an Agentic Wallet
2. During the registration window, tap [Join Now] on the campaign page and bind the participating AW — **only trades after registration count; the wallet cannot be changed once confirmed**
3. Compliant / non-restricted jurisdiction (bStock is only open to permitted-jurisdiction qualified users)

**3 hard requirements** (all must hold at campaign end to rank / receive rewards):

| # | Requirement | Detail |
|---|-------------|--------|
| 1 | **CMC market-data x402 call** | Enough valid AI-analysis x402 calls via the CMC Agent Hub during the campaign |
| 2 | **Agent Studio stock-analysis x402 call** | Enough valid x402 calls via the BNB Chain Agent Studio Stock Analyze Agent during the campaign (usage fees sponsored by BNB Chain; beyond the sponsored quota, charged at the official published price and borne by the user) |
| 3 | **Realized PnL ≥ 0** | At the end, Realized PnL on eligible trading pairs must be ≥ 0 |

> 📌 **Terminology: `x402` and `b402` refer to the same thing.** `b402` is the Binance facilitator's naming; the official campaign page / announcement may use `b402`. **When the user says "b402 call" = the x402 call described in this file** — handle it per the x402 flow, no need to ask about the difference. This file uses x402 consistently (matching the CLI command `baw x402-payment` and request headers).

> **The required number of calls, sponsored quota, and overage unit price — per the official campaign page** (current guidance is ≥ 3 calls for each of the two AI tasks; numbers may change, do not hard-code). Missing any requirement → not ranked, not paid. A user may rank on PnL first, but will be removed on refresh if requirements are not met.

---

## 3. Complete the AI-call tasks (core; the two services have different flows)

> **Do not treat these two calls as a box-ticking chore.** Their output has real reference value for the user — **after each call you must distill the key conclusions for the user** (which assets to watch, what risks exist, what the data indicates), not just reply "completed call N".
> **Even if the user only says "help me complete the call tasks / rack up the count", each call must be accompanied by an interpretation relevant to their holdings / competition goals** (e.g. "this data shows X, which for your current position means Y") — turning box-ticking into useful reference. **All conclusions are for reference, not investment advice; the user decides to buy/sell and DYOR.**
> - **CMC**: crypto-market **overall sentiment** (fear & greed, BTC dominance, altseason, macro event calendar) — helps the user judge the "enter vs. wait" macro environment.
> - **Agent Studio**: BNB Chain's official **cloud-deployed automated stock-analysis Agent**, generating a **complete research report** in real time for any stock ticker — including rating, target price with up/down-side, fundamentals, technicals, investment thesis, rebalance/stop-loss reference, risk panel. Rich content, usable as **reference** for researching bStock. **After obtaining the report, faithfully summarize the rating / target price / key risks for the user, helping them understand what the analysis means for their holdings — but the final buy/sell decision is the user's own. The above is third-party analysis, not investment advice; the user should DYOR.**

Both requirements are counted by **number of successfully completed valid calls**. A call counts once its x402 payment succeeds; use `baw x402-payment preview/sign` to complete the signature. **Both CMC and Agent Studio charge every call — there is no free period.** **Final completion status is per the campaign page.**
Both services now use the unified x402 v2 standard header names: **402 returns `payment-required`, the payment request header is `PAYMENT-SIGNATURE`, settlement returns `payment-response`**.

> 💱 **Payment token for AI calls: per the `accepts` returned by `preview`, do not hard-code.** CMC and Agent Studio both support **U / USDT / USDC / USD1** as payment; however **the tokens actually available at any time are per the `accepts` list returned by each `x402-payment preview`** (may be fewer than four due to temporary server-side adjustment). Select the READY_TO_SIGN option returned by preview; do not assume any given token will or won't work.
> - Note the distinction: this is the token for **paying AI-call fees**; the **payment token for buying bStock** (BNB/USDT/USDC/U/USD1, see "4") is a separate matter — do not conflate them.
> - If the user's held tokens are not in this `accepts` → truthfully inform them "this AI payment does not support that token, you need to swap to one in accepts first", and you may guide `market-order swap`.

> ⏱️ **The signature is short-lived (~30 seconds); confirmation must be done at the `preview` stage.** Correct rhythm: after `preview` returns options, **first show the user the payment details (amount/token/purpose) and get confirmation** → after the user agrees, `sign` → **as soon as `sign` returns a signature, replay the request immediately**. **Never insert a manual confirmation or long pause between `sign` and replay** — if the signature expires (`signatureExpiresAt`) you must start over from `preview`. That is, "confirmation happens before signing; after signing it is a continuous automated action".

### 3.1 CMC (synchronous mode, endpoint `https://mcp.coinmarketcap.com/x402/mcp`)

MCP (JSON-RPC) over x402, **one 200 returns data directly, no jobId**. **Every call is paid — there is no free period**; about $0.01 each (the exact amount and supported payment tokens are per the API response).

**⚠️ Only calling the following【4 designated tools】counts as a valid call (counts toward the requirement) — not "any paid call counts"**:
`execute_skill`, `get_crypto_metrics`, `get_global_metrics_latest`, `get_upcoming_macro_events`.
Calling any tool other than these 4 (even if paid successfully) **does not count toward the requirement** — the free `tools/list`, `find_skill`, `search_*` naturally don't count, and **other paid tools likewise don't count**; don't let the user spend money for nothing. Per the official definition.

Flow:
1. `POST` endpoint, `tools/call` invoking a designated tool (no payment) → **402** + `payment-required` header (base64)
2. Decode → `baw x402-payment preview --paymentRequirements '<JSON>' --json` → select the READY_TO_SIGN option
3. `baw x402-payment sign --paymentId <id> --selectedIndex <n> --json` → obtain `paymentHeaderValue`
4. Replay the same request with the `PAYMENT-SIGNATURE: <value>` header → **200** + `payment-response`(settled) + data (same response)
5. The request needs the header `Accept: application/json, text/event-stream`; data is in the SSE `data:` line at `result.content[0].text` (parse one more level)

### 3.2 Agent Studio (asynchronous two-stage, endpoint `https://stock-agent.bnbchain.org`)

Stock analysis, **pay to get jobId → poll → download report**. **Every call is paid — there is no free period.** Each call costs about **0.1 U** (the exact amount and supported payment tokens are per the API response). The x402 payment must succeed for the call to count toward the requirement.

Endpoints: `GET /x402/price` (quote), `POST /x402/analyze/async` (submit), `GET /x402/jobs/{jobId}` (poll, header `X-Job-Token`)

> **⚠️ Every call is charged (~0.1 U).** Before submitting, **clearly tell the user this call costs about 0.1 U (exact amount/token per the API response) and which token, get consent, then proceed to sign**. The precise fee and supported payment tokens are per the `GET /x402/price` response and the `payment-required` challenge — do not hard-code; read them at call time.

> **Practical notes (common failures):**
> - **Prefer U / USD1** — they sign via EIP-3009 and need no on-chain approval. **USDC / USDT use Permit2 and require a one-time allowance**; if the user picks one without allowance set, the payment fails. When the user hasn't specified, default to U or USD1 if present in `accepts`.
> - **Per-wallet rate limit: 30 new calls per rolling hour.** On HTTP 429 (`wallet_rate_limited`), relay the error and honor `Retry-After` — **do not immediately re-sign and retry**.
> - **On `settlement_pending` (503), replay the exact same proof — never sign a new one** (a new signature risks a second charge).

Flow:
1. `POST /x402/analyze/async`, body `{"symbols":["AAPL","NVDA"],"analysis_type":"comprehensive"}` (no payment) → **402** + `payment-required` header
2. `baw x402-payment preview/sign` (select the token from the returned `accepts`, e.g. U/eip3009) → obtain signature
3. Replay with the `PAYMENT-SIGNATURE` header → **202** + `payment-response` (with on-chain txHash) + `{jobId, jobToken}`
4. Poll `GET /x402/jobs/{jobId}` with `X-Job-Token`, status `queued→running→succeeded` (usually 2~5 minutes)
5. On succeeded, returns `downloadUrl` (S3 presigned) → `GET` to download the Markdown report (rating/target price/fundamentals/technicals/risk)

#### Strictly non-blocking polling (mandatory)

After a successful submission, **the current conversation turn must end immediately and return control to the user.** The report is detailed and comprehensive, so it typically takes **2~5 minutes** to generate; do not make the user wait through it.

**"Background polling" means:**
- The user can keep sending and having other requests handled;
- You must NOT, within the same turn, chain `wait`, `write_stdin`, `sleep`, or any other blocking tool to wait for the report;
- Launching an async shell/session and then continuing to wait on it **still counts as foreground blocking and is forbidden**.

**Before submitting — confirm you can persist the credentials.** `jobId` + `jobToken` is the only credential that retrieves the report: there is no "list my jobs by address" endpoint, so a lost credential is unrecoverable and unappealable, and since every call is paid, the payment is lost with it. Confirm you have somewhere durable to write them (cross-turn task state, **not** a transient shell variable) **before** calling `POST /x402/analyze/async` — the moment the signed request is replayed the payment is made and cannot be undone.

**Mandatory steps after submission:**
1. **Write `jobId` and `jobToken` to that durable state immediately, before the first poll.** If the write fails anyway, do not quietly continue: the job is already paid for and cannot be un-submitted, so **show the user both values in plaintext right away** and ask them to keep them, so the report stays retrievable by hand.
2. Reply to the user along these lines: "Analysis submitted. The report is detailed and comprehensive, so it takes about 2~5 minutes to generate — thanks for your patience. You can keep doing other things; I'll bring you the result as soon as it's ready."
3. **End the current turn immediately — do not wait for the first poll result.**
4. **If the runtime supports background monitoring / thread wake-up**: create a single background monitor task, poll once every 10–20 seconds, and on completion wake the current task and return the report.
5. **If the runtime cannot actively wake up**: do not pretend to run in the background. Frame it gently and honestly, e.g. "The report is detailed and comprehensive, so it takes a few minutes (about 2~5) to generate — thanks for your patience. I'm not able to ping you on my own here, so just send me any message when you're ready and I'll fetch the finished report for you right away." Then on the user's next message, poll the saved job first before anything else.
6. **Always poll the same `jobId`; never re-submit because it is taking longer** (a re-submit = double payment).

**Acceptance criteria:**
- Zero `wait`/`write_stdin`/`sleep` calls in the same turn as the submission;
- The user can continue the conversation without waiting for the report to finish;
- `jobId` + `jobToken` is not lost before the job completes;
- No second analysis job is created before the report completes.

> **If a job fails**: poll may return `status: failed`. **Only if the response also has `retryable: true`**, call `POST /x402/jobs/{jobId}/resume` (with the `X-Job-Token` header) to retry — **resume does not charge again** (no new payment/signature). If `retryable` is false or resume returns 409/410, the job is permanently done; do not create a new paid job to work around it without telling the user (that would pay twice).

> **Counting note**: **one successfully completed call counts as 1** (per a successful x402 payment; every call is paid), not tied to whether the final report is produced. **Final completion status is per the campaign page.**

> **Shell compatibility**: in polling scripts, do not name a variable `status` — use `job_status` instead, and test the script against a mock response before real submission.

---

## 4. Eligible trading assets (two sources: API for addresses + list for eligibility)

> ⚠️ **Distinguish two things**: ① where the **contract address** comes from ② **whether it counts toward campaign PnL** (eligibility). The two sources differ — do not conflate.
> - **Address source = `type=3` API** (authoritative, contains all bStock contract addresses, fetchable anytime).
> - **Eligibility = weekly eligible list** (updated weekly, determines whether the asset counts this week; in the list = eligible).
> Before buying: **first get the bStock contract address from the API → then check against the current week's list for eligibility** — do both steps.

**① Use the `type=3` API to resolve bStock contract addresses** (the full set of bStock, with Ticker / symbol / contractAddress / chainId / multiplier):

```bash
curl -sS --max-time 25 \
  -H 'Accept-Encoding: identity' -H 'User-Agent: binance-web3/1.1 (Skill)' \
  'https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai?type=3'
```

- `type=3` = bStock (symbol suffix `B`); `type=1` = Ondo (suffix `on`); `type=2` = xStocks-style (suffix `x`). **Resolving bStock must use `type=3`**.
- The `binance-tokenized-securities-info` skill is **optional** — it wraps the same API and adds live market data, but older versions of it only know `type=1` (Ondo). Do not rely on it to resolve a bStock unless you have confirmed the installed version handles `type=3`; call the endpoint above directly instead.
- When the user reports a Ticker with a `b`/`B` suffix (e.g. "DRAMb") → it almost certainly means the bStock; find it in `type=3` by ticker/symbol (e.g. DRAM → `DRAMB`), and **never resolve to the Ondo `DRAMon`**.

**② Use the weekly eligible list to determine whether it counts toward campaign PnL** (updated weekly, **not embedded** in this skill):

**The eligible list's authoritative source is the "Eligible bStock List" page in the official developer docs** (updated weekly, with effective week + Ticker/symbol/project name/contract address):

- English: `https://web3.binance.com/en/dev-docs/products/agentic-wallet/use-cases/campaigns/bstock-eligible-tokens`
- Chinese: replace `/en/` with `/zh-CN/`

To determine whether an asset counts: **in the current-week list on that page = counts**; not in the list → clearly tell the user "does not count toward the campaign this week" (still tradable, just not scored). First check the "Effective week" at the top of the page and tell the user "this list is as of week X".

- **Having an address ≠ counting toward the campaign**: a bStock in the `type=3` full set (see "4①") is not necessarily in the current-week eligible list. It can be bought, but whether PnL counts is per the list.

**Determination rules (general, invariant across list updates)**:
- **A bStock in the current-week eligible list is eligible**; eligibility is assessed **per week**, and once removed it stops counting from the new effective week.
- **Only eligible-token trades completed via Agentic Wallet count**; trades via Binance Alpha, third-party dApps, or non-AW **do not count at all**.
- The list may include **leveraged/inverse ETFs** (e.g. 3X/2X long/short) — amplified volatility, amplified risk and reward; be especially careful when maintaining PnL≥0.
- If the list page is temporarily unavailable (network / doc changes): **truthfully tell the user the live list is temporarily unavailable and recommend the official campaign page; do not fabricate or pad with an old list**. Eligibility is then unconfirmed, so the security pre-check exemption below does **not** apply.

**Trading guidance (default behavior in the campaign context)**:
- When the user says "buy/sell some stock" in the campaign flow (e.g. "buy some Nvidia", "add to SPY"), **interpret it by default as trading the corresponding eligible bStock** (NVDAB / SPYB…), without repeatedly asking "do you mean the bStock". First confirm the asset is in the current-week list, then proceed directly with the bStock trade; only clarify if the asset is not in the list or the user explicitly means a different asset.
- **⚠️ Tokenized stocks must be resolved as bStock, not Ondo.** Tokenized US stocks exist in multiple systems: **Ondo** (suffix `on`), **xStocks-style** (suffix `x`), **bStock** (suffix `B`). Resolve bStock contract addresses using the **`type=3` API** from "4①" (not `type=1` — that is Ondo). Therefore:
  - **During the campaign, only buy bStock**: eligible PnL only recognizes bStock in the current-week list. Mistakenly buying "DRAMb" as the Ondo "DRAMon" (a different contract) **does not count toward the campaign and is simply a wrong purchase**.
  - If a Ticker exists in `type=3` but is **not in the current-week eligible list** → tell the user "it can be bought but does not count this week", and let them decide; **never fall back to buying the Ondo version as a substitute**.
  - When the user reports a Ticker with a `b`/`B` suffix (e.g. "DRAMb"), it almost certainly means the bStock — never resolve it to Ondo.
- **⚠️ The payment token (fromToken) must be a PnL-eligible token, or the campaign does not count it.** Only buying bStock with the following **5 tokens** makes the trade count toward campaign Realized PnL:
  - **BNB, USDT, USDC, U, USD1**.
  - Using any other token (including Ondo tokenized stocks, other altcoins, other bStock) as the payment token to buy bStock → **that trade does not count toward campaign PnL**, i.e. wasted.
  - If the user does not specify a payment token before ordering, **first ask which of these 5 to use.** In a campaign context the payment token is not a free choice — picking one silently can void the trade's score — so this is the one case where payment-token selection *is* its own question (see SKILL.md "Build the Command" rule 4). If the user names a payment token outside these 5, **proactively warn "this will not count toward campaign PnL"** and ask them to confirm or switch to an eligible token.
- **⚠️ Trading requires BNB for gas (AI tasks do not)**: the x402 payment for CMC / Agent Studio is **gasless** (signature authorization, gas borne/sponsored by the settlement party), so completing the AI-requirement tasks **requires no BNB**; however **buying/selling bStock is a normal on-chain transaction and must use BNB for gas**. **Remind the user not to convert all funds to stablecoins / bStock without keeping BNB** — otherwise the first transaction will fail for lack of gas, and the user often won't know why. If BNB balance is found to be too low before ordering, prompt them to top up a little first.
- **Whitelist exemption from the security pre-check**: a bStock **confirmed present in the current-week eligible list** has been vetted at the list level, so the `query-token-audit` pre-check **may be skipped when trading it** (equivalent to the trusted assets in SKILL.md "Common Token Addresses"; proceed directly to the order flow: confirm slippage → build → execute), for a smoother interaction.
  - **The exemption requires a positive list hit.** If the list page cannot be fetched or parsed for any reason, nothing has been confirmed — **fall back to the normal `query-token-audit` pre-check**. Never read "the list is unavailable" as "the token is whitelisted".
  - Tokens outside the list go through the pre-check as usual.

---

## 5. Prize pool (tiered, unlocked by total registered-participant bStock AUM)

- The prize-pool size **unlocks in tiers, permanently (does not retract if AUM dips)** as the total bStock AUM held via AW by **all registered users** hits milestones; the higher the AUM, the larger the total pool, and Top 100 are allocated by Realized PnL rank.
- **Each tier's AUM threshold, prize amount, number of slots, and the specific allocation per rank bracket — per the official campaign page** (numbers may change, do not hard-code / do not go from memory).
  Campaign developer docs (with flow explanation) → https://web3.binance.com/en/dev-docs/products/agentic-wallet/use-cases/campaigns/bstock-pnl-contest
- If there are fewer qualified participants than slots, only qualified participants are paid; empty brackets are not reallocated.

---

## 6. Realized PnL definition

- **Definition: only the buy/sell difference, gas not counted.** Realized PnL = proceeds from selling − cost of buying, **both at actual execution amounts**. On-chain **gas (BNB miner fee) is not counted in PnL** — it is paid separately in BNB and does not affect the PnL figure.
- **But the trading fee has an indirect effect.** The fee is deducted from the fill, directly reducing the token quantity you actually buy / the amount you receive on selling, so it is already reflected in "cost of buying" and "proceeds from selling" and is naturally included in PnL.
- ⚠️ **Do not conflate gas with PnL.** Book PnL reflects only the buy/sell difference; your wallet's actual profit/loss must further subtract gas. In small trades gas may far exceed book PnL, but **the campaign ranking only looks at book PnL, not gas**. **Final definition is per the official campaign page / rules.**
- **FIFO lot-by-lot matching (not "one calc with an average price")**: each sell is matched **first-in-first-out**, deducting the corresponding quantity lot-by-lot from the earliest open buy lots and computing PnL lot-by-lot, then summing all closed lots. **With multiple buy lots, never use the simplified "(sell price − average buy price) × sell quantity" — it computes wrong.**
  - **Cross-lot example**: buy 2 shares @ $10 (lot A), then buy 2 shares @ $20 (lot B), then sell 3 shares @ $15. FIFO matching: the 3 shares sold = all 2 of lot A + 1 of lot B. Realized PnL = ($15−$10)×2 + ($15−$20)×1 = $10 − $5 = **+$5**. Remaining position: 1 share of lot B @ $20 (open, not counted in Realized PnL).
  - If the simplified formula wrongly uses the average buy price $15: (15−15)×3 = $0, far from the correct +$5 — this is why lot-by-lot is required.
- **Only sold-and-realized counts**: positions not sold at campaign end produce no Realized PnL and do not rank (a rule fact, not an operational suggestion).
- **Rule fact**: Realized PnL only counts the closed portion; AUM milestones look at the held amount. The two are measured by separate rules — **buy/sell decisions are the user's own; this skill does not provide timing or position advice.**
- **⚠️ Eligible payment tokens**: buying bStock with the 5 tokens **BNB / USDT / USDC / U / USD1** counts toward PnL; buying with other tokens does not (see "4. Trading guidance").

---

## 7. Reward distribution & review

End → 72h post-campaign review → 72h public display (may contact official support to appeal) → USDC sent to the participating AW within 14 business days.
The leaderboard's and eligibility-status's refresh cadence and definition are per the official campaign page; final results are per the post-campaign review.

---

## 8. Common pitfalls

- Trades before registration don't count — register first, then trade; the wallet cannot be changed once confirmed.
- Only touch bStock in the current-week eligible list (see "4"), via AW; Alpha/third-party dApps don't count.
- **Payment token only BNB/USDT/USDC/U/USD1** — buying bStock with other tokens does not count toward PnL (see "4. Trading guidance").
- **Keep BNB for gas** — AI-analysis tasks are gas-free, but buying/selling bStock needs a little BNB for gas; don't convert the whole balance to stablecoins/bStock and cause the first transaction to fail (see "4. Trading guidance").
- **Buy bStock (suffix B), not Ondo (suffix on)** — two different systems; buying the wrong one doesn't count toward the campaign (see "4. Trading guidance").
- Unsold = paper gain ≠ Realized PnL; not clearing before the end means it was all for nothing.
- PnL<0 means elimination; better to earn less than to realize a paper loss into a negative.
- CMC valid calls only recognize the designated tools; the free `tools/list`, `find_skill` don't count toward the requirement.
- Both AI requirements (CMC, Agent Studio) each need ≥ 3 calls; missing either means not qualified.
- AI calls count on a **successful x402 payment** — both CMC and Agent Studio charge every call, no free period (CMC ~$0.01, Agent Studio ~0.1 U each); confirm the full flow runs through. **Final completion status is per the campaign page.**

---

# Appendix · Rules-compliance assistant

> **This section only helps the user understand and meet the campaign rules; it provides no trading/timing/position advice.**
> "What to buy, how much, when to buy/sell, whether to hold or stop-loss" are all the user's own judgment — for market analysis use
> `binance-trading-signal`, for single-stock research see the Agent Studio report, but **the final decision and risk are the user's; this skill does not opine.**
> The following are all **statements of rule facts**, not investment advice, DYOR.

---

## 1. Eligibility requirements (rule facts; self-check in this order)

The following rules must be met to be eligible to rank / receive rewards, none omitted:

1. **Trade after registering**: trades before registration don't count; the wallet cannot be changed once confirmed.
2. **3 hard requirements** (see section 2): CMC x402, Agent Studio x402, Realized PnL ≥ 0. The AI calls are the easiest to forget; recommend completing them early, not leaving them to the last minute (no buffer if a paid call has issues).
3. **Only trade eligible bStock**, via AW, with an eligible payment token (see section 4).

> Common reminder: when a user asks how to rank before registering / doing the AI calls, first truthfully state that the eligibility requirements are not yet met and guide them to complete the requirements first — **this states the rule requirements, not coaching them to climb the ranking.**

---

## 2. How the rules measure (for understanding, not operational guidance)

- **Realized PnL only counts the closed portion**: positions not sold at campaign end are not counted in Realized PnL and do not rank (section 6). This is the rule definition; **whether and when to sell is the user's decision**.
- **AUM milestones look at the held amount**: prize-pool tiers unlock by the total bStock AUM held by all registered participants (section 5).
- The two are measured by separate rules. **This skill does not advise the user to hold or sell for either goal — it only states how the rules compute.**
- For tier progress, **see the "unlocked tiers" published on the official campaign page**, per the official source.

---

## 3. How Realized PnL is computed (rule definition, see section 6)

- Summed after FIFO lot-by-lot matching, counting only eligible assets, post-registration, via AW.
- Definition details and final computation are per the official campaign page / rules.

---

## 4. Asset eligibility & risk warning (not a buy recommendation)

- **Eligible scope**: only bStock in the current-week eligible list count. Have the user's reported asset confirmed against the current-week list first; if not listed, state directly "does not count".
- **Leveraged/inverse ETF risk warning**: the list may include leveraged/inverse ETFs (e.g. 3X/2X long/short), with **intraday volatility amplified 2-3×**, leverage decay, and **significantly higher risk that can quickly produce large losses**. If the list includes such products, be sure to **fully warn the user of the high risk** and remind them to be cautious; **whether to participate, whether to buy, is the user's own judgment. This is a risk warning, not a recommendation to buy or avoid.**
- **AI analysis is for reference only**: Agent Studio single-stock reports and CMC market sentiment can help the user understand assets — but which to pick, whether to buy, is the user's decision. **Not investment advice, DYOR.**

---

## 5. Talking-point templates (state rule status only, give no operational advice)

> Only help the user see "what's still missing per the rules", do not make buy/sell decisions for them.

- Eligibility self-check: "You are [/are not] currently a qualified participant. Per the rules you still need X (e.g. N more AI calls / not yet registered). Would you like to complete this first?"
- Rule clarification: "Realized PnL only counts the portion already sold; unsold positions do not count in the ranking — this is the rule definition. Whether and when to sell is your decision; I won't judge the market for you."
- Boundary note: "You're asking whether to sell now / hold on — that's a trading decision, beyond what I can give. I can only tell you how the rules compute; please make the operational call yourself and DYOR."
