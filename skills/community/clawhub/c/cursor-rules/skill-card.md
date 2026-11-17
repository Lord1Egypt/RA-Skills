## Description:

Cursor IDE guidance for configuring .cursorrules, MDC rules, Agent mode, and MCP integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Cursor IDE guidance for AI-assisted coding workflows, rule configuration, Agent mode, and MCP integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent or yolo mode may execute commands without sufficient review.

Mitigation: Use yolo mode only in disposable or sandboxed projects and review proposed commands and diffs before applying them.

Risk: MCP filesystem examples can expose broader local files than intended.

Mitigation: Configure MCP servers with the narrowest practical filesystem path.

Risk: MCP GitHub examples can expose tokens if copied into committed configuration.

Mitigation: Keep GitHub tokens out of committed files and store credentials through local secret-management practices.

Risk: Unpinned MCP package examples can change behavior over time.

Mitigation: Pin package versions where possible before adopting the examples.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with configuration examples, tables, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Cursor rule examples, keyboard shortcut tables, MCP configuration examples, and workflow guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
