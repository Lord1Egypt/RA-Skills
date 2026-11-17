## Description:

Queries a Bilibili creator's public video portfolio by UID through the RedFox API and returns paginated results sorted by play count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, MCN operations teams, content researchers, and Bilibili viewers use this skill to retrieve public creator video portfolios, browse paginated results, and compare works by play count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a user-provided Bilibili UID and REDFOX_API_KEY to RedFoxHub.

Mitigation: Use it only when you trust RedFoxHub with the API key and lookup request, and keep the key in environment configuration rather than prompts, logs, or output files.

Risk: Generated video links are external links.

Mitigation: Verify result links point to Bilibili before opening them, especially if a response looks unusual.

Risk: Cursor-based pagination can continue a prior lookup context.

Mitigation: Use pagination requests only for the active Bilibili lookup and avoid reusing stale cursor values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bilibili-portfolio-search)
- [Core workflow](artifact/references/core_workflow.md)
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with inline Bilibili links, plus JSON emitted by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; supports UID input and cursor-based pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
