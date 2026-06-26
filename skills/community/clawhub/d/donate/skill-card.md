## Description: <br>
Detects a user's donation, tipping, reward, or gift intent; collects and validates the amount; confirms with the user; then calls a payment skill to create the payment flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sayxxx](https://clawhub.ai/user/sayxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External assistants can use this skill to handle donation or tipping flows by collecting a positive amount, enforcing the single-payment limit, confirming user intent, and passing the request to a payment skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real payment creation while ignoring recipient information from the user's message. <br>
Mitigation: Install only where the payment skill, recipient, and merchant identity are verified, and show the recipient or merchant identity to the user before any payment link is opened. <br>
Risk: Users may be asked to open or copy payment links returned from another skill. <br>
Mitigation: Review the payment skill integration and payment-link domain before deployment, and require user confirmation before handing off to payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sayxxx/donate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Conversational text or Markdown prompts, plus a payment-skill call with amount, order_type, and description parameters.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects an amount, confirms with the user, relays payment results, and does not collect a recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
