## Description:

Provides a queue-based controller for agent spawning with fail-closed concurrency defaults, permission logging, and serialized execution for tasks that are not explicitly marked concurrency-safe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suda6632](https://clawhub.ai/user/suda6632)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route sub-agent work through a priority queue, reduce session conflicts, and log sensitive or critical operations before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval gate and plaintext result storage are weak enough to warrant review before installation.

Mitigation: Treat the skill as a queue and logging helper, and keep an independent trusted approval layer for payments, public posting, external sends, file overwrites, and configuration changes.

Risk: Completion results can include sensitive data that may be stored in plaintext under the OpenClaw workspace.

Mitigation: Do not pass secrets or full agent outputs into completion results; redact or summarize sensitive data before calling completion handlers.

Risk: Critical operations are returned as pending confirmation rather than being fully authorized by this controller.

Mitigation: Require separate human or policy confirmation before executing critical actions after a PENDING_CONFIRMATION result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suda6632/skills/agent-concurrency-controller)
- [Publisher profile](https://clawhub.ai/user/suda6632)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/agent_concurrency_controller.py](artifact/agent_concurrency_controller.py)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python API examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces queue status strings such as QUEUED, STARTED, DENIED, and PENDING_CONFIRMATION; writes local JSONL audit logs and JSON queue state when used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
