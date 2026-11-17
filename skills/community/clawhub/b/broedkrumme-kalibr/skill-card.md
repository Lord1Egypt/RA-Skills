## Description:

Captures agent outcomes and LLM telemetry for continuous self-improvement and optional intelligent model routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:

ISC

## Use Case:

Developers and agent operators use this plugin to record agent run outcomes and LLM usage data for Kalibr-backed analysis. They can optionally allow Kalibr to influence model routing for agent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telemetry and outcome capture can send session identifiers, tool history, token counts, and failure metadata to the configured Kalibr service.

Mitigation: Use only a trusted Kalibr endpoint and disable captureOutcomes or captureLlmTelemetry unless organizational policy permits sending that data.

Risk: When routing is enabled, the external service can influence model selection and tool-call parameters.

Mitigation: Keep enableRouting disabled unless that behavior is explicitly desired and review any routed model or parameter changes in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/broedkrummen/skills/broedkrumme-kalibr)

## Skill Output:

**Output Type(s):** [text, configuration, API calls]

**Output Format:** [Plain text status output, structured status responses, and SDK-mediated telemetry or outcome reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May override model and provider selection, and may merge service-provided tool parameters, when routing is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
