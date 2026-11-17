## Description:

Converts natural-language questions into SQL queries and executes them, with support for multi-turn conversation, intent recognition, SQL auditing, and visualization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovenervermore](https://clawhub.ai/user/lovenervermore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to answer natural-language business questions by generating SQL, executing database queries, and returning concise summaries and suggested visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on unreviewed local project code from a hard-coded Winner-Ai path before executing database-query logic.

Mitigation: Package or verify the referenced project code before installation, and deploy only in a controlled environment.

Risk: Generated SQL may query or modify data beyond the user's intent if database permissions are too broad.

Mitigation: Use read-only or tightly scoped database credentials, require user approval for sensitive queries, and enforce database-level permissions.

Risk: Unpinned or broad dependencies can change behavior across installations.

Mitigation: Pin dependencies to reviewed versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovenervermore/skills/chat-ai)
- [Publisher profile](https://clawhub.ai/user/lovenervermore)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [JSON object containing status, SQL, result rows, summary, processing regions, and optional error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw message data from the underlying orchestration flow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
