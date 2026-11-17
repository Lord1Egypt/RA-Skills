## Description:

Use when operating inside one ALab experiment worktree with that worktree token context to inspect status, edit candidate source, run evaluations, submit final results, and read visible experiment evidence without project admin or root privileges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bebetterest](https://clawhub.ai/user/bebetterest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and experiment workers use this skill to operate safely inside a single ALab experiment worktree: inspect visible evidence, make focused source edits, run evaluations, and submit supported results without project admin or root authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may operate in the wrong ALab worktree or token context.

Mitigation: Confirm the intended worktree and token context before submission-capable tasks, and use only the current worktree token surface.

Risk: The skill can edit task files, run evaluations, and submit final results.

Mitigation: Review final edits and runs before allowing autonomous experiment submission, especially when a passed run is required.

Risk: Visible artifacts, logs, or local files may contain sensitive material.

Mitigation: Inspect only task-relevant evidence and avoid reading, printing, copying, committing, or rewriting raw tokens, keys, hidden evaluator assets, or secret files.

## Reference(s):

- [ALab Experiment Worker Commands](references/commands.md)
- [ALab Experiment Worker Commands (Chinese)](references/commands_cn.md)
- [ClawHub Skill Page](https://clawhub.ai/bebetterest/skills/alab-experiment-worker)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and task-focused code or configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay scoped to the current ALab worktree token context and avoid raw tokens, hidden logs, secret files, and admin-only operations.]

## Skill Version(s):

0.1.9 (source: server release metadata, created 2026-06-20T10:52:10.841Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
