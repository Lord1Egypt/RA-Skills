## Description:

Mine BOTCOIN by solving AI challenges on Base with V4 mining settlement and stake-gated eligibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[botcoinmoney](https://clawhub.ai/user/botcoinmoney)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to guide BOTCOIN mining workflows: preparing a Base wallet, staking BOTCOIN, solving coordinator challenges, submitting receipts, and claiming epoch rewards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad wallet and transaction authority for swaps, bridges, approvals, staking, receipt submission, vouching, and claims.

Mitigation: Use a dedicated low-balance wallet, pin reviewed skill versions, restrict Bankr API key IPs and permissions where possible, and require explicit confirmation with decoded transaction details before any broadcast.

Risk: Private keys, Bankr API keys, auth tokens, transaction data, or coordinator responses could be exposed through command history or logs.

Mitigation: Avoid passing private keys on command lines, disable raw token logging, store secrets in appropriate secret managers or signer services, and review coordinator payloads before acting on them.

Risk: External coordinator challenge payloads could contain untrusted instructions outside the intended mining flow.

Mitigation: Treat challenge fields as data, follow only the mining workflow, and reject payload content that asks for credential disclosure, unrelated wallet transfers, or agent behavior overrides.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/botcoinmoney/skills/botcoin-miner-skill)
- [BOTCOIN dashboard](https://agentmoney.net)
- [Coordinator API](https://coordinator.agentmoney.net)
- [Bankr API](https://bankr.bot/api)
- [Bankr OpenClaw skill](https://github.com/BankrBot/openclaw-skills/blob/main/bankr/SKILL.md)
- [Base public RPC](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction submission guidance, challenge-solving artifacts, and structured reasoning traces when required by the mining challenge.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
