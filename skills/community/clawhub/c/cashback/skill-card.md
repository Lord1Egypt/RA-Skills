## Description: <br>
Cashback helps users generate affiliate cashback links, check rebate rates for supported overseas merchants, and review personal cashback orders through the feima-lab affiliate API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn supported Adidas, Space NK NL, and designwebstore DE shopping links into cashback links, query merchant rebate rates, and check recent cashback order status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsupported merchant links, shopping queries, and order-related data may be sent to an external affiliate API. <br>
Mitigation: Use the skill only for supported merchants, avoid sending sensitive shopping or order details unless comfortable sharing them with the provider, and review outputs before relying on cashback status. <br>
Risk: The skill requires a sensitive FX_AI_API_KEY credential and a separate fx-base dependency. <br>
Mitigation: Keep FX_AI_API_KEY private, install fx-base only from a trusted source, and review the dependency before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/cashback) <br>
- [feima-lab Open Platform](https://platform.feima.ai/) <br>
- [link-convert output template](references/link-convert-output.md) <br>
- [store-rebate output template](references/store-rebate-output.md) <br>
- [order-query output template](references/order-query-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses populated from JSON API results, with shell command invocations for the skill scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, the FX_AI_API_KEY environment variable, and the fx-base dependency installed alongside the skill.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
