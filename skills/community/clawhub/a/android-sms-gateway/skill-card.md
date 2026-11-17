## Description:

Self-hosted SMS gateway support for sending, receiving, checking, and bulk-sending SMS through Android phone HTTP gateway apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nadjihamid](https://clawhub.ai/user/nadjihamid)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, operators, and security teams use this skill to route SMS workflows through an Android device they control, including alerts, received-message checks, webhook setup, and bulk notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send SMS, read received SMS, and use gateway credentials.

Mitigation: Install only when agent access to SMS functions and gateway credentials is acceptable; protect configuration files and credentials.

Risk: SMS traffic and webhooks may expose sensitive message content or metadata if sent over weak transport or public collectors.

Mitigation: Prefer HTTPS, VPN, or a private trusted network; avoid public webhook collectors for real SMS traffic.

Risk: Bulk sends can unintentionally contact multiple recipients.

Mitigation: Use dry-run before bulk sends and apply workflow-level limits before sending messages.

Risk: Test webhooks can remain active after validation.

Mitigation: Delete test webhooks after use.

## Reference(s):

- [SMS Gateway API Reference](references/api_reference.md)
- [capcom6/android-sms-gateway Quick Reference](references/capcom6_reference.md)
- [Android SMS Gateway ClawHub Page](https://clawhub.ai/nadjihamid/skills/android-sms-gateway)
- [SMS Gateway for Android Private Server Documentation](https://docs.sms-gate.app/getting-started/private-server/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke shell scripts that call Android SMS gateway HTTP APIs when the agent or user executes them.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
