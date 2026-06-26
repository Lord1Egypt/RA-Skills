## Description: <br>
Searches and books real flights across 500+ airlines with USDC payments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobuta23](https://clawhub.ai/user/kobuta23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to search flight availability, compare fares, create bookings, and guide USDC payment on Base after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles passenger personal data and sends booking data to Cabin and travel providers. <br>
Mitigation: Collect only required passenger details, confirm them with the user before booking, and disclose that booking data will be sent to Cabin and travel providers. <br>
Risk: The skill can lead an agent toward real USDC payments that may be irreversible. <br>
Mitigation: Require explicit user approval for each booking and payment, and verify fare, amount, Base deposit address, token, and network before any payment step. <br>
Risk: An agent with wallet capabilities could execute payment without sufficient user oversight. <br>
Mitigation: Do not grant unattended wallet authority; require human confirmation before wallet commands or checkout actions. <br>


## Reference(s): <br>
- [Cabin ClawHub listing](https://clawhub.ai/kobuta23/cabin) <br>
- [Cabin homepage](https://cabin.team) <br>
- [Cabin API](https://api.cabin.team) <br>
- [Clawdis homepage metadata](https://github.com/yolo-maxi/cabin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Shell commands, API calls] <br>
**Output Format:** [Markdown guidance with JSON request examples, curl commands, URLs, and structured booking details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rendered flight-result image URLs, booking references, USDC payment amounts, deposit addresses, checkout URLs, confirmation URLs, and check-in URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
