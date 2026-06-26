## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser navigation, DOM interaction, form filling, UI testing, page inspection, screenshots, recordings, and structured data extraction through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and invokes an external browser automation CLI package. <br>
Mitigation: Install only from trusted package sources and review the package/source before use. <br>
Risk: Browser automation can interact with sensitive logged-in sessions and submit forms or make account changes. <br>
Mitigation: Use isolated browser profiles, avoid sensitive accounts unless necessary, and review important actions before submission or account changes. <br>
Risk: Screenshots, recordings, traces, cookies, and auth-state files may contain sensitive data. <br>
Mitigation: Store generated browser artifacts carefully and delete or restrict access to sensitive outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayakolin/agent-browser-skip) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with inline shell command examples and optional JSON command output guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The wrapped CLI can create screenshots, PDFs, videos, traces, cookies, and saved browser state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
