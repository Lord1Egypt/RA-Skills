## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knightluozichu](https://clawhub.ai/user/knightluozichu)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to automate browser navigation, page inspection, form filling, screenshots, recordings, and web UI testing through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent control of browser sessions, including authenticated sessions.

Mitigation: Install only from a trusted agent-browser package source, pin a reviewed version or commit where possible, and scope browser sessions to the minimum required task.

Risk: Saved browser state, cookies, localStorage, credentials, traces, screenshots, PDFs, and videos may contain sensitive information.

Mitigation: Keep generated state and media out of repositories and shared folders, restrict file permissions, and delete files or revoke sessions when finished.

## Reference(s):

- [Agent Browser 0.2.0 on ClawHub](https://clawhub.ai/knightluozichu/skills/agent-browser-0-2-0)
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill Issues](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create browser state, screenshots, PDFs, traces, and recordings when executed by an agent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); artifact metadata version 0.2.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
