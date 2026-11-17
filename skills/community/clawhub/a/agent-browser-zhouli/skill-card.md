## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to drive headless browser workflows, inspect pages, fill forms, capture screenshots or PDFs, and test web UIs through structured CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent authenticated browser state and captured artifacts can expose sensitive session data or secrets.

Mitigation: Treat auth.json, screenshots, PDFs, videos, traces, cookies, storage, and network logs as sensitive; do not commit or share them, and delete them when no longer needed.

Risk: Global or mutable installation of the agent-browser package/source can introduce unreviewed changes.

Mitigation: Install only from trusted sources, prefer pinned package versions or audited commits, and avoid elevated privileges during installation.

Risk: Browser automation can operate in authenticated sessions and perform actions on live sites.

Mitigation: Review target URLs and proposed actions before execution, use isolated sessions where practical, and save or load session state only when necessary.

## Reference(s):

- [Agent Browser ClawHub Release](https://clawhub.ai/onlyloveher/skills/agent-browser-zhouli)
- [agent-browser CLI Repository](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; generated browser state, screenshots, PDFs, videos, traces, cookies, storage, and network logs may contain sensitive data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
