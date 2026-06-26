## Description: <br>
Use Chrome DevTools MCP through UXC over local stdio for page navigation, DOM/a11y snapshots, network inspection, console inspection, and performance tooling, with a live-browser autoConnect default and optional browserUrl or isolated fallback modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to Chrome DevTools MCP through UXC for browser inspection, diagnostics, and guarded page interaction. It supports live Chrome attachment, explicit browser URL attachment, and isolated headless fallback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live Chrome DevTools session can let an agent inspect or act through a logged-in browser session. <br>
Mitigation: Prefer isolated or headless mode, use a dedicated browser profile for sensitive work, avoid autoConnect around private accounts, and require explicit confirmation before page-changing actions. <br>
Risk: Fetching chrome-devtools-mcp with the latest package tag can change behavior over time. <br>
Mitigation: Pin the MCP package version when repeatability or release review is required. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance favors JSON envelope parsing, read-first browser inspection, and confirmation before page-changing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
