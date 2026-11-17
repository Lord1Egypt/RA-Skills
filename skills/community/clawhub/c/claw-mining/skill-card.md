## Description:

Mine $CLAW tokens via Proof of AI Work on Ethereum. Install this Skill and tell your agent 'mine CLAW' - the agent handles everything automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minewithclaw](https://clawhub.ai/user/minewithclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run a local CLAW miner that calls an AI API, requests Oracle verification, and submits Ethereum mainnet mint transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a live Ethereum private key for local transaction signing.

Mitigation: Use a dedicated hot wallet with minimal ETH and never use a main wallet or hardware-wallet seed.

Risk: The automatic miner can keep signing mainnet mining transactions while it runs.

Mitigation: Run auto-mining only when you intend continuous transactions, monitor the process, and stop it when mining should pause.

Risk: Custom AI or Oracle endpoints could expose requests or route mining through untrusted services.

Mitigation: Use trusted HTTPS endpoints and review endpoint configuration before running the miner.

Risk: Installing and running the miner executes third-party Node.js code locally.

Mitigation: Review the cloned code and dependencies before running npm install, npx, or the mining commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/minewithclaw/skills/claw-mining)
- [Project Homepage](https://minewithclaw.com)
- [Source Repository](https://github.com/Cliai21/clawing)
- [Mining Guide](docs/MINING_GUIDE.md)
- [Oracle Service](https://oracle.minewithclaw.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands, environment configuration, and local CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js, git, an AI API key, an Ethereum RPC URL, a wallet private key, and ETH for gas.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
