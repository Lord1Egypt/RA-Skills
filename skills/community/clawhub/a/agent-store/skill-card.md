## Description:

Use when the user wants to buy, purchase, order, pay for, or top up API keys or API credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levey](https://clawhub.ai/user/levey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to buy API keys or top up API credits through an agent-run purchase flow and receive a concise delivery or failure report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate a real purchase using a wallet-backed payment flow.

Mitigation: Require explicit user confirmation before wallet unlock, approval, signing, and payment submission.

Risk: Payment challenge fields may not be strongly validated before signing.

Mitigation: Validate payment amount, token, recipient, chain, spender, RPC URL, and provider endpoint against trusted allowlists before proceeding.

Risk: A successful API key purchase can lead to persistent runtime provider configuration changes and active-model changes.

Mitigation: Require explicit confirmation before editing runtime configuration, sending verification requests, or changing the active model.

## Reference(s):

- [Agent Store on ClawHub](https://clawhub.ai/levey/skills/agent-store)
- [levey ClawHub Profile](https://clawhub.ai/user/levey)
- [awp-wallet](https://github.com/awp-core/awp-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary plus JSON delivery output and plain-text logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update runtime model-provider configuration after a successful API key purchase.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
