## Description:

Complex Task Orchestrator helps agents break down long, multi-step, batch, or failure-prone tasks into checkpointed execution strategies with recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwz119](https://clawhub.ai/user/xwz119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan, checkpoint, monitor, and recover complex tasks such as batch research, multi-step engineering work, large document operations, and sub-agent coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent task logging can capture secrets, customer data, document tokens, business plans, or sensitive file paths.

Mitigation: Keep workspace boundaries clear and avoid recording raw sensitive details in daily notes or checkpoints.

Risk: The checkpoint helper has an unvalidated file path risk when task IDs are not trusted.

Mitigation: Do not run the checkpoint helper with untrusted task IDs until path validation is fixed.

Risk: Orchestration proposals can introduce incorrect or misleading execution guidance.

Mitigation: Review the selected strategy and validate outputs before deploying or acting on results.

## Reference(s):

- [Common Task Orchestration Patterns](artifact/references/common-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/xwz119/skills/complex-task-orchestrator)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with examples, checklists, tables, JSON checkpoint shapes, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend persistent checkpoints and workspace logs for long-running tasks.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
