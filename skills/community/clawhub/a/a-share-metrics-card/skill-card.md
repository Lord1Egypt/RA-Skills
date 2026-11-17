## Description:

Generates a Markdown metrics card for a single China A-share stock, covering valuation, profitability quality, cash flow, debt, dividend, and trading activity for comparison and tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joifg](https://clawhub.ai/user/joifg)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch public A-share market and financial data, then generate a repeatable Markdown card for single-stock research, comparison, and tracking. The skill supports learning-oriented analysis and explicitly avoids buy, sell, or target-price advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted output path or stock symbol can cause the script to write outside the intended notes directory or overwrite an existing file.

Mitigation: Use normal six-digit stock symbols, keep output paths under notes/stocks/cards, and add validation that rejects path traversal and confirms overwrites.

Risk: Public market and financial data sources may be delayed, unavailable, rate-limited, or changed upstream.

Mitigation: Review the generated data-source notes and timestamps, and verify important figures against authoritative market or company filings before relying on the card.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joifg/skills/a-share-metrics-card)
- [Publisher profile](https://clawhub.ai/user/joifg)
- [Eastmoney stock quote API](https://push2.eastmoney.com/api/qt/stock/get)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown card written to a local .md file, with a status or path summary returned to the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamps, data-source notes, and no buy, sell, or target-price recommendation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
