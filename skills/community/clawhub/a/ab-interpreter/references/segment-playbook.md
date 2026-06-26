# Segment Playbook

A topline win that contradicts within a segment is not a clean win. Always cut the following segments and interpret the contradictions.

## Standard cuts to run on every ecommerce test

1. **New vs. returning visitors.** Returning visitors have stronger priors about your brand and respond differently to copy changes. A lift concentrated in new visitors often decays as the audience mix stabilizes.
2. **Device class.** Mobile, tablet, desktop behave differently. A mobile-first test must not regress desktop AOV, and vice versa.
3. **Traffic source.** Paid search, paid social, organic, email, and direct each carry different intent. A lift that only appears in paid social may be a paid-media artifact.
4. **Geography.** Country and — for large enough samples — major metro area. International traffic can have different price sensitivity and payment-method familiarity.
5. **Logged-in vs. guest checkout.** Logged-in users have stored payment methods and prior purchase history.
6. **New product vs. established SKU.** A copy change on a brand-new product may lift for different reasons than on a catalog staple.

## What each contradiction signals

- **Lift in new, flat in returning.** Change is attractive to unfamiliar visitors but neutral to people who already know your brand. Consider rolling out only to new traffic.
- **Lift in mobile, regression on desktop.** Usually a visual or layout issue. Check that your variant renders correctly at every breakpoint.
- **Lift in one traffic source only.** Your test may be picking up a shift in attribution or a difference in landing pages. Rerun with a consistent referrer.
- **Lift in one geography only.** Check currency display, payment methods, and shipping copy. A lift from fixing a localization bug does not generalize.
- **Lift in guests, flat for logged-in.** The change probably reduced friction on a path that logged-in users already skipped. Worth shipping but do not expect equal impact across the base.

## Segment significance thresholds

A segment cut multiplies the number of comparisons. A "regression" in a small segment may just be noise. Apply a Bonferroni correction across your segment tests: divide your alpha (0.05) by the number of segments. Or treat segment cuts as directional guidance rather than hypothesis tests — they should raise flags but not overturn a clean topline call on their own.

## Reporting segments

Present segment results as a small table with observed lift, sample size per arm, and CI. Highlight any segment where the lift direction contradicts the aggregate. Never hide a contradicting segment to make the story cleaner.

## When to stop cutting

If you cut more than six segments you will start finding spurious contradictions. Pre-commit to which segments matter and stop there. Additional cuts can be explored as hypothesis generators for follow-up tests, not as gates on the current ship decision.
