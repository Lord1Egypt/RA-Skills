## Description:

Look up real-estate listings, property details, photos, price history, and resolve addresses on Compass via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and real-estate researchers use this skill to ask an agent for Compass listing searches, property details, photos, price history, address resolution, comparisons, and local mortgage or affordability calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses unpinned third-party package and repository install commands.

Mitigation: Pin compass-mcp package versions and fetchproxy repository commits, then review the exact package, repository, and extension permissions before installation.

Risk: Network-backed tools route requests through a signed-in Compass browser session.

Mitigation: Use a dedicated browser profile or low-privilege environment for Compass access and avoid sharing unrelated sensitive browser sessions with the bridge.

Risk: Compass data extraction depends on rendered page state, authentication, and WAF/session behavior rather than a public API.

Mitigation: Treat returned listing details as best-effort and verify important property, price, and availability information against Compass or other primary sources before decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/compass-mcp)
- [compass-mcp npm package](https://www.npmjs.com/package/compass-mcp)
- [compass-mcp linked repository](https://github.com/chrischall/compass-mcp)
- [fetchproxy linked repository](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with tool results, JSON snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed tools require compass-mcp, the fetchproxy extension, and an active signed-in Compass browser session; local mortgage and affordability calculations can run without the session.]

## Skill Version(s):

0.11.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
