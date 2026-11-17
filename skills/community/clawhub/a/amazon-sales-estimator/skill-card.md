## Description:

Amazon Sales Estimator helps sellers and product researchers estimate monthly units, revenue, and market size from BSR, ASINs, product URLs, or keywords across 12 Amazon marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, product researchers, and e-commerce operators use this skill to estimate Amazon product sales, revenue, competitor performance, and niche market size from public BSR, ASIN, URL, or keyword inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global installation examples can make the skill available across sessions when that scope is not intended.

Mitigation: Verify the publisher and source before installing, and avoid global installation unless broad availability is desired.

Risk: ASINs, Amazon URLs, and keywords used in lookup modes may be sent to external web services.

Mitigation: Avoid entering sensitive product research terms or URLs unless external lookup is acceptable for the use case.

Risk: Sales estimates may be incomplete because the skill cannot access historical BSR data, actual seller sales figures, or PPC conversion metrics.

Mitigation: Treat estimates as directional and validate important business decisions with authoritative marketplace, seller, or analytics data.

## Reference(s):

- [Amazon Sales Estimator ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-sales-estimator)
- [Publisher profile](https://clawhub.ai/user/phheng)
- [Nexscope](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with tables, estimates, and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are directional estimates based on public Amazon page data, BSR tables, category multipliers, and user-provided product or keyword inputs.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
