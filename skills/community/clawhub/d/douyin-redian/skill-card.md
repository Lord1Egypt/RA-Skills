## Description:

Searches public Douyin videos, creators, comments, and trending topics, returning structured data for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, marketers, and analysts use this skill to find popular videos and creators, inspect public posts and comments, track trends, and support competitor, audience, or content planning analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and noted a possible mismatch with the skill's stated purpose.

Mitigation: Review the package contents and confirm the commands and data handling match the intended use before installation.

Risk: Search terms and content links, along with the API token, are sent to the third-party GuaiKei service.

Mitigation: Use public content only, avoid sensitive terms or identifiers, and keep the API token private.

## Reference(s):

- [Skill usage and command reference](artifact/readme.md)
- [Request and response contract](artifact/references/contract.md)
- [Search options](artifact/references/options.md)
- [Demand analysis guide](artifact/references/demand-mining.md)
- [Public audience acquisition guide](artifact/references/customer-acquisition.md)
- [GuaiKei service](https://www.guaikei.com)
- [ClawHub release](https://clawhub.ai/engheng-art/skills/douyin-redian)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON with concise text summaries or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin data; results may be empty or limited by the service plan.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
