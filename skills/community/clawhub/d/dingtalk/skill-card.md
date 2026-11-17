## Description:

DingTalk channel plugin for OpenClaw - send and receive messages via DingTalk (钉钉).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chayjan](https://clawhub.ai/user/chayjan)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this channel plugin to connect agents to DingTalk for enterprise direct-message and group-chat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound DingTalk callbacks may be accepted without callback authentication.

Mitigation: Do not expose the callback endpoint until callback signature verification and sender or group allowlist enforcement are confirmed.

Risk: Webhook configuration may allow arbitrary webhook destinations.

Mitigation: Restrict webhook URLs to the official DingTalk robot endpoint and review webhook configuration before deployment.

Risk: DingTalk credentials can authorize message sending and organization access.

Mitigation: Use tightly scoped DingTalk credentials and store secrets in environment variables or protected secret storage.

## Reference(s):

- [ClawHub Dingtalk skill page](https://clawhub.ai/chayjan/skills/dingtalk)
- [DingTalk Open Platform](https://open.dingtalk.com)
- [DingTalk server API overview](https://open.dingtalk.com/document/isv/server-api-overview)
- [DingTalk group robot API](https://open.dingtalk.com/document/isv/group-robot)
- [DingTalk app types](https://open.dingtalk.com/document/isv/app-types)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [DingTalk text messages, OpenClaw channel configuration, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw >=2026.2.0 and DingTalk app or robot credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
