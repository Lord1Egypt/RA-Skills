## Description:

A-share market data skill for fetching data from Tushare, querying market and valuation data, and running technical analysis including moving averages, RSI, MACD, and Bollinger Bands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhkong7](https://clawhub.ai/user/lhkong7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch A-share market datasets, query local stock and valuation data, and produce concise technical-analysis summaries for symbols or market slices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tushare token for authenticated market-data requests.

Mitigation: Keep the token in a local .env file or pass it at runtime, avoid sharing .env, and run the skill in a constrained project directory.

Risk: The skill downloads and stores market data locally.

Mitigation: Review local data-directory permissions and retention before use, especially in shared workspaces.

Risk: Market data and technical indicators may be incomplete, stale, or unsuitable as financial advice.

Mitigation: Treat outputs as analysis aids and verify data freshness and investment conclusions independently.

## Reference(s):

- [AMtkSkill ClawHub Release](https://clawhub.ai/lhkong7/skills/amtk-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and tabular command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a Tushare token and local Parquet/CSV market-data files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
