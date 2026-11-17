## Description:

Automate web navigation, interaction, and data extraction using a fast Rust-based headless browser CLI with Node.js fallback and structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxw975](https://clawhub.ai/user/gxw975)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser workflows such as login, form filling, structured page extraction, and web UI testing through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install an unpinned third-party CLI.

Mitigation: Verify the agent-browser npm package and intended version before installation; prefer a pinned or local install where possible.

Risk: Browser automation can expose sensitive session data such as credentials, screenshots, videos, cookies, storage, and internal pages.

Mitigation: Run automation in a least-privileged browser profile without unrelated saved sessions, and only capture or enter sensitive data with explicit authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxw975/skills/clawhub-publish-146156)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with inline bash commands and CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-browser commands may produce page snapshots, screenshots, PDFs, videos, and browser session data when invoked.]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
