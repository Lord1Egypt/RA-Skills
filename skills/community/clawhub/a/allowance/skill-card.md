## Description: <br>
Allowance agent purchase wallet. Use when the user asks to buy something, make a purchase, order an item, book travel, reserve something, pay, or spend money on their behalf. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[useallowance](https://clawhub.ai/user/useallowance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to request scoped spending approval, receive limited virtual cards, complete checkout, and report purchase outcomes without exposing the user's real card. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can complete real purchases after scoped user approval. <br>
Mitigation: Install only when an agent should be able to spend money on the user's behalf, and use strict spending caps with clear item, merchant, variant, and shipping constraints. <br>
Risk: After phone approval, the agent is instructed to submit checkout without a second confirmation when the purchase remains within the approved scope. <br>
Mitigation: Require a new user decision when the total exceeds the approved cap, the item or variant materially changes, or checkout needs details the agent cannot retrieve from Allowance-scoped commands. <br>
Risk: Virtual card details and scoped personal details are sensitive checkout data. <br>
Mitigation: Type card details directly into the merchant checkout form, never reveal them in chat, and request identity or address details only when the merchant form requires them. <br>
Risk: Local checkout automation requires browser control that may be unavailable in some agent sessions. <br>
Mitigation: Verify the current session can navigate, click, type, and inspect a local browser before creating an approval request. <br>


## Reference(s): <br>
- [Allowance homepage](https://useallowance.com) <br>
- [Canonical hosted skill file](https://useallowance.com/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/useallowance/allowance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers approval requests, browser checkout requirements, virtual card handling, MCP setup when explicitly requested, and outcome reporting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
