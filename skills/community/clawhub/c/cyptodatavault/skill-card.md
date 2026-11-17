## Description:

CyptoDataVault provides AI agents with real-time cryptocurrency prices, on-chain Ethereum data, and DeFi metrics through a unified set of market-data tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshuniguang](https://clawhub.ai/user/wangshuniguang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to let agents retrieve crypto market prices, funding rates, Ethereum account data, gas prices, DeFi TVL, yield, and stablecoin metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact imports core implementation code that is not included in the artifact.

Mitigation: Review the surrounding repository layout before installation and install only in an isolated environment.

Risk: The setup and test scripts install mutable Python dependencies.

Mitigation: Use a pinned release or lockfile before using the skill with real credentials.

Risk: Wallet addresses and API keys may be used when calling on-chain or provider-backed data tools.

Mitigation: Treat wallet addresses and API keys as sensitive and avoid exposing production credentials in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshuniguang/skills/cyptodatavault)
- [DataVault website](https://datavault.io)
- [Project repository listed in artifact metadata](https://github.com/wangshuniguang/DataVault)
- [OpenClaw installation guide](artifact/README_OPENCLAW.md)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Markdown usage guidance with JSON-like tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses may include live market, on-chain, and DeFi data from external services.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
