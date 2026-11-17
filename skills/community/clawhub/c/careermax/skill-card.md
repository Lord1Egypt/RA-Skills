## Description:

Use CareerMax when the user wants to review their career context, manage their job pipeline, improve career materials, prepare for interviews, find referrals, or build skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulphenomenon](https://clawhub.ai/user/rahulphenomenon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use CareerMax to review career context, manage a job pipeline, improve career materials, prepare for interviews, find referrals, and build skills through a connected CareerMax account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm MCP toolkit that can change after review.

Mitigation: Use a pinned and reviewed @careermax/agent-toolkit version and run it in a constrained environment.

Risk: The MCP process uses a CareerMax API key that can access the user's CareerMax account.

Mitigation: Use a dedicated least-privileged CareerMax agent key, keep it in secure environment configuration, and rotate it if compromise is suspected.

Risk: Some CareerMax tools create or change durable account records.

Mitigation: Require explicit user confirmation before creating or changing lasting CareerMax records, using the confirmation-token flow described by the artifact.

## Reference(s):

- [CareerMax AI Agent](https://careermax.ai/ai-agent)
- [ClawHub CareerMax Skill](https://clawhub.ai/rahulphenomenon/skills/careermax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with CareerMax MCP tool calls and setup commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAREERMAX_API_KEY and npx; durable CareerMax record changes require explicit user confirmation.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
