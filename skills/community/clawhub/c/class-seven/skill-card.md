## Description:

Class Seven coordinates complex development work by orchestrating specialized PM, architect, developer, tester, and debugger agents with tool selection guidance for Claude Code, Kimi, and native tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

Developers and engineers use Class Seven to coordinate multi-agent software delivery workflows across requirements, architecture, implementation, testing, code review, debugging, and integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can route sensitive code, logs, or repository context to external model tools.

Mitigation: Use it only with explicit approval for external model calls, and sanitize logs and repository content before sharing them with external tools.

Risk: The artifact recommends remote installer commands and persistent Claude/Kimi configuration changes.

Mitigation: Independently trust and verify installer commands before execution, and review any proposed agent configuration changes before applying them.

## Reference(s):

- [Class Seven Workflow Patterns](references/workflows.md)
- [Class Seven Tool Integration Guide](references/tools-guide.md)
- [Class Seven Example Projects](references/examples.md)
- [Class Seven ClawHub Release](https://clawhub.ai/russellfei/skills/class-seven)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose role-specific agent outputs such as requirements, architecture notes, implementation code, test plans, root cause analysis, fixes, and delivery summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
