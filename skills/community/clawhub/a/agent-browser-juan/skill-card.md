## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amorypaz1781](https://clawhub.ai/user/amorypaz1781) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to control browser sessions, inspect page state, fill forms, collect structured page output, and debug web UI flows through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad browser-control authority, including access to authenticated sessions and browser state. <br>
Mitigation: Install only when the upstream agent-browser CLI is trusted and require confirmation before logging in, submitting forms, uploading files, changing accounts, using eval, CDP, or network interception, or saving and loading session state. <br>
Risk: Saved state files, cookies, storage dumps, screenshots, PDFs, traces, and recordings can expose credentials or private data. <br>
Mitigation: Treat generated browser artifacts as sensitive, keep them out of repositories, restrict access to them, and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amorypaz1781/agent-browser-juan) <br>
- [Skill Issue Repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>
- [Upstream agent-browser CLI Repository](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser artifacts such as saved state, screenshots, PDFs, traces, and recordings may contain sensitive data.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
