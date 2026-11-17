## Description:

Guides an agent through project-level ALab administration, including experiment coordination, project configuration, evidence review, and credential-separated worker handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bebetterest](https://clawhub.ai/user/bebetterest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate an existing ALab project with a project admin key while keeping project-level administration separate from experiment worker execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project admin credentials could be exposed through command arguments, logs, prompts, reports, or worker sessions.

Mitigation: Provide the project admin key only through a private environment variable or secure stdin, prefer --key-stdin, and withhold admin or root credentials from experiment workers.

Risk: Project lifecycle and cleanup commands can remove or alter experiments, sources, worktrees, validations, annotations, secrets, or configuration.

Mitigation: Review destructive operations before execution, run dry-run removal commands first, and require exact confirmation only after blockers and cleanup consequences are understood.

Risk: Worker sessions may operate with excessive authority or in the wrong filesystem context.

Mitigation: Launch workers in the specific experiment worktree, provide only the experiment worker instructions and non-secret helper variables, and clear unrelated admin, root, and ambient token variables.

## Reference(s):

- [commands.md](references/commands.md)
- [commands_cn.md](references/commands_cn.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes project-level summaries, command patterns, credential-handling guidance, worker handoff instructions, and risk-aware lifecycle recommendations.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
