## Description:

Eli Prompt Guard scans outbound automated submissions for prompt injection attempts and sensitive data before allowing them to proceed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danlct27](https://clawhub.ai/user/danlct27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to guard automated posting, form submission, external API submission, and shared file-write workflows against prompt injection and sensitive-data leakage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated outbound submissions may be paused or rejected when prompt-injection or sensitive-data patterns match benign content.

Mitigation: Use the owner approve, reject, and review flow, tune platform severity settings, and keep the timeout configuration appropriate for the workflow.

Risk: Alert and logging workflows can expose sensitive submitted content if previews or logs are not handled carefully.

Mitigation: Redact sensitive data in notifications and prefer logging only suspicious submissions unless broader audit logging is explicitly required.

Risk: Disabling the guard or enabling optional file-write checks without review can reduce protection or expand the scope of blocked actions.

Mitigation: Restrict the /guardian disable path to owner or admin control and review configuration before enabling optional file-write checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danlct27/skills/eli-prompt-guard)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration JSON examples, and owner alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-submit checks can proceed, notify the owner, request approval, reject, or show sanitized content for review.]

## Skill Version(s):

2.0.0 (source: server release metadata and openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
