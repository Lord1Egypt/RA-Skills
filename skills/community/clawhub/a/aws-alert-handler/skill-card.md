## Description: <br>
Normalize Security Hub ASFF, Inspector v2, and CloudWatch alarm JSON into a consistent shape, auto-unwrapping SNS and EventBridge envelopes when an AWS alert from any delivery path needs structured fields or before handoff to incident-triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggettert](https://clawhub.ai/user/ggettert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and operations teams use this skill to normalize AWS Security Hub, Inspector v2, and CloudWatch alarm payloads before triage, routing, or webhook-driven incident workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [AWS Alert Formats](references/alert-formats.md) <br>
- [Severity Mapping](references/severity-mapping.md) <br>
- [Webhook setup](references/webhook-setup.md) <br>
- [incident-triage Skill](https://clawhub.ai/ggettert/incident-triage) <br>
- [OpenClaw Gateway Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [Normalized JSON emitted by shell parser scripts, with Markdown guidance and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq; preserves the original alert payload in raw unless callers strip it before sharing.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
