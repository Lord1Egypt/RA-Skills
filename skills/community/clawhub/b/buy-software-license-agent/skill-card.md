## Description: <br>
Agent buys SaaS or software licenses on the user's behalf using a CAI custodial wallet after the user confirms the payee and amount. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to purchase or renew SaaS and software licenses through CAI after confirming the vendor, payee, amount, chain, and token. It is intended for agent-assisted license payment workflows that require a CAI API key and explicit user confirmation before transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports CAI-backed license payments and wallet use. <br>
Mitigation: Install only for expected payment workflows and approve transfers only after independently verifying the vendor, invoice, payee address, amount, chain, and token. <br>
Risk: The skill requires a sensitive CAI_API_KEY. <br>
Mitigation: Keep the API key as narrowly scoped as CAI allows and avoid broader pay or full scope unless the workflow requires it. <br>
Risk: Incorrect or spoofed billing details could lead to payment to the wrong recipient. <br>
Mitigation: Require explicit user confirmation and proceed only when payment details are specific, expected, and independently checked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernardtai/buy-software-license-agent) <br>
- [CAI skill reference](https://cai.com/skill.md) <br>
- [CAI agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md) <br>
- [CAI developer documentation](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and ordered task steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY with pay or full scope; payment transfer is described only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
