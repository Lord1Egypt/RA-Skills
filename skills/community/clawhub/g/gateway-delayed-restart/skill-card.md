## Description:

Delays an OpenClaw Gateway restart by a specified number of minutes and reports completion through OpenClaw messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanl754](https://clawhub.ai/user/hanl754)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to schedule an OpenClaw Gateway restart after a short delay, such as after browser failures, planned maintenance, or task completion. It can also send a completion notification through the configured OpenClaw messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can restart the OpenClaw Gateway, which may interrupt active work or running tasks.

Mitigation: Use it only when gateway restart authority is intended, notify affected users before execution, and add confirmation or cancellation controls for operational use.

Risk: The security evidence reports a hard-coded Feishu recipient in the notification path.

Mitigation: Remove the hard-coded recipient and require the notification target to be explicitly configured for each deployment.

Risk: The security evidence reports unsafe delay argument handling.

Mitigation: Validate the delay value before execution and restrict it to an acceptable numeric range.

## Reference(s):

- [OpenClaw Gateway Documentation](https://docs.openclaw.ai/gateway)
- [OpenClaw CLI Documentation](https://docs.openclaw.ai/cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown documentation with shell and Python examples; runtime output is terminal text and OpenClaw message notifications.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces delayed restart status, completion timing, process information, and optional Feishu notification text.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
