## Description:

Async Command gives OpenClaw agents guidance for running long shell commands asynchronously, polling progress, and stopping background jobs when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guytogay](https://clawhub.ai/user/guytogay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide when to run long shell commands asynchronously, how to poll their progress, and how to stop them when interruption is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stopping a long-running command can interrupt migrations, installs, deployments, or data-processing jobs.

Mitigation: Before stopping a background command, consider whether interruption is safe and whether the operation needs cleanup, rollback, or a status check.

Risk: Forgetting a background job can waste resources or leave work incomplete.

Mitigation: Track session IDs and poll background jobs periodically until they complete or are intentionally stopped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guytogay/skills/async-command)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown with inline command and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code or generated files; output is instructional guidance for agent command workflow decisions.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
