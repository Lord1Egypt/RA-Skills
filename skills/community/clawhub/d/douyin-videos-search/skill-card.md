## Description:

Searches public Douyin videos, users, creator posts, comments, individual post details, and trending topics, returning structured data for content and audience research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use the skill to find public Douyin content, research creators and trends, and review post engagement or comments. It supports topic research, competitor monitoring, and public audience insight using returned structured data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence and partial analysis, and flags account search as broader than the declared capabilities.

Mitigation: Use account search for creator or account discovery when relevant to the request, and review its returned scope before summarizing results.

Risk: The service receives submitted search terms and supplied Douyin links or IDs.

Mitigation: Use public Douyin content and non-sensitive search terms; do not submit private or sensitive material.

## Reference(s):

- [Service and token setup](https://www.guaikei.com)
- [Usage guide and command reference](readme.md)
- [Output contract](references/contract.md)
- [Error handling guidance](references/errors.md)
- [Comment demand analysis guidance](references/demand-mining.md)
- [Public audience research guidance](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise analytical summaries or tables when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Douyin data; requires Node.js 16.14+ and GUAIKEI_API_TOKEN. Search terms and supplied Douyin links or IDs are sent to guaikei.com.]

## Skill Version(s):

1.5.0 (source: release evidence, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
