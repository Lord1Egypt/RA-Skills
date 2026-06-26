## Description: <br>
Private shielded transactions on Solana via ClawShield. Shield and withdraw SOL, USDC, USDT anonymously using ZK proofs. Keys never leave your agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Muzzy5150](https://clawhub.ai/user/Muzzy5150) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to offer shielded Solana deposits, withdrawals, balance checks, and transaction submission through the ClawShield API. It is intended for workflows involving SOL, USDC, or USDT where users want an optional private transaction route. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route Solana withdrawals and transfers through an external private transaction service, which creates financial loss risk if recipient, token, amount, or fees are wrong. <br>
Mitigation: Require explicit user approval for every transfer and inspect recipient, token, amount, and fees before signing or submitting any transaction. <br>
Risk: A persistent preference such as always using private transactions can weaken future confirmation boundaries. <br>
Mitigation: Treat the preference as a routing default only; keep final approval mandatory for each financial transaction. <br>
Risk: The security scan flagged broad transaction-routing authority with weak limits on confirmation and future defaults. <br>
Mitigation: Use only wallets and amounts the user is comfortable risking, start with small transactions, and review the generated unsigned transaction locally before signing. <br>


## Reference(s): <br>
- [ClawShield homepage](https://clawshield.network) <br>
- [ClawShield API base URL](https://clawshield.network/api) <br>
- [ClawHub skill page](https://clawhub.ai/Muzzy5150/clawshield-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, code, configuration] <br>
**Output Format:** [Markdown with HTTP request examples, JSON payloads, and transaction-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local transaction signing and user review before submitting financial transfers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
