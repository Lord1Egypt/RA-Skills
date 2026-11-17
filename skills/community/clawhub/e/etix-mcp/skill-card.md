## Description:

Search Etix events, venues, and performers and pull event and venue details through an MCP server that requires etix-mcp, the fetchproxy extension, and an open etix.com browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent search Etix events, venues, and performers, retrieve event or venue details, resolve locations, and check the browser-extension bridge health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned external code for the MCP package and browser extension.

Mitigation: Pin exact package and repository versions, review the code before installation, and build in a disposable environment.

Risk: Requests are routed through a browser extension using the user's Etix browser session.

Mitigation: Use a dedicated browser profile with no unrelated signed-in accounts and approve the bridge only when needed.

Risk: The MCP is unofficial and uses Etix website endpoints and pages rather than a public consumer API.

Mitigation: Confirm use is consistent with Etix terms, limit use to appropriate public event-discovery data, and expect site changes to break behavior.

## Reference(s):

- [etix-mcp npm package](https://www.npmjs.com/package/etix-mcp)
- [fetchproxy extension repository](https://github.com/chrischall/fetchproxy)
- [Etix ticket site](https://www.etix.com/ticket/)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/etix-mcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [MCP tool results with Markdown setup guidance, JSON configuration snippets, and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local MCP server, the fetchproxy browser extension, and an active etix.com browser tab.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
