# Quality Checklist

Pre-delivery validation checklist for Conversion Rate Doctor outputs. Complete all applicable items before finalizing a diagnosis. Mark each item as Pass, Fail, or N/A.

---

## Data Completeness (8 items)

- [ ] Traffic volume confirmed and exceeds 1,000 sessions per analyzed funnel stage
- [ ] Device split (mobile vs. desktop) documented and used in analysis
- [ ] Data time period specified with start and end dates
- [ ] Comparison period identified (historical baseline or benchmark)
- [ ] Traffic source mix noted and considered in interpretation
- [ ] Average order value documented
- [ ] Any data gaps or missing funnel stages explicitly flagged
- [ ] External factors (seasonality, promotions, market events) noted if present during the data period

## Funnel Coverage (6 items)

- [ ] All funnel stages from landing through order confirmation mapped (Mode A) or target stage clearly scoped (Mode B)
- [ ] Transition rates calculated between every adjacent stage
- [ ] Absolute visitor drop-off calculated at each stage, not just percentages
- [ ] Both mobile and desktop funnels analyzed separately where data permits
- [ ] Drop-off stages ranked by absolute visitor loss, not just percentage
- [ ] Healthy stages acknowledged, not just underperforming ones

## Benchmark Accuracy (6 items)

- [ ] Category-specific benchmarks used (not generic ecommerce averages)
- [ ] Benchmarks presented as ranges, not point estimates
- [ ] Device-specific benchmarks applied (mobile compared to mobile, desktop to desktop)
- [ ] Seasonal adjustment applied if data period falls during a peak or trough
- [ ] Benchmark source context noted (benchmarks are directional, not absolute)
- [ ] Status labels (Healthy / Warning / Critical) applied using standard deviation thresholds

## Fix Quality (8 items)

- [ ] Every fix is specific and actionable (a designer or developer could implement without further clarification)
- [ ] Every fix includes expected impact as a range, not a point estimate
- [ ] Every fix includes implementation effort rating (Low / Medium / High)
- [ ] Fixes are prioritized by the standard formula: (Traffic x Expected Lift x AOV) / Effort Score
- [ ] Quick wins (high impact, low effort) are clearly identified and sequenced first
- [ ] Each fix includes a measurement plan with metric, expected lift, and recommended test duration
- [ ] No more than 5 fixes recommended for simultaneous implementation (testability preserved)
- [ ] Fixes grouped into a phased implementation roadmap

## Evidence Integrity (7 items)

- [ ] Every finding labeled with evidence tier: T1 (A/B test), T2 (analytics correlation), or T3 (heuristic)
- [ ] T3 (heuristic) findings clearly framed as hypotheses requiring validation, not confirmed diagnoses
- [ ] No causal claims made from correlational data without appropriate qualification
- [ ] Sample size adequacy addressed for any statistical claims
- [ ] Confounding factors acknowledged (traffic mix shifts, pricing changes, competitive dynamics)
- [ ] Distinction maintained between UX-caused conversion issues and non-UX causes (pricing, product-market fit, traffic quality)
- [ ] A/B test recommendations included for T2 and T3 findings to validate hypotheses

## Psychology Mapping (5 items)

- [ ] Every finding mapped to at least one named psychology principle from the reference guide
- [ ] The mechanism is explained for each mapping (how the principle applies to this specific issue, not just naming it)
- [ ] Psychology principles cited accurately (definitions match the reference)
- [ ] No principle applied where it does not genuinely fit (avoid forced mappings)
- [ ] Fix patterns align with the prescribed remedies for the cited principles

## Output Standards (7 items)

- [ ] Executive summary present and limited to 3-5 sentences covering rate, bottleneck, opportunity, and first action
- [ ] Current metrics snapshot table complete with all stages, rates, benchmarks, and status labels
- [ ] Findings numbered sequentially and following the standard detail format
- [ ] Prioritized fix list table complete with rank, description, revenue impact, and effort
- [ ] Implementation roadmap organized into phased timeline
- [ ] Output follows the appropriate template (Mode A or Mode B) from `references/output-template.md`
- [ ] Language is clear, professional, and free of jargon that the target audience would not understand

## Safety and Honesty (5 items)

- [ ] No guaranteed outcomes stated — all impact estimates presented as ranges with appropriate uncertainty language
- [ ] Limitations of the analysis explicitly acknowledged (data gaps, evidence tier constraints, scope boundaries)
- [ ] No fabricated or assumed data — missing information flagged rather than invented
- [ ] Recommendations stay within scope (no medical, legal, or financial advice beyond conversion optimization)
- [ ] Competitive analysis based only on publicly observable information; no proprietary data assumptions made
