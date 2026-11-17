## Description:

Queries logistics index data for carriers by statistical date, metric, and region.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-vb](https://clawhub.ai/user/a-vb)

### License/Terms of Use:

MIT-0

## Use Case:

Operations analysts and logistics teams use this skill to query carrier logistics index values, industry averages, carrier rankings, and seven-day trend information for selected dates, metrics, and regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries a referenced logistics index system that may require authorization.

Mitigation: Install and use it only where access to that system and the requested logistics data is authorized.

Risk: Omitted filters can broaden the query to all carriers, national scope, previous-day data, or all logistics metrics.

Mitigation: Provide explicit carrier, date, metric, and region filters when narrower results are required.

## Reference(s):

- [Jingwe Logistics Index Overview](http://jingwe.jdl.com/#/indexCenter/indexOverview)
- [Jingwe Shipper Overview](http://jingwe.jdl.com/#/indexCenter/shipperOverview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown with logistics index values, rankings, comparisons, and trend summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a seven-day trend chart or chart description when supported by the agent interface.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
