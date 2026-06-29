## Description: <br>
Searches Etix events, venues, and performers and retrieves event or venue details through the etix-mcp MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to find Etix events, venues, performers, and showtimes, then retrieve structured event or venue details through an MCP-enabled agent. It is useful when the user has etix-mcp installed, the fetchproxy extension active, and an open etix.com browser tab. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external etix-mcp npm package and fetchproxy extension. <br>
Mitigation: Install only after reviewing and trusting those dependencies, and keep the browser extension and MCP package scoped to explicit Etix lookup workflows. <br>
Risk: Requests are made through the user's active Etix browser tab, including that browser session, cookies, and TLS context. <br>
Mitigation: Use a dedicated Etix tab/session where practical, approve pairing deliberately, and close or disconnect the bridge when Etix lookups are complete. <br>
Risk: Etix does not publish a public consumer API, so website endpoints or pages may change without notice. <br>
Mitigation: Use the documented health check when results fail and verify important event, venue, pricing, or availability details directly on Etix before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chrischall/etix-mcp) <br>
- [etix-mcp npm package](https://www.npmjs.com/package/etix-mcp) <br>
- [fetchproxy extension](https://github.com/chrischall/fetchproxy) <br>
- [Etix ticket site](https://www.etix.com/ticket/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with MCP tool names, JSON configuration examples, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on an external MCP package, the fetchproxy browser extension, and the user's active Etix browser session.] <br>

## Skill Version(s): <br>
0.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
