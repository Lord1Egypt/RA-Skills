## Description:

Analyzes KRX-listed Korean stocks using Naver Finance financial, news, and chart inputs to produce a weighted Investment Attractiveness Score and BUY/HOLD/AVOID-style verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saebyeok-im](https://clawhub.ai/user/saebyeok-im)

### License/Terms of Use:


## Use Case:

External users, analysts, and developers use this skill to prepare structured Korean equity research for a specific KRX ticker or company. It is intended to score financial fundamentals, recent news, and basic chart timing in a conservative framework rather than provide personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces BUY/HOLD/AVOID labels that could be mistaken for personalized financial advice.

Mitigation: Use the output as informational equity research, verify current market data independently, and apply human review before acting on any recommendation.

Risk: The workflow is scoped to Korean KRX equities and may be misleading for non-Korean stocks, cryptocurrency, or unsupported assets.

Mitigation: Use it only for KRX-listed Korean stocks and decline or redirect unsupported asset requests.

Risk: Reports depend on current Naver Finance data and user-provided or extracted news and chart summaries, which may be stale or incomplete.

Mitigation: Confirm financial metrics, news, and chart inputs from current independent sources before relying on the score.

Risk: The included analysis workflow can write to an output file path selected by the user.

Mitigation: Avoid pointing output to an existing file unless overwriting it is acceptable.

## Reference(s):

- [Equity Analysis Framework](references/framework.md)
- [Naver Finance Stock Page](https://finance.naver.com/item/main.naver?code={ticker})

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Structured plain text report with numeric subscores, final score, verdict, and a reasoning summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Financial, News, and Chart scores with a final Investment Attractiveness Score from 0 to 100.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
