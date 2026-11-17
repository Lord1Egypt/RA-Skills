## Description:

Find eSIM plans for travel by searching plans by country, filtering by data and duration, ranking by value, checking device compatibility, and surfacing deals through a remote HTTP MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladkomudrich](https://clawhub.ai/user/vladkomudrich)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use this skill to compare travel eSIM plans, identify suitable data and duration options, check device compatibility, and find current provider deals. Developers can also use it to configure the remote HTTP MCP endpoint for supported clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local stdio setup runs an unpinned npm package automatically.

Mitigation: Prefer the remote HTTP MCP endpoint. If local stdio is required, verify the npm package publisher and version first and use a pinned package version.

Risk: Default buy links use disclosed affiliate tracking and short redirects.

Mitigation: Tell users when buy links are tracked and provide the raw partner affiliate URL when they ask for a direct link.

Risk: Plan results can be misleading if user intent is translated into overly broad or incorrect filters.

Mitigation: Use the documented country, duration, and data filters; rely on the API ranking fields; and avoid labeling loose ranges as exact matches.

## Reference(s):

- [ClawHub eSIM Agent listing](https://clawhub.ai/vladkomudrich/skills/esimagent)
- [eSIM Agent homepage](https://esimagent.vdigital.app/mcp)
- [Remote HTTP MCP endpoint](https://esimagent.vdigital.app/api/mcp/mcp)
- [MCP auto-discovery endpoint](https://esimagent.vdigital.app/.well-known/mcp.json)
- [Device compatibility checker](https://esimagent.vdigital.app/checker)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with plan summaries, URLs, and JSON MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current eSIM Agent API results when tools or direct HTTP access are available; buy links may include disclosed affiliate tracking.]

## Skill Version(s):

1.8.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
