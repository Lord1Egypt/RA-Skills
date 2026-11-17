## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxz9909](https://clawhub.ai/user/cxz9909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, interaction, UI testing, form filling, page snapshots, screenshots, PDFs, and structured data extraction through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser state files, cookies, storage dumps, screenshots, PDFs, traces, and recordings may contain account access or private page data.

Mitigation: Treat these artifacts as sensitive, keep them out of project repositories, restrict file permissions, and delete them when they are no longer needed.

Risk: Installing browser automation tooling from an untrusted release or with elevated privileges can increase local execution risk.

Mitigation: Install from a version or commit you trust and avoid administrator privileges where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxz9909/skills/cxz9909-agentbrowser)
- [Agent Browser CLI upstream project](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser artifacts such as screenshots, PDFs, traces, recordings, cookies, storage dumps, and saved session state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
