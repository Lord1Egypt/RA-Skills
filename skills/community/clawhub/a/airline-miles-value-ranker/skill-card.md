## Description:

Use when deciding how to spend frequent-flyer miles or credit-card points — comparing redemption options, judging a "deal," choosing between pay-with-miles, booking awards directly, or transferring points to partners — computes cents-per-point for each option with fare-comparison math, checks against 12 known partner sweet spots, prices the cash-fare floor, and issues BURN / HOARD / NEVER verdicts so a 300k-point balance never gets flushed at 0.4¢.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and points holders can compare cash fares, award bookings, and transfer options to estimate redemption value and prioritize frequent-flyer miles or credit-card points. Treat expiry-driven recommendations as decision support, not a substitute for checking current prices and terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expiry-based BURN recommendations can favor an option worse than cashing out or paying cash.

Mitigation: Compare the recommendation with cash-out and cash-purchase alternatives; do not rely on the expiry verdict alone.

Risk: Fare prices, award availability, and reward terms can change, making comparison guidance stale.

Mitigation: Check current fares, award space, fees, and transfer terms before booking or moving points.

Risk: Saved comparison details remain in a local plaintext file until cleared.

Mitigation: Avoid entering sensitive details and clear the saved comparison file when it is no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/airline-miles-value-ranker)
- [Redemption Math](artifact/references/redemption-math.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Text and Markdown comparisons with cents-per-point estimates, ranked options, and BURN / HOARD / NEVER verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on user-provided fare and award details; verify live pricing and reward terms independently.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
