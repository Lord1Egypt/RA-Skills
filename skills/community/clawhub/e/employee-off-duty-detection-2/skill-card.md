## Description:

Intelligent workplace inspection system with guided setup, configurable inspection tasks, AI-powered image analysis, and Feishu alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsygcn](https://clawhub.ai/user/wsygcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workplace operations teams use this skill to configure camera-based inspections, analyze workplace images with a vision model, and send alerts for employee presence, security patrol, or facility inspection findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workplace camera monitoring can create legal, consent, and privacy risk for affected employees.

Mitigation: Install only with clear authority to monitor the covered workplace, and document required notice or consent before use.

Risk: Camera access tokens and device identifiers are sensitive credentials that may be stored in local configuration.

Mitigation: Store camera tokens in a secret manager where possible, restrict configuration file permissions, and rotate credentials if configuration is exposed.

Risk: Employee images and analysis results may be sent to external AI or alerting services.

Mitigation: Define image retention, external sharing, and alert-recipient policies before deployment, and limit cameras and recipients to the intended inspection scope.

Risk: Camera capture behavior relies on configured endpoints and capture tooling.

Mitigation: Use explicitly scoped camera devices and approved capture commands or APIs, and review endpoint configuration before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsygcn/skills/employee-off-duty-detection-2)
- [EZVIZ Cloud capture API endpoint](https://open.ys7.com/api/open/cloud/v1/capture/save)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Console text, JSON configuration, and alert message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include camera-derived images and AI analysis results in configured alerts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
