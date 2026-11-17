## Description:

Provides a standard OpenClaw gateway restart procedure with five validation gates, backup checks, self-termination avoidance, and continuationMessage restart receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangsuann](https://clawhub.ai/user/tangsuann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as a safety checklist for user-authorized OpenClaw gateway configuration validation and restart messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect OpenClaw configuration changes or premature restart authorization can interrupt gateway operation.

Mitigation: Review configuration changes, keep the required backup, complete the validation gates, and authorize restart only when gateway interruption is acceptable.

Risk: Running stop-and-start shell sequences from an active agent session can terminate the session before restart completes.

Mitigation: Use the platform-managed gateway restart path with a continuationMessage, or run a single restart command from outside the session and verify status afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangsuann/skills/gateway-restart-message)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes restart authorization conditions, validation gates, rollback guidance, and post-restart checks.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
