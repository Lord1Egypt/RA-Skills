## Description:

Automate browser tasks with the BrowserMCP MCP server and Chrome extension, including navigation, form interaction, screenshots, and console-log retrieval in a user's connected Chrome tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankausberlin](https://clawhub.ai/user/frankausberlin)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to set up BrowserMCP and guide browser automation in a connected Chrome tab. Typical workflows include authenticated navigation, form completion, testing, debugging, information gathering, and screenshot-based verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls connected tabs in a real browser profile and may interact with authenticated sessions.

Mitigation: Use a dedicated Chrome profile where practical and require explicit user confirmation before logins, two-factor authentication, purchases, posts, account changes, or other sensitive actions.

Risk: Screenshots and console-log collection can expose sensitive page content or account data.

Mitigation: Avoid collecting screenshots or console logs on sensitive sites unless the user has explicitly approved the action and understands what may be captured.

Risk: The setup evidence installs the MCP server with an unpinned npm package version.

Mitigation: Pin the npm package to a reviewed exact version and avoid global installation unless the deployment owner has approved it.

Risk: The skill promotes real-browser automation that may avoid basic bot detection.

Mitigation: Respect site terms, rate limits, and security challenges; pause for user review before actions that could bypass normal account or platform safeguards.

## Reference(s):

- [BrowserMCP Setup Guide](references/setup.md)
- [BrowserMCP Tools Reference](references/tools.md)
- [BrowserMCP Common Workflows](references/workflows.md)
- [BrowserMCP Best Practices](references/best-practices.md)
- [BrowserMCP Website](https://browsermcp.io)
- [BrowserMCP Documentation](https://docs.browsermcp.io)
- [BrowserMCP GitHub Repository](https://github.com/browsermcp/mcp)
- [Playwright MCP GitHub Repository](https://github.com/microsoft/playwright-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON configuration and JavaScript-style BrowserMCP tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes BrowserMCP tool names, element-reference workflows, setup configuration, troubleshooting steps, and safety cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
