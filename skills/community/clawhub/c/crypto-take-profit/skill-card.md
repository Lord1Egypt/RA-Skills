## Description: <br>
Automated crypto take-profit orders. Gasless, oracle-protected across 8 EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eranp-orbs](https://clawhub.ai/user/eranp-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn crypto trading intent into normalized EVM swap order parameters, EIP-712 typed data, signed relay payloads, and follow-up query or cancellation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide wallet approval, EIP-712 signing, and signed swap order submission to an external relay beyond simple take-profit orders. <br>
Mitigation: Use it only when the user intends to create crypto swap orders and can independently verify the order type, signed payload, and relay submission. <br>
Risk: Incorrect approval amount, chain ID, contract address, token address, recipient, deadline, nonce, or signature can create unintended crypto orders. <br>
Mitigation: Verify every approval amount, chain ID, contract address, token address, recipient, deadline, nonce, and signed payload before submission. <br>
Risk: Changing the output recipient away from the swapper can direct proceeds to a different address. <br>
Mitigation: Keep the recipient equal to the swapper unless the user explicitly requests and confirms a different recipient address. <br>


## Reference(s): <br>
- [Quickstart](references/quickstart.md) <br>
- [Params](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [Common Token Addressbook](assets/token-addressbook.md) <br>
- [RePermit Typed Data Template](assets/repermit.template.json) <br>
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf) <br>
- [Spot Configuration](https://github.com/orbs-network/spot/blob/master/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; produces local params, EIP-712 typed data, relay payloads, and lifecycle guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
