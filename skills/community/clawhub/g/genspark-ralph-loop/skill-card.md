## Description:

Genspark Ralph Loop helps Genspark Claw implement PRD tasks one at a time, verify results, record progress, and resume interrupted development work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sueelly](https://clawhub.ai/user/sueelly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in Genspark Claw to execute PRD task lists sequentially, validate each task, retry failures, and resume interrupted development work from recorded state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify project code, PRD checkboxes, and .ralph-claw tracking files.

Mitigation: Install it only for projects where agent edits are acceptable, and review changes before committing, pushing, deploying, or using them on sensitive repositories.

Risk: The skill may run local verification commands as part of task validation.

Mitigation: Use it in trusted workspaces and review command results before treating a task as complete.

Risk: The skill may spawn Genspark child sessions, and provider limits or account credit issues can interrupt completion.

Mitigation: Set clear iteration limits, preserve checkpoint files, and confirm existing child-session status before retrying interrupted work.

## Reference(s):

- [Genspark local runtime connection](references/genspark-local-runtime.md)
- [ClawHub skill page](https://clawhub.ai/sueelly/skills/genspark-ralph-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, JSON state files, code changes, shell command summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update PRD checkboxes and .ralph-claw tracking files in the target project after verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
