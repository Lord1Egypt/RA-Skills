## Description:

Validate JSON data against schemas and compile it to binary .grm files for schema-enforced data contracts for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porco-rs](https://clawhub.ai/user/porco-rs)

### License/Terms of Use:


## Use Case:

Developers and agents use GERMANIC to validate structured JSON against built-in or custom schemas, produce .grm binaries, inspect compiled files, and configure the local MCP server when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external germanic CLI installed from a package channel or source build.

Mitigation: Install only from a trusted channel, prefer a pinned version or verified release artifact, and confirm `germanic --version` reports 0.2.3 before use.

Risk: Enabling the MCP server makes germanic commands callable through the configured MCP client.

Mitigation: Review MCP client configuration before enabling `germanic serve-mcp` and limit use to workspace data intended for validation or compilation.

Risk: Valid string fields are stored as data in compiled output and may still contain user-controlled text.

Mitigation: Treat compiled fields as typed data rather than instructions, and continue applying downstream content handling for string values.

## Reference(s):

- [GERMANIC ClawHub Skill Page](https://clawhub.ai/porco-rs/skills/germanic)
- [GERMANIC GitHub Homepage](https://github.com/germanicdev/germanic)
- [GERMANIC Workflow Examples](references/examples.md)
- [GERMANIC Schema Types](references/schema-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and file-oriented workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or validation of JSON schemas, JSON inputs, .grm output files, and MCP client configuration.]

## Skill Version(s):

0.2.3 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
