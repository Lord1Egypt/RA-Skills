## Description:

Boiling Point - The hottest launchpad for onchain OpenClaw agents. Launch and trade omnichain tokens across Base, Solana, Ethereum and BNB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisciszak](https://clawhub.ai/user/chrisciszak)

### License/Terms of Use:


## Use Case:

External developers and OpenClaw agent operators use this skill to launch, browse, quote, trade, and manage onchain agent tokens through the Token Layer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real blockchain transactions from third-party API responses.

Mitigation: Require the agent to show and confirm each transaction's chain, destination, value, and calldata before broadcasting.

Risk: Using a funded Token Layer API key can expose assets to loss from mistaken token launches, trades, or reward claims.

Mitigation: Use a wallet with limited funds, prefer testnet or small initial amounts, and avoid API keys connected to wallets holding assets you cannot afford to lose.

Risk: The security verdict is suspicious because final transaction safeguards are not sufficiently enforced by the skill text.

Mitigation: Review the skill carefully before installation and require human approval before any send-transaction call.

## Reference(s):

- [Boiling Point homepage](https://boilingpoint.ai)
- [ClawHub skill page](https://clawhub.ai/chrisciszak/skills/boiling-point)
- [Token Layer API base](https://api.tokenlayer.network/functions/v1)
- [Token Layer agent wallets](https://app.tokenlayer.network/agent-wallets)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENLAYER_API_KEY plus jq and curl.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
