## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janeaaaa](https://clawhub.ai/user/janeaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate browser workflows, inspect page state, fill forms, extract structured page data, and test web interfaces through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad control over web sessions, including authenticated pages, forms, cookies, localStorage, file uploads, and saved browser state. <br>
Mitigation: Use a dedicated browser profile or test account, avoid exposing session files unless needed, and require explicit approval before submitting forms, uploading files, changing account data, or replaying authenticated sessions. <br>
Risk: Screenshots, PDFs, recordings, traces, and saved auth state can contain private account data or credentials. <br>
Mitigation: Do not commit auth.json, recordings, screenshots, PDFs, or traces from logged-in sessions; review generated files before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/janeaaaa/agent-browser-v2) <br>
- [Publisher profile](https://clawhub.ai/user/janeaaaa) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, PDFs, recordings, traces, saved session state, and structured page snapshots through CLI commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
