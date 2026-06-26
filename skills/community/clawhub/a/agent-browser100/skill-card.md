## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Keyserkazi1](https://clawhub.ai/user/Keyserkazi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to drive browser sessions for web navigation, data extraction, form filling, UI testing, screenshots, recording, storage inspection, and network debugging through structured shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents reusable logged-in browser state and page-capture capabilities. <br>
Mitigation: Use disposable or task-specific browser sessions where possible and treat saved state files, screenshots, videos, PDFs, traces, cookies, and request logs as secrets. <br>
Risk: Browser automation can perform account-changing or public actions through forms, uploads, purchases, submissions, and posts. <br>
Mitigation: Require explicit confirmation before uploads, submissions, purchases, public posts, or account changes. <br>
Risk: Installation depends on an external agent-browser npm package and source repository. <br>
Mitigation: Install only when the external package and source are trusted for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Keyserkazi1/agent-browser100) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create browser state files, screenshots, PDFs, videos, traces, and request logs when the documented commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
