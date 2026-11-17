## Description:

Query up-to-date library documentation and code examples using Context7 MCP for current, version-specific guidance across npm packages, Python libraries, and other programming ecosystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to resolve library identifiers and query current Context7 documentation or code examples while working with package APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation queries are sent to Context7 and may expose sensitive package names, questions, or snippets if included.

Mitigation: Avoid sending private code, secrets, or confidential project details in documentation queries unless that external service is approved for the data.

Risk: The first run may create a local context7-mcp-cli link through uxc.

Mitigation: Review the link command and stop on command-name conflicts before creating or using the fixed command.

## Reference(s):

- [Context7 Usage Patterns](references/usage-patterns.md)
- [uxc Skill](https://github.com/holon-run/uxc/tree/main/skills/uxc)
- [Context7 MCP Endpoint](https://mcp.context7.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and Context7 documentation query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require network access to Context7 and a local context7-mcp-cli link created through uxc.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
