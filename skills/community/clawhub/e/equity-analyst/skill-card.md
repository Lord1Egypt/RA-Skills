## Description:

Equity Analyst analyzes Korean KRX stocks using Naver Finance financial metrics, news, and simple chart context to produce an Investment Attractiveness Score and a conservative BUY_LEAN, HOLD, or AVOID-style verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saebyeok-im](https://clawhub.ai/user/saebyeok-im)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to structure Korean stock research around financial fundamentals, recent news, and basic chart conditions. The output is intended as informational analysis that supports review, not as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes local Python reporting scripts that can open an OpenClaw browser profile, scrape Naver Finance, and write files into the local workspace.

Mitigation: Review scripts before installation, use only the documented analyzer and scraper workflow when possible, and avoid daily or morning report scripts until their shell invocation and hardcoded paths are fixed.

Risk: Stock scores and verdicts may be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational analysis only and require qualified human review before making investment decisions.

## Reference(s):

- [Equity Analysis Framework](references/framework.md)
- [Naver Finance ticker page](https://finance.naver.com/item/main.naver?code={ticker})
- [ClawHub skill page](https://clawhub.ai/saebyeok-im/skills/equity-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Structured Markdown-style investment analysis report with scores, verdict, and reasoning; scripts may also emit local report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores are 0-100 and follow the documented Financial, News, and Chart weighting framework.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
