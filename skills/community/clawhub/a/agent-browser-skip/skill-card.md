## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, page inspection, form filling, UI testing, data extraction, screenshots, PDFs, recordings, and browser state workflows through structured shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable authenticated browser state can expose cookies, storage, or account sessions if saved or shared carelessly.

Mitigation: Use isolated sessions or test accounts, treat saved state files as sensitive credentials, and never commit auth.json or similar browser state artifacts.

Risk: Screenshots, PDFs, traces, recordings, cookies, and storage dumps may contain private data.

Mitigation: Store captured artifacts only where access is controlled, review them before sharing, and delete them when they are no longer needed.

Risk: Mutable global installation can execute tooling from a package version the user has not reviewed.

Mitigation: Install only from a trusted version or commit and avoid running installers with administrative privileges.

Risk: Browser automation against important accounts or production systems can perform unintended actions.

Mitigation: Review proposed agent-browser actions before execution and prefer sandboxed or non-production sessions for high-impact workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayakolin/skills/agent-browser-skip)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm, and uses the agent-browser CLI for browser automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
