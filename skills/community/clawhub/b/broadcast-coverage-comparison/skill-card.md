## Description:

Compare indexed television coverage across stations and shows with Crawlora GDELT TV search, charts, timelines, and discovery, keeping match channels, station windows, processing lag, and metric denominators distinct.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and researchers use this skill to compare indexed television coverage across stations and shows, with source-linked examples and clearly labeled coverage gaps and metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and the Crawlora API key are sent to Crawlora; sensitive topics or exposed credentials may create privacy or security concerns.

Mitigation: Keep the API key out of logs and avoid submitting sensitive or confidential topics unless intended.

Risk: Processing delays, incomplete station windows, and differing metric denominators can make comparisons misleading.

Mitigation: Use bounded, equivalent queries; label gaps and lag; retain sources and compare only metrics with compatible units.

## Reference(s):

- [Broadcast coverage comparison endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/broadcast-coverage-comparison)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown brief with query ledger, comparison tables, timelines, and source-linked examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates match channels, units and denominators, processing lag, and coverage gaps.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
