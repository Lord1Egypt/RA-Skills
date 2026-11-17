## Description:

Checks airline baggage compliance, carry-on versus checked rules, excess baggage, and the cheapest compliant packing plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinayunyunyun](https://clawhub.ai/user/tinayunyunyun)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel support agents use this skill to decide whether baggage and special items can fly, how to pack them, and which compliant option has the lowest verified cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel rules and baggage prices can be wrong or outdated when official airline or authority sources are unavailable or require login.

Mitigation: Use official screenshots or precise official links for each report, and mark unresolved prices or rules as needing official confirmation.

Risk: Travel-data lookups may require sensitive booking details if a price is only visible after login.

Mitigation: Avoid sharing booking credentials; if confirmation requires login, record that the price or rule needs official confirmation instead of estimating.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tinayunyunyun/skills/flight-baggage-check)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Simplified Chinese Markdown report with three required sections and evidence screenshots or official links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires official baggage and dangerous-goods source checks; prices that cannot be verified are marked as pending official confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
