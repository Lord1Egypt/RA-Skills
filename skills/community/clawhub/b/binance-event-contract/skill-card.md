## Description:

Coordinates Binance-only BTCUSDT and ETHUSDT event-contract data fetching, signal calculation, ICT structure analysis, risk checks, advisory execution logging, and reporting for human-reviewed trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acwxpunh](https://clawhub.ai/user/acwxpunh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading workflow operators use this skill system to monitor Binance BTC/ETH event-contract market data, generate advisory entry, target, and stop guidance, run risk checks, and summarize signal performance without placing orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unattended, poll Binance continuously, cache and share market data, and produce trading recommendations.

Mitigation: Require explicit opt-in scheduling, provide pause or uninstall controls, and review the workflow before deployment.

Risk: The release uses mutable installer commands.

Mitigation: Use pinned and reviewed installer and skill versions.

Risk: The security summary flags flawed high-impact risk guidance in the risk manager.

Mitigation: Do not rely on risk-manager output until position-size math is corrected and independently tested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/acwxpunh/skills/binance-event-contract)
- [ClawHub Publisher Profile](https://clawhub.ai/user/acwxpunh)
- [Binance API Endpoint](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style advisory reports with inline installation and trigger commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces market-data summaries, signal recommendations, ICT structure reports, risk-check results, execution logs, P&L monitoring, alerts, and periodic performance reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
