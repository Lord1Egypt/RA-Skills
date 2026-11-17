## Description:

使用混合多智能体架构进行牛津联盟制中文多辩手辩论，支持任何辩题

This skill is ready for commercial/non-commercial use.

## Publisher:

[fitler-lin](https://clawhub.ai/user/fitler-lin)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and debate facilitators use this skill to turn a topic into an Oxford Union-style debate, test argument strength, and produce a balanced debate summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad debate or argument-testing requests may be steered into a multi-round Oxford Union-style debate format.

Mitigation: Confirm the user's desired format before continuing when the request is ambiguous.

Risk: Role-based debate outputs may present persuasive but unverified claims.

Mitigation: Treat generated arguments as debate material and verify factual claims with reliable sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fitler-lin/skills/chinese-moa-debate)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese Markdown debate transcript with a structured JSON-derived summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable debate completeness threshold and maximum round count; final output includes pro, con, rebuttals, attacks, and balance sections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
