## Description:

Apollo Renal helps an agent filter noisy conversation context while preserving useful decisions, user preferences, active tasks, and open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor conversation context, estimate token load and information density, and decide when to prune or summarize noise while preserving important working memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect current conversation memory and related Dream state, then recommend or trigger context pruning with limited user control.

Mitigation: Use explicit confirmation before pruning or enabling heartbeat automation, and review filter reports before deleting or compressing retained context.

Risk: The checker can write persistent filter metrics about the workspace context state.

Mitigation: Install only in workspaces where persistent filter-state records are acceptable, and periodically review or clear .renal/filter-state.json according to local retention expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-renal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style context status report with optional JSON filter-state output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The checker can write persistent filter metrics to .renal/filter-state.json when run in an OpenClaw workspace.]

## Skill Version(s):

2.0.0 (source: release evidence, changelog, and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
