## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kendrick-lu](https://clawhub.ai/user/kendrick-lu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use AgentBrowser to automate browser workflows such as web navigation, data extraction, form filling, UI testing, state inspection, and browser artifact capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can expose saved state files, cookies, credentials, screenshots, PDFs, videos, traces, and network logs. <br>
Mitigation: Store generated artifacts in protected locations, avoid unnecessary logged-in sessions, and clear saved browser state when work is complete. <br>
Risk: The skill depends on the external agent-browser npm package and upstream browser tooling. <br>
Mitigation: Install only when the external package and browser tooling are trusted for the target environment. <br>
Risk: Automated navigation, form filling, JavaScript evaluation, request routing, and storage changes can affect live websites or accounts. <br>
Mitigation: Review intended commands before execution and prefer test accounts or isolated sessions for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub AgentBrowser release page](https://clawhub.ai/kendrick-lu/agentbrowser) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides use of the agent-browser CLI, which can produce page snapshots, screenshots, PDFs, videos, traces, network logs, cookies, storage data, and saved browser state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
