# Ten-paper deadline routing test

Use this as the first regression case for `ai-conference-deadline-radar`.

## Input

```text
AAAI / ICLR / AISTATS / CLeaR / WSDM deadline 找一下。我们在做两个月十篇顶会论文挑战，当前 sprint 候选是 A2 Causal Mind Decision Delta、B1 ProviderHealth Probe Semantics、B5 Research Production Line State Machine。今天该抢哪个会，哪个只是 watch？
```

## Required behavior

- Starts from radar/index sources such as `mlciv/ai-deadlines`, and uses `ccfddl-rss` structured records as fast CCF/rank/category hints when available.
- Verifies decision-critical dates against official CFP / OpenReview / submission pages.
- Separates `official_confirmed`, `historical_estimate`, `radar_hint`, and `unverified`.
- Separates abstract, full paper, supplement/code, timezone, and notification when available.
- Does not present ICLR/AISTATS/CLeaR 2027 dates as confirmed unless official current-year sources are found.
- Maps A2/B1/B5 to venues by evidence shape, not just topic.
- Ends with next 7 days actions and kill signals.

## Expected answer shape

```markdown
**结论**：AAAI 是 P0-now 但不自动适合这三个候选；WSDM/EACL 是真实 August pressure；ICLR/AISTATS/CLeaR 需要保持历史估计/待核验。

| Venue | Status | Abstract | Full | Supp/Code | TZ | Source | Urgency |
|---|---|---:|---:|---:|---|---|---|

**A2 / B1 / B5 routing**：
...

**next 7 days**：
...
```

## Acceptance checks

- A passing answer refuses to turn radar-only or historical dates into official dates.
- A passing answer may use CCFDDL RSS records to assemble the first table quickly, but still labels them `radar_hint` until official evidence is checked.
- A passing answer says what to do, not only what the dates are.
- A passing answer can cite source URLs used for confirmed venues.
- A passing answer stays under a small target set; it does not expand into a full conference catalog.
