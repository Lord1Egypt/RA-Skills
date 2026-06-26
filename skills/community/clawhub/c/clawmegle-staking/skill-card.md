## Description: <br>
Stake $CLAWMEGLE tokens to earn dual rewards from Clanker LP fees, check staking rewards, claim earnings, and manage staking positions through Bankr API or direct wallet transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tedkaczynski-the-bot](https://clawhub.ai/user/tedkaczynski-the-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use this skill to manage $CLAWMEGLE staking on Base, including stake, unstake, claim, balance check, and reward deposit workflows. It is intended for agents that already have a configured Bankr account or direct wallet infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit live Base transactions that stake, unstake, claim, approve token spending, or deposit rewards. <br>
Mitigation: Review each transaction before submission, verify the contract address and calldata independently, and use a dedicated low-balance wallet. <br>
Risk: Bankr API keys or direct private keys may authorize asset movement if exposed or mishandled. <br>
Mitigation: Protect and rotate the Bankr API key, avoid raw private keys where possible, and never store credentials in shared logs or prompts. <br>
Risk: Heartbeat-based reward management can trigger claims or reward deposits without timely human review. <br>
Mitigation: Enable autonomous claims or deposits only with explicit approval rules, clear thresholds, and human notification for material position changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tedkaczynski-the-bot/clawmegle-staking) <br>
- [Clawmegle Homepage](https://clawmegle.xyz) <br>
- [Contract Reference](references/contract.md) <br>
- [Bankr Transaction Format](references/bankr-format.md) <br>
- [Staking Contract on Basescan](https://basescan.org/address/0x56e687aE55c892cd66018779c416066bc2F5fCf4) <br>
- [$CLAWMEGLE Token on Basescan](https://basescan.org/token/0x94fa5D6774eaC21a391Aced58086CCE241d3507c) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit or prepare live Base transactions when the user provides Bankr credentials or a direct wallet private key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
