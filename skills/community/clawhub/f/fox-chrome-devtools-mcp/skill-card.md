## Description:

Chrome DevTools MCP lets agents control Chrome through the MCP protocol for browser testing, web automation, performance analysis, network inspection, console debugging, form filling, and visual regression workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinthqod](https://clawhub.ai/user/qinthqod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to configure and operate a Chrome DevTools MCP server for browser automation, UI testing, debugging, network inspection, and performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup and launch paths use chrome-devtools-mcp@latest, so the external package can change between runs.

Mitigation: Pin or preinstall a reviewed chrome-devtools-mcp version before using the skill in controlled environments.

Risk: The MCP server gives an agent broad authority to control a live Chrome browser.

Mitigation: Run it only for explicitly authorized browser automation tasks and review actions before using it on production, admin, financial, or sensitive workflows.

Risk: Browser page content, session state, screenshots, network details, and performance data may be exposed through the agent/server workflow.

Mitigation: Avoid sensitive logged-in sessions and disable usage statistics and CrUX reporting when privacy requirements call for it.

## Reference(s):

- [Chrome DevTools MCP homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [ClawHub skill page](https://clawhub.ai/qinthqod/skills/fox-chrome-devtools-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/qinthqod)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The configured MCP server can return browser screenshots, DOM snapshots, console output, network request details, and performance trace analysis.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
