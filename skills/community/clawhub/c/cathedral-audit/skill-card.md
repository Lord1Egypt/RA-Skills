## Description:

Run a full spec-code audit on the Cathedral codebase, produce forward and reverse audit reports, prioritize fixes, and drive follow-up work through Claude Code sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hydroculator](https://clawhub.ai/user/hydroculator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to measure spec-code drift in a Cathedral C# codebase, identify missing or divergent implementation work, and convert audit findings into prioritized repair tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify repository files, run build commands, and create commits through delegated shell-enabled sessions.

Mitigation: Run it on a clean branch, review generated task briefings before execution, restrict delegated tools to the current task, inspect diffs, and commit only after successful build verification.

Risk: The workflow mentions an unspecified recurring cron monitor.

Mitigation: Prefer in-session monitoring; if a scheduled monitor is explicitly needed, define its scope, owner, and cleanup step before installing it.

Risk: The workflow uses /tmp/task.md for task handoff.

Mitigation: Use a secure per-run temporary file or a workspace-scoped task file with restrictive permissions instead of a predictable shared path.

Risk: A delegated session may be interrupted or killed before verification completes.

Mitigation: Check the diff, rerun dotnet build manually, log the incident, and resolve partial changes before committing.

## Reference(s):

- [CC Task Briefing Template](references/cc-task-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports, prioritized task briefings, shell commands, and repository changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces daily memory logs, audit files, build verification notes, and commit references when fixes are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
