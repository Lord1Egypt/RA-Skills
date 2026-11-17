## Description:

Autonomous DeFi trading agent for BNB Chain with multi-strategy engine, network switching, and reinforced learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alannetwork](https://clawhub.ai/user/alannetwork)

### License/Terms of Use:

MIT

## Use Case:

External developers and DeFi operators use this skill to run and monitor a BNB Chain yield-farming agent that can evaluate vaults, execute harvest/compound/rebalance actions, switch networks, and report performance through a CLI and dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests wallet signing authority for financial automation.

Mitigation: Use a fresh testnet wallet or a wallet with funds you can afford to lose, and do not place a mainnet private key in .env.

Risk: The scheduler can repeatedly submit live transactions without sufficient safety controls.

Mitigation: Avoid unattended live execution until dry-run or manual approval defaults, transaction limits, gas limits, and bounded approvals are configured.

Risk: The local API can expose operational controls or logs if reachable from untrusted networks.

Mitigation: Keep the API bound to trusted interfaces and add authentication before exposing any API port beyond the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alannetwork/skills/clawtrade-bnb)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [README_STRATEGY.md](artifact/README_STRATEGY.md)
- [README_ADVANCED.md](artifact/README_ADVANCED.md)
- [LIVE_EXECUTION_GUIDE.md](artifact/LIVE_EXECUTION_GUIDE.md)
- [contracts/README.md](artifact/contracts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented instructions with JavaScript/JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction plans, runtime status, logs, metrics, dashboard views, and BNB Chain transaction references when configured for live execution.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
