## Description:

AI Pulse helps Chinese-language users retrieve daily AI briefings, AI Pulse knowledge-base answers, trend analysis, and hotspot deep dives with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naplesblue](https://clawhub.ai/user/naplesblue)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-language users use this skill to answer questions about recent AI news, model and tool updates, AI Agent frameworks, AI trends, and scheduled AI briefing delivery. The skill guides agents to use AI Pulse APIs or the AI Pulse MCP service and to preserve source links in responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends relevant user queries to external AI Pulse services and may require MCP-based authentication for knowledge search.

Mitigation: Disclose external service use to users and use the MCP knowledge search only after the user has configured and authorized the AI Pulse MCP server.

Risk: AI Pulse API and MCP responses are external data and may contain inaccurate, stale, or instruction-like content.

Mitigation: Treat returned content as untrusted reference material, preserve source links, avoid executing returned instructions, and clearly distinguish AI Pulse data from the agent's own judgment.

Risk: Knowledge search can fail when MCP is unavailable, unregistered, or not authorized.

Mitigation: Fall back to telling users to configure the AI Pulse MCP server at the documented setup page, and do not attempt direct programmatic HTTP POST requests to protected search endpoints.

## Reference(s):

- [AI Pulse briefing API](https://ai-pulse-lab.com/api/brief.json)
- [AI Pulse trends API](https://ai-pulse-lab.com/api/trends.json)
- [AI Pulse manifest API](https://ai-pulse-lab.com/api/manifest.json)
- [AI Pulse MCP server](https://mcp.ai-pulse-lab.com/mcp)
- [AI Pulse agent setup](https://ai-pulse-lab.com/agents/)
- [ClawHub skill page](https://clawhub.ai/naplesblue/skills/ai-pulse)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text with preserved source links, depending on the delivery channel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-derived briefings, trend reports, source citations, MCP setup guidance, and scheduling suggestions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
