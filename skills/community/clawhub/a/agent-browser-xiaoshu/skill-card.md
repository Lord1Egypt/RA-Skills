## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate web navigation, page inspection, form filling, data extraction, UI testing, and browser debugging through concise agent-browser CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can expose sensitive cookies, local storage, screenshots, recordings, traces, uploaded files, or saved session state.

Mitigation: Use disposable test accounts for login workflows, treat saved state such as auth.json as a secret, and avoid committing or sharing browser state, screenshots, recordings, or traces.

Risk: The documented installation flow uses an unpinned global npm install, which may install a newer or unexpected agent-browser version.

Mitigation: Review before installing, prefer pinned trusted versions of agent-browser, and avoid running installation with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaomaju-888/skills/agent-browser-xiaoshu)
- [agent-browser upstream CLI](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command results may be text, JSON, screenshots, PDFs, videos, traces, or saved browser state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; uses the agent-browser CLI and may create browser state, media, trace, and document files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
