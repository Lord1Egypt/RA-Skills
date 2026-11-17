## Description:

Implements agents using Deep Agents. Use when building agents with create_deep_agent, configuring backends, defining subagents, adding middleware, or setting up human-in-the-loop workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Deep Agents with create_deep_agent, LangGraph-compatible persistence and streaming, backend storage choices, subagents, middleware, MCP tools, and human approval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FilesystemBackend and execute examples can grant real disk and shell access.

Mitigation: Scope root_dir narrowly, sandbox filesystem and shell access, and require approval for writes, deletes, and external actions.

Risk: MCP subprocess examples and token use can expand host access or expose credentials if copied directly.

Mitigation: Pin MCP packages, avoid copying npx -y examples unchanged, and use short-lived least-privilege credentials from environment or secret management.

Risk: Persistent stores and checkpoints can retain data beyond a single conversation.

Mitigation: Use deliberate thread identifiers, limit stored paths to intended memory locations, and apply retention and access controls for production stores.

## Reference(s):

- [Built-in Tools Reference](references/tools.md)
- [Common Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides implementation patterns for Deep Agents, including persistence, filesystem access, MCP integration, subagents, middleware, streaming, and human-in-the-loop controls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
