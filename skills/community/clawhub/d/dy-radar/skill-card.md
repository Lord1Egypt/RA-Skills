## Description:

A read-only Douyin data skill that returns structured results from keyword and user searches, creator posts, post details, comments, and hot lists for content opportunity analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and analysts use this skill to inspect public Douyin posts, creators, comments, and trends, then identify topic ideas, audience needs, and account benchmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may transfer supplied links or identifiers to a third-party service.

Mitigation: Review the data transfer before use and submit only public information or inputs approved for that service.

Risk: The security scan reports a benign result with medium confidence, but only 59.3% of components were fully inspected.

Mitigation: Review the bundled code and security findings before installation or use.

Risk: Timestamps use Beijing time and can be misread in time-sensitive analysis.

Mitigation: Confirm the timezone or convert timestamps before comparing events across regions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/dy-radar)
- [Guaikei API and support](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis guidance]

**Output Format:** [Structured JSON results and concise analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN. Query links or identifiers are sent to the third-party API; results can optionally be saved locally.]

## Skill Version(s):

1.5.1 (source: SKILL.md frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
