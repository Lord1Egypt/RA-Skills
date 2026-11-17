## Description:

Fetch China A-share stock market data, including bars, realtime quotes, and tick-by-tick transactions, through the mootdx/TDX protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangdinglu](https://clawhub.ai/user/wangdinglu)

### License/Terms of Use:


## Use Case:

Developers and data engineers use this skill to build or operate agent workflows that retrieve China A-share market bars, realtime quotes, batch quotes, and tick-by-tick transaction data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and live market-data connectivity can introduce setup, availability, and supply-chain risk.

Mitigation: Install in a virtual environment or container and prefer pinned, hash-verified dependencies for production use.

Risk: The trading-hour bypass can prevent empty transaction results caused by timezone checks, but it does not prove that returned data is valid for every timestamp.

Mitigation: Treat the bypass as a data-quality choice, validate dates against a trading calendar, and verify timestamps against Beijing trading sessions.

Risk: Unsupported Beijing Stock Exchange symbols or non-trading-day queries can return empty or misleading data.

Mitigation: Filter out .BJ symbols before calling mootdx and check weekend or holiday dates before querying historical data.

## Reference(s):

- [Detailed mootdx API Reference](api-reference.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API call patterns, stock-code conversion rules, and data-quality cautions for market-calendar, timezone, and unsupported-exchange cases.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
