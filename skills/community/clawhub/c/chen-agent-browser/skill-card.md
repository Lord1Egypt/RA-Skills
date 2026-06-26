## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser workflows including navigation, interaction, form filling, data extraction, UI testing, screenshots, recording, and session state management through structured CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over browser sessions and can interact with sensitive websites or authenticated pages. <br>
Mitigation: Use isolated browser profiles or test accounts and require explicit confirmation before uploads, purchases, form submissions, credential use, cookie or storage changes, or network request mocking. <br>
Risk: Saved browser state files may contain sensitive session data. <br>
Mitigation: Protect saved state files like credentials, avoid production or admin sessions unless necessary, and remove session files when no longer needed. <br>
Risk: The skill depends on an external agent-browser CLI installed through node and npm. <br>
Mitigation: Install only if the external tool is trusted and verify the installed CLI before allowing agent-driven browser automation. <br>


## Reference(s): <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands; CLI commands may return JSON, screenshots, PDFs, video recordings, or saved browser state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; uses the external agent-browser CLI for browser automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
