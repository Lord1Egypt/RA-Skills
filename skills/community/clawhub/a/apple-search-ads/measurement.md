# Measurement — Which Numbers to Trust and How to Read Them

Attribution sources disagree by design. This file is the canonical home of the provisional-window rule, source-of-truth selection, LTV estimation, incrementality testing, and cohort ROAS. Implementation of the SDKs lives in `ios-integration.md`; this is the analysis side.

Contents: Source of Truth · Why Counts Never Match · Provisional Windows · Reconciliation Drill · LTV Estimation · Cohort ROAS · Brand Incrementality Holdout · Reading SKAN

## Source of Truth per KPI

Pick once per KPI, record the choice in `~/Clawic/data/apple-search-ads/memory.md`, never switch mid-analysis. Defaults (with `mmp` set in config, the MMP takes the install/event rows):

| KPI | Source | Why |
|---|---|---|
| Spend, taps, impressions | ASA reports | Apple bills on these; no other system sees them |
| Installs (per campaign/keyword) | MMP if present, else ASA | MMP deduplicates across channels; ASA only sees itself |
| Cross-channel comparison | MMP only | ASA numbers are not comparable to other networks' self-reported installs |
| Trials, purchases, retention | MMP or your backend | ASA stops at the install |
| Revenue | Store reports / your backend | The only figures that survive finance review |
| Aggregate install validation | SKAN postbacks | Apple-signed counts, immune to SDK misconfiguration |

## Why the Counts Never Match

Structural gaps — expected, not bugs:

| Gap source | Mechanism |
|---|---|
| Attribution window | ASA credits a 30-day tap-through window; MMPs apply their own (usually shorter) window to ASA traffic — taps older than the MMP window count for ASA only |
| Date basis | ASA books the install on the TAP date; MMPs book it on the install date; SKAN books it on postback arrival. Three timelines for one install |
| Re-downloads | ASA counts them (reported separately as `redownloads`); MMPs may classify the same event as a re-attribution, not an install |
| Consent | AdServices attribution works without ATT at campaign level, so ASA and the MMP's ASA integration keep counting; anything IDFA-based in the MMP shrinks with consent rates |
| SKAN privacy thresholds | Low-volume campaigns get null or coarse conversion values withheld by crowd anonymity — missing data, by design |
| Modeled rows | Some MMPs model installs where signals are missing; modeled and measured rows should never be summed silently — check the flag |

## Provisional Windows (canonical rule)

Installs attribute retroactively to their tap date across the full 30-day window. Consequences:

- A report row is only stable once its end date is **≥2 days back**; the newest 1-2 days always under-count installs and over-state CPA. This is the #1 false CPA alarm (`troubleshooting.md`).
- Judgment windows: 7 days for most decisions, 14 for competitor campaigns (`strategy.md`), always ending ≥2 days back — the same rule SKILL.md Output Gates enforces.
- Spend is final same-day; installs are not. A "yesterday" report is a spend report, not a CPA report.
- Long-tail backfill: a window can still gain a few installs up to 30 days after its last tap date. Treat month-old rows as final; treat week-old rows as ~stable; treat yesterday as noise.

## Reconciliation Drill

When someone asks "which install number is right":

1. Fix the timezone — one `report_timezone` value (config) in every ASA request; confirm the MMP dashboard is set to the same zone.
2. Fix the window — both sources over the same dates, ending ≥2 days back.
3. Fix the date basis — you cannot fully align tap-dated (ASA) and install-dated (MMP) rows; expect bleed at both edges of the window.
4. Compare per campaign, not account totals — a gap concentrated in one campaign is a clue (re-downloads, one keyword, one country); a uniform gap is structural.
5. Accept the residual — after alignment a stable percentage gap persists. Track that its SIZE stays stable month over month; a stable gap is structure, a moving gap is a new problem.
6. Report the number from the declared source of truth, with the gap noted once — never average the two sources.

## LTV Estimation

LTV anchors target CPA (= LTV / `ltv_divisor`, config; `strategy.md` runs the bid math). Use the highest rung of this ladder you can reach:

1. **Mature cohorts (≥6 months of revenue history)** — measure it: cumulative net revenue per user of a cohort, read off your own curve. No modeling needed.
2. **Young app with some history** — LTV ≈ D30 ARPU × (LTV ÷ D30-ARPU ratio taken from your OLDEST comparable cohort). The multiplier must come from your own curves — category-average multipliers imported from blog posts are the top source of inflated bids.
3. **Subscription app, pre-history** — build it from the funnel: LTV ≈ paywall-view rate × trial-start rate × trial-to-paid rate × (price × expected retained periods). Every factor is measurable within weeks except retained periods — take that one conservatively and revisit monthly.
4. **Paid app** — LTV ≈ price net of Apple's commission plus measured IAP/upsell ARPU. The simplest case; the mistake is forgetting the commission.

Recompute quarterly; a target CPA computed from a stale LTV silently misprices every bid in the account.

## Cohort ROAS

- ROAS(d) = cohort net revenue through day d ÷ cohort spend. Always cohort-based (users acquired in period X), never calendar-based (revenue in period X ÷ spend in period X) — calendar ROAS mixes old users' revenue with new users' cost and flatters every scaling decision.
- Choose the payback window from runway, then derive the early gate from your own curve: if your curve shows D30 revenue is ~1/3 of D180 revenue, a 100%-by-D180 payback target implies a ~33% D30 ROAS gate. The shape ratio comes from your cohorts, not from a benchmark.
- Judge campaigns against the gate at the same cohort age — comparing a 10-day-old cohort's ROAS to a 90-day-old one's is the calendar mistake in disguise.

## Brand Incrementality Holdout

Tests whether brand-term spend buys installs you would have gotten organically (SKILL.md Rule 5 and Where Experts Disagree).

Protocol:
1. Baseline 2 weeks: record TOTAL daily installs (paid + organic, from App Store Connect) and paid brand installs, in a stable period (no feature releases, no press).
2. Pause the brand campaign 2 weeks; record total installs.
3. Incremental fraction = (total_on − total_off) ÷ paid_brand_installs_on. Near 1 → brand spend is genuinely additive. Near 0 → organic absorbed the demand; those users searched your name and installed anyway.
4. Watch the search results page during the OFF weeks: if a competitor takes the top slot on your brand terms, the test is measuring defense, not incrementality — defense value is real and the answer is "keep defending" regardless of the fraction (Rule 5).
5. Multi-country accounts: run the holdout in ONE comparable market instead of alternating time — cleaner than a time split when seasonality is strong.

## Reading SKAN

Implementation (bit mapping, postback registration) is in `ios-integration.md`. Analysis rules:

- Three postbacks per install over 0-2, 3-7, and 8-35 day windows; only the first carries the fine 0-63 value. With randomized delays on top, a cohort's SKAN picture is not complete until ~6 weeks after install — schedule SKAN-based reviews accordingly.
- Never daypart or day-compare on SKAN install timing; postback arrival is deliberately decoupled from install time (SKILL.md Traps).
- Null and coarse conversion values concentrate in low-volume campaigns (privacy thresholds). Consolidating tiny campaigns raises measurable signal — a real argument against over-fragmenting the account structure.
- Use SKAN as the validation layer: if MMP-reported ASA installs exceed SKAN counts by a wide and growing margin, suspect the MMP's window or modeling settings — Apple-signed postbacks do not inflate.
