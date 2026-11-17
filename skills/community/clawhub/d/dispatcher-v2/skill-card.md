## Description:

OpenClaw 三层架构分离主调度员，纯调度不执行，所有工作派给子代理，独立验证通过才能汇报完成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovenini12344-code](https://clawhub.ai/user/lovenini12344-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route OpenClaw work through a dispatcher, delegated executors, and an independent verifier before reporting completion. It is intended for multi-agent workflows where task state, recovery, and verification gates are part of the operating process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly changes the agent's operating pattern by requiring dispatcher-led delegation and persistent task state.

Mitigation: Adopt it only for workflows that need multi-agent dispatch, and review whether its progress-file and synchronization expectations fit the local workspace.

Risk: Task context may be shared with reusable sub-agent sessions.

Mitigation: Use it in projects where delegated sessions are allowed to receive the task context, and avoid sensitive work unless session retention and scope are controlled.

Risk: Persistent memory and CURSOR_SYNC updates may write cross-session state.

Mitigation: Constrain writable locations and review or disable memory and CURSOR_SYNC updates before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovenini12344-code/skills/dispatcher-v2)
- [Publisher profile](https://clawhub.ai/user/lovenini12344-code)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with structured status updates and JSON spawn examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task plans, progress-state conventions, verification outcomes, recovery guidance, and delegation instructions for sub-agent sessions.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
