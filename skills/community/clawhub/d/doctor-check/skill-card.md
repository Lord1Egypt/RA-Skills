## Description:

Doctor Check provides Chinese-language system diagnostics for checking OpenClaw and runtime environment health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soroyue](https://clawhub.ai/user/soroyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run doctor-style checks of local environment, service status, configuration, and logs when diagnosing OpenClaw runtime health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output may include sensitive details from local configuration, service status, permissions, API-key validity checks, or logs.

Mitigation: Review diagnostic output before sharing it and invoke the skill explicitly when those local checks are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soroyue/skills/doctor-check)
- [Publisher profile](https://clawhub.ai/user/soroyue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports normal, warning, and problem findings for environment, service, configuration, and log checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
