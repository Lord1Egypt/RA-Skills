## Description:

Summarizes public Douyin comments and related content into user questions, purchase concerns, usage feedback, demand themes, and sentiment evidence for product improvement and customer support preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers can search public Douyin videos, profiles, trends, and comments, then summarize feedback and demand themes for content planning, product decisions, and customer support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account discovery and identifiable lead-generation capabilities, with partial scan coverage.

Mitigation: Review the package and confirm those capabilities fit the intended use before deployment; limit collection and retention to what the task needs.

Risk: Supplied links or identifiers are sent to the Guaikei third-party service, and collected comments or profile data may be identifying.

Mitigation: Review the service's data handling before submitting identifiers, and follow applicable privacy rules when storing or sharing results.

## Reference(s):

- [Comment demand analysis guide](artifact/references/demand-mining.md)
- [Public comment research guide](artifact/references/customer-acquisition.md)
- [Output contract](artifact/references/contract.md)
- [Release page](https://clawhub.ai/why20261/skills/douyin-comment-consumer-insights)
- [Guaikei API service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise natural-language analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin data only; query results may be saved as local JSON logs.]

## Skill Version(s):

1.5.0 (source: server-resolved release, artifact/SKILL.md, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
