## Description:

Safely update OpenClaw gateway configuration (openclaw.json) with automatic validation, backup, and 30-second health-check rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allthebadthings](https://clawhub.ai/user/allthebadthings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to modify OpenClaw gateway settings, ports, provider credentials, and network bindings with validation, backup, health checking, and rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls sensitive OpenClaw gateway configuration and could disrupt access if applied incorrectly.

Mitigation: Review the proposed configuration change before execution and confirm rollback state is recoverable.

Risk: Security evidence reports material safety and command-injection weaknesses in the safety script.

Mitigation: Harden the script by validating numeric inputs, checking each copy and restart result, enforcing GATEWAY_LOCKOUT, and documenting who can clear lockout state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allthebadthings/skills/gateway-safety)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human review before applying sensitive gateway configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
