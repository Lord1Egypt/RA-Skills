## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JohnnyEisen](https://clawhub.ai/user/JohnnyEisen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive headless browser workflows, including web navigation, page interaction, structured extraction, form filling, UI testing, screenshots, recordings, and browser state management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-driven browser automation can expose logged-in browsing data, cookies, local storage, and saved session artifacts. <br>
Mitigation: Use isolated browser profiles or test accounts, require explicit approval before reading cookies or storage or saving and loading auth state, and delete saved auth files when finished. <br>
Risk: Screenshots, traces, recordings, PDFs, uploads, and form submissions can disclose sensitive information or perform unintended actions. <br>
Mitigation: Review target sites and intended actions before capture, upload, export, or form submission, especially on sensitive logged-in accounts. <br>
Risk: The skill depends on an external npm package for browser automation. <br>
Mitigation: Verify or pin the external npm package before installation and use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JohnnyEisen/agent-browser-qw) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to produce JSON command output when the documented --json option is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
