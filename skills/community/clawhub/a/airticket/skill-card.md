## Description: <br>
AI机票助手 - 实现国内航班搜索、舱位查询、预订下单、机票改期、机票退票。适用于用户询问航班、查询机票价格、提交机票订单、改期航班、退票时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers or travel-support agents use this skill to search domestic flights in China, compare fares and cabin rules, and run booking, order lookup, cancellation, change, and refund workflows after user confirmation. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real booking, cancellation, change, and refund actions that may affect orders, payments, and travel plans. <br>
Mitigation: Require explicit user review of order number, passengers, dates, fees, and refund or change effects before approving any booking, cancellation, change, or refund command. <br>
Risk: Server evidence reports weak transport security and warns that the flight-service endpoint must be trusted. <br>
Mitigation: Install only if the publisher and service endpoint are trusted, confirm TLS verification is fixed, and verify FBT_API_URL is not redirecting requests before use. <br>
Risk: Server evidence reports insecure local credential storage, and the skill handles passenger PII and apiKey-based authentication. <br>
Mitigation: Avoid shared machines, do not expose personal data or credentials in logs or replies, and clear local authentication state when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release: AI机票预订助手](https://clawhub.ai/ryan-zry/airticket) <br>
- [Publisher profile: ryan-zry](https://clawhub.ai/user/ryan-zry) <br>
- [Configured flight service endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with plaintext tables, inline shell commands, and order or payment links when returned by the service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and stores temporary authentication and selected-seat state for follow-on commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, release evidence, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
