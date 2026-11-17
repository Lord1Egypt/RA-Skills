## Description:

Real-time supervisor and control interface for the DRADIS prediction-market trading engine (Polymarket International, Polymarket US, and Kalshi). Full support for DRADIS_API_KEY authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbordash](https://clawhub.ai/user/mbordash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor DRADIS trading status, portfolio data, telemetry, logs, and pending LLM recommendations, and to make explicitly approved configuration changes for DRADIS instances they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring and configuration actions affect a DRADIS trading system where real money can be at risk.

Mitigation: Install only for a DRADIS instance the user controls, prefer read-only mode where appropriate, and require explicit human approval before any configuration change.

Risk: A DRADIS_API_KEY can authorize protected DRADIS routes.

Mitigation: Use a dedicated least-privilege API key and review every proposed configuration or LLM-action approval before accepting it.

Risk: Incorrect strategy configuration patches can appear successful if unknown keys are ignored.

Mitigation: Validate editable fields against the config schema and confirm the changed value from the response before reporting success.

## Reference(s):

- [DRADIS project repository](https://github.com/mbordash/DRADIS)
- [ClawHub skill listing](https://clawhub.ai/mbordash/skills/dradis-tactical-command)
- [Publisher profile](https://clawhub.ai/user/mbordash)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and concise text with JSON configuration fragments when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose and verify DRADIS configuration changes only after explicit human approval.]

## Skill Version(s):

1.5.1 (source: server release metadata and skill H1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
