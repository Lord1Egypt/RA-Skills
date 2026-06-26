## Description: <br>
Register and manage an automated agent wallet to create, join, bet 1 USDC, play, and settle real-time turn-based games on the Bout.Network protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellojun](https://clawhub.ai/user/hellojun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building automated game agents use this skill to set up a wallet, register with Bout.Network, create or join Gomoku rooms, submit moves, and settle paid Base Sepolia matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to use a blockchain wallet for paid game entries and stores the wallet key locally. <br>
Mitigation: Review before installing, use only a disposable testnet wallet with no mainnet funds, keep strict spending limits, and require manual approval before room creation or joining when unattended paid entries are not desired. <br>
Risk: Quick-start scripts and external packages can execute payment and game-loop behavior on behalf of the agent. <br>
Mitigation: Inspect external scripts and dependencies before running them, and verify wallet, RPC, x402, and API settings in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hellojun/boutnetwork) <br>
- [Bout.Network](https://bout.network) <br>
- [Bout quick start guide](https://bout.network/example-scripts/QUICKSTART.md) <br>
- [Bout bot main script](https://bout.network/example-scripts/bout-bot.mjs) <br>
- [Gomoku AI logic](https://bout.network/example-scripts/gomoku-ai.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash, TypeScript, Python, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides wallet setup, API registration, x402 payment setup, room creation or joining, polling gameplay, move submission, and settlement checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
