## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to let an agent request, monitor, and make online purchases through CreditClaw wallets and payment rails under owner-defined spending controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an agent controlled financial authority and can initiate real spending through CreditClaw payment rails. <br>
Mitigation: Start with approval required for every purchase, keep transaction and period limits low, and use allowlists, blocked categories, and transaction monitoring. <br>
Risk: Exposure of CREDITCLAW_API_KEY can allow unauthorized use of the agent wallet. <br>
Mitigation: Store CREDITCLAW_API_KEY only in a secure secrets manager or protected environment variable, and never send it to domains other than creditclaw.com. <br>
Risk: Remote guide files from creditclaw.com influence agent behavior for spending workflows. <br>
Mitigation: Review remote guide files before allowing the agent to use them for purchase or payment actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jononovo/creditcard) <br>
- [Publisher profile](https://clawhub.ai/user/jononovo) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [Self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata; artifact frontmatter reports 2.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
