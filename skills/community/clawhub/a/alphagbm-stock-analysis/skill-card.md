## Description:

AlphaGBM Stock Analysis helps agents analyze US, HK, and A-share stock tickers using AlphaGBM's Five Pillars framework and returns a 1-10 composite score, actionable signals, target-price context, and risk information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to retrieve stock quotes, request AlphaGBM stock analysis, and present recommendations, target prices, risk scores, stop-loss context, EV estimates, and AI-generated reports for supported tickers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated buy/sell labels, target prices, and risk scores may be mistaken for automatic financial advice or trading authority.

Mitigation: Present analysis as research support, keep users responsible for investment decisions, and avoid autonomous trading based only on this skill's output.

Risk: Using real AlphaGBM analysis can send requested tickers and an API key to the AlphaGBM service.

Mitigation: Use the skill only when the user accepts AlphaGBM processing, store the API key in the environment, and avoid exposing secrets in prompts or output.

## Reference(s):

- [AlphaGBM Website](https://alphagbm.com)
- [AlphaGBM API Base URL](https://alphagbm.zeabur.app)
- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-stock-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown stock-analysis summary with optional inline API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommendation labels, target price, risk score, stop-loss price, EV estimate, and AI report excerpts; full analysis requires an AlphaGBM API key while limited mock-data behavior is available for selected tickers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
