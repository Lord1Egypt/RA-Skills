## Description:

Automates multi-coin spot grid trading on Bitget with dynamic adjustments, risk management, portfolio monitoring, and analysis tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hotflame-cloud](https://clawhub.ai/user/hotflame-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to configure, monitor, and operate Bitget spot grid strategies across assets such as BTC, ETH, SOL, and BNB. It supports balance checks, grid deployment, order cancellation, optimization, dynamic adjustment, and status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports live-looking credentials and examples that default to live trading.

Mitigation: Replace shipped credential files, use restricted API keys, disable withdrawal permissions, apply IP restrictions, and test with paper trading or very small amounts before any live use.

Risk: The skill can place market or limit orders and cancel existing orders on Bitget.

Mitigation: Review commands before execution, confirm target symbol and order size, and require operator approval for order placement or cancellation.

Risk: The skill can configure recurring OpenClaw or cron-based monitoring activity.

Mitigation: Remove or disable cron setup unless recurring activity is explicitly intended, and periodically audit installed scheduled jobs.

Risk: Cryptocurrency grid trading can lose capital during volatile or trending markets.

Mitigation: Set conservative position limits, keep order sizes small, monitor grids actively, and stop strategies when price moves outside configured ranges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hotflame-cloud/skills/bitget-data)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Bitget website](https://www.bitget.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell command examples, JavaScript script references, JSON configuration, and generated report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading operations that may call external exchange APIs and write local status, configuration, and report files.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
