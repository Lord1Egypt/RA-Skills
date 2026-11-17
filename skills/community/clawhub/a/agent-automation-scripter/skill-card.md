## Description:

Imported specialist agent skill for automation scripter. Use when requests match this domain or role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nntrivi2001](https://clawhub.ai/user/nntrivi2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft and review bash or Python automation for recurring workflow tasks, including logging, error handling, idempotency, and scheduling with systemd timers or cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps create unattended local automation, including cron or systemd timer changes.

Mitigation: Require explicit approval before making scheduling changes, review generated scripts before scheduling them, and monitor the first automated run through logs.

Risk: The artifact points agents to a local automation-patterns template file outside the package.

Mitigation: Inspect any external local template file before allowing an agent to load or apply it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nntrivi2001/skills/agent-automation-scripter)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduling guidance, validation checklists, and debugging commands for unattended automation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
