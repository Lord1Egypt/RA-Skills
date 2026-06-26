## Description: <br>
Use when managing Crunch coordinators, competitions (crunches), rewards, checkpoints, staking, or cruncher accounts via the crunch-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philippWassibauer](https://clawhub.ai/user/philippWassibauer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to translate natural-language Crunch protocol administration requests into crunch-cli commands for coordinators, competitions, staking, checkpoints, rewards, and cruncher accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward wallet-backed Crunch/Solana transactions. <br>
Mitigation: Require explicit manual confirmation before deposits, drains, staking actions, withdrawals, delegation changes, claims, registrations, checkpoint creation, or competition state changes. <br>
Risk: Commands may run against the wrong wallet, RPC endpoint, profile, or Solana network. <br>
Mitigation: Verify the active profile, wallet path, RPC URL, and network before executing any state-changing command. <br>
Risk: A wallet keypair could be exposed or overfunded during agent-assisted operations. <br>
Mitigation: Use a dedicated limited-balance wallet and do not read, display, generate, or commit wallet keypair files unless the user explicitly requests an appropriate action. <br>


## Reference(s): <br>
- [Coordinator CLI Full Reference](references/cli-reference.md) <br>
- [Crunch CLI npm package](https://www.npmjs.com/package/@crunchdao/crunch-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Markdown, Text] <br>
**Output Format:** [Markdown or plain text with inline shell commands and optional Slack, Telegram, Discord, JSON, table, or YAML formatting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose wallet-backed on-chain operations through crunch-cli and should preserve user-selected profile, network, wallet, RPC, and output settings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
