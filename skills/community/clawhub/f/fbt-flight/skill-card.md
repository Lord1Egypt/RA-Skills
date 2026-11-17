## Description:

分贝通机票助手帮助代理通过分贝通机票服务完成国内航班搜索、舱位价格查询、订单创建、订单查询、取消订单、改期和退票流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents and assistants use this skill to search Chinese domestic flights, compare seat pricing and rules, and carry out booking, cancellation, rescheduling, and refund workflows after user authentication and confirmation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles real flight booking, cancellation, change, and refund operations.

Mitigation: Require explicit user confirmation before any transaction-changing action, including booking, cancellation, rescheduling, and refund submission.

Risk: Passenger identity data, phone numbers, order details, and authentication tokens may be exposed through output or local storage.

Mitigation: Do not use production accounts or real passenger identity data until sensitive output is redacted and credentials are stored in a protected per-user secret location.

Risk: Network and endpoint handling are called out by the security evidence as unsafe.

Mitigation: Restore TLS certificate verification and constrain endpoint overrides before operational use.

Risk: Temporary transaction files can retain seat or change workflow state.

Mitigation: Secure or remove temporary transaction files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/fbt-flight)
- [Publisher profile](https://clawhub.ai/user/ryan-zry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and plaintext tables with inline shell commands, order identifiers, prices, and payment or detail links when returned by the service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and authenticated access to the Fenbeitong flight service; flight, price, passenger, order, cancellation, change, and refund results are displayed from script output.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
