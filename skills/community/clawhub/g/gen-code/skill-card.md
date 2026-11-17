## Description:

Gen Code helps agents generate project code from tasks, design documents, contracts, and coding standards, with support for new projects and context-aware changes in existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lf951515851](https://clawhub.ai/user/lf951515851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate or update application code from task IDs, design documents, or contract and specification files. It is suited to workflows that need repository-aware code generation, scaffolding, task-status updates, and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read project documentation and source files and write substantial repository changes.

Mitigation: Use explicit /gen-code commands and review planned and generated file changes before accepting auto or scaffold modes.

Risk: Generated scaffolding may include database configuration placeholders, including development password templates.

Mitigation: Replace plaintext database password templates with environment variables or local-only secret handling before use.

Risk: Generated code may still contain functional, security, or integration mistakes despite built-in quality checks.

Mitigation: Run project tests and perform code review before deploying generated changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lf951515851/skills/gen-code)
- [Publisher profile](https://clawhub.ai/user/lf951515851)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, file lists, generated source files, configuration snippets, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write substantial repository changes, including frontend and backend scaffolding, source code, tests, configuration files, and task status updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
