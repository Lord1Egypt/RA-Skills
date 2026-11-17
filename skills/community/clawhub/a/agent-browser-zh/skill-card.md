## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a browser through the agent-browser CLI for web navigation, structured page extraction, form filling, UI testing, and session-based automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can interact with authenticated pages and preserve cookies or saved login state.

Mitigation: Use an isolated, unprivileged browser profile or container and delete session files when the task is done.

Risk: Screenshots, recordings, traces, cookies, storage dumps, and network logs may contain secrets.

Mitigation: Treat these artifacts as secrets; do not commit or share them.

Risk: Mutable global installation of the agent-browser package can change behavior over time.

Mitigation: Pin the agent-browser package version or Git commit before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayakolin/skills/agent-browser-zh)
- [agent-browser CLI Repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill Issue Repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime commands can return text, JSON, screenshots, PDFs, recordings, and trace files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser sessions may produce saved state, cookies, local storage, screenshots, recordings, traces, and network logs.]

## Skill Version(s):

0.2.2 (source: server release evidence and target metadata; artifact frontmatter and artifact/_meta.json report 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
