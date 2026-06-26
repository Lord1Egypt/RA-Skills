## Description: <br>
Creates gasless, non-custodial, oracle-protected crypto limit order payloads across 8 EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eranp-orbs](https://clawhub.ai/user/eranp-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn EVM swap intent into signed Spot order payloads, including parameter normalization, token and chain checks, approval guidance, relay submission, status polling, and cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet approvals and signed order submissions can affect real funds. <br>
Mitigation: Before signing or submitting, verify the chain, relay URL, contract or spender, token addresses and decimals, amount and maxAmount, recipient, slippage, deadline, recurrence settings, and cancellation path. <br>
Risk: Unlimited token approvals can expose more funds than a single order requires. <br>
Mitigation: Use the documented default approval for input.maxAmount; treat maxUint256 standing approval as an explicit repeat-use choice only. <br>
Risk: Changing the output recipient can route proceeds away from the swapper. <br>
Mitigation: Keep output.recipient equal to swapper unless the user explicitly requests and verifies a different recipient. <br>
Risk: Retrying after an ambiguous relay failure can create confusion if the original order was accepted. <br>
Mitigation: Persist the exact populated typedData and signature, query the relay for order status, and resolve the previous submission before rebuilding from fresh inputs. <br>


## Reference(s): <br>
- [Quickstart](references/quickstart.md) <br>
- [Params](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [RePermit Typed-Data Template](assets/repermit.template.json) <br>
- [Common Token Addressbook](assets/token-addressbook.md) <br>
- [Spot Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf) <br>
- [Spot Runtime Config](https://github.com/orbs-network/spot/blob/master/config.json) <br>
- [Relay Submit Endpoint](https://agents-sink.orbs.network/orders/new) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces locally populated order params, EIP-712 typed data, relay payloads, approval guidance, and lifecycle commands; signing or submitting orders can affect real funds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
