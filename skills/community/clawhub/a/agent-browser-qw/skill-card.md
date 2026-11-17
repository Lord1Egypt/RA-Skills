## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyeisen](https://clawhub.ai/user/johnnyeisen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation agents use this skill to drive browser sessions for navigation, interaction, data extraction, form filling, UI testing, screenshots, PDF/video capture, and session state workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad authenticated browser control and saved session state can expose cookies, local storage, screenshots, PDFs, videos, traces, and request logs.

Mitigation: Keep saved state and browser artifacts out of source control and shared directories, and only load authenticated sessions for accounts and sites the agent is intended to control.

Risk: The installation guidance uses a global package install without a pinned package version.

Mitigation: Use a pinned, trusted agent-browser version where possible and avoid privileged global installs.

Risk: Browser automation commands can navigate, interact with pages, submit forms, intercept network requests, and evaluate JavaScript.

Mitigation: Review target sites and planned commands before execution, especially when using authenticated sessions or production accounts.

## Reference(s):

- [Agent Browser Qw ClawHub skill page](https://clawhub.ai/johnnyeisen/skills/agent-browser-qw)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; agent-browser commands can return plain text, JSON, screenshots, PDFs, videos, traces, and other browser artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; may preserve cookies, storage, screenshots, PDFs, videos, traces, request logs, and saved session state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
