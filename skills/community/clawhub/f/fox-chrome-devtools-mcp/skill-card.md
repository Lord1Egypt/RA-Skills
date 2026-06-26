## Description: <br>
Chrome DevTools MCP lets agents control Chrome through Puppeteer for browser testing, web automation, debugging, screenshots, performance tracing, and network inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinthqod](https://clawhub.ai/user/qinthqod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to connect an agent to Chrome for browser testing, web automation, UI verification, form workflows, performance analysis, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-controlled Chrome sessions can navigate, click, submit forms, inspect pages, and interact with accounts available in the browser. <br>
Mitigation: Use a dedicated test browser profile or headless session, and avoid running it with sensitive logged-in accounts. <br>
Risk: Usage statistics and performance CrUX reporting may be enabled by default. <br>
Mitigation: Disable telemetry with --no-usage-statistics and --no-performance-crux when privacy requirements call for it. <br>
Risk: Installing chrome-devtools-mcp with @latest can change behavior between runs. <br>
Mitigation: Pin the npm package version in controlled or production-like environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinthqod/fox-chrome-devtools-mcp) <br>
- [Chrome DevTools MCP homepage](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide setup, status checks, and browser-control workflows for a Chrome DevTools MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
