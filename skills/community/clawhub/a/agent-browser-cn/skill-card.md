## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v585](https://clawhub.ai/user/v585)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate web pages from the command line, including navigation, element snapshots, form filling, data extraction, screenshots, PDFs, recordings, and saved browser sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser sessions may expose authenticated state, cookies, localStorage, screenshots, videos, PDFs, traces, and saved state files.

Mitigation: Use contained environments, avoid sensitive accounts unless necessary, treat generated state and media artifacts as secrets, and delete them after use.

Risk: The documented global npm install path can pull the latest package without pinning.

Mitigation: Prefer a pinned, reviewed local install before using the skill in production or commercial workflows.

Risk: Browser automation can interact with external sites, submit forms, alter storage, and intercept network requests.

Mitigation: Review target sites and commands before execution, re-snapshot after navigation, and require explicit approval before sensitive or destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/v585/skills/agent-browser-cn)
- [ClawHub publisher profile](https://clawhub.ai/user/v585)
- [agent-browser CLI repository referenced by artifact](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce browser snapshots, screenshots, PDFs, recordings, traces, saved state files, cookies, localStorage, and network request data.]

## Skill Version(s):

1.0.0 (source: target metadata and server release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
