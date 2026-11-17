## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate browser workflows, inspect pages, fill forms, capture screenshots or PDFs, manage browser state, and test web UIs through structured shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a mutable global browser automation CLI, so behavior may change when the upstream package changes.

Mitigation: Use a pinned and reviewed agent-browser version and re-scan the skill when the CLI version changes.

Risk: Browser automation can interact with authenticated pages and saved browser sessions.

Mitigation: Use low-privilege or test accounts, avoid running as root, keep saved auth state out of repositories and shared workspaces, restrict file permissions, and delete or rotate saved sessions after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/agent-browser-zc)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline shell commands and command output examples; agent-browser commands can also emit JSON when invoked with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, PDFs, recordings, traces, saved session state files, cookies, local storage values, and network request summaries through the wrapped CLI.]

## Skill Version(s):

0.2.4 (source: server release metadata; artifact/_meta.json lists 0.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
