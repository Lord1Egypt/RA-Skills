## Description:

Manage Linear issues, projects, and cycles through Linear's GraphQL API using curl-based commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achilles2200ai-sys](https://clawhub.ai/user/achilles2200ai-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product engineers, and team leads use this skill to query, create, update, comment on, and summarize Linear issues, projects, and cycles from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, comment on, and bulk-change live Linear workspace data.

Mitigation: Require user confirmation before mutations or bulk operations, and preview affected issues before execution.

Risk: The skill requires a Linear API key and may use examples with write-capable access.

Mitigation: Use the least-privilege Linear API key available, store it only in the configured environment, and rotate it if exposed.

Risk: Some GraphQL examples interpolate user-provided values into shell strings.

Mitigation: Prefer GraphQL variables or carefully escaped JSON payload construction for user-controlled titles, comments, search terms, and IDs.

Risk: Security evidence says permission metadata understates subprocess use.

Mitigation: Review requested execution permissions before installation and account for curl and jq subprocess behavior in deployment policy.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/achilles2200ai-sys/skills/clawbounty-2-linear)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON responses when the generated curl examples are executed against Linear.]

## Skill Version(s):

1.0.0 (source: server release metadata and effector.toml; changelog top entry also reports 1.0.0 released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
