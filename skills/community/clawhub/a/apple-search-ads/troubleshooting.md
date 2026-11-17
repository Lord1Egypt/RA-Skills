# Troubleshooting — Symptom to Cause

Diagnosis chains for Apple Search Ads, ordered by probability. Each step is a check, not a guess. Numbers (spend gate, windows, bid steps) are the canonical ones from SKILL.md Core Rules and `strategy.md` — this file applies them, it never redefines them.

Contents: First Three Checks · No Impressions · Campaign Not Spending · Spend But No Installs · CPA Suddenly Spiked · ON_HOLD / Rejected · API Errors · Counts Disagree · Truly Stuck

## The Universal First Three

1. **Status chain, top down**: campaign → ad group → keyword. A campaign shows ENABLED while its only ad group is paused, or the keyword sits in PAUSED — the dashboard summary hides this. Via API: `servingStatus` and `servingStateReasons` on the campaign object name the exact blocker (billing, dates, approval).
2. **Re-pull the window that ended ≥2 days back** (`measurement.md`). Installs attribute retroactively to tap date; the most common "problem" is a provisional report row.
3. **Open the search term report.** What actually spent the money is frequently not the keyword you are staring at — exact match serves plurals and misspellings (SKILL.md Rule 3).

## No Impressions on a Keyword

Ordered by frequency:

1. **Status chain** — the first-three check above; also confirm the keyword's own status is ACTIVE.
2. **App not eligible in that storefront** — `GET /apps/{adamId}/eligibilities?countriesOrRegions=...` (`api-reference.md`); an app not live in a country buys nothing there, silently.
3. **Bid below the auction floor** — raise stepwise per the bid rules in `strategy.md` ("Impressions ≈ 0 but keyword relevant" branch). If impressions appear but TTR sits <3%, it is relevance, and no bid fixes it.
4. **Relevance too low to enter the auction** — ASA weighs app metadata against the query. If the term is nowhere in your App Store metadata and TTR history is poor, Apple stops serving you. Fix order: ASO metadata first, then re-bid (route to `aso` for the listing work).
5. **You are competing with yourself** — the same query is targeted in two of your campaigns without cross-negatives; one of them wins, the other reads as dead. Check the search term report of every campaign for the term (`strategy.md` → cross-negation wiring).
6. **Genuinely low query volume** — long-tail terms can be correct and near-zero. Judge by the spend gate, not impressions: a $0 keyword costs nothing to keep.

## Campaign Not Spending Its Budget

1. **`servingStateReasons`** — billing failure, end date passed, or pending approval show here explicitly before any auction logic matters.
2. **Bids too low to win enough auctions** — expected taps/day = daily budget ÷ avg CPT. $50/day at $2.50 CPT is only 20 taps; if actual taps run far below that, bids are losing, not budget capping. Raise per `strategy.md` bid rules.
3. **`cpaGoal` set too tight** — it never caps spend (SKILL.md Traps) but it does signal Apple to suppress delivery when predicted CPA exceeds it. It fails in both directions. When diagnosing under-delivery, remove `cpaGoal`, wait a full day, compare.
4. **Keyword pool too small or all long-tail** — 10 exact long-tail terms cannot absorb $100/day. Add tier-3/4 keywords or a discovery ad group (`strategy.md` → Keyword Tiers).
5. **Dayparting or geo refinements** — a `daypart` window or `adminArea` list quietly shrinks supply; audience refinements additionally exclude every Personalized-Ads-off user (SKILL.md Traps).
6. **Country CPT mismatch** — a bid ported from a cheap market loses every auction in an expensive one. Bids are per-market decisions (SKILL.md Rule 6).

## Spend But No Installs

