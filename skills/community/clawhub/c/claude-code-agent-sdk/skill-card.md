## Description:

Claude Agent SDK documentation - build production AI agents with Claude Code as a library in Python or TypeScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as concise Claude Agent SDK reference material for building, configuring, debugging, securing, observing, and deploying Python or TypeScript agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples can enable high-impact agent automation in real projects.

Mitigation: Review examples before reuse, keep human approval for sensitive tool calls, and use least-privilege tool allow and deny rules.

Risk: Unpinned MCP package execution such as npx @latest can introduce unreviewed code into an agent environment.

Mitigation: Pin package versions and audit MCP servers before connecting them to production agents.

Risk: Bash and bypassPermissions can permit broad system changes when copied into insufficiently isolated deployments.

Mitigation: Use sandboxed containers or VMs, block dangerous tools where possible, and reserve bypassPermissions for isolated trusted environments.

Risk: Session persistence, telemetry, and broad filesystem or token access can expose sensitive project data.

Mitigation: Scope credentials and mounted files narrowly, protect or disable persistent session state for sensitive work, and route telemetry through approved controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/claude-code-agent-sdk)
- [Agent SDK Overview](artifact/references/overview.md)
- [Quick Start](artifact/references/quickstart.md)
- [Configuring Permissions](artifact/references/permissions.md)
- [Hosting the Agent SDK](artifact/references/hosting.md)
- [Python SDK API Reference](artifact/references/python.md)
- [TypeScript SDK API Reference](artifact/references/typescript.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; outputs are reference guidance and copyable examples rather than executable skill code.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
