## Description:

Launch a persistent headless Chromium with remote debugging (CDP) for browser automation, including page navigation, clicks, form filling, screenshots, and cookie import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redf426](https://clawhub.ai/user/redf426)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give OpenClaw agents a persistent headless browser for web navigation, interaction, screenshots, and authenticated browsing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a persistent authenticated headless browser and import cookies, which may expose account sessions if used with sensitive accounts.

Mitigation: Use a dedicated unprivileged environment, avoid importing high-value account cookies, and delete imported cookie files and browser profiles when finished.

Risk: The Chromium launch script disables Chromium sandboxing, increasing exposure when visiting untrusted websites.

Mitigation: Treat the disabled sandbox as a serious risk, browse only necessary sites, and isolate the runtime from sensitive host resources.

Risk: Optional always-on browser startup can keep authenticated browsing state available longer than intended.

Mitigation: Do not add the optional cron startup unless continuous browsing is required.

## Reference(s):

- [Cookie-Editor](https://cookie-editor.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and browser-tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch and manage a persistent local browser profile and CDP endpoint when installed and executed.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
