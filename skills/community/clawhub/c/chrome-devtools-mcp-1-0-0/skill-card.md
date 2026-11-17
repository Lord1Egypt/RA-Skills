## Description:

Chrome DevTools MCP gives agents control of Chrome or Chromium through Puppeteer and the Chrome DevTools Protocol for browser testing, web automation, performance analysis, UI testing, form filling, and visual regression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to configure and operate a Chrome DevTools MCP server so an agent can navigate pages, interact with UI elements, capture screenshots and snapshots, inspect network and console output, and run performance traces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a mutable external npm package with @latest, so behavior can change without a skill update.

Mitigation: Pin a reviewed chrome-devtools-mcp package version before production use.

Risk: Browser-control access can expose active sessions, page contents, console output, network data, screenshots, and form inputs to an agent.

Mitigation: Use a fresh or isolated Chrome profile and avoid connecting the agent to browser sessions that contain sensitive accounts or data.

Risk: Usage statistics and performance CrUX behavior may disclose telemetry or performance-related data.

Mitigation: Run with --no-usage-statistics and --no-performance-crux when privacy matters.

## Reference(s):

- [Chrome DevTools MCP homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [ClawHub skill page](https://clawhub.ai/sieyer/skills/chrome-devtools-mcp-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/sieyer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands for npx, OpenClaw MCP configuration, setup/status/test script usage, and browser automation workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
