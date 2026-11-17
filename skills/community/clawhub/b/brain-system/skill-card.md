## Description:

人脑系统 is an agent workflow skill for long-term memory, task continuity, context checkpoints, reflection, and local self-maintenance without claiming consciousness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaxia01-1](https://clawhub.ai/user/xiaxia01-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add durable memory routines, task queues, checkpoints, recall, and post-task consolidation to long-running assistant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory and backup scripts can duplicate private workspace state.

Mitigation: Install only in workspaces where durable local memory is intended; review backup paths and prune sensitive files before running backup or consolidation scripts.

Risk: Recall and checkpoint scripts can expose private memory, tool notes, or cross-skill authority state in agent output.

Mitigation: Review scope before recall or checkpoint use and redact unrelated private state from generated notes.

Risk: Watcher behavior can automatically trigger checkpoint and consolidation when watched files change.

Mitigation: Run the watcher only when continuous local refresh is desired; disable or remove it in sensitive workspaces.

Risk: Status and fullness scripts inspect local workspace state and use shell process checks.

Mitigation: Review shell checks before use and run with the least necessary local permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaxia01-1/skills/brain-system)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local memory, checkpoint, queue, consolidation, and backup files under the agent workspace.]

## Skill Version(s):

0.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
