## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyhh](https://clawhub.ai/user/xyhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser workflows such as navigation, page inspection, form filling, web UI testing, data extraction, file upload, authentication workflows, and recording or screenshot capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser state, cookies, screenshots, recordings, PDFs, traces, and storage output may expose active sessions or sensitive page content. <br>
Mitigation: Keep files such as auth.json out of repositories and shared folders, restrict file permissions, and delete captured artifacts when they are no longer needed. <br>
Risk: Browser automation and JavaScript evaluation can perform actions in active web sessions. <br>
Mitigation: Use the skill only on trusted sites and accounts, review commands before execution, and avoid sensitive accounts unless browser automation is necessary. <br>
Risk: The skill depends on the upstream agent-browser npm package. <br>
Mitigation: Install it only when the upstream package is trusted and consider pinning or reviewing the package version in controlled environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xyhh/agent-browser-xyhh) <br>
- [agent-browser CLI Repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser Skill Issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown command reference with bash examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser state files, recordings, screenshots, PDFs, and traces may be produced by invoked commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
