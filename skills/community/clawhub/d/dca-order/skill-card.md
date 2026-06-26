## Description: <br>
DCA orders for crypto. Split buys over time, gasless, oracle-protected, 8 EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eranp-orbs](https://clawhub.ai/user/eranp-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate wallet intent into normalized DCA order parameters, EIP-712 typed data, approval guidance, a signed relay payload, and follow-up query or cancellation steps for supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags the release as suspicious because its documentation may cover broader crypto order-building behavior than the stated DCA scope. <br>
Mitigation: Review supported order types before use, keep the workflow scoped to the user's requested DCA behavior, and use demo or test mode before handling real funds. <br>
Risk: The skill requires wallet signing and can produce payloads that affect crypto assets. <br>
Mitigation: Require explicit user confirmation before live submission and validate every address, amount, chain, timing value, approval, and signature. <br>
Risk: The helper token addressbook is a convenience list and may not cover every token or user-provided address. <br>
Mitigation: Treat explicit user-provided addresses as authoritative and verify token decimals or addresses onchain when uncertain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eranp-orbs/dca-order) <br>
- [Quickstart](references/quickstart.md) <br>
- [Parameters](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [Common Token Addressbook](assets/token-addressbook.md) <br>
- [RePermit typed-data template](assets/repermit.template.json) <br>
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces order-building guidance and payloads; live submission requires user wallet signing and explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
