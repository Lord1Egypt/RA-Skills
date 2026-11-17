## Description:

Intellectia stock/crypto screener for Bullish/Bearish Tomorrow/Week/Month presets. Calls /gateway/v1/stock/screener-list (no auth) and summarizes results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xanxustan](https://clawhub.ai/user/xanxustan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch bullish or bearish stock and crypto screener candidates from Intellectia presets, then summarize or compare returned fields such as probability, profit, price, and change ratio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screener query choices are sent to Intellectia's API.

Mitigation: Use the skill only when this external API call is acceptable for the user's workflow.

Risk: Financial screener outputs can be incomplete, stale, or unsuitable as investment advice.

Mitigation: Treat results as informational screening data and verify financial decisions against appropriate sources and review processes.

Risk: The skill depends on Python requests in addition to curl and python3.

Mitigation: Use an isolated Python environment and pin or review the requests dependency where supply-chain controls require it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xanxustan/skills/ai-screener)
- [Intellectia API base URL](https://api.intellectia.ai)
- [Intellectia screener-list endpoint example](https://api.intellectia.ai/gateway/v1/stock/screener-list?symbol_type=0&period_type=0&trend_type=0&profit_asc=false&market_cap=0&price=0&page=1&size=20)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summarized screener tables or raw API JSON depending on the user's request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
