## Description:

Operate the Dynamix Solana trading dashboard, purchase access, sign in, manage wallets, configure automated trading strategies, monitor live trades, and manage account settings at dynamix.gg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dynamixgg](https://clawhub.ai/user/dynamixgg)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for step-by-step guidance operating the Dynamix web dashboard, including purchase, authentication, wallet setup, automated Solana trading configuration, live trade monitoring, and account settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users into high-risk crypto wallet custody and unattended automated trading.

Mitigation: Use a separate low-balance wallet dedicated to trading, avoid importing a primary wallet, and confirm stop or revocation controls before enabling automation.

Risk: Server-side automation can continue spending funds while the browser is closed or after sign-out.

Mitigation: Stop the bot before signing out when ongoing trading is not intended, and review wallet authority and balances after each session.

Risk: The artifact includes repeated commercial steering through a promo code.

Mitigation: Treat promo or referral codes as optional and evaluate costs, terms, and trading risk independently before purchase.

## Reference(s):

- [Dynamix homepage](https://dynamix.gg)
- [Dynamix documentation](https://dynamix.gg/documentation)
- [ClawHub skill listing](https://clawhub.ai/dynamixgg/skills/dynamix-gg)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with links, checklists, and parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for using a third-party trading dashboard.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
