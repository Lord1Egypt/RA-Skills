## Description:

Create documentation optimized for AI agent consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylervovan](https://clawhub.ai/user/tylervovan)

### License/Terms of Use:


## Use Case:

Developers and documentation authors use this skill to create agent-readable SKILL.md files, README files, API docs, AGENTS.md indexes, and llms.txt documentation. It helps structure content for retrieval, token efficiency, security constraints, and hybrid context loading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation can introduce incorrect, stale, or overly broad agent instructions into a project.

Mitigation: Review generated AGENTS.md, llms.txt, CI snippets, and security rules before adopting them.

Risk: External retrieval guidance can expand prompt-injection or data-exfiltration exposure if adopted without controls.

Mitigation: Use domain allow-lists, human review for external retrieval, and auditing for external requests.

## Reference(s):

- [Advanced Documentation Patterns for AI Agents](references/advanced-patterns.md)
- [Agent Docs on ClawHub](https://clawhub.ai/tylervovan/skills/agent-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documentation should be reviewed before adoption in a project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
