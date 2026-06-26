## Description: <br>
Create and manage non-custodial smart wallets on Base (EVM) and Solana with gasless transactions, spending limits, and passkey-based human control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xArtex](https://clawhub.ai/user/0xArtex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to guide wallet setup and operation for Base and Solana agents, including key generation, wallet creation, spending limits, transactions, status checks, limit changes, token limits, and emergency pauses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents real authority to spend crypto assets. <br>
Mitigation: Prefer managed wallets with human passkey approval, configure daily, per-transaction, and per-token limits before funding, and avoid unmanaged mode for real assets. <br>
Risk: Private keys and machine-readable keygen output can be exposed through shared terminals, CI logs, chat, or automation logs. <br>
Mitigation: Generate and store keys in secure storage or a secrets manager, avoid logging key material or --json output, and do not run key generation in shared or logged environments. <br>
Risk: Transactions are irreversible and incorrect recipients or excessive limits can cause asset loss. <br>
Mitigation: Verify recipient addresses, check remaining budget before large transactions, and use the pause workflow when activity looks suspicious. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xArtex/agentwallet-cli) <br>
- [Release artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with shell commands and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional JSON command output examples for agent wallet workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
