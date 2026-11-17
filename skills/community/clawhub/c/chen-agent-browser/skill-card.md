## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, inspect page state, extract web data, fill forms, test web UIs, and capture screenshots or recordings through structured agent-browser commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad live-browser control, including navigation, clicks, typing, uploads, downloads, JavaScript evaluation, storage access, and network interception.

Mitigation: Run it in a sandbox or test environment, use reviewed pinned versions, and require explicit approval before form submission, file upload, account changes, traffic interception, or eval commands.

Risk: Saved browser state, cookies, local storage, traces, recordings, screenshots, PDFs, and uploaded files may expose sensitive account or page data.

Mitigation: Treat saved state and captured artifacts as secrets, avoid production accounts unless necessary, and delete or restrict access to generated files after use.

Risk: Automation against real websites can cause unintended actions if the agent selects stale references or misinterprets page state.

Mitigation: Snapshot after navigation or major page changes, verify target elements before destructive actions, and keep human approval on irreversible workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-agent-browser)
- [Publisher profile](https://clawhub.ai/user/cs995279497-byte)
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser CLI skill repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from agent-browser commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI may produce browser snapshots, screenshots, PDFs, traces, videos, and saved state files; the skill declares node and npm as required binaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
