## Description:

The orchestration tool for OpenClaw, managing and coordinating all your skills seamlessly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okoddcat](https://clawhub.ai/user/okoddcat)

### License/Terms of Use:


## Use Case:

Developers and operators use ClawOps to coordinate installed OpenClaw skills, resolve dependencies, schedule multi-skill actions, and monitor workflow health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad coordination over installed skills and secrets without clear access boundaries.

Mitigation: Require explicit allowlists for controlled skills, permitted triggers, and actions before using it with real workflows.

Risk: Centralized monitoring and logging can expose sensitive workflow or secret-handling details.

Mitigation: Define secret storage and reference rules, and require log redaction for sensitive values.

Risk: Automated dependency resolution and multi-skill scheduling can trigger unintended actions.

Mitigation: Use review or approval gates for scheduled actions until workflow behavior is verified.

## Reference(s):

- [ClawOps ClawHub listing](https://clawhub.ai/okoddcat/skills/clawops)
- [okoddcat publisher profile](https://clawhub.ai/user/okoddcat)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown or plain text instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
