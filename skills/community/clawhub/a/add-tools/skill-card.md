## Description:

Search engine for AI agents to discover free and paid tools, APIs, and MCP servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmmel](https://clawhub.ai/user/simmmel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to discover tools, APIs, and MCP servers for agent workflows, including free and x402-enabled paid endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool-search terms and optional feedback are sent to add.tools over HTTPS and may contain privacy-relevant workflow details.

Mitigation: Do not include secrets, personal data, proprietary prompts, or sensitive workflow details in search queries or feedback payloads.

Risk: Search results may include free and paid third-party tools, APIs, and MCP servers with their own terms, pricing, and reliability profiles.

Mitigation: Review selected tools before use and confirm pricing, permissions, and suitability for the workflow.

## Reference(s):

- [add.tools website](https://add.tools)
- [add-tools GitHub organization](https://github.com/add-tools)
- [ClawHub skill page](https://clawhub.ai/simmmel/skills/add-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to JSON search results from add.tools when used with an Accept header or format parameter.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
