## Description:

A Stock Vcp helps agents request A-share VCP breakout stock-screening results and present short-list trading references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users, short-term traders, technical-analysis users, and agents can use this skill to request A-share VCP breakout candidates and summarize the returned stock signal details. The output is for reference only and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises paid, current A-share trading signals while the included API evidence returns fixed simulated recommendations.

Mitigation: Confirm whether the deployed endpoint returns live market data before relying on results, and label any simulated output clearly.

Risk: The release claims x402 payment behavior, but the included API evidence does not enforce payment.

Mitigation: Verify payment enforcement on the deployed endpoint before commercial use.

Risk: Returned stock recommendations could be mistaken for current financial advice.

Mitigation: Use the output only as a reference signal and require independent validation and risk controls before trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinboh68-prog/skills/a-stock-vcp)
- [Configured API endpoint](https://a-stock-signals.vercel.app/v)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or text summaries of stock screening results returned by an API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock code, name, sector, price, percentage change, relative volume, strength rating, stop-loss level, target level, rationale, timestamp, and payment details.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
