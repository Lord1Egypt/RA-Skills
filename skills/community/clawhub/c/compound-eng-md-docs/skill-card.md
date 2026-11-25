## Description:

Updates or creates project context and documentation files after checking their claims against the codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or update project context and documentation files, including AGENTS.md, CLAUDE.md, README.md, CONTRIBUTING.md, and existing DOCS.md, with content checked against repository files and commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some evaluation and diagnostic commands may not fit a target repository, and scanner confidence is medium because some references could not be resolved and command implementations were unavailable for assessment.

Mitigation: Review unresolved references and inspect the relevant commands in the target repository before running them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/iliaal/skills/compound-eng-md-docs)
- [SKILL.md](artifact/SKILL.md)
- [Documentation workflows](artifact/references/documentation-workflows.md)
- [Context content and writing](artifact/references/context-content-and-writing.md)
- [Initialize context workflow](artifact/references/init-agents.md)
- [Monorepo handling](artifact/references/monorepo.md)
- [Update context files workflow](artifact/references/update-agents.md)
- [Update CONTRIBUTING workflow](artifact/references/update-contributing.md)
- [Update README workflow](artifact/references/update-readme.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown documentation and concise command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project documentation within each workflow's stated limits.]

## Skill Version(s):

5.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
