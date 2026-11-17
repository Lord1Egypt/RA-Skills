## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amorypaz1781](https://clawhub.ai/user/amorypaz1781)

### License/Terms of Use:


## Use Case:

Developers and AI agent operators use this skill to automate browser navigation, interaction, form filling, UI testing, page snapshots, and structured data extraction through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can act on authenticated sessions, submit forms, change account state, intercept network traffic, and reuse stored sessions.

Mitigation: Use isolated installations, scope each task to a specific site, avoid elevated privileges, and require confirmation before form submissions or account changes.

Risk: Saved state, screenshots, PDFs, videos, traces, cookies, and storage dumps can expose sensitive data.

Mitigation: Treat generated artifacts as secrets, store them only in restricted locations, and delete or redact them before sharing.

Risk: Debug, JavaScript evaluation, upload, CDP, and network routing commands can alter page behavior or expose data.

Mitigation: Review commands before execution, prefer pinned CLI versions, and use test accounts or sandboxed sites for untrusted workflows.

## Reference(s):

- [agent-browser upstream CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and optional JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can also create screenshots, PDFs, videos, traces, saved browser state, cookies, and storage dumps during browser automation.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
