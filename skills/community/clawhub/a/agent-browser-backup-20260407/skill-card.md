## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejianjun000](https://clawhub.ai/user/xiejianjun000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to control agent-browser for web navigation, form filling, UI testing, data extraction, screenshots, recordings, PDFs, and stateful browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved authenticated browser sessions can expose cookies or credentials if stored insecurely.

Mitigation: Treat saved state files like passwords, store them outside shared projects with restrictive permissions, and delete them when no longer needed.

Risk: An unpinned global CLI install can pull unexpected updates.

Mitigation: Prefer a pinned agent-browser version and avoid root or administrator installs unless explicitly required.

Risk: Browser automation can interact with arbitrary websites and submit forms.

Mitigation: Run against authorized targets, use test accounts where possible, and review navigation and form-submission commands before execution.

Risk: Screenshots, videos, PDFs, traces, and saved state can capture sensitive page data.

Mitigation: Write artifacts to controlled locations, restrict access, inspect outputs before sharing, and remove sensitive files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejianjun000/skills/agent-browser-backup-20260407)
- [agent-browser CLI Repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and optional JSON or file outputs from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create screenshots, PDFs, videos, trace files, and saved browser state through agent-browser.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
