## Description:

Handles Feishu message construction, sending with retries, rate-limit detection, delivery diagnostics, and dead-letter queue management for geo alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to build and send Feishu notifications for geopolitical market alerts, then inspect delivery outcomes and retry or rate-limit handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardcoded default Feishu webhook can send messages to a fixed external destination when no configuration is supplied.

Mitigation: Remove or rotate the embedded webhook, require explicit webhook configuration, and limit outbound destinations to the intended Feishu endpoint before use.

Risk: Messages passed to the skill may be transmitted outside the user's environment through Feishu delivery.

Mitigation: Review and minimize message content before sending, and treat supplied alert text as externally transmitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liweijie0709-cmyk/skills/geo-push-ops)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Plain text Feishu messages, Python API objects, and Markdown/code guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send outbound HTTPS messages to Feishu when used with a webhook configuration.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
