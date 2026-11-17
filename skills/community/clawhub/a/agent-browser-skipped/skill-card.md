## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[susiemiles443](https://clawhub.ai/user/susiemiles443)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser navigation, UI testing, form filling, page snapshots, screenshots, session state, and structured data extraction through agent-browser CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-control authority can expose sensitive accounts, pages, cookies, local storage, screenshots, recordings, traces, and network logs.

Mitigation: Run the skill only in trusted, isolated environments; avoid sensitive accounts unless necessary; treat saved session files and capture artifacts as secrets and delete them when they are no longer needed.

Risk: Mutable global installs such as latest npm packages can change behavior between reviews.

Mitigation: Prefer pinned and reviewed agent-browser versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/susiemiles443/skills/agent-browser-skipped)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create browser automation artifacts such as screenshots, PDFs, recordings, traces, saved session state, cookies, storage exports, or network logs when the referenced CLI commands are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
