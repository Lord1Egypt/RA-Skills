## Description:

Search engine for AI agents to discover free and paid tools, APIs, and MCP servers

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmmel](https://clawhub.ai/user/simmmel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to find tools, APIs, and MCP servers that match an agent's task, including free and x402-enabled paid endpoints. Agents can query add.tools for ranked tool results and optionally submit feedback about selected tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries sent to add.tools may disclose task intent or sensitive tool-selection context.

Mitigation: Do not include confidential prompts, customer data, secrets, or proprietary details in search queries.

Risk: Feedback submission is optional data sharing with an external service.

Mitigation: Submit feedback only when sharing the query, chosen tool, and success outcome is acceptable.

## Reference(s):

- [add.tools website](https://add.tools)
- [add.tools GitHub organization](https://github.com/add-tools)
- [ClawHub skill page](https://clawhub.ai/simmmel/skills/addtools)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example curl commands for JSON search requests and optional feedback submission.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
