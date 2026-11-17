## Description:

Multi-step scheduler for in-depth agent requests that detects when work needs multiple steps, proposes a user-approved plan, persists state, and runs a heartbeat-aware flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gostlightai](https://clawhub.ai/user/gostlightai)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to break complex requests into approved, ordered steps, persist execution state, and resume or retry work through heartbeat checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heartbeat checks can keep launching configured agent work after a plan is approved.

Mitigation: Require explicit plan approval, use a trusted STEP_AGENT_CMD, and review state before enabling heartbeat execution.

Risk: A user-controlled STEP_RUNNER path can redirect scheduler execution.

Mitigation: Leave STEP_RUNNER unset or set it only to a path you fully control.

Risk: Retries and resumed steps can repeat non-idempotent work.

Mitigation: Avoid purchases, public posting, destructive changes, and other non-idempotent steps until stronger concurrency controls are available.

## Reference(s):

- [Agent Step Sequencer ClawHub page](https://clawhub.ai/gostlightai/skills/agent-step-sequencer)
- [README](README.md)
- [State schema](references/state-schema.md)
- [Scripts README](scripts/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON state examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and STEP_AGENT_CMD; persists step progress in state.json.]

## Skill Version(s):

1.1.0 (source: server release metadata and changelog, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
