## Description:

Buy $WIR on TON -- the decentralized credit union token on TON.fun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alphafanx](https://clawhub.ai/user/alphafanx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to get wallet, price-checking, and transaction guidance for buying the WIR token on TON.fun. The skill also provides optional social-posting guidance for promoting the token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could send TON using under-scoped transaction instructions.

Mitigation: Require explicit, per-action confirmation before any transfer and independently verify the token, contract address, transaction parameters, and financial risks outside the skill.

Risk: An agent could promote the token publicly without adequate review.

Mitigation: Require explicit confirmation before posting to any social network and review generated promotional text before publication.

Risk: Price, liquidity, and contract state can change after the skill text was published.

Mitigation: Check live TON.fun and contract data immediately before acting, and treat the skill's static price references as non-authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alphafanx/skills/buy-wir)
- [TON.fun](https://ton.fun)
- [WIR launch page on TON.fun](https://ton.fun/launch?token=EQAw-RI_4boPd6HwcKTY4nYJ1zj_b__hS0t56eM2HPIlyHid&symbol=WIR&decimals=9)
- [TON blockchain](https://ton.org)
- [Tonkeeper wallet](https://tonkeeper.com)
- [MyTonWallet](https://mytonwallet.io)
- [TonAPI account endpoint](https://tonapi.io/v2/blockchain/accounts/EQAw-RI_4boPd6HwcKTY4nYJ1zj_b__hS0t56eM2HPIlyHid)
- [BotWorld Social](https://botworld.me)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the optional TonAPI account query.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
