# A/B Readout Quality Checklist

Run this before you deliver any readout. If you cannot check a box, either fix the gap or name it explicitly in the Risk block.

## Setup completeness

- [ ] Hypothesis was written before the test launched
- [ ] Primary metric was named before launch
- [ ] Minimum detectable effect was set before launch
- [ ] Guardrail metrics were listed before launch
- [ ] Sample size target was computed from MDE and power
- [ ] Test duration covers at least two full weekly cycles

## Data hygiene

- [ ] Observed traffic split within 1% of planned (SRM check)
- [ ] No tracking outages during the window
- [ ] Bot traffic filtered
- [ ] Deduplicated across visits (one assignment per visitor)
- [ ] No external promo or press spike overlapped the test
- [ ] Sample size achieved the pre-committed target

## Statistical rigor

- [ ] Correct test type chosen for the metric shape
- [ ] p-value reported with the test name
- [ ] 95% CI on the lift is provided (not just the point estimate)
- [ ] Achieved power at the observed lift is at least 80%
- [ ] Absolute and relative lift both reported, not conflated
- [ ] Multiple-metric correction applied if relevant

## Practical significance

- [ ] Observed lift compared against pre-committed MDE
- [ ] Lower bound of the CI assessed, not just the midpoint
- [ ] Revenue impact estimated under current traffic volume
- [ ] Cost of rollout (engineering, merch) noted if non-trivial

## Segments and guardrails

- [ ] New vs. returning cut
- [ ] Device class cut
- [ ] Traffic source cut
- [ ] Geography cut where sample allows
- [ ] Every guardrail checked and reported
- [ ] Any contradicting segment called out explicitly

## Novelty and durability

- [ ] Week-one vs. week-two lift compared
- [ ] Front-loaded decay flagged if present
- [ ] Seasonality or promo overlap noted
- [ ] Post-ship monitoring window and metric prescribed

## Delivery

- [ ] Verdict is one line: Ship, Kill, Extend, or Redesign
- [ ] Reasoning a skeptic would demand is written out
- [ ] Next step is concrete and owner-assigned
- [ ] Readout is scannable in under two minutes
- [ ] Source data or dashboard link attached for reproducibility
