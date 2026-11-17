## Description:

Akshare-Stock-Analyzer helps agents analyze A-share stocks and ETFs using intraday snapshots, recent daily trends, buy/sell/hold signals, and short-term technical scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanfuc](https://clawhub.ai/user/yuanfuc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect single A-share stocks or ETFs, fetch current market snapshots, and summarize recent technical trend, momentum, risk level, signal, and score. Outputs are technical indicators only and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned akshare and pandas dependencies may change behavior across installs.

Mitigation: Install in a dedicated virtual environment and review dependency installation before running setup_env.py.

Risk: The skill makes network calls to public market-data providers, so upstream outages or delays can affect results.

Mitigation: Treat failed or stale data fetches as blockers for analysis and avoid fabricating market conclusions.

Risk: fetch.py can write local CSV output when run directly.

Mitigation: Run the skill in an expected working directory and review generated files before sharing or retaining them.

Risk: Buy, sell, and hold outputs can be mistaken for financial advice.

Mitigation: Present outputs as short-term technical indicators only and include an investment-advice disclaimer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanfuc/skills/akshare-stock-analyzer)
- [Publisher profile](https://clawhub.ai/user/yuanfuc)
- [English README](artifact/README.en.md)
- [Chinese README](artifact/README.md)
- [AnalysisResult field reference](artifact/scripts/analyze_result.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional shell commands and structured technical-analysis fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trend, weekly_change_pct, today_change_pct, signal, score, moving-average context, MACD, RSI, reversal_hint, and risk_level.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
