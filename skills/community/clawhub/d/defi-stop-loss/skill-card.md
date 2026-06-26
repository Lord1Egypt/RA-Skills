## Description: <br>
Decentralized stop-loss orders for DeFi. Gasless, oracle-protected, 8 EVM chains supported. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eranp-orbs](https://clawhub.ai/user/eranp-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi agents use this skill to convert user intent into normalized Spot order parameters, EIP-712 typed data, approval guidance, signed relay payloads, and query or cancellation steps for supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The stop-loss listing understates that the skill can guide broader signed trading orders, including market, limit, TWAP, take-profit, delayed-start, and chunked orders through an external relay. <br>
Mitigation: Confirm the intended order type before signing and review the normalized order fields against the user's request. <br>
Risk: Incorrect approvals or signatures can authorize unintended token spending or submit an unintended DeFi order. <br>
Mitigation: Before approving or signing, verify the chain, contract, token addresses, recipient, amount, deadline, trigger values, slippage, and relay destination. <br>
Risk: Standing max approvals increase exposure for repeat use. <br>
Mitigation: Prefer exact approvals for input.maxAmount and use maxUint256 approvals only when the user deliberately accepts that exposure. <br>
Risk: Native input is not supported by the skill workflow. <br>
Mitigation: Use ERC-20 input tokens or wrap native assets before creating an order. <br>


## Reference(s): <br>
- [Quickstart](references/quickstart.md) <br>
- [Params](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [Common Token Addressbook](assets/token-addressbook.md) <br>
- [RePermit typed-data template](assets/repermit.template.json) <br>
- [Spot security audit report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf) <br>
- [Spot supported chain config](https://github.com/orbs-network/spot/blob/master/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, EIP-712 typed-data configuration, shell commands, and JavaScript examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local normalized params, approval guidance, signed relay payloads, status queries, and cancellation commands; wallet signing is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
