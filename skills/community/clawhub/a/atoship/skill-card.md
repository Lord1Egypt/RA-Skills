## Description: <br>
Ship packages with AI — compare rates across USPS, FedEx, and UPS, buy discounted labels, track shipments, and manage orders. Requires user confirmation before any purchase or wallet-affecting action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atoship-dev](https://clawhub.ai/user/atoship-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External e-commerce sellers, small business operators, logistics coordinators, and developers use this skill to compare carrier rates, create shipping labels, track packages, validate addresses, and manage shipping orders through the Atoship API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make wallet-affecting API calls such as purchasing labels or voiding labels. <br>
Mitigation: Require explicit user confirmation after showing carrier, service, price, and full address details before any purchase or void request. <br>
Risk: Server security evidence says the skill treats remote order creation as read-only even though it changes remote state. <br>
Mitigation: Require explicit confirmation before creating orders or performing any other remote state-changing action. <br>
Risk: The Atoship API key authorizes shipping activity and wallet charges. <br>
Mitigation: Use a test key or small wallet balance while evaluating, keep the API key private, and rotate or revoke keys if exposure is suspected. <br>


## Reference(s): <br>
- [Atoship homepage](https://atoship.com) <br>
- [Atoship documentation](https://atoship.com/docs) <br>
- [Atoship API reference](https://atoship.com/docs/api) <br>
- [Atoship ClawHub listing](https://clawhub.ai/atoship-dev/atoship) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include carrier rates, tracking details, label links, account balance summaries, and order or shipment status returned from the Atoship API.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
