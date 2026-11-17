## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to drive a headless browser from structured commands for web navigation, UI testing, data extraction, form filling, and page capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables browser-session capabilities that can interact with authenticated pages and produce sensitive cookies, saved state files, screenshots, PDFs, videos, traces, and logs.

Mitigation: Limit use to intended sites and accounts, review actions before operating on authenticated pages, and protect or delete generated session artifacts after use.

Risk: Installation guidance includes global latest installs and curl-to-shell setup paths.

Mitigation: Prefer a pinned, verified agent-browser release and review installation commands before execution.

Risk: Security evidence marks the release suspicious because scoping and warnings are insufficient for sensitive browser automation.

Mitigation: Review the skill before installing, add local usage boundaries for allowed sites and data handling, and scan updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/agent-browser-tool)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; invoked CLI commands may return text, JSON, screenshots, PDFs, videos, or trace files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm according to release metadata; browser state and generated artifacts may contain sensitive session data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
