## Description: <br>
AI机票预订助手 helps agents search domestic flights, query fares and rules, create flight orders, manage order details, change flights, and request refunds through Python command-line API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search flights, compare fare details, create bookings, inspect orders, and submit change or refund requests after user confirmation. The skill requires phone-based authentication and handles passenger identity data for booking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles passenger identity data, phone numbers, login tokens, and refund actions. <br>
Mitigation: Use only after trusting the flight service, obtain explicit user confirmation for booking, change, and refund actions, and avoid exposing passenger data in logs or responses. <br>
Risk: The security summary reports unsafe transport and credential-storage practices. <br>
Mitigation: Do not use for booking, changing, or refunding tickets until TLS verification is enabled and credentials are stored in a protected location. <br>
Risk: Refund and change workflows can affect real tickets and payments. <br>
Mitigation: Confirm the exact order, ticket, passenger, fee, and action with the user before submitting any change or refund request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/ai-flight) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ryan-zry) <br>
- [AI flight service API endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with plaintext tables and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include flight tables, fare details, order identifiers, payment links, authentication status, and change or refund results.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