1. **Provisional window** — installs lag spend inside the report; re-check once the window ends ≥2 days back (`measurement.md`) before touching anything.
2. **Apply the spend gate** — any keyword at ≥2× target CPA with 0 installs acts today (SKILL.md Rule 7): cut the bid 30-50% or pause.
3. **Wrong queries, right keyword** — search term report: broad and Search Match buying adjacent-but-wrong intent. Negate the junk terms; the keyword itself may be fine.
4. **Page-query mismatch** — taps are real, CVR is broken: the product page does not pay off what the query promised. Custom Product Page per theme (`strategy.md`) or route to `aso`.
5. **Attribution broken, installs real** — spend and taps with zero installs across ALL campaigns simultaneously is an integration smell, not a performance one: verify AdServices/MMP wiring (`ios-integration.md` → Testing Attribution).
6. **Re-downloads absorbing the wins** — check `redownloads` vs `newDownloads` (`api-reference.md` → metrics): reaching your existing users is retention spend, not acquisition.

## CPA Suddenly Spiked

Check in this order; each is a one-minute test:

| Suspect | Check |
|---|---|
| Provisional rows (the #1 false alarm) | Does the window end ≥2 days back? Spend lands same-day, installs trickle in — fresh windows always over-state CPA (`measurement.md`) |
| Budget raised beyond the 20-30% step band | Compare budget change log to the spike date; revert to the last stable budget the same day (`strategy.md` → Scaling) |
| New competitor entered the auction | Impression share band dropped over the same days; brand terms hit first (SKILL.md Rule 5) |
| Search-term mix shift | Search term report before/after: broad or Search Match found a new expensive query — negate it |
| Product page or price changed | Any App Store metadata/screenshot/price release near the spike date; CVR moves every CPA in the account |
| Seasonality / weekend pattern | Compare same weekday last month before concluding anything from a 2-day move |
| One keyword dragging the blend | Keyword-level report sorted by spend: a single runaway keyword often explains a campaign-level spike — spend gate it |

## Campaign ON_HOLD or Ad Rejected

- **Billing** — card declined or credit line exhausted; the single most common ON_HOLD cause. `servingStateReasons` states it; fix in account settings, campaigns resume without recreation.
- **App state** — app removed from sale, pulled from a storefront, or a rejected app update: ads pause with it. Check App Store Connect first, ASA second.
- **Creative review** — Today tab placements require creative approval before serving; a rejection there stalls only that campaign. Search results ads use your live product page and have no separate review.
- **Country eligibility change** — an app pulled from one storefront kills that country's campaign while others run; the eligibilities endpoint confirms.

## API Errors

| Error | Causes in order | Fix |
|---|---|---|
| 401 UNAUTHORIZED | Access token >1h old · client secret JWT malformed (wrong `aud`, missing `kid`, not ES256) · JWT `exp` passed | Mint a new token; regenerate the client secret only if the token exchange itself fails (`api-reference.md` → Authentication) |
| 403 FORBIDDEN | `X-AP-Context: orgId=` missing or pointing at an org this user can't touch (multi-org accounts) · API access not granted to this user/key in account settings · resource belongs to another org | `GET /acls` lists the orgs and roles your credentials actually hold — compare against the orgId you are sending |
| 404 NOT_FOUND | Wrong campaign/adgroup/keyword ID, or right ID under the wrong org context | Re-list the parent to confirm the ID exists under this orgId |
| INVALID_FIELD | Payload shape drift — commonly money objects (`{"amount":"5.00","currency":"USD"}` with amount as string) or a phased-out field | Compare against the request bodies in `api-reference.md` |
| 429 LIMIT_EXCEEDED | Per-org throttle, or token minting per request | Backoff and batching rules in `api-reference.md` → Rate Limits |

## ASA, SKAN, and MMP Counts Disagree

They always disagree; the question is whether the gap is structural or a bug. Reconciliation drill, expected gap sources, and the source-of-truth table live in `measurement.md`.

## When You Are Truly Stuck

Reduce to a known-good minimum: one campaign, one ad group, one exact-match brand keyword, bid at tier-1 level (`strategy.md`), no refinements, no `cpaGoal`. Your own brand term with a strong bid should show impressions within a day — if it does, the account plumbing works and the problem is in whatever you removed; re-add one layer at a time. If it doesn't, the problem is account-level: eligibility, billing, or approval — the chains above name where to look.
