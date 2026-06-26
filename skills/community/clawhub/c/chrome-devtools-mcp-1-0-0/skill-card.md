## Description: <br>
Chrome DevTools MCP lets agents control Chrome through Puppeteer and the Chrome DevTools Protocol for browser testing, web automation, performance analysis, UI testing, form filling, screenshots, network inspection, console debugging, and visual regression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and testing teams use this skill to connect an agent to Chrome or Chromium for browser automation, UI testing, debugging, screenshots, network inspection, and performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over a live Chrome browser, including navigation, form input, uploads, page-script execution, screenshots, network inspection, and performance tracing. <br>
Mitigation: Use a separate or isolated browser profile, avoid sensitive accounts unless necessary, and confirm form submissions, uploads, or script execution before relying on the agent. <br>
Risk: The setup examples run chrome-devtools-mcp with @latest, so the external MCP package can change after publication. <br>
Mitigation: Prefer a pinned and vetted chrome-devtools-mcp package version for controlled environments. <br>
Risk: Usage statistics and performance CrUX data collection may be enabled unless disabled. <br>
Mitigation: Disable telemetry and CrUX collection where appropriate with --no-usage-statistics and --no-performance-crux. <br>


## Reference(s): <br>
- [Chrome DevTools MCP project](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP server setup commands, OpenClaw configuration, browser automation workflows, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
