## Description:

Searches public Douyin videos, creator posts, comments, and trending lists, returning structured data for content research and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, and analysts use this skill to research public Douyin videos, creator accounts, comments, and trends for topic planning, competitor monitoring, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Douyin links are sent to the third-party Guaikei API.

Mitigation: Avoid including sensitive information in search terms or links, and review the provider's data handling before use.

Risk: The skill includes account search in addition to its headline flow-monitoring use.

Mitigation: Use account search only when it matches the user's request, and review the returned public account data.

Risk: The security review was partial, with 22 of 53 components only partly analyzed.

Mitigation: Review the partly analyzed components before deploying the skill broadly.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-traffics-monitor)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [Guaikei service and token support](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Query options](references/options.md)
- [Error handling](references/errors.md)
- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands, Analysis guidance]

**Output Format:** [Structured JSON envelope with CLI examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video, creator, comment, and trending data; most query results are saved as JSON files.]

## Skill Version(s):

1.5.0 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
