## Description:

Normalize Security Hub ASFF, Inspector v2, and CloudWatch alarm JSON into a consistent shape, including SNS and EventBridge envelope handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggettert](https://clawhub.ai/user/ggettert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to normalize AWS Security Hub, Inspector v2, and CloudWatch alert payloads before incident triage, webhook routing, or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook-delivered alerts can be spoofed if SNS signatures and expected topic, account, or region are not verified before agent invocation.

Mitigation: Use a Lambda, EventBridge connection, or trusted proxy that verifies SNS signatures and expected source metadata before forwarding alerts.

Risk: Raw alert payloads may contain sensitive data and are preserved in parser output.

Mitigation: Strip the raw field before posting normalized alerts to visible channels or external systems.

Risk: Multi-finding Security Hub or Inspector batches may result in only the first finding being emitted.

Mitigation: Split or reject multi-finding batches upstream before invoking the parser.

Risk: CloudWatch skip patterns can silently drop alerts that match routine-alarm filters.

Mitigation: Review and tighten or disable skip patterns for production accounts where matching alarms may represent incidents.

Risk: Passing raw alert text directly into an agent can introduce prompt-injection content from alert fields.

Mitigation: Treat alert payloads as data, avoid using raw fields as instructions, and pass structured normalized fields to downstream workflows.

## Reference(s):

- [AWS Alert Formats](references/alert-formats.md)
- [Severity Mapping](references/severity-mapping.md)
- [Webhook Setup](references/webhook-setup.md)
- [incident-triage Skill](https://clawhub.ai/ggettert/incident-triage)
- [OpenClaw Gateway Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from parser scripts, with Markdown guidance and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser output preserves the original alert payload in raw unless callers strip it before sharing.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
