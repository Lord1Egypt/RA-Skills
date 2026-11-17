## Description:

Comprehensive A-share stock analysis skill covering core financials, technical indicators, valuation analysis, shareholder holdings, market sentiment, brokerage forecasts, K-line charts, financial reports, announcements, news, and exchange Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request multi-dimensional analysis of A-share stocks through a ClawHub/Prana remote runner. It helps agents return stock-analysis results that may include financial, technical, valuation, sentiment, forecast, chart, disclosure, news, and exchange-interaction context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends credentials and user prompts to a configurable remote endpoint.

Mitigation: Use only the intended Prana/Claw endpoint and avoid passing a custom base URL unless it has been reviewed.

Risk: API keys may be stored locally in config/api_key.txt.

Mitigation: Prefer environment variables or a secret manager, set PRANA_SKILL_SKIP_WRITE_API_KEY=1 when auto-fetching keys, and keep config/api_key.txt out of public repositories.

Risk: Stock-analysis output may be incomplete, delayed, or unsuitable for investment decisions.

Mitigation: Review generated analysis against authoritative market and issuer sources before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luokeer52/skills/getmeastock)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON returned by the remote skill runner, with setup guidance expressed as shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ClawHub/Prana API credentials and network access; Python and Node runners are provided.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
