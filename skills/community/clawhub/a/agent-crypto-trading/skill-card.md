## Description: <br>
AI agent crypto trading. Gasless limit, DCA, stop-loss & take-profit across 8 EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eranp-orbs](https://clawhub.ai/user/eranp-orbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert crypto trading intent into normalized order parameters, typed-data signing steps, relay payloads, status queries, and cancellation guidance for supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through token approvals, wallet signatures, relay submissions, and cancellations that may affect real funds. <br>
Mitigation: Require explicit user approval before any approval transaction, wallet signature, relay submission, or cancellation, and test with small amounts first. <br>
Risk: Incorrect chain IDs, token addresses, recipients, amounts, deadlines, slippage settings, or relay endpoints can create unintended orders. <br>
Mitigation: Verify each chain ID, token address, recipient, amount, deadline, slippage value, and relay endpoint before signing or submitting. <br>
Risk: Typed data, signatures, and saved relay payloads authorize trading actions and can be sensitive. <br>
Mitigation: Store and transmit typed data, signatures, and relay payloads carefully, reuse exact payloads only for resolving ambiguous submissions, and avoid unlimited approvals unless intentionally chosen. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eranp-orbs/agent-crypto-trading) <br>
- [Quickstart](references/quickstart.md) <br>
- [Parameters](references/params.md) <br>
- [Template, Sign, And Submit](references/sign.md) <br>
- [Lifecycle](references/lifecycle.md) <br>
- [Examples](references/examples.md) <br>
- [Token Addressbook](assets/token-addressbook.md) <br>
- [RePermit typed-data template](assets/repermit.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; generated order details, typed data, signatures, relay payloads, and cancellation data should be treated as sensitive authorization material.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
