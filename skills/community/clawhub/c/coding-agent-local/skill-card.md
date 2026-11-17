## Description:

Delegate coding tasks to Codex, Claude Code, or Pi agents via background process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to delegate feature work, PR reviews, refactors, and iterative code changes to local CLI coding agents while selecting the appropriate execution mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to launch other coding agents with broad local authority.

Mitigation: Use sandboxed modes where possible, avoid --yolo and bypassPermissions unless explicitly authorized for a disposable or tightly scoped workspace, and review generated commands before running them.

Risk: The skill recommends high-privilege, low-oversight execution patterns that require careful installation review.

Mitigation: Review the skill before deployment and do not post GitHub comments, create PRs, push branches, or emit OpenClaw events without checking the generated content first.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are proposed for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
