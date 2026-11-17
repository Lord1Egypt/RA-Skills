## Description:

Control Chrome browser with AI using MCP protocol. Use when users want to automate browser tasks, take screenshots, fill forms, click elements, navigate pages, search browsing history, manage bookmarks, or perform any browser-based automation. Works with your existing Chrome browser and login sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:


## Use Case:

Developers and other MCP client users use this skill to automate browser navigation, screenshots, form entry, content extraction, history and bookmark operations, and network monitoring in an existing Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can connect an AI client to an existing Chrome profile with active login sessions.

Mitigation: Use a dedicated Chrome profile without unrelated logins, saved passwords, history, or bookmarks.

Risk: Cookie-backed requests, network capture, history searches, bookmark deletion, and actions on logged-in sites can expose or change sensitive data.

Mitigation: Require explicit confirmation before these actions and review the target site, selector, URL, and requested data scope.

Risk: Persistent bridge and extension components are not pinned in the artifact instructions.

Mitigation: Pin and verify the exact bridge and extension versions before installation, and review extension permissions.

## Reference(s):

- [Browser Automation on ClawHub](https://clawhub.ai/femto/skills/browser-automation-2)
- [mcp-chrome GitHub repository](https://github.com/femto/mcp-chrome)
- [mcp-chrome releases](https://github.com/femto/mcp-chrome/releases)
- [mcp-chrome-bridger npm package](https://www.npmjs.com/package/mcp-chrome-bridger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON configuration, and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose browser actions that should be reviewed before execution, especially on logged-in sites.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
