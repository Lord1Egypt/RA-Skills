## Description:

Use when managing tasks with the agkan CLI tool - creating, listing, updating tasks, managing tags, blocking relationships, or tracking project progress with the kanban board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gendosu](https://clawhub.ai/user/gendosu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage project tasks with the agkan CLI, including task status, tags, blocking relationships, metadata, and kanban-style progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can delete local agkan tasks when following documented delete commands.

Mitigation: Prefer closing tasks for a reversible record and reserve deletion for cases where permanent removal is intended.

Risk: Task and metadata updates can alter local project tracking state.

Mitigation: Review planned agkan commands before execution and confirm the target task identifiers.

## Reference(s):

- [Agkan skill page](https://clawhub.ai/gendosu/skills/agkan)
- [gendosu publisher profile](https://clawhub.ai/user/gendosu)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, YAML configuration, and JSON schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include agkan CLI command examples and JSON output schema guidance.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
