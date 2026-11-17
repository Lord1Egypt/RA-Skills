## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kdegeek](https://clawhub.ai/user/kdegeek)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to automate browser navigation, form interaction, page inspection, screenshots, PDFs, recordings, and structured web data extraction through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running an external agent-browser CLI package and installer.

Mitigation: Install only trusted, preferably pinned package versions and avoid elevated privileges during installation.

Risk: Saved auth state, cookies, traces, screenshots, PDFs, and recordings may contain sensitive data.

Mitigation: Store generated browser artifacts securely, redact before sharing, and delete them when no longer needed.

Risk: Browser automation can submit forms, upload files, alter sessions, or interact with untrusted sites.

Mitigation: Use isolated browser sessions for untrusted sites and review targets, uploads, and state-changing commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kdegeek/skills/agent-browser-0)
- [agent-browser CLI Repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and optional JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of browser artifacts such as screenshots, PDFs, recordings, traces, and saved session state when the agent-browser CLI is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
