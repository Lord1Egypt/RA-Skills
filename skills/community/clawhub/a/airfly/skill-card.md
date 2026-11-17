## Description:

AI机票助手实现国内航班搜索、舱位查询、预订下单、机票改期和机票退票，适用于用户询问航班、查询机票价格、提交机票订单、改期航班或退票时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search domestic flights, compare seat and fare details, create flight orders, and manage order details, cancellations, changes, and refunds through an external flight service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials, passenger identity data, and ticket transactions with unsafe storage, logging, and network protections.

Mitigation: Review before real bookings; trust only approved flight service endpoints, redact passenger identity data from responses and logs, and store credentials and transaction files in user-private locations with restrictive permissions.

Risk: The scripts disable normal TLS certificate verification for API requests.

Mitigation: Enable normal TLS verification and restrict the API endpoint before production or real-booking use.

Risk: Refund and change operations can affect paid tickets and fees.

Mitigation: Require an explicit separate user confirmation after fee review before submitting refund or change applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/airfly)
- [Publisher profile](https://clawhub.ai/user/ryan-zry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with plaintext table code blocks, command invocations, order identifiers, and payment or order links when returned by the service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and phone verification before authenticated flight, booking, change, cancellation, or refund operations.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
