## Description:

Analyze creator revenue streams (Stripe, PayPal, affiliate, sponsorships) to calculate true profitability per content piece, identify unprofitable segments, forecast cash flow gaps, and recommend high-margin content verticals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, solopreneurs, and digital agencies use this skill to analyze revenue, costs, content ROI, audience segment profitability, and cash runway across connected financial and reporting platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for access to financial and reporting services such as Stripe, PayPal, Slack, and Airtable.

Mitigation: Use test or read-only credentials where possible and scope each API key to the minimum permissions required.

Risk: Financial reports and automated Slack alerts may expose sensitive revenue, runway, or dispute information.

Mitigation: Confirm Slack and Airtable destinations before enabling recurring reports and restrict reports to appropriate recipients.

Risk: Profitability forecasts and content recommendations can be misleading if source data, attribution, or cost assumptions are incomplete.

Mitigation: Review assumptions, fee rates, time-cost estimates, and forecast outputs before making financial or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/creator-financial-health-auditor)
- [Project homepage](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with financial tables, forecasts, alerts, recommendations, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include revenue breakdowns, cash-flow forecasts, content ROI rankings, Slack report drafts, and credential setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
