## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liguang00806](https://clawhub.ai/user/liguang00806)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to control browser sessions for web interaction, structured extraction, form filling, UI checks, screenshots, PDFs, and debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to control browser sessions, including authenticated sessions.

Mitigation: Use it only with trusted agents and sites, avoid production accounts when practical, and review actions before submitting sensitive forms or changing account state.

Risk: Saved browser state, cookies, screenshots, PDFs, traces, videos, and auth files can contain sensitive data.

Mitigation: Treat saved state files like credentials and delete generated artifacts when they are no longer needed.

Risk: Installation uses mutable third-party package sources.

Mitigation: Prefer pinned package versions or reviewed commits and install only after trusting the package source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liguang00806/skills/agent-browser-temp)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser CLI skill issues](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser sessions may produce saved state, screenshots, traces, videos, PDFs, cookies, and auth files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
