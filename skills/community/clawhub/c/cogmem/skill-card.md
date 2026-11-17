## Description:

Install and connect cogmem as a durable memory backend for OpenClaw. Version 2.5.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuqin164](https://clawhub.ai/user/liuqin164)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, migrate, and operate cogmem as a durable memory backend for OpenClaw workspaces, including recall, turn capture, MCP bridge use, and background memory consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable remote code from a main branch.

Mitigation: Prefer a pinned, reviewed commit and run the installer in a low-privilege workspace.

Risk: Automatic memory capture can retain profile, memory, and conversation data beyond the current session.

Mitigation: Decide which files should be imported, avoid secrets or regulated data, and confirm how to disable hooks, background queues, services, and retained memory files before enabling automatic memory.

## Reference(s):

- [Cogmem Memory on ClawHub](https://clawhub.ai/liuqin164/skills/cogmem)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, TOML, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, migration, runtime wiring, debugging, background service, and MCP bridge guidance.]

## Skill Version(s):

2.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
