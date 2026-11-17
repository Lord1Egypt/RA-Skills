## Description:

Multi-Cursor orchestration for parallel task execution and AI council deliberation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to coordinate multiple Cursor agents through tmux for independent coding work, technical decision reviews, and synthesis of multi-model recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated agents may run with force-style approval and make unintended workspace changes.

Mitigation: Use disposable branches, worktrees, or sandboxes; remove force-style approval by default; and review agent prompts and proposed changes before accepting them.

Risk: Council prompts and outputs may contain sensitive project details when sent to external models.

Mitigation: Redact secrets and internal details before sharing prompts, and follow the project's data-handling rules for any generated logs.

Risk: Parallel agents may edit overlapping files or create merge conflicts.

Mitigation: Assign non-overlapping task boundaries, use separate branches where possible, and merge only after reviewing each session's output.

## Reference(s):

- [Cursor Council on ClawHub](https://clawhub.ai/xiaoyaner0201/skills/cursor-council)
- [Parallel Execution Guide](references/parallel-execution.md)
- [Council Deliberation Guide](references/council-deliberation.md)
- [Persona Engineering for AI Council](references/persona-engineering.md)
- [Session README Template](references/session-readme-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create tmux sessions and local council log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
