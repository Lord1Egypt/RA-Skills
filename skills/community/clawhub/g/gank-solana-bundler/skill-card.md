## Description:

Manage Solana wallets, launch pump.fun tokens, run coordinated buys, volume bots, copy trades, and related GANK trading terminal API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pissdart](https://clawhub.ai/user/pissdart)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent operate the GANK Solana trading terminal API for wallet management, token launches, coordinated trading, copy trading, volume sessions, market data, and position monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to perform live crypto trading and wallet operations with real funds.

Mitigation: Use test wallets first, prefer low-balance or tightly scoped keys where available, and require manual confirmation before trading or wallet actions.

Risk: The GANK API key can authorize sensitive trading and wallet activity if exposed.

Mitigation: Store the key only in the configured secret location or environment variable, and keep it out of prompts, logs, and generated examples.

Risk: Wallet drain, fund-routing, volume-bot, copy-trade, sweep, buy, and sell actions are high-impact operations.

Mitigation: Require explicit user confirmation before these actions and review each request against the intended wallet, token, amount, route, and duration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pissdart/skills/gank-solana-bundler)
- [GANK](https://gank.dev)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint descriptions, JSON payloads, shell setup commands, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GANK API key supplied through GANK_API_KEY or the skill configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
