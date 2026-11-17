## Description:

Build, integrate, debug, and secure MCP servers and clients in any language, enabling AI agents to call external tools via Model Context Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design, implement, test, secure, debug, and publish MCP servers and client integrations for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied logging examples may expose tokens, request bodies, or other sensitive fields if used without changes.

Mitigation: Redact or allowlist logged fields and avoid logging secrets, tokens, or full request bodies.

Risk: Copied package commands may install changing npx or npm package versions.

Mitigation: Pin package versions before using generated commands in repeatable or production workflows.

Risk: MCP tools created from the templates may receive broader permissions than needed.

Mitigation: Scope tools to least privilege and require explicit confirmation for writes or deployment actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1kalin/skills/afrexai-mcp-engineering)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, configuration snippets, shell commands, checklists, and rubrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; copied templates should be reviewed and adapted before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
