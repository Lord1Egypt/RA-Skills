## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Knightluozichu](https://clawhub.ai/user/Knightluozichu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate browser navigation, page snapshots, structured data extraction, form filling, UI testing, screenshots, recordings, and session state management through concise shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can interact with logged-in sessions, private pages, uploads, and high-impact form submissions. <br>
Mitigation: Use it only for explicit browsing, testing, or data-extraction tasks, and confirm uploads or high-impact submissions before execution. <br>
Risk: Saved auth state, screenshots, PDFs, traces, recordings, cookies, and storage exports may contain sensitive page or session data. <br>
Mitigation: Delete or protect generated artifacts and saved session state, and avoid exposing private files or secrets to browser actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Knightluozichu/agent-browser-0-2-0) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce or save screenshots, PDFs, video recordings, traces, cookies, storage state, and authentication state files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
