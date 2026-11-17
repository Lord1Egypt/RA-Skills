## Description:

Control browser automation agents via the Bits MCP server for web scraping, form filling, data extraction, and browser-based automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbiethompson18](https://clawhub.ai/user/robbiethompson18)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to connect an agent to the Bits MCP server for browser navigation, data extraction, form filling, authenticated flows, multi-window control, and structured JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm MCP server.

Mitigation: Pin `usebits-mcp` to a reviewed version before installation and review updates before changing the pinned version.

Risk: Browser automation may use stored credentials or authentication flows.

Mitigation: Use a dedicated, revocable Bits API key, avoid high-privilege accounts, and restrict local MCP configuration file permissions.

Risk: Automated browsing can expose secrets, regulated data, or sensitive business data to Bits, the target site, or the executed package.

Mitigation: Do not submit sensitive data unless the Bits service, target site, and npm package version have been reviewed and trusted for that use.

## Reference(s):

- [Bits web app](https://app.usebits.com)
- [Bits API OpenAPI specification](https://api.usebits.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/robbiethompson18/skills/bits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration snippets, TypeScript examples, and structured JSON results from browser automation tasks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Bits API key and execution of the usebits-mcp npm package through an MCP client.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
