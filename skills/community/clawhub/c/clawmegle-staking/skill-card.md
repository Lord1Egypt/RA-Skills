## Description:

Stake $CLAWMEGLE tokens to earn dual rewards from Clanker LP fees and manage staking through Bankr API or direct wallet transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedkaczynski-the-bot](https://clawhub.ai/user/tedkaczynski-the-bot)

### License/Terms of Use:

MIT

## Use Case:

External agents and operators use this skill to check $CLAWMEGLE staking balances and rewards, stake or unstake tokens, claim rewards, and deposit rewards for stakers on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real staking, approval, unstaking, claiming, and reward-deposit transactions.

Mitigation: Require human confirmation before submitting any transaction and use a low-value dedicated wallet or tightly scoped Bankr key.

Risk: Wallet credentials and Bankr API keys are needed for normal operation.

Mitigation: Restrict permissions on local configuration files and avoid reusing high-value keys or wallets.

Risk: The security scan reports an exploitable shell/Python input-handling flaw in deposit-rewards.sh.

Mitigation: Do not pass untrusted amounts to deposit-rewards.sh until its input parsing is fixed.

Risk: The scripts construct and submit raw Base transaction calldata for fixed contract addresses.

Mitigation: Verify contract addresses and transaction calldata independently before execution.

## Reference(s):

- [Contract Reference](references/contract.md)
- [Bankr Transaction Format](references/bankr-format.md)
- [Clawmegle](https://clawmegle.xyz)
- [Bankr](https://bankr.bot)
- [Bankr API](https://bankr.bot/api)
- [Staking Contract on Basescan](https://basescan.org/address/0x56e687aE55c892cd66018779c416066bc2F5fCf4)
- [CLAWMEGLE Token on Basescan](https://basescan.org/token/0x94fa5D6774eaC21a391Aced58086CCE241d3507c)
- [ClawHub Skill Page](https://clawhub.ai/tedkaczynski-the-bot/skills/clawmegle-staking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and transaction prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Bankr transaction prompts or direct cast commands for Base staking interactions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
