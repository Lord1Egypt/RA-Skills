## Description: <br>
AI机票预订助手 helps agents search domestic flights, compare cabin prices and rules, create flight bookings, and manage order details, changes, cancellations, and refunds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers or travel-assisting agents use this skill to search Chinese domestic flights, review fares and change/refund rules, create bookings, and manage cancellations, changes, and refunds after mobile verification. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit bookings, cancellations, changes, and refunds for real flight orders. <br>
Mitigation: Require explicit confirmation immediately before every order-affecting command and restate the relevant flight, order, and fee details. <br>
Risk: The skill handles passenger names, phone numbers, ID numbers, order IDs, ticket IDs, and an API key. <br>
Mitigation: Mask PII in agent responses and logs, avoid storing auth keys in temporary storage, and rotate or re-authenticate if secrets may have been exposed. <br>
Risk: The security guidance reports unsafe transport behavior. <br>
Mitigation: Restore normal HTTPS certificate verification before production deployment. <br>
Risk: Raw debug or order-detail output can expose sensitive passenger or order data. <br>
Mitigation: Remove raw debug prints and review displayed fields so only necessary, masked information is shown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/ctrip-flight) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ryan-zry) <br>
- [Fenbeitong flight API endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plaintext tables from Python script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and authenticated flight API access; order-affecting actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, artifact metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
