## Description:

Dex Skill helps agents create Python crypto trading strategies, run server-side backtests and parameter optimization, and set up live monitoring or optional Hyperliquid trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyaosk](https://clawhub.ai/user/miyaosk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language crypto trading ideas into Python strategy scripts, evaluate them with backtests and optimization, and manage live signal monitoring. Users should treat live execution as a real-money workflow that requires explicit trust in the third-party service, credentials, dependencies, and risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated live trading can place real-money Hyperliquid orders if order execution is enabled.

Mitigation: Use read-only or testnet mode first, and enable automatic order execution only after reviewing the server, dependency chain, credentials, and risk controls.

Risk: The third-party trading service receives strategy code, trading signals, and a persistent client identifier.

Mitigation: Install only if that data sharing is acceptable, and avoid sending sensitive strategy logic or account context beyond what is required.

Risk: Wallet-key setup and broad environment overrides can increase credential exposure and operational risk.

Mitigation: Keep wallet credentials narrowly scoped, avoid broad environment overrides, and review required environment variables before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miyaosk/skills/dex-quant-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown/text responses, Python strategy code, JSON strategy signals, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce backtest or optimization chart image files and may send strategy code, signals, and monitoring requests to the configured DEX Quant service.]

## Skill Version(s):

3.47.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
