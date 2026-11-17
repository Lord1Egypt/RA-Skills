## Description:

Atlas Framework provides a structured AI-assisted development methodology using the GOTCHA 6-layer architecture and a 5-step application-building workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlowne12](https://clawhub.ai/user/marlowne12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and build applications, workflows, agentic systems, data systems, and external-service integrations with a structured design-first process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to read project memory and log files broadly, which may expose private historical notes, secrets, or unrelated context.

Mitigation: Use only in workspaces where project-local memory is intended, and add consent, scoping, and deletion controls before enabling broad memory reads.

Risk: The skill can guide automatic creation of persistent memory folders and SQLite databases.

Mitigation: Review the generated file and database locations before use, and keep persistence limited to the intended project workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marlowne12/skills/atlas-framework)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, architecture notes, file-structure conventions, and command or configuration suggestions when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of project-local memory files, logs, folders, and SQLite databases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
