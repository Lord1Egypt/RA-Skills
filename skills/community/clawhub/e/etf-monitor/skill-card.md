## Description:

Monitors configured ETFs for price movement and prints alerts when a percentage threshold is exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zitjubiz](https://clawhub.ai/user/zitjubiz)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and automation agents use this skill to monitor a configured list of ETFs and receive JSON alerts when price movement crosses a configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ETF alerts rely on public quote data requested over HTTP, so values may be delayed or unreliable for financial decisions.

Mitigation: Treat alerts as advisory, verify market data before acting, and consider a trusted data source for production financial workflows.

Risk: The skill makes outbound network requests and depends on the requests Python package.

Mitigation: Install dependencies in a limited virtual environment and allow outbound network access only to expected quote endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zitjubiz/skills/etf-monitor)
- [Tencent Finance quote endpoint](http://qt.gtimg.cn/q=sz159985)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON alerts printed to stdout, with stderr text for quote-fetch errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alert entries include ETF code, name, current price, percent change, and direction; empty results are returned as {"alerts": []}.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
