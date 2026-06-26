## Description: <br>
Gate Pay payment execution skill for completing merchant charges through Gate Pay when the user has selected Gate Pay, provided complete payment details, and completed payment authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to complete prepared Gate Pay merchant order charges, including pay-first flows such as HTTP 402, after verifying payment intent, order details, and Gate Pay authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute irreversible Gate Pay charges. <br>
Mitigation: Use only for trusted merchant orders and verify the exact order ID, amount, currency, merchant context, selected Gate Pay method, and Gate Pay account before allowing payment. <br>
Risk: Broad activation language could route payment requests too aggressively. <br>
Mitigation: Require clear user payment intent in the current or immediately previous user turn and block execution when intent, authorization, or required payment fields are missing. <br>
Risk: The package references mutable external Gate runtime rules that are not pinned inside the package. <br>
Mitigation: Review the referenced runtime rules before installation and before payment execution in sensitive environments. <br>
Risk: Duplicate payment attempts can occur if a status check is mistaken for a new charge request. <br>
Mitigation: Do not charge the same order twice in the conversation context; if no status query tool is available, explain the limitation instead of charging again. <br>


## Reference(s): <br>
- [Gate Pay MCP Specification](references/mcp.md) <br>
- [Gate Pay Payment Scenarios](references/scenarios.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-exchange-pay) <br>
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [Exchange Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Localized Markdown receipts, planned-charge summaries, and failure guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Gate Pay MCP charge tool after explicit payment intent, complete order details, and valid Gate Pay authorization are verified.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
