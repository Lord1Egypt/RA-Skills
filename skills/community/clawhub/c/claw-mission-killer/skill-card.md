## Description:

Interrupt a running OpenClaw agent task, terminate the target agent process, and roll back its session transcript to the state before the last triggering user message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorianyoung7702](https://clawhub.ai/user/dorianyoung7702)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an OpenClaw agent is stuck, running the wrong task, or needs to be redirected. It provides commands and helper scripts to target one agent or all non-main agents, stop running work, back up removed transcript entries, and restore the agent to standby.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad process-killing behavior can stop the wrong process when markers, workspace matching, or agent targeting are incorrect.

Mitigation: Use dry-run and single-agent targeting before broad interruption, prefer the run.py marker workflow for precise process targeting, and verify the resolved agent before execution.

Risk: Install and watcher scripts can persistently append protocol text to AGENTS.md files and alter future agent behavior.

Mitigation: Avoid watcher or cron automation unless persistent AGENTS.md changes are acceptable, review affected files after install, and use dry-run or specific-agent installation where possible.

Risk: Transcript rollback removes the last user message and later entries, which can discard useful session state if the target is wrong.

Mitigation: Keep separate backups, inspect rollback files in interrupt-logs before relying on the edited transcript, and restore backed-up lines when the rollback removed needed context.

## Reference(s):

- [agent-interrupt: AGENTS.md integration rules](references/agents-md-integration.md)
- [ClawHub skill page](https://clawhub.ai/dorianyoung7702/skills/claw-mission-killer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local process-control commands, OpenClaw AGENTS.md integration guidance, running-process marker files, and rollback backup files.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
