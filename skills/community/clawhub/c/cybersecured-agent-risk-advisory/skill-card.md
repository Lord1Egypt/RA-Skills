## Description:

Guides AI agents through Cybersecured risk service setup, local security scanning, risk assessment submission, service application status checks, coverage review, and incident information submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cybersecured-cn](https://clawhub.ai/user/cybersecured-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agent owners use this skill to configure Cybersecured risk advisory services, collect local assessment materials, submit service applications, monitor coverage status, and prepare security incident reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can collect and transmit broad local security, configuration, skill, plugin, and environment information.

Mitigation: Inspect and redact the assessment directory before submission, and submit only information required for the service application.

Risk: The workflow documents test HTTP endpoints and certificate verification bypass for self-signed test environments.

Mitigation: Use trusted HTTPS endpoints for normal operation and avoid --no-verify-ssl outside isolated test environments.

Risk: The authentication flow uses API keys and warns against sending real keys to test endpoints.

Mitigation: Use production API keys only with trusted production endpoints, and rotate or revoke any key that may have been exposed.

Risk: Running the scan from cloud instances can expose metadata services or broad local agent configuration.

Mitigation: Avoid scanning from cloud instances with accessible metadata services, or restrict metadata and local configuration access before running the scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cybersecured-cn/skills/cybersecured-agent-risk-advisory)
- [Cybersecured AI service site](https://www.cybersecured.cn/ai)
- [Status handling guide](references/status-guide.md)
- [Risk factors collection format](references/risk-factors-format.md)
- [Questionnaire guide](references/questionnaire-guide.md)
- [Questionnaire JSON Schema](references/questionnaire-schema.json)
- [Data storage specification](references/data-storage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON assessment or questionnaire files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local CLI workflows for authentication, agent binding, scanning, assessment submission, service application, status review, coverage checks, and incident reporting.]

## Skill Version(s):

1.0.16 (source: evidence.json release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
