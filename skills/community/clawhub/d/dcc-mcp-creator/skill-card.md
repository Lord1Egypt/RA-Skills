## Description:

Build or modernize DCC-MCP adapters and standalone studio MCP services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and studio engineers use this skill to implement or modernize adapters for digital content creation applications and standalone studio MCP services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing a standalone studio service can create unauthorized access risk.

Mitigation: Review network exposure plans and use operator-managed TLS, authentication, firewall rules, audit controls, and secret storage where applicable.

Risk: Source-level checks may not reveal behavior in a live DCC application.

Mitigation: Keep source or mock validation separate from real-host acceptance and validate requested behavior in the intended host.

## Reference(s):

- [DCC-MCP Creator skill source](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp-creator/SKILL.md)
- [Adapter and service workflow](references/ADAPTER_WORKFLOW.md)
- [Host pattern matrix](references/HOST_PATTERN_MATRIX.md)
- [Internal service workflow](references/INTERNAL_SERVICE_WORKFLOW.md)
- [Runtime integration](references/RUNTIME_INTEGRATION.md)
- [Python runtime selection](references/PYTHON_RUNTIME_SELECTION.md)
- [Native extension workflow](references/NATIVE_EXTENSION_WORKFLOW.md)
- [Async recovery](references/ASYNC_RECOVERY.md)
- [Core escalation checklist](references/CORE_ESCALATION_CHECKLIST.md)
- [Failure routing](references/FAILURE_ROUTING.md)
- [Integration examples](references/INTEGRATION_EXAMPLES.md)
- [Testing and release](references/TESTING_AND_RELEASE.md)
- [DCC-MCP core protocol ownership decision](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/docs/adr/027-protocol-type-ownership.md)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with code examples and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the requested DCC host or standalone studio service.]

## Skill Version(s):

0.19.117 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
