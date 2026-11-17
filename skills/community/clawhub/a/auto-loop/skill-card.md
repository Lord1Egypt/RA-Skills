## Description:

Auto Loop provides automated scheduling for timed, recurring, and one-off tasks with status tracking and failure recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to define scheduled jobs, recurring scripts, task retries, and status monitoring for routine work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring jobs, retries, and recovery can repeat task side effects such as file changes, API calls, messages, deletions, or spending actions.

Mitigation: Review each task before making it recurring, limit retries and concurrency for side-effecting work, and monitor failure records.

Risk: The scheduler persists local task state and execution metadata in the workspace.

Mitigation: Run it in an appropriate workspace and avoid putting sensitive data in task names, metadata, errors, or results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/auto-loop)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduling patterns, retry settings, task-management commands, and implementation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
