## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lim1202](https://clawhub.ai/user/lim1202) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate browser navigation, form filling, UI testing, page inspection, and session-based web workflows from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser state, cookies, headers, screenshots, PDFs, videos, traces, and captured requests can contain sensitive account or session data. <br>
Mitigation: Store these artifacts only in restricted locations, keep them out of source control and shared workspaces, and delete them when they are no longer needed. <br>
Risk: Browser automation against high-value production accounts can trigger unintended actions or expose privileged sessions. <br>
Mitigation: Use the skill only when browser automation is needed, prefer lower-risk accounts or environments, and review actions before running workflows that modify live services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lim1202/agent-browser-local) <br>
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser artifacts such as screenshots, PDFs, videos, traces, saved state, cookies, headers, and captured network request data when the documented CLI commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
