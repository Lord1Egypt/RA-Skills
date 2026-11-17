## Description:

AI机票助手 - 实现国内航班搜索、舱位查询、预订下单、机票改期、机票退票。适用于用户询问航班、查询机票价格、提交机票订单、改期航班、退票时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to search domestic flights, compare seat prices and rules, create flight bookings, query orders, and submit cancellation, rescheduling, or refund requests. The skill requires mobile authentication and sends passenger information to an external flight service when booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles login tokens and passenger identity data with unsafe transport and storage controls.

Mitigation: Do not use with real passenger data or live bookings until TLS verification is restored and credentials are stored in a protected per-user secret store.

Risk: The skill calls an external flight service and depends on the configured API endpoint.

Mitigation: Fix or allowlist the API endpoint before deployment and review all outbound requests before installation.

Risk: Temporary booking and seat-selection state may expose sensitive travel data or affect subsequent order actions.

Mitigation: Protect or eliminate temporary state files and redact sensitive output before logs or responses are shared.

Risk: Cancellation, refund, and rescheduling actions can change real orders and fees.

Mitigation: Require explicit final confirmation tied to the exact order, passenger, action, and fees before executing those operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/ctrip-flight)
- [Fenbeitong flight skill API endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with plaintext tables, links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and stores temporary authentication and flight selection state on the local filesystem.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
