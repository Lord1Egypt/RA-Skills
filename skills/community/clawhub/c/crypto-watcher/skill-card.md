## Description:

Monitor ETH wallets and DeFi positions across chains with alerts for balance changes, gas prices, health factors, and large token transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto operators use this skill to configure wallet monitoring for public Ethereum-compatible addresses, token balances, gas prices, DeFi checks, and alert thresholds across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watched public wallet addresses may be shared with public RPC providers and related crypto APIs during monitoring.

Mitigation: Monitor only addresses whose activity you are comfortable exposing to those services, and avoid wallets whose monitoring activity must remain private.

Risk: Dependency caveats were identified for this release, including a recommendation to pin dependencies and move ws to a patched version.

Mitigation: Prefer an updated release with pinned dependencies and a patched ws version before using the skill in sensitive or production environments.

Risk: Using private keys or seed phrases with a monitoring workflow can create avoidable credential exposure.

Mitigation: Use public wallet addresses only; do not provide private keys, seed phrases, or signing credentials to this skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xraini/skills/crypto-watcher)
- [Skill Documentation](artifact/SKILL.md)
- [DefiLlama API](https://api.llama.fi)
- [CoinGecko API](https://api.coingecko.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CLI-oriented monitoring guidance and configuration examples for public wallet data; private keys or seed phrases are not required.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
