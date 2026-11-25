## Description:

Provides read-only access to public Douyin video and image search, creator search, post details, comments, and trending data, returning structured JSON for content and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content and marketing teams use this skill to find public Douyin videos and creators, track trends, inspect post details and comments, and identify audience interests for topic planning and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send supplied keywords, links, or video IDs to the Guaikei service; the security review was benign but incomplete.

Mitigation: Review the service's data practices and send only query details you are comfortable sharing; avoid including sensitive or private information.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/dy-engine)
- [Guaikei API and token information](https://www.guaikei.com)
- [Data output contract](references/contract.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise analysis or summaries for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data for search, creator, post, comment, and trend analysis.]

## Skill Version(s):

1.5.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
