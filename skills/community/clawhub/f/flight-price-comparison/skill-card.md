## Description:

Helps an agent compare flight prices for requested routes and dates across travel platforms and return a concise recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nodermachine](https://clawhub.ai/user/nodermachine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to request one-way or round-trip flight price comparisons, summarize candidate fares, and identify a lowest-price or preferred itinerary. Review the implementation before relying on returned prices because the security evidence describes the release as an unfinished prototype.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store travel-site passwords in TOOLS.md.

Mitigation: Use manual or QR login in a dedicated browser profile, and avoid storing travel-site passwords in shared agent files.

Risk: Security evidence describes the release as an unfinished prototype that overstates implemented flight search and price extraction behavior.

Mitigation: Review and test the implementation before deployment, and treat returned fares as advisory until search, extraction, credential handling, and platform scope are verified.

Risk: Flight prices and booking conditions can change after lookup.

Mitigation: Confirm current price, taxes, fees, availability, and refund or change rules on the travel platform before purchase.

## Reference(s):

- [Account Configuration](references/account-config.md)
- [Flight Price Comparison on ClawHub](https://clawhub.ai/nodermachine/skills/flight-price-comparison)
- [Fliggy](https://www.fliggy.com/)
- [Ctrip](https://www.ctrip.com/)
- [Qunar](https://www.qunar.com/)
- [Umetrip](https://www.umetrip.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route, date, fare, flight, airline, recommendation, and booking-link fields when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
