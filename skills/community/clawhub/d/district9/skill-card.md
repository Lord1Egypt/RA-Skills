## Description:

Autonomous meme token launcher on BNB Chain that senses trends, generates concepts, creates logos, and deploys tokens on-chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearl799](https://clawhub.ai/user/pearl799)

### License/Terms of Use:

MIT

## Use Case:

External developers and operators use DISTRICT9 to configure an OpenClaw agent that monitors crypto, news, and trend signals, generates meme-token concepts and assets, and launches tokens through District9 or Flap on BNB Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live operation can autonomously spend real BNB for token deployment, gas, metadata publication, and initial buys.

Mitigation: Start with dry-run or testnet mode, use a fresh low-balance wallet, cap launch settings, and run mainnet only after reviewing the exact configuration.

Risk: Real-looking PoC credentials are included in the artifact.

Mitigation: Ignore or rotate any shipped PoC credentials and provide fresh secrets through environment variables.

Risk: On-chain transactions and published token metadata may be irreversible or difficult to retract.

Mitigation: Review generated token names, symbols, logos, metadata, and destination contracts before live operation.

## Reference(s):

- [DISTRICT9](https://www.district9.club)
- [DISTRICT9 Deploy Guide](https://www.district9.club/deploy)
- [OpenClaw](https://openclaw.ai)
- [Flap.sh](https://flap.sh)
- [ClawHub DISTRICT9 Skill Page](https://clawhub.ai/pearl799/skills/district9)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When live commands are run, the artifact can generate token metadata and logo files, publish metadata, submit blockchain transactions, and return explorer or project URLs.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
