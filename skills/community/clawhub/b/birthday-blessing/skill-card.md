## Description: <br>
Generates Chinese birthday blessing messages for a requested recipient or occasion after a paid order and payment-verification flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulian822](https://clawhub.ai/user/liulian822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can request short Chinese birthday wishes tailored to a relationship or celebration context. The skill is intended for paid greeting generation and requires order creation, payment handling, and payment verification before returning the blessing text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a paid workflow that handles payment credentials and configurable payee information. <br>
Mitigation: Install only when the paid birthday-blessing workflow and configured payee are expected, then verify the payment flow before use. <br>
Risk: The skill stores local order records and uses payment credentials during verification. <br>
Mitigation: Review where order files and payment credentials are stored, and confirm how they can be removed after use. <br>
Risk: The source instructions ask the agent to disclose internal reasoning. <br>
Mitigation: Remove or ignore the thought-process disclosure instruction before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liulian822/birthday-blessing) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese text with command-line workflow guidance and payment status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local order files and a payment credential before blessing generation completes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
