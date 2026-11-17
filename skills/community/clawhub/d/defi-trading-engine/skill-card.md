## Description:

DeFi Trading Engine is an autonomous DeFi trading helper for OpenClaw agents that scans opportunities, executes Bankr-based trades, logs performance, and supports review-driven parameter updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avmw2025](https://clawhub.ai/user/avmw2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system operators use this skill to set up automated DeFi trading workflows on Base or other EVM chains, including token scanning, risk checks, trade execution, trade journaling, and daily performance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can assist with real cryptocurrency transactions, and release security evidence flags under-scoped safety controls that could cause unintended live transactions.

Mitigation: Review the scripts before installation, use a dedicated low-balance wallet, and pass --dry-run explicitly until live execution behavior is verified.

Risk: Risk checks can be bypassed for live trades.

Mitigation: Do not use --skip-risk-check for live trading, and confirm risk-manager.py approves position size, daily trade count, cooldown, and drawdown before execution.

Risk: The workflow depends on the external Bankr CLI for wallet and trade operations.

Mitigation: Pin and review the Bankr CLI before funding any wallet, keep wallet/API secrets out of the repository, and test with small amounts before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avmw2025/skills/defi-trading-engine)
- [Bankr CLI setup guide](artifact/references/bankr-setup.md)
- [Trading strategies](artifact/references/strategies.md)
- [CoinGecko API documentation](https://www.coingecko.com/en/api/documentation)
- [Base Chain documentation](https://docs.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, Python scripts, JSON trading candidates and logs, and Markdown review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading workflow guidance and local artifacts such as candidates.json, trades/YYYY-MM-DD.json, and reviews/review-YYYY-MM-DD.md.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
