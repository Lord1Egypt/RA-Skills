## Description:

Monitors Frigate NVR MQTT events and sends real-time WhatsApp and email alerts with camera snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rupertcachandler](https://clawhub.ai/user/rupertcachandler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and home or facility operators use this skill to connect Frigate camera detections to outbound WhatsApp and email notifications with snapshots and rate limiting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The notifier handles camera images, outbound messages, and a long-running MQTT listener with under-scoped security controls.

Mitigation: Deploy only with authenticated TLS MQTT, broker ACLs, HTTPS for Frigate, and a dedicated unprivileged service account.

Risk: The notifier relies on local SMTP and notification credentials.

Mitigation: Store secrets in an owner-only config file or a secret store, and use SMTP TLS with app-specific credentials.

Risk: Snapshot attachments are created from event data and temporary files.

Mitigation: Validate event IDs and use safe temporary-file handling before enabling attachments or background operation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rupertcachandler/skills/frigate-notifier)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON configuration examples and Python scripts; runtime alerts are text messages with optional image attachments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration for MQTT, Frigate, WhatsApp, SMTP, cooldown, and notification limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
