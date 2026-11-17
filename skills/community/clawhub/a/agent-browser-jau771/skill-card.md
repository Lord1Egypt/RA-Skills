## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jau771](https://clawhub.ai/user/jau771)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to automate browser navigation, page inspection, form interaction, UI testing, screenshots, PDFs, recording, and session/state handling through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation can navigate pages, interact with forms, upload files, and control sessions in ways that affect real accounts or services.

Mitigation: Use test accounts where possible, review commands before execution, and explicitly approve uploads, screenshots, PDFs, and recordings.

Risk: Saved browser state files can contain session credentials.

Mitigation: Protect or delete saved state files such as auth.json and avoid attaching the skill to a personal live browser through CDP.

Risk: The release was flagged as suspicious because it gives agents broad browser and session control without enough safety framing.

Mitigation: Install only when full browser automation is needed, prefer a pinned reviewed package version or commit, and avoid administrator privileges during install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jau771/skills/agent-browser-jau771)
- [Upstream agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser Skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; documented workflows may create saved state files, screenshots, PDFs, videos, and traces.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
