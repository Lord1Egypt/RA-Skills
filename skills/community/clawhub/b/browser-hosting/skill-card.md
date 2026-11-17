## Description:

OpenClaw browser hosting and automation capabilities for web interaction, scraping, and UI testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frisky1985](https://clawhub.ai/user/frisky1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to drive isolated or remote browser sessions for web scraping, UI workflow automation, testing, content extraction, and browser snapshot-based interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation authority can interact with web pages, forms, uploads, and content visible in a browser session.

Mitigation: Install only when this authority is acceptable, use the isolated openclaw profile for routine automation, and review browser actions before sensitive interactions.

Risk: Chrome relay or remote CDP profiles can expose an existing logged-in browser or remote browser endpoint to the agent.

Mitigation: Avoid chrome mode unless access to that session is intentional, and use only trusted TLS-protected remote CDP or browserless endpoints.

Risk: Tokens, passwords, or browserless credentials may be exposed through command lines or configuration examples.

Mitigation: Store secrets in environment variables or protected configuration and avoid placing credentials directly in shell commands.

Risk: The packaging helper and file upload workflows are unsafe for untrusted skill directories or unreviewed files.

Mitigation: Run packaging only on trusted skill directories and review files before upload or execution.

## Reference(s):

- [Browser Hosting ClawHub Page](https://clawhub.ai/frisky1985/skills/browser-hosting)
- [Configuration Guide](artifact/references/configuration.md)
- [Browser Profiles Reference](artifact/references/profiles.md)
- [Browser Snapshot System](artifact/references/snapshot-system.md)
- [Example Workflow](artifact/assets/example-workflow.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance, Text, Markdown]

**Output Format:** [Markdown guidance with inline bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide actions that produce browser snapshots, screenshots, PDFs, extracted text, network observations, or UI automation results.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
