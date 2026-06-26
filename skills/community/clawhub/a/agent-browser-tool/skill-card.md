## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser workflows such as navigation, form filling, UI testing, page inspection, screenshots, PDFs, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control browser sessions across websites, including clicks, typing, uploads, form submissions, and other actions that may be hard to reverse. <br>
Mitigation: Use isolated test accounts or sessions, review targets before execution, and require explicit approval before uploads, submissions, purchases, account changes, or other irreversible website actions. <br>
Risk: Saved browser state and captured artifacts may expose cookies, login sessions, page contents, screenshots, PDFs, traces, or recordings. <br>
Mitigation: Keep auth.json and media artifacts out of repositories and shared logs, store them only as needed, and delete them when the task is complete. <br>
Risk: The skill depends on an externally installed agent-browser package. <br>
Mitigation: Install only from a trusted package source and pin a known version when using the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/agent-browser-tool) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands may return text, JSON, screenshots, PDFs, traces, or recordings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm, and uses the external agent-browser CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
