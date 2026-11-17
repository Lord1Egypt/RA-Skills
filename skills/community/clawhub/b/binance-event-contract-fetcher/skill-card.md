## Description:

Fetches Binance BTCUSDT and ETHUSDT event contract market data every minute, including K-lines, liquidity, prices, and contract rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acwxpunh](https://clawhub.ai/user/acwxpunh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Binance market data for BTCUSDT and ETHUSDT event contract analysis, signal calculation, and risk-control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is described as making Binance API requests every minute in the background.

Mitigation: Require explicit opt-in for scheduled execution and document how to inspect, pause, and remove the recurring fetch behavior.

Risk: The security summary flags the release for review before installation.

Mitigation: Install a pinned version only after reviewing the skill behavior and confirming the required Binance API access pattern.

Risk: Cached or fallback market data can become stale after fetch failures.

Mitigation: Surface cache age in downstream use and pause signal generation when verified live data is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acwxpunh/skills/binance-event-contract-fetcher)
- [Publisher profile](https://clawhub.ai/user/acwxpunh)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with structured market data fields and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches and caches Binance market data on a one-minute cadence; output may include fallback data when live fetches fail.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
