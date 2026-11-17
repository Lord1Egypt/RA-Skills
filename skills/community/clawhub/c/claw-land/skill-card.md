## Description:

Play on-chain odd/even games on Solana devnet via Clawland. Mint GEM from SOL or USDC, bet odd or even, win 2x. Scripts handle wallet setup, minting, and autoplay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice-coldbell](https://clawhub.ai/user/ice-coldbell)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to set up a devnet Solana wallet, mint GEM tokens, play Clawland odd/even games, check balances, and interact with Clawland API features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a local Solana wallet key and Clawland API key.

Mitigation: Use a dedicated devnet-only wallet, keep wallet.json and API keys private, and never use a mainnet wallet or real assets with this skill.

Risk: The skill can execute automated mint, play, redeem, and autoplay actions.

Mitigation: Review command arguments before execution, start with small devnet amounts, and monitor balances during autoplay.

Risk: The scripts install npm dependencies at runtime if required packages are missing.

Mitigation: Prefer installing and reviewing pinned dependencies in advance before running the skill scripts.

## Reference(s):

- [Clawland skill page](https://clawhub.ai/ice-coldbell/skills/claw-land)
- [Clawland homepage](https://www.clawlands.xyz)
- [Clawland API Reference](references/API.md)
- [Clawland On-Chain Games (Solana)](references/SOLANA.md)
- [AgentWallet skill](https://agentwallet.mcpay.tech/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, curl, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access, Node.js v18 or newer, curl, CLAWLAND_API_KEY, and a local Solana devnet wallet for on-chain actions.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
