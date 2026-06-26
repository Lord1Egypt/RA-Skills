## Description: <br>
分贝通机票助手实现国内航班搜索、舱位查询、预订下单、机票改期和机票退票。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel coordinators use this skill to search domestic flights, compare seat pricing, create flight orders, inspect order details, and submit cancellation, change, or refund requests through Fenbeitong flight services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles credentials, passenger identity data, order records, bookings, changes, and refunds. <br>
Mitigation: Use only in a trusted local environment, avoid logging or echoing passenger and order data, and require explicit user confirmation before booking, cancelling, changing, or refunding tickets. <br>
Risk: Server security evidence reports weak transport and privacy safeguards, including a TLS verification bypass. <br>
Mitigation: Fix TLS certificate verification before using the skill with real accounts or sensitive travel data. <br>
Risk: Command output can include passenger and order data. <br>
Mitigation: Treat command output as sensitive and redact passenger phone numbers, identity numbers, API keys, and order details from logs and shared transcripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryan-zry/fbt-flight) <br>
- [Fenbeitong Flight Skill API Endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with plaintext tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, phone-based authentication, and user-supplied trip, passenger, order, and confirmation details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
