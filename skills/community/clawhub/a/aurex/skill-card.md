## Description: <br>
Issue virtual crypto-funded cards and manage Aurex API workflows for users, deposits, card issuance, top-ups, partner markup, and transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aurexcards](https://clawhub.ai/user/aurexcards) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and payment operations teams use this skill to guide Aurex API workflows for virtual card issuance, wallet deposits, top-ups, card detail retrieval, partner markup, and transaction review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact payment-card actions such as issuing cards, topping up balances, and changing partner markup. <br>
Mitigation: Require manual confirmation before card issuance, top-ups, markup changes, or other value-moving actions. <br>
Risk: The Aurex API key may allow card, wallet, and commission operations. <br>
Mitigation: Use a dedicated, revocable API key with the lowest available permissions and limited balances. <br>
Risk: Card numbers, CVV, expiry, and OTP values are sensitive payment credentials. <br>
Mitigation: Avoid retrieving or displaying full card details unless strictly necessary, and never log or store them in plaintext. <br>


## Reference(s): <br>
- [Aurex website](https://aurex.cash) <br>
- [Aurex API base URL](https://aurex.cash/api/dashboard) <br>
- [Aurex documentation](https://docs.aurex.cash) <br>
- [ClawHub skill page](https://clawhub.ai/aurexcards/aurex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP examples, shell commands, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AUREX_API_KEY as the required environment credential.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
