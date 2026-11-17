## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorexxar](https://clawhub.ai/user/lorexxar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to drive headless browser workflows: navigating pages, inspecting interactive elements, filling forms, testing web UIs, managing browser state, and extracting structured page data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser sessions, cookies, screenshots, PDFs, traces, and recordings can contain sensitive data.

Mitigation: Avoid saving these artifacts from sensitive sites unless necessary, and delete or protect them immediately after use.

Risk: Passwords or tokens passed directly in browser automation commands may be captured in logs or shell history.

Mitigation: Use test credentials or secure secret-handling workflows, and avoid placing real secrets directly in command text.

Risk: Unpinned global installation can fetch a changed upstream browser automation package.

Mitigation: Install only trusted reviewed versions when possible and verify the installed CLI version before using it in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorexxar/skills/agent-browser-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser commands may save screenshots, PDFs, recordings, traces, cookies, storage, and session state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
