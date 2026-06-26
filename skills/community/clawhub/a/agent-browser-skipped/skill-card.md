## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[susiemiles443](https://clawhub.ai/user/susiemiles443) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser-based workflows such as navigation, form filling, UI testing, page inspection, screenshots, recording, and data extraction through structured CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can control browser sessions, including authenticated pages, cookies, local storage, uploads, recordings, screenshots, and saved state. <br>
Mitigation: Use disposable sessions where possible, avoid sensitive logged-in accounts unless necessary, and require confirmation before credential entry, file upload, cookie or storage access, recording, screenshots, saved-state handling, or account-changing actions. <br>
Risk: The skill depends on the upstream agent-browser package and grants broad browser-control authority once installed. <br>
Mitigation: Install only when the upstream package is trusted, keep the package current, and review browser actions before execution in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/susiemiles443/agent-browser-skipped) <br>
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, PDFs, video recordings, traces, and saved browser state files when those agent-browser commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
