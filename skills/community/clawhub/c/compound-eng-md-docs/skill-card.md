## Description:

Manages project documentation files including CLAUDE.md, AGENTS.md, README.md, CONTRIBUTING.md, and DOCS.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or update project context and documentation files based on the repository's actual structure, commands, and conventions. It can also update an existing CONTRIBUTING.md or DOCS.md when asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says evaluation and diagnostic commands are described, but their implementation was not supplied.

Mitigation: Inspect those commands in the target repository and run only workflows that fit your intended use.

Risk: The release evidence reports one referenced path as missing.

Mitigation: Check referenced files in the target repository before following a workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-md-docs)
- [Context content and writing](references/context-content-and-writing.md)
- [Documentation workflows](references/documentation-workflows.md)
- [Initialize context files](references/init-agents.md)
- [Monorepo guidance](references/monorepo.md)
- [Update AGENTS.md](references/update-agents.md)
- [Update CONTRIBUTING.md](references/update-contributing.md)
- [Update README.md](references/update-readme.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [Markdown documentation files and concise change summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

5.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
