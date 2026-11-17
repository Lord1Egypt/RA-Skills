## Description:

Universal AI resource registry - search and invoke agents, MCP servers, and APIs through a single MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agent3-666](https://clawhub.ai/user/agent3-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can connect an MCP client to Agent3 Hub to search, resolve, and invoke registered AI agents, MCP servers, APIs, and content-search resources through one endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned downloaded package through npx.

Mitigation: Prefer a pinned or locally reviewed mcp-remote installation before connecting production clients.

Risk: API-keyed requests are sent to a broad third-party resource registry and downstream tools.

Mitigation: Avoid sending secrets, regulated data, or sensitive queries through the hub, and store AGENT3_API_KEY carefully.

Risk: Invoked resources may be operated by third parties beyond the skill publisher.

Mitigation: Review and trust each downstream resource before invoking it, especially for actions outside search or read-only workflows.

## Reference(s):

- [Agent3 Hub ClawHub listing](https://clawhub.ai/agent3-666/skills/agent3-hub)
- [Agent3 Hub registry](https://hub.agent3.me)
- [Agent3 Hub documentation](https://hub.agent3.me/docs)
- [Agent3 Hub MCP endpoint](https://hub.agent3.me/api/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENT3_API_KEY for authenticated tool calls; public listing and initialization endpoints are also described.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
