## Description:

Analyzes short-term trends for Chinese A-share stocks and ETFs using bundled data-fetching and technical-analysis scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanfuc](https://clawhub.ai/user/yuanfuc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect intraday snapshots and recent daily technical trends for A-share stocks and ETFs, including trend direction, weekly and daily percentage moves, buy/sell/hold signal, score, and risk hints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may pull unpinned packages into the active Python environment.

Mitigation: Install only in a virtual environment and review or pin dependencies before running setup_env.py.

Risk: Stock symbols or names may be sent to external market-data APIs.

Mitigation: Avoid submitting sensitive watchlists or private strategy context, and disclose external API use where required.

Risk: Buy/sell/hold signals may be mistaken for financial advice.

Mitigation: Present outputs as short-term technical reference only and include the non-investment-advice caveat in user-facing summaries.

## Reference(s):

- [China Stock Analyzer on ClawHub](https://clawhub.ai/yuanfuc/skills/china-stock-analyzer)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina real-time quote endpoint pattern](https://hq.sinajs.cn/list={codes_str})

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes technical indicators, buy/sell/hold signals, scores, risk hints, and a financial-advice caveat.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
