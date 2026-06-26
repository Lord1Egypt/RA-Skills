## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser sessions for web UI testing, page inspection, form filling, structured data extraction, screenshots, PDFs, recordings, and debugging through agent-browser CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over browser sessions, including logged-in state and actions on websites. <br>
Mitigation: Use separate test accounts or disposable sessions, avoid sensitive logged-in sites unless necessary, and require confirmation before cookie or storage access, uploads, purchases, posts, or form submissions. <br>
Risk: Saved auth state, screenshots, PDFs, recordings, and traces may contain secrets or private data. <br>
Mitigation: Treat auth.json and generated browser artifacts as secrets, keep them out of shared locations, and delete them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/agent-browser-zc) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser Skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON, Files] <br>
**Output Format:** [Markdown with inline shell commands; CLI commands may return text or JSON and can create screenshots, PDFs, traces, recordings, or saved state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; agent-browser installation is expected before use.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
