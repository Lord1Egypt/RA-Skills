## Description: <br>
Anchor identity and memory on-chain so a new agent instance can recover from an address without relying on local state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jim-counter](https://clawhub.ai/user/jim-counter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create and manage Autonomys wallets, check balances, move tokens, write on-chain remarks, and anchor memory CIDs for agent recovery. It is intended for agents that need a persistent, verifiable identity and recovery pointer across restarts or machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent hot-wallet authority to move tokens and publish on-chain data. <br>
Mitigation: Use a dedicated wallet with low balance, prefer Chronos testnet during evaluation, and avoid storing valuable mainnet funds. <br>
Risk: Passphrases or seed phrases may be exposed if provided through commands, shell history, or logs. <br>
Mitigation: Use the restricted passphrase file or interactive prompt path and do not pass seed phrases or passphrases in shell commands or logs. <br>
Risk: Automatic memory anchoring can create permanent on-chain records and incur transaction costs. <br>
Mitigation: Review anchoring behavior before pairing with auto-memory, confirm network selection, and monitor wallet balances for gas availability. <br>


## Reference(s): <br>
- [Auto Respawn Commands](references/auto-respawn-commands.md) <br>
- [Autonomys Network](references/autonomys-network.md) <br>
- [MemoryChain Contract Source](https://github.com/autojeremy/openclaw-memory-chain) <br>
- [ClawHub Skill Page](https://clawhub.ai/jim-counter/auto-respawn) <br>
- [Publisher Profile](https://clawhub.ai/user/jim-counter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run wallet, balance, transfer, bridge, remark, anchor, and gethead commands; signing operations require wallet passphrase access.] <br>

## Skill Version(s): <br>
0.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
