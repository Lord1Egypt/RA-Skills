## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangsaizz](https://clawhub.ai/user/zhangsaizz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused agents use this skill to drive web browsers from the terminal for UI testing, data extraction, form filling, authentication workflows, screenshots, recordings, and structured page inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs and invokes a browser automation package that can affect local browser state and dependencies.

Mitigation: Install in a least-privilege or disposable environment where possible, and pin and verify the agent-browser package before use.

Risk: Saved sessions, cookies, localStorage, screenshots, PDFs, traces, videos, request logs, and CDP-connected sessions may contain sensitive data.

Mitigation: Treat those outputs as sensitive artifacts, protect or delete them after use, and avoid sharing them without review.

Risk: Browser automation can interact with real sites and accounts.

Mitigation: Use the browser commands only on sites and accounts the operator is authorized to automate.

## Reference(s):

- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Claw Browser Automation issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)
- [ClawHub skill page](https://clawhub.ai/zhangsaizz/skills/claw-browser-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON-producing CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce screenshots, PDFs, traces, recordings, saved browser state, and request logs through the underlying CLI.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
