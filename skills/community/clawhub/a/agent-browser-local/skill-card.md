## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lim1202](https://clawhub.ai/user/lim1202)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, interaction, data extraction, form filling, UI testing, screenshots, PDFs, recordings, and saved sessions through structured agent-browser commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable third-party agent-browser CLI.

Mitigation: Review the installer before use, pin a trusted agent-browser version where practical, and avoid elevated privileges for installation commands.

Risk: Saved browser state, screenshots, traces, PDFs, and recordings may capture authenticated sessions or sensitive page data.

Mitigation: Use separate per-task sessions, handle generated artifacts as sensitive, and delete auth.json or other captured files when no longer needed.

## Reference(s):

- [Agent Browser Local on ClawHub](https://clawhub.ai/lim1202/skills/agent-browser-local)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with bash command examples; CLI commands may return text, JSON, screenshots, PDFs, traces, recordings, or saved browser state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm. Browser sessions, screenshots, traces, PDFs, recordings, and saved state can contain sensitive data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
