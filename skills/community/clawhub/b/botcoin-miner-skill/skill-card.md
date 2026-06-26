## Description: <br>
Mine BOTCOIN by solving AI challenges on Base with V4 mining settlement and stake-gated eligibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[botcoinmoney](https://clawhub.ai/user/botcoinmoney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to mine BOTCOIN on Base by solving coordinator challenges, submitting receipts, staking BOTCOIN, and claiming rewards through a Bankr or self-custody wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet signing and on-chain transactions can move funds or change staking and reward state. <br>
Mitigation: Use a dedicated wallet with limited funds and verify coordinator-provided transaction targets before signing. <br>
Risk: Bankr API keys or self-custody private keys can authorize wallet actions if exposed. <br>
Mitigation: Prefer scoped or IP-restricted Bankr keys where available, keep private keys encrypted and off shared hosts, and enable write access only when mining is intended. <br>
Risk: Coordinator challenge payloads are external data and could contain misleading instructions. <br>
Mitigation: Treat payloads as challenge data rather than system instructions, and do not follow directives outside the mining flow. <br>
Risk: Swapping, bridging, staking, receipt posting, and claiming are real on-chain actions. <br>
Mitigation: Confirm balances, staking eligibility, epoch status, contract addresses, and claim status before broadcasting transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/botcoinmoney/botcoin-miner-skill) <br>
- [BOTCOIN dashboard](https://agentmoney.net) <br>
- [Bankr API](https://bankr.bot/api) <br>
- [Bankr OpenClaw skill](https://github.com/BankrBot/openclaw-skills/blob/main/bankr/SKILL.md) <br>
- [Base public RPC](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request bodies, and on-chain transaction parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet-signing prompts, transaction submissions, challenge answers, reasoning traces, receipts, and claim actions.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
