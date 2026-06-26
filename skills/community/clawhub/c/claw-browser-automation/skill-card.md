## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangsaizz](https://clawhub.ai/user/zhangsaizz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser sessions from an agent for web UI testing, form filling, data extraction, screenshots, PDFs, recordings, and debugging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over a browser session. <br>
Mitigation: Use isolated browser profiles or test accounts, and require manual approval before uploads, purchases, account changes, or public posts. <br>
Risk: Saved auth state, cookies, screenshots, PDFs, videos, and traces may contain sensitive information. <br>
Mitigation: Protect generated artifacts during use and delete them when they are no longer needed. <br>
Risk: The skill depends on the upstream agent-browser package. <br>
Mitigation: Install it only in environments where the upstream package is trusted and appropriate for the intended browser automation task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangsaizz/claw-browser-automation) <br>
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser) <br>
- [Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create browser artifacts such as screenshots, PDFs, videos, traces, cookies, and saved session state when the agent runs the documented commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
