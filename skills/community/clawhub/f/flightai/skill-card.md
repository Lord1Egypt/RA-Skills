## Description: <br>
AI机票助手 - 实现国内航班搜索、舱位查询、预订下单、机票改期、机票退票。适用于用户询问航班、查询机票价格、提交机票订单、改期航班、退票时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search domestic flights, compare cabin prices and rules, create flight orders, query order details, cancel unpaid orders, and request ticket changes or refunds. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real flight orders, refunds, credentials, and passenger identity data. <br>
Mitigation: Use it only for intended flight booking workflows after confirming the user understands that identity data is sent to the configured external service. <br>
Risk: Security evidence reports unsafe transport and storage choices. <br>
Mitigation: Restore normal TLS verification and store credentials in a protected per-user location before real order use. <br>
Risk: Booking, cancellation, rescheduling, and refund actions can affect real travel or payments. <br>
Mitigation: Require explicit user confirmation before submitting any booking, cancellation, rescheduling, or refund request. <br>
Risk: Passenger PII may appear in outputs or logs. <br>
Mitigation: Mask passenger identity data in outputs and avoid logging personal information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryan-zry/flightai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with plaintext tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and authenticated access before flight booking, order, change, or refund operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
