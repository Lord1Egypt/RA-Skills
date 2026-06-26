## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Liguang00806](https://clawhub.ai/user/Liguang00806) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate browser navigation, page inspection, form entry, UI testing, and structured extraction through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over browser sessions, including logged-in pages and sensitive browser data. <br>
Mitigation: Use a separate browser profile or disposable session, avoid sensitive logged-in accounts unless necessary, and keep saved state files such as auth.json private. <br>
Risk: Browser automation can perform high-impact actions such as purchases, account changes, public posts, file uploads, credential use, or cookie and localStorage exposure. <br>
Mitigation: Require explicit user confirmation before those actions and review commands before execution. <br>
Risk: The workflow depends on an external npm CLI that must be trusted before installation and use. <br>
Mitigation: Install only when the external agent-browser package is acceptable for the environment and review the package source and behavior before deployment. <br>


## Reference(s): <br>
- [Agent Browser Temp on ClawHub](https://clawhub.ai/Liguang00806/agent-browser-temp) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-browser commands can return page text, snapshots, screenshots, PDFs, videos, JSON, cookies, storage data, and saved browser state files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
