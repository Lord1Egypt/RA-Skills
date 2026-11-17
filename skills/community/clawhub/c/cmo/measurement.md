# Measurement — Attribution, Incrementality, Dashboards, Forecasting

Three different questions get confused into one word. Keep them separate and most measurement fights end:

| Question | Instrument | Never use it for |
|----------|-----------|------------------|
| Which ad/keyword/page performed better inside a channel? | Platform and web analytics | Deciding budget between channels |
| Where should the next dollar go across channels? | Self-reported + spend-to-pipeline over quarters + MMM | Optimizing a single ad |
| Did this spend cause revenue that would not have happened? | Holdout / incrementality test | Weekly optimization; it is slow and expensive |

## Attribution

Every method lies in a known direction; use each only for what it can see:

| Method | Blind spot | Use for |
|--------|-----------|---------|
| Software (touch-based) | Word of mouth, dark social, podcasts — undercounts creation | In-channel optimization: which ad, which keyword |
| Self-reported (required "how did you hear about us?" free-text field on signup/demo forms) | Memory bias toward recent and memorable touches | Budget allocation across channels |
| Spend-to-pipeline correlation over quarters | Slow, confounded by everything | Validating big shifts and brand spend |
| Media mix modelling (MMM) | Needs years of spend variation; cannot see creative | Portfolio allocation at large, multi-channel spend |

- Never allocate budget from last-touch alone: it awards the cash register, not the shelf.
- Run software and self-reported side by side; where they disagree is exactly where hard-to-track channels are working.
- First-touch flatters demand creation, last-touch flatters capture, and linear flatters whoever has the most touchpoints. All three are ways of dividing credit, none is a measurement of cause.
- Signal loss is permanent, not a bug to fix: platform privacy changes, consent banners, and ad blockers mean a growing share of conversions are modelled rather than observed. Build the measurement stack on the assumption that tracking sees less every year — the self-reported field and holdout tests both survive it.

## Incrementality Testing (the only causal instrument)

Ranked by cost and rigour:

1. **Geo holdout** — split comparable regions into test and control, hold spend at zero in control for a defined window, compare total outcomes (not tracked ones). Best general-purpose test for paid and brand.
2. **Audience holdout** — a randomly withheld share of the target audience; supported natively by several large ad platforms as a lift study. Cheaper, narrower.
3. **Pulse test (on/off)** — pause a channel entirely for a period and read total pipeline. Blunt, confounded by seasonality, but free and often decisive for brand-term spend (`paid.md`).
4. **Ghost/PSA ads** — control group sees an unrelated ad; measures ad exposure effects cleanly where available.

Design rules: pre-register the metric, the window, and the decision *before* starting; make the window at least one full sales cycle plus the reporting lag; pick control regions on historical similarity, not on convenience; and accept that a well-run test can only detect effects large enough to matter — if the expected lift is smaller than the noise, do not run it, and say so instead of running an underpowered test.

Cadence: the two largest spend lines get a holdout at least annually (SKILL.md Rule 9), and any line before a proposed doubling.

## UTM and Naming Taxonomy

Decide once, write it down, enforce it in a link builder rather than in human discipline:

```
utm_source   = the platform            (linkedin, google, newsletter-name)
utm_medium   = the paid/organic class  (cpc, paid-social, email, referral, organic-social)
utm_campaign = campaign slug           (2026q1-security-launch)
utm_content  = the asset variant       (video-a, static-b)
utm_term     = keyword or audience
```

Rules: lowercase everything (parameters are case-sensitive and `LinkedIn` and `linkedin` become two channels); never UTM your own internal links (it restarts the session and destroys the original source); keep a single source-of-truth sheet; and audit quarterly against the channel-grouping rules in analytics. A taxonomy change is a breaking change — annotate the date or next year's comparison is nonsense.

## Dashboards

- **Executive (monthly)**: pipeline created and influenced by channel, CAC and payback trend, spend vs. plan, one brand-health indicator (`brand.md`).
- **Operational (weekly)**: stage-by-stage conversion per channel, campaign performance vs. kill lines, lead SLA compliance, creative fatigue signals.
- **Experiment log (continuous)**: every test with its kill line, its read date, and its outcome — including the ones that were killed. Without the log, the same failed channel gets re-tested every 18 months by a new hire.
- Every metric needs a named owner and a threshold that triggers action; a metric nobody acts on is decoration.
- Brand metrics get quarterly review, not weekly — they move on brand timescales (`brand.md`).
- Default cadence follows `reporting_cadence` in Configuration.

## Data Hygiene Before Insight

Most "the numbers are wrong" incidents are one of these: duplicate conversion events firing twice, a consent banner blocking analytics for a share of visitors, a form that stopped writing the source field, self-referrals from a payment redirect, bot traffic inflating a channel, or a CRM stage renamed without an annotation. Check these six before rebuilding a model.

Annotate every change — tracking, taxonomy, site structure, pricing, stage definitions — on a shared timeline. Six months later that timeline is the only thing that explains the step change in the chart.

## Forecasting

Build the forecast from the demand waterfall (`demand.md`), not from a growth rate: for each channel, expected volume × stage conversion rates × ACV, offset by the stage duration. Then apply two adjustments and show them separately — capacity (can sales work this volume?) and seasonality (from your own history, not from an industry chart).

Publish a range, not a point, and state the assumption that would break it first. A forecast whose miss cannot be traced to a named assumption teaches nobody anything.

## Reporting to the Board and the CEO

Lead with the pipeline number against plan, then the two decisions you need, then the evidence. Three habits that build credibility fast: show the same metric definitions every quarter (a redefined metric reads as a cover-up); report the experiments that failed alongside the ones that worked; and separate "what we control" (spend, output, conversion rates) from "what we influence" (revenue, win rate) so that a sales-side miss does not get argued as a marketing failure — or vice versa.
