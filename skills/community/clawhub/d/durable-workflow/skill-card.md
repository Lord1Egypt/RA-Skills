## Description:

Provides patterns and JavaScript helpers for building multi-step agent workflows with checkpoints, retries, timeouts, dead letter handling, alerting, and single-instance locks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[old-greggyboy](https://clawhub.ai/user/old-greggyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design resilient automations, pipelines, and agent loops that can resume after failures, avoid duplicate work, and surface failed items for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled workflow scripts include file-locking and temporary-file weaknesses that may matter for business-critical or non-idempotent workflows.

Mitigation: Review and harden lock and temporary-file creation before deployment, and keep state and lock files in a private directory.

Risk: Workflow state, dead letter, and lock files can expose operational data if stored in shared or predictable locations.

Mitigation: Configure state, dead letter, and lock paths to private directories with restrictive permissions.

Risk: Failure alerts can expose raw exception details to Telegram or another external alert channel.

Mitigation: Sanitize alert messages and avoid sending secrets, raw exception text, or sensitive workflow data to external channels.

## Reference(s):

- [Agent Workflow Failure Taxonomy](references/failure-taxonomy.md)
- [ClawHub skill page](https://clawhub.ai/old-greggyboy/skills/durable-workflow)
- [ClawHub publisher profile](https://clawhub.ai/user/old-greggyboy)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable workflow and lock scripts for adaptation by the agent.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
